# Bank statement vs YNAB reconciliation

Use when the user shares bank statement screenshots/pasted rows and asks what is missing from YNAB, then wants entries added.

## Procedure
1. Get statement rows: transcribe screenshots with vision, or use pasted text. Screenshots may cover only part of the statement; ask for or expect a later paste of the rest.
2. `list_accounts` to find the account id (WestPac Choice = `317d8e8d-94e4-4081-8983-cebb730c1a1c`). Compare the statement closing balance with `get_account` balance/cleared_balance first, to size the gap.
3. `list_transactions(account_id=..., since_date=<a few days before statement start>)`. Match each statement row by amount and date (YNAB dates can differ by 1-3 days from statement posting dates; EFTPOS rows post days after the purchase). Transfers, deposits and the mortgage direct debit usually already exist.
4. Report the missing rows as a table with date, description, amount. Sum them and compare with the balance gap; any remainder means rows are hidden above/below the screenshot or an entry was added meanwhile. Re-pull the account before declaring a row missing, since the user may have added it in the app in parallel.
5. Do NOT guess payee/category. Ask the user once for all missing rows; they typically answer with merchant identity (e.g. `HJs` = Hungry Jack's, `DK` = Donut King) and category in one message. Skip rows the user says are already handled.
6. Create with `create_transactions` (`cleared: cleared`, `approved: true`, memo only when the user gave a description). Use readable payee names, not the raw bank string. Reuse the same payee name for repeated merchants.
7. Fix categories afterwards with `update_transactions` (id + category_id only).
8. Verify: `get_account` balance equals the statement closing balance.

## Category lookup
`list_categories` output is huge and spills to a file; parse that file in `execute_code` and regex the names (see SKILL.md pitfall). Frequently used (Australia budget):
- 🥡 Dining Out `0c46f750-56fa-4220-a28e-2a49fa42fd1a`
- 🍞 Breakfast & Snacks `81f4c970-af37-4884-a6f9-05d51df24d60` (donuts, cafe snacks)
- 🎁 Gifts `2eb524ab-2f2e-4d94-bc92-45151d9cc712`
- 🕐 One Time Expenses `97f8f15c-ccee-4f60-9cb4-c0c920b0cdcb`
- 🤷‍♀️ Jo's Fun Money `1f67136e-c55b-412a-8ffe-7d306f054017`
- 🤷‍♂️ Sathya's Fun Money `a6a7daaf-34b1-433a-8392-2bb2f77794ca`
- 💇🏽‍♀️ Salon Visits `95bf8e11-a604-4fc9-8084-91c1892ea99f` (nails)
- 🍌 Groceries `89ef3964-379d-43e6-ac92-fcc0ec6de3a8`
- 👩‍💼 Jo's Office Food `566f262e-504d-4dae-a02d-c7ecfa8beffd`
- 🛠 Home Maintenance `1610cb93-1382-4825-aa9e-364dc6f70ce1`
Ignore hidden categories (Dining Out Week N, etc.).

## Reconciled status
- The YNAB API cannot set an account's `last_reconciled_at`; it is read-only. Setting transactions to `cleared: reconciled` via `update_transactions` works but does NOT move that date. Only the app's Reconcile button does. Tell the user to press Reconcile in the app once balances match.
- Marking reconciled is a bulk write the user did not ask for: do it only on request, and skip scheduled-transaction instances (ids like `<uuid>_YYYY-MM-DD`, e.g. the mortgage), which the update call does not cover.
