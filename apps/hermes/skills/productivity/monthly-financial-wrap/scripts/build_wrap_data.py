#!/usr/bin/env python3
"""Build the data, tables and charts for the YNAB monthly financial wrap.

Usage: build_wrap_data.py [YYYY-MM]   (default: previous month in Australia/Sydney)

Fetches from the YNAB MCP over HTTP (MCP_YNAB_MCP_API_KEY), applies the wrap
expense rules, reconstructs month-end balances (loan interest derived from
balances), renders two PNG charts into the Obsidian vault, and writes:
  /opt/data/workspace/ynab-wrap/<YYYY-MM>/data.json     full computed data
  /opt/data/workspace/ynab-wrap/<YYYY-MM>/tables.md     ready-to-paste tables
stdout: a compact JSON summary for the agent to write insights from.
Run with matplotlib available, e.g. `uv run --with matplotlib python3 ...`.
"""
import json, os, sys, urllib.request, datetime as dt
from collections import defaultdict
from zoneinfo import ZoneInfo

URL = "https://wraeclast.bishop-bass.ts.net/ynab-mcp"
BUDGET = "924a80ac-d251-40ed-96a3-a4a3d6f620d5"
VAULT = "/opt/data/obsidian/notes"
ASSETS = f"{VAULT}/queries/assets"
WORK = "/opt/data/workspace/ynab-wrap"
EXCLUDED_CATS = {None, "Uncategorized", "Inflow: Ready to Assign", "Split"}
# Accounts where YNAB cannot mark transfers cleared: treat as cleared.
ALWAYS_CLEARED = {"WestPac Mortgage"}


class MCP:
    def __init__(self):
        key = os.environ.get("MCP_YNAB_MCP_API_KEY")
        if not key:
            raise SystemExit("MCP_YNAB_MCP_API_KEY is not set")
        self.h = {"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                  "Accept": "application/json, text/event-stream"}
        self.sid, _ = self._post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2024-11-05", "capabilities": {},
            "clientInfo": {"name": "monthly-wrap", "version": "1"}}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})
        self.n = 1

    def _post(self, body):
        h = dict(self.h)
        if getattr(self, "sid", None):
            h["Mcp-Session-Id"] = self.sid
        req = urllib.request.Request(URL, json.dumps(body).encode(), h)
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.headers.get("mcp-session-id"), r.read().decode()

    def call(self, name, **args):
        self.n += 1
        args.setdefault("budget_id", BUDGET)
        _, body = self._post({"jsonrpc": "2.0", "id": self.n, "method": "tools/call",
                              "params": {"name": name, "arguments": args}})
        for line in body.splitlines():
            if line.startswith("data: "):
                d = json.loads(line[6:])
                if "error" in d:
                    raise RuntimeError(f"{name}: {d['error']}")
                res = d["result"]
                text = res["content"][0]["text"]
                if res.get("isError"):
                    raise RuntimeError(f"{name}: {text[:500]}")
                return json.loads(text)
        raise RuntimeError(f"{name}: no data in response")


def month_bounds(ym):
    y, m = map(int, ym.split("-"))
    first = dt.date(y, m, 1)
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return first, nxt


def prev_ym(ym):
    first, _ = month_bounds(ym)
    return (first - dt.timedelta(days=1)).strftime("%Y-%m")


def money(v):
    return f"−${abs(v):,.2f}" if v < 0 else f"${v:,.2f}"


def delta(a, b):
    x = round(a - b, 2)
    return "$0.00" if x == 0 else ("+" if x > 0 else "−") + f"${abs(x):,.2f}"


def pct(a, b):
    return "new" if b == 0 else f"{(a / b - 1) * 100:+.1f}%"


def expand(txns):
    """Yield one row per categorised line (splits expanded), deleted removed."""
    for t in txns:
        if t.get("deleted"):
            continue
        subs = [s for s in (t.get("subtransactions") or []) if not s.get("deleted")]
        for s in (subs or [t]):
            cat = (s.get("category_name") or "").strip() or None
            yield {"date": t["date"], "payee": t.get("payee_name"), "account": t["account_name"],
                   "cat": cat, "cat_id": s.get("category_id"), "amt": s["amount_currency"],
                   "memo": s.get("memo") or t.get("memo"), "import_id": t.get("import_id"),
                   "transfer": bool(t.get("transfer_account_id"))}


def main():
    sydney_today = dt.datetime.now(ZoneInfo("Australia/Sydney")).date()
    T = sys.argv[1] if len(sys.argv) > 1 else (sydney_today.replace(day=1) - dt.timedelta(days=1)).strftime("%Y-%m")
    P = prev_ym(T)
    PP = prev_ym(P)
    t_first, t_next = month_bounds(T)
    out_dir = f"{WORK}/{T}"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(ASSETS, exist_ok=True)

    mcp = MCP()
    tx = {m: mcp.call("list_transactions", month=f"{m}-01") for m in (T, P)}
    months = {m: mcp.call("get_month", month=f"{m}-01") for m in (T, P)}
    accounts = [a for a in mcp.call("list_accounts") if not a.get("deleted")]
    after = mcp.call("list_transactions", since_date=t_next.isoformat())

    group_of = {}
    budget_rows = {}
    for m in (T, P):
        for c in months[m]["categories"]:
            group_of[c["name"].strip()] = c["category_group_name"]
            budget_rows.setdefault(m, []).append(c)

    # ---- expenses ----
    rows = {m: list(expand(tx[m])) for m in (T, P)}
    cats = defaultdict(lambda: {T: 0.0, P: 0.0})
    counts = defaultdict(lambda: {T: 0, P: 0})
    payees = defaultdict(lambda: {T: defaultdict(float), P: defaultdict(float)})
    inflows = {T: [], P: []}
    rta = {T: [], P: []}
    excluded = {T: [], P: []}
    for m in (T, P):
        for r in rows[m]:
            if r["cat"] == "Inflow: Ready to Assign":
                rta[m].append(r)
                continue
            if r["cat_id"] is None or r["cat"] in EXCLUDED_CATS:
                excluded[m].append(r)
                continue
            if r["amt"] < 0:
                cats[r["cat"]][m] += -r["amt"]
                counts[r["cat"]][m] += 1
                payees[r["cat"]][m][r["payee"]] += -r["amt"]
            elif r["amt"] > 0:
                inflows[m].append(r)
    gross = {m: sum(v[m] for v in cats.values()) for m in (T, P)}
    mortgage_cat = next((c for c in cats if "Mortgage" in c), None)
    mort = {m: cats[mortgage_cat][m] if mortgage_cat else 0.0 for m in (T, P)}
    groups = defaultdict(lambda: {T: 0.0, P: 0.0})
    for c, v in cats.items():
        for m in (T, P):
            groups[group_of.get(c, "?")][m] += v[m]

    # same-date repeat candidates (evidence only; totals unchanged)
    repeats = []
    for m in (T, P):
        seen = defaultdict(list)
        for r in rows[m]:
            if r["amt"] < 0 and r["cat_id"] and r["cat"] not in EXCLUDED_CATS:
                seen[(r["date"], r["payee"], r["amt"], r["account"])].append(r)
        for (d, p, a, acct), v in seen.items():
            if len(v) > 1:
                repeats.append({"month": m, "date": d, "payee": p, "amount": -a, "account": acct,
                                "category": v[0]["cat"], "n": len(v),
                                "import_suffixes": [(x["import_id"] or "manual").split(":")[-1] for x in v]})

    # ---- loans: interest derived from balance (API omits interest charges) ----
    loans = {}
    for a in accounts:
        if a["type"] in ("mortgage", "autoLoan", "studentLoan", "personalLoan", "otherDebt", "medicalDebt"):
            hist = [t for t in mcp.call("list_transactions", account_id=a["id"]) if not t.get("deleted")]
            pays = [t for t in hist if t.get("debt_transaction_type") == "payment"]
            interest_total = a["balance_currency"] - sum(t["amount_currency"] for t in hist)
            n = len(pays)
            mins = a.get("debt_minimum_payments") or {}
            rates = a.get("debt_interest_rates") or {}
            last_min = mins[max(mins)] / 1000 if mins else None
            last_rate = rates[max(rates)] / 1000 if rates else None
            pay_by_month = defaultdict(float)
            for t in pays:
                pay_by_month[t["date"][:7]] += t["amount_currency"]
            uncleared = [t for t in hist if t["cleared"] == "uncleared"]
            loans[a["name"]] = {
                "id": a["id"], "type": a["type"], "balance": a["balance_currency"],
                "interest_total": round(-interest_total, 2), "payments_counted": n,
                "first_payment": min((t["date"] for t in pays), default=None),
                "avg_interest": round(-interest_total / n, 2) if n else 0.0,
                "payment_in_target": round(pay_by_month.get(T, 0.0), 2),
                "payment_in_prior": round(pay_by_month.get(P, 0.0), 2),
                "ynab_min_payment_latest": last_min, "ynab_rate_latest_pct": last_rate,
                "min_payment_mismatch": bool(last_min and pay_by_month.get(T) and abs(pay_by_month[T] - last_min) > 0.01),
                "uncleared_count": 0 if a["name"] in ALWAYS_CLEARED else len(uncleared),
            }

    # ---- month-end balances: reverse transactions back from today ----
    def acct_sums(txns):
        s = defaultdict(float)
        npay = defaultdict(int)
        for t in txns:
            if t.get("deleted"):
                continue
            s[t["account_name"]] += t["amount_currency"]
            if t.get("debt_transaction_type") == "payment":
                npay[t["account_name"]] += 1
        return s, npay

    def roll_back(bal, txns):
        s, npay = acct_sums(txns)
        res = {}
        for name, v in bal.items():
            change = s.get(name, 0.0)
            if name in loans:  # loan balance also moved by interest not visible in txns
                change -= loans[name]["avg_interest"] * npay.get(name, 0)
            res[name] = v - change
        return res

    current = {a["name"]: a["balance_currency"] for a in accounts}
    end = {T: roll_back(current, after)}
    end[P] = roll_back(end[T], tx[T])
    end[PP] = roll_back(end[P], tx[P])
    atype = {a["name"]: a["type"] for a in accounts}

    def bucket(name):
        t = atype[name]
        if t == "mortgage":
            return "Mortgage"
        if name in loans:
            return "Car and other loans"
        if t == "creditCard":
            return "Credit cards"
        if t == "otherAsset":
            return "Super" if "super" in name.lower() else "Investments"
        if t == "otherLiability":
            return "Other liabilities"
        return "Cash and bank"

    nw = {}
    for m in (T, P, PP):
        b = defaultdict(float)
        for name, v in end[m].items():
            b[bucket(name)] += v
        b["Net worth"] = sum(end[m].values())
        nw[m] = {k: round(v, 2) for k, v in b.items()}
    reval = {}
    for m in (T, P):
        reval[m] = round(sum(r["amt"] for r in rows[m] if r["payee"] in ("Reconciliation Balance Adjustment", "Manual Balance Adjustment")
                             and atype.get(r["account"]) == "otherAsset"), 2)
    nw_change = {T: round(nw[T]["Net worth"] - nw[P]["Net worth"], 2),
                 P: round(nw[P]["Net worth"] - nw[PP]["Net worth"], 2)}
    loan_end = {name: {m: round(end[m][name], 2) for m in (PP, P, T)} for name in loans}

    income = {m: months[m]["income_currency"] for m in (T, P)}
    rta_sum = {m: round(sum(r["amt"] for r in rta[m]), 2) for m in (T, P)}

    # ---- charts ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    import numpy as np
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    lab = lambda m: dt.date(*map(int, m.split("-")), 1).strftime("%b %Y")
    short = lambda m: dt.date(*map(int, m.split("-")), 1).strftime("%b")
    fmtk = FuncFormatter(lambda v, _: f"${v / 1000:,.0f}k" if abs(v) >= 1000 else f"${v:,.0f}")

    fig, ax = plt.subplots(figsize=(8, 4.6))
    x = np.arange(3)
    w = 0.36
    for i, (m, col) in enumerate([(P, "#9aa5b1"), (T, "#2b6cb0")]):
        vals = [income[m], gross[m], nw_change[m]]
        bars = ax.bar(x + (i - 0.5) * w, vals, w, label=lab(m), color=col)
        for r, v in zip(bars, vals):
            ax.annotate(f"${v:,.0f}", (r.get_x() + r.get_width() / 2, v), xytext=(0, 3 if v >= 0 else -12),
                        textcoords="offset points", ha="center", fontsize=8)
    ax.axhline(0, color="#333", lw=0.8)
    ax.set_xticks(x, ["Income\n(Ready to Assign)", "Expenses\n(gross categorised)",
                      "Change in net worth\n(all accounts incl. stocks/super)"])
    ax.yaxis.set_major_formatter(fmtk)
    ax.legend(frameon=False)
    ax.set_title(f"Income, expenses and net-worth change: {short(P)} vs {short(T)} {T[:4]}")
    note = "Loan balances net of interest."
    if reval[T]:
        note = f"{short(T)} includes investment/super revaluations ({money(reval[T])}). " + note
    fig.text(0.01, 0.01, note + " Source: YNAB Australia budget.", fontsize=7, color="#555")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    chart1 = f"{T}-income-expenses-networth.png"
    fig.savefig(f"{ASSETS}/{chart1}", dpi=150)
    plt.close(fig)

    chart2 = None
    if loans:
        names = list(loans)
        fig, axs = plt.subplots(1, len(names), figsize=(4.5 * len(names), 4))
        axs = np.atleast_1d(axs)
        colors = ["#c05621", "#2f855a", "#6b46c1", "#2c7a7b"]
        for ax, name, col in zip(axs, names, colors):
            ms = [PP, P, T]
            bal = [-loan_end[name][m] for m in ms]
            bars = ax.bar([f"End {short(m)}" for m in ms], bal, color=col, alpha=0.85)
            ax.set_ylim(min(bal) * 0.985, max(bal) * 1.004)
            for r, v in zip(bars, bal):
                ax.annotate(f"${v:,.0f}", (r.get_x() + r.get_width() / 2, v), xytext=(0, 3),
                            textcoords="offset points", ha="center", fontsize=8)
            ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v / 1000:,.1f}k"))
            L = loans[name]
            pay = L["payment_in_target"] or L["payment_in_prior"]
            ax.set_title(f"{name}\n${pay:,.2f}/month ≈ ${L['avg_interest']:,.0f} interest + ${pay - L['avg_interest']:,.0f} principal", fontsize=10)
        fig.text(0.01, 0.01, "Y-axes truncated. Interest is the average of YNAB interest charges, derived from balances (the API exposes only the total).",
                 fontsize=7, color="#555")
        fig.tight_layout(rect=(0, 0.04, 1, 1))
        chart2 = f"{T}-mortgage-car-loan.png"
        fig.savefig(f"{ASSETS}/{chart2}", dpi=150)
        plt.close(fig)
    os.chmod(ASSETS, 0o755)
    for c in (chart1, chart2):
        if c:
            os.chmod(f"{ASSETS}/{c}", 0o644)

    # ---- tables.md ----
    L = []
    L += [f"| Measure | {lab(T)} | {lab(P)} | Change |", "|---|---:|---:|---:|",
          f"| Gross categorised expenses | {money(gross[T])} | {money(gross[P])} | {delta(gross[T], gross[P])} ({pct(gross[T], gross[P])}) |",
          f"| Mortgage | {money(mort[T])} | {money(mort[P])} | {delta(mort[T], mort[P])} |",
          f"| Expenses excluding mortgage | {money(gross[T] - mort[T])} | {money(gross[P] - mort[P])} | {delta(gross[T] - mort[T], gross[P] - mort[P])} ({pct(gross[T] - mort[T], gross[P] - mort[P])}) |", ""]
    L += ["<!-- income-nw -->", f"| Measure | {lab(T)} | {lab(P)} |", "|---|---:|---:|",
          f"| Income (Inflow: Ready to Assign) | {money(income[T])} | {money(income[P])} |",
          f"| Gross categorised expenses | {money(gross[T])} | {money(gross[P])} |",
          f"| Change in net worth (all accounts) | {money(nw_change[T])} | {money(nw_change[P])} |",
          f"| Change excluding investment/super revaluations | {money(nw_change[T] - reval[T])} | {money(nw_change[P] - reval[P])} |",
          f"| Net worth at month end | {money(nw[T]['Net worth'])} | {money(nw[P]['Net worth'])} |", ""]
    buckets = ["Cash and bank", "Investments", "Super", "Credit cards", "Mortgage", "Car and other loans", "Other liabilities"]
    L += ["<!-- nw-buckets -->", f"| Type | End {short(T)} | End {short(P)} | End {short(PP)} | {short(T)} change |", "|---|---:|---:|---:|---:|"]
    for b in buckets:
        if any(b in nw[m] for m in (T, P, PP)):
            L.append(f"| {b} | {money(nw[T].get(b, 0))} | {money(nw[P].get(b, 0))} | {money(nw[PP].get(b, 0))} | {delta(nw[T].get(b, 0), nw[P].get(b, 0))} |")
    L.append("")
    L += ["<!-- loans -->", f"| Loan | End {short(PP)} | End {short(P)} | End {short(T)} | Repayment | Interest (avg) | Principal (avg) |", "|---|---:|---:|---:|---:|---:|---:|"]
    for name, Lo in loans.items():
        pay = Lo["payment_in_target"] or Lo["payment_in_prior"]
        L.append(f"| {name} | {money(-loan_end[name][PP])} | {money(-loan_end[name][P])} | {money(-loan_end[name][T])} | {money(pay)} | ≈{money(Lo['avg_interest'])} | ≈{money(pay - Lo['avg_interest'])} |")
    L.append("")
    L += ["<!-- groups -->", f"| Group | {lab(T)} | {lab(P)} | Change |", "|---|---:|---:|---:|"]
    for g, v in sorted(groups.items(), key=lambda kv: -kv[1][T]):
        L.append(f"| {g} | {money(v[T])} | {money(v[P])} | {delta(v[T], v[P])} ({pct(v[T], v[P])}) |")
    L.append("")
    L += ["<!-- categories -->", f"| Category | {lab(T)} | {lab(P)} | Change |", "|---|---:|---:|---:|"]
    for c, v in sorted(cats.items(), key=lambda kv: -(kv[1][T] + kv[1][P])):
        L.append(f"| {c} | {money(v[T])} | {money(v[P])} | {delta(v[T], v[P])} |")
    L.append(f"| **Total** | **{money(gross[T])}** | **{money(gross[P])}** | **{delta(gross[T], gross[P])}** |")
    open(f"{out_dir}/tables.md", "w").write("\n".join(L) + "\n")

    # ---- data.json + compact summary ----
    def top(c, m, k=5):
        return [[p, round(a, 2)] for p, a in sorted(payees[c][m].items(), key=lambda kv: -kv[1])[:k]]

    cat_detail = []
    for c, v in sorted(cats.items(), key=lambda kv: -abs(kv[1][T] - kv[1][P])):
        cat_detail.append({"cat": c, "group": group_of.get(c), T: round(v[T], 2), P: round(v[P], 2),
                           "delta": round(v[T] - v[P], 2), "n": [counts[c][T], counts[c][P]],
                           "avg": [round(v[T] / counts[c][T], 2) if counts[c][T] else None,
                                   round(v[P] / counts[c][P], 2) if counts[c][P] else None],
                           "top_payees": {T: top(c, T), P: top(c, P)}})
    big = [{"month": m, "date": r["date"], "payee": r["payee"], "cat": r["cat"], "amt": r["amt"], "memo": r["memo"]}
           for m in (T, P) for r in rows[m] if r["amt"] <= -250 and r["cat_id"] and r["cat"] not in EXCLUDED_CATS]
    overspent = {m: [{"cat": c["name"].strip(), "group": c["category_group_name"], "budgeted": c["budgeted_currency"],
                      "activity": c["activity_currency"], "balance": c["balance_currency"]}
                     for c in budget_rows[m] if c["balance_currency"] < 0 and not c.get("deleted") and not c.get("hidden")]
                 for m in (T, P)}
    summary = {
        "target_month": T, "prior_month": P, "generated_sydney": sydney_today.isoformat(),
        "wiki_page": f"{VAULT}/queries/{T}-monthly-financial-wrap.md",
        "tables_md": f"{out_dir}/tables.md", "data_json": f"{out_dir}/data.json",
        "charts": [f"assets/{c}" for c in (chart1, chart2) if c],
        "gross_expenses": {T: round(gross[T], 2), P: round(gross[P], 2)},
        "mortgage": {T: mort[T], P: mort[P]},
        "income_get_month": income, "income_rta_sum": rta_sum,
        "income_reconciles": all(abs(income[m] - rta_sum[m]) < 0.01 for m in (T, P)),
        "rta_lines": {m: [[r["date"], r["payee"], r["amt"], r["memo"]] for r in rta[m]] for m in (T, P)},
        "category_inflows": {m: [[r["date"], r["payee"], r["cat"], r["amt"], r["memo"]] for r in inflows[m]] for m in (T, P)},
        "excluded_uncategorised_non_transfer": {m: [[r["date"], r["payee"], r["account"], r["amt"], r["memo"]]
                                                    for r in excluded[m] if not r["transfer"]] for m in (T, P)},
        "to_be_budgeted": {m: months[m]["to_be_budgeted_currency"] for m in (T, P)},
        "overspent": overspent,
        "groups": {g: {T: round(v[T], 2), P: round(v[P], 2)} for g, v in groups.items()},
        "categories_by_abs_delta": cat_detail,
        "large_outflows_250_plus": big,
        "same_date_repeats": repeats,
        "net_worth": nw, "net_worth_change": nw_change, "asset_revaluations": reval,
        "loans": loans, "loan_month_end": loan_end,
        "notes": ["Loan balances are reconstructed net of average interest; only the target month-end balance is exact.",
                  "WestPac Mortgage transfers cannot be cleared in YNAB; treated as cleared.",
                  "Property is not tracked in YNAB, so net worth includes the mortgage with no house value."],
    }
    json.dump(summary, open(f"{out_dir}/data.json", "w"), indent=1, ensure_ascii=False)
    # compact stdout: drop the bulkiest fields (still in data.json)
    compact = dict(summary)
    compact["categories_by_abs_delta"] = cat_detail[:15]
    print(json.dumps(compact, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
