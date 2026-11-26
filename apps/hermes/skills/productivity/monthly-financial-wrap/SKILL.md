---
name: monthly-financial-wrap
description: Use when creating monthly YNAB wraps. Reconcile spending.
triggers:
  - "monthly financial wrap"
  - "monthly spending summary"
  - "expenses by category"
  - "compare this month with last month"
---

# Monthly Financial Wrap

Create an accurate, decision-useful monthly financial wrap for the YNAB Australia budget.

## Automated run (scheduled job or "run the monthly wrap")

Use `scripts/build_wrap_data.py` for the data. Do not re-fetch it by hand. The script is run by `/opt/data/scripts/ynab_monthly_wrap.sh`, a cron pre-run that proceeds only at 12:00 Australia/Sydney. Set `FORCE_WRAP=1` to run it manually, optionally passing `YYYY-MM`; by default it covers the previous Sydney month.

The script does the following:
- calls the YNAB MCP over HTTP using `MCP_YNAB_MCP_API_KEY`;
- applies every expense rule below;
- derives loan interest from balances;
- reconstructs the month-end balances for net worth;
- renders `queries/assets/<YYYY-MM>-income-expenses-networth.png` and `<YYYY-MM>-mortgage-car-loan.png`;
- writes `/opt/data/workspace/ynab-wrap/<YYYY-MM>/tables.md` (ready-made tables, with sections marked by `<!-- … -->`) and `data.json`;
- prints a compact JSON summary to stdout.

Agent steps after the script:
1. Read the summary from the script output. If you need more detail, read `data.json` with `read_file`.
2. Write `queries/<YYYY-MM>-monthly-financial-wrap.md` following the 2026-10 page as the reference layout. Copy each table verbatim from `tables.md`; never retype numbers. The sections are:
   - Headline
   - Income, expenses and net worth, with the chart and the net-worth tables
   - Mortgage and car loan, with the chart, the loans table, the interest method note, and any minimum-payment mismatch
   - Expenses by category group
   - Expenses by category
   - Income and category inflows
   - Insights (3–7, evidence-based, from `categories_by_abs_delta`, `large_outflows_250_plus`, `overspent` and the inflows)
   - Same-date repeat charges
3. If the prior month's wiki page shows a different prior-month total, state the restated figure and the difference.
4. Update `index.md` (date, LLM-wiki count +1, Financial planning entry) and append a `create` entry to `log.md`. Set permissions to 644.
5. If the script fails or `income_reconciles` is false, still save what can be verified, and flag the problem in both the page and the final reply.
6. In a scheduled run, the final reply is delivered to the Discord home channel. Keep it to 1–3 lines: the wrap was saved to the wiki, the page path, and the headline expense change. Do not post the full report.

## Prerequisites

1. Load the `ynab` skill and follow its transaction and split-handling rules.
2. Set the default budget to Australia: `924a80ac-d251-40ed-96a3-a4a3d6f620d5`.
3. Fetch both target month and prior month with `list_transactions(month="YYYY-MM-01")`.
4. Also fetch each month through `get_month(month="YYYY-MM-01")` when budget availability, income, or overspending needs analysis.
5. Large MCP responses are commonly written to spillover files. Parse the saved output using `execute_code`; do not re-request an identical query.

## Expense calculation rules

- Expand split transactions and attribute each subtransaction to its actual category. Do not count the split parent.
- Exclude deleted transactions.
- Exclude unclassified account-to-account movements: missing `category_id`, `Uncategorized`, and `Inflow: Ready to Assign`.
- Include a transfer that has a real spending category, such as Mortgage or Car Loan.
- Calculate **gross expenses** from negative categorised amounts only. Keep positive categorised amounts as a separate `category inflows/refunds` figure.
- Never headline net category activity as expenses: refunds, reimbursements, stock sales, foreign-exchange movements, and funding transfers can make it misleading.
- Show all nonzero category outflows for each month. A compact table is fine, but do not silently omit smaller categories; aggregate only when clearly labelled.

## Income reconciliation

Treat these distinctly:

1. **YNAB income:** transactions categorised `Inflow: Ready to Assign`; reconcile this to `get_month().income_currency`.
2. **Employment income:** salary/wage transactions within the above; separate reimbursements if they should not be presented as ordinary income.
3. **Asset/cash movements:** stock-sale proceeds, FX conversions, and internal transfers. Report separately, never as salary or routine income.

For August 2026, the correct YNAB Inflow: Ready to Assign calculation was $35,475.28: The Trade Desk $28,941.98 + XPT Software $6,480.80 + a $52.50 phone reimbursement. The separate $15,285.56 stock-sale/FX movement was not salary income.

## Required presentation

Include:

1. Headline gross expenses for both months and dollar/percentage change.
2. Expenses excluding mortgage when relevant.
3. A full category table: target month, prior month, and change.
4. Category inflows/refunds and reimbursements explained separately where material.
5. Three to seven evidence-based insights. Focus on large deltas, recurring-vs-one-off costs, spending frequency, budget availability/overspending, and categorisation issues. For material food, commuting, fitness, or office-spend changes, compare transaction counts and average ticket size; identify the largest merchants only when verified from the transaction data.
6. State explicitly if a comparison is affected by travel, large annual/quarterly bills, asset sales, reimbursements, or other exceptional movements.

## Quality checks

- Check exact transaction details for unusually large entries before describing their cause.
- Detect same-date/same-payee repeats, but do not call them duplicates merely because values match; use distinct import IDs/transactions as evidence and describe cautiously. List materially affecting candidates with their date, payee, amount, account, and distinct import-ID suffixes, then recommend statement reconciliation rather than changing totals.
- Reconcile key totals programmatically. Use `execute_code` or `terminal` for arithmetic; do not calculate manually.
- If using percentage changes, handle a zero prior month as `new` rather than dividing by zero.

## Net worth and loan charts (when asked)

- `list_accounts` gives current balances only. Reconstruct month-end balances by subtracting transactions dated after month end (including today's), then reversing each month's per-account transaction sums (`list_transactions(month=...)`, all accounts, including transfers and uncategorised reconciliation adjustments).
- Group accounts into cash/bank, investments (IBKR, Stock Plan, AGSN, eTrade), super, credit card, mortgage and car loan. Property is not tracked in YNAB, so net worth is negative; say so.
- Investments are revalued only through occasional "Reconciliation Balance Adjustment" entries. Report the change in net worth with and without those entries.
- Sathya enters actual interest charges on loans in the YNAB web app. The API and MCP do not return them: there are no `debt_transaction_type: "interest"` rows, which was checked against a direct API call. Derive interest as current balance − starting balance − payments − adjustments, then average it over the repayments. Do not estimate from `debt_interest_rates`, because the rate gave about $7.6k/month against an actual ≈$6.0k for the mortgage. When reconstructing earlier month-end loan balances, reverse each payment net of interest.
- WestPac Mortgage transfers cannot be marked cleared in YNAB. Treat their "uncleared" status as cleared and don't flag it.
- Compare the payment made with `debt_minimum_payments`.
- Charts: build matplotlib in a uv venv under the scratch directory, and save PNGs to `queries/assets/`, embedding them with `![[assets/<file>.png]]`.
- Discord delivery: `hermes send` from the TUI shell fails because DISCORD_BOT_TOKEN is not in this shell's environment, even though the gateway's Discord connection works. Ask the user how to deliver before trying a workaround. The #ynab-finance channel ID is 699249623281303604; cron jobs post there with `deliver: discord:699249623281303604`. For a summary with the detail as a threaded reply under it (how the AustralianSuper monthly report posts), follow `scheduled-job-maintenance` → `references/report-jobs.md`.

## Save to the Obsidian wiki (only when asked)

1. Load the `obsidian` skill and read `/opt/data/obsidian/notes/SCHEMA.md`, `index.md`, and `log.md`.
2. Store the durable wrap in `/opt/data/obsidian/notes/queries/` using a lowercase hyphenated filename, e.g. `2026-08-monthly-financial-wrap.md`.
3. Include YAML frontmatter: `title`, `created`, `updated`, `type`, `tags`, and `sources`.
4. In the same task, update `index.md` with the current date, correct LLM-wiki count, and a catalogue entry; append a dated `create`, `update`, `archive`, or `delete` record to `log.md` that names every changed path.
5. Verify the writes and use `chmod 755` on newly created directories and `chmod 644` on files for Syncthing/host readability.

## Output style

Use AUD formatting, concise tables, and direct insights. Do not treat category inflows as income. Do not state unverified causes for a delta.
