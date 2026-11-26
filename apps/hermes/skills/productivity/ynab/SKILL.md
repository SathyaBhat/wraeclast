---
name: ynab
description: Query and manage YNAB budgets — spending analysis, transactions, categories, accounts, and scheduled transactions via the YNAB MCP tools.
triggers:
  - "how much did I spend on X"
  - "YNAB"
  - "budget"
  - "transactions"
  - "spending this month"
  - "gym / fitness spending"
  - "categorise transaction"
---

# YNAB Skill

## Default Budget
Always set the default budget to the **Australia** budget at session start if it isn't already set:
- Budget ID: `924a80ac-d251-40ed-96a3-a4a3d6f620d5`
- Use `set_default_budget` once and omit `budget_id` on all subsequent calls.

If the default isn't configured, `list_budgets` will tell you — pick the most recently modified AUD budget.

## How the MCP Server is Called

The YNAB MCP runs as an HTTP/SSE MCP server (not a local process). The Hermes runtime handles the session negotiation transparently — just use the tools normally. If you ever need to call it directly via `curl` (debugging, scripting), the flow is:

1. **Initialize** — POST to the server URL with `{"method":"initialize",...}`. Grab the `Mcp-Session-Id` header from the response.
2. **All subsequent calls** — POST with `Mcp-Session-Id: <id>` header and `{"method":"tools/call","params":{"name":"<tool>","arguments":{...}}}`.
3. **Responses** come back as SSE: parse lines starting with `data: ` and extract `.result.content[0].text`, then JSON-parse that string to get the actual payload.

See `references/mcp-http-curl.md` for a working curl template.

For comparing a bank statement against YNAB and adding missing entries (or reconciling an account), see `references/bank-statement-reconciliation.md`.

## Typical Workflow: Spending by Category

1. `set_default_budget` with the Australia budget ID (once per session).
2. Call `list_transactions` with `since_date` / `until_date` (ISO format).
3. If the response is truncated, **grab any `category_id` visible in the truncated output** and use it to call `list_transactions(category_id=..., since_date=..., until_date=...)` — this returns only that category's transactions in full, without hitting the size limit.
4. If you need to discover category IDs first, call `list_categories` — but be aware the response can be **274KB+ (single escaped JSON line)**; see pitfalls below. To extract IDs efficiently, save the file and use `execute_code` with a Python script that strips the outer `{"result": "..."}` wrapper and searches `name` fields with regex/keyword matching.
5. Sum `amount_currency` fields (negative = outflow). Group by `payee_name` or `memo` for a breakdown.

## Typical Workflow: Like-for-Like Multi-Month Spending Comparison

Use this when comparing spending "through the 20th" (or another day) across several months.

1. Fetch transactions for the same inclusive day range in every month, e.g. `YYYY-MM-01` through `YYYY-MM-20`.
2. Expand split transactions into their subtransactions; attribute each child to the parent payee for merchant analysis.
3. Exclude deleted entries and unclassified account-to-account movements (`category_id` null, `Uncategorized`, or `Inflow: Ready to Assign`). Retain a transfer only when it has a genuine spending category such as `🏡 Mortgage`.
4. Report **gross expenses** as the sum of negative categorised transaction amounts, not only net category activity. State refunds/category inflows separately. This prevents stock/forex proceeds, reimbursements, emergency-fund movements, or refunds from making an expense month appear negative.
5. Separately show **excluding mortgage** spending. Identify exceptional outliers (tax settlements, work trips, major home purchases) and provide an adjusted comparison that excludes them, while retaining them in the headline total.
6. Present a compact aligned-month table plus the largest category deltas; label a month-to-date projection as a simple run rate, not a forecast.

### Pitfall: Net spending can be misleading
Summing negative and positive categorised amounts together is useful for a cash-flow net, but not a standalone expenses comparison. Positive amounts may be genuine refunds, but can also be proceeds or funding movements miscategorised into expense categories. Always calculate gross outflows first and reconcile the difference to positive category inflows before drawing a trend conclusion.

## Typical Workflow: Full Billing History for a Category

When the user asks "what about before/after" or wants a complete picture across all time:
1. Call `list_transactions(category_id=<id>)` with **no date filter** — returns all transactions ever for that category.
2. Present results sorted by date with a running context (e.g. which season/quarter each bill covers).
3. Note any anomalies: double bills in the same month (possible adjustment/credit), large YoY jumps (tariff increases), gaps (missed quarter = direct debit or credit applied).

## Typical Workflow: Merchant-Based Spend (cross-category)

When the user asks how much was spent with a merchant/service, do **not** assume its category is reliable. Transactions can be miscoded.
1. Identify the payee ID from any known matching transaction, then call `list_transactions(payee_id=<id>, since_date=...)` to capture every transaction for that payee across categories.
2. Sum negative `amount_currency` values, excluding deleted entries and transfers.
3. Report any miscategorizations separately. Example: EV charging payee `Evie/NRMA/Chargefox` includes a charge that was categorised under `🔦 Electricity`, not `⚡ Charging`.
4. If the user names multiple merchant spellings (e.g. Evie or Chargefox), search/payee-scope each resolved payee rather than relying on one category.

## Typical Workflow: Weekly/Monthly Financial Wrap

1. `set_default_budget` → Australia budget.
2. `list_transactions(since_date="YYYY-MM-DD")` — fetches all transactions from that date forward.
3. **Expand split transactions**: if `subtransactions` is non-empty, iterate those for the real category breakdown (the parent has `category_name: "Split"` which is meaningless).
4. **Handle transfers by category, not transfer status alone.** Skip deleted transactions and unclassified account-to-account movements (`category_id` is null / category is `Uncategorized` or `Inflow: Ready to Assign`) to prevent double-counting. But **include a negative transfer with a genuine spending category**—for example, the categorised `🏡 Mortgage` outflow—to avoid omitting real spending.
5. `get_month(month="YYYY-MM-01")` — returns 187 categories with `balance_currency`, `budgeted_currency`, `activity_currency`, `goal_target_currency`. Use this for the "remaining balance" column. The month-level `activity` is spending activity; report income separately rather than treating activity as inflated by income.
6. **Reconcile income explicitly.** `get_month.income_currency` is YNAB's total of entries categorised `Inflow: Ready to Assign`. Derive its source breakdown from positive transactions in that category, excluding internal transfers. Keep reimbursements distinct from employment/operating income. Do **not** call positive inflows in ordinary spending categories (e.g. refunds, work-trip reimbursements, stock-sale/FX movements) income; report them as category inflows or asset/cash movements, with their category and treatment stated.
7. Flag over-budget categories where `balance_currency < 0` with 🚨.
8. See `templates/weekly-wrap.md` for the output format and category emoji map.

## Key Tool Names (confirmed working)
`set_default_budget`, `list_transactions`, `get_month`, `list_categories`, `get_category`,
`list_accounts`, `get_account`, `list_payees`, `get_payee`, `list_months`,
`create_transactions`, `update_transaction`, `update_transactions`,
`list_scheduled_transactions`, `list_budgets`, `get_budget`,
`list_money_movements`, `list_money_movement_groups`.

> ⚠️ `get_budget_month` does NOT exist — use `get_month` to get category balances for a month.

## Key Categories (Australia budget)
- 🧘 Fitness: `2c21a8cd-923b-4a18-a6d4-68cb84a724ac`
- ♨️ Gas (Fixed Bills): `e1d2f4ab-9a23-499b-acb5-ee065040fee9` — AGL, quarterly bills ~$140–$240
- 🔦 Electricity (Fixed Bills): `350a65fc-5ab0-4aaf-80e3-e022f2c28e40`
- 🚰 Water (Fixed Bills): `3513e32d-2c91-4265-9470-ce5368a055c9`
- 💻 Internet (Fixed Bills): `ec30c4c1-ab8a-4113-995d-2823ce204790`

## User Context
- **Fitbox** (Fitbox Lawnton) = new gym, regular charge ~$50/week. Drop-in sessions were $27 each.
- **BBB** (WODIFY* WP BBB GYM NOR NORTH SYDNEY) = old gym / PT sessions at $230 each, being wound down.
- **Blacktown Council** = swim class for kids ("swim class for big"), $43.45/session, recurring ~monthly.

## Pitfalls

### Large tool responses
`list_categories` returns a 274KB response as a **single line** with the entire JSON array double-escaped inside a `{"result": "..."}` wrapper. Standard `json.loads` will fail on the truncated file saved to disk. To parse it correctly in `execute_code`, strip the wrapper and unescape manually:
```python
import json, re
with open('/tmp/hermes-results/<file>.txt') as f:
    raw = f.read()
m = re.match(r'^\{"result": "(.*?)"\}$', raw, re.DOTALL)
inner = m.group(1).replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
data = json.loads(inner)
# Then keyword-search name/category_group_name fields to find category IDs
```
Better approach: **avoid `list_categories` for spending queries** — grab `category_id` from transaction output instead.

### Transaction output truncation
`list_transactions` without a scope filter across all categories can truncate at ~179K chars. Always scope by `category_id`, `payee_id`, or a narrow date range when possible.

### Multiple budgets
Sathya has 7 budgets (EUR, INR ×4, RON, AUD). The Australia (AUD) budget (ID 924a80ac-d251-40ed-96a3-a4a3d6f620d5) is the default and active one. EV charging transactions can be miscategorised under Electricity (e.g. a $32.49 Evie/FastCities charge); for EV-cost queries also search the Evie/NRMA/Chargefox payees as well as the Charging category. For the Home Assistant Finance dashboard, prefer visual spent-versus-budget bar charts over text tables, prioritising Food Bills, Variable Expenses and Just For Fun. Always confirm you're on the right budget before making writes.
