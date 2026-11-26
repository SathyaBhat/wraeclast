---
name: australian-foreign-share-cgt
description: "Use for Australian CGT on foreign shares and vested RSUs."
---
# Australian foreign-share CGT

Treat results as provisional until residency, ESS classification and valuations are established; recommend registered tax-agent review for cross-border ESS.

- Read all broker lots with openpyxl and Decimal; reconcile quantities and cost/proceeds/gain columns. US RSU acquisition cost can be zero while adjusted cost includes vest income. Neither establishes Australian basis automatically. US ESPP qualifying-disposition adjustments are not Australian ESS classifications.
- Establish tax residency separately from visa PR. Check temporary visa history, spouse citizen/PR/protected NZ status, previous disqualifying residency, and the date temporary residency ended. Keep group-chat participants' tax facts separate.
- Read current ITAA1997 s768-955: https://www.ato.gov.au/law/view/document?DocID=PAC/19970038/768-955 . Subsections (2)-(3) reset market-value cost/reduced cost base and acquisition time when temporary residency ends while Australian residency continues. Subsection (4) excludes pending deferred ESS taxing points and qualifying startup interests—not all ESS shares. Prefer the statute over broad ATO summary wording. Check taxing-point completion, disposal restrictions, purchases and vesting dates.
- Separate historical ESS employment income from later CGT. Fully vested/purchased foreign interests whose taxing points completed before Australian residence generally do not generate new ESS income on a later sale. Foreign withholding at vest is not an additional sale cost or automatically an Australian tax credit.
- Obtain market value at actual cessation time. A US calendar-day close occurs the following morning in eastern Australia. Check PR grant/effective timestamp and time zones. Label daily-close illustrations as assumptions; do not silently use a future US close as PR-time value.
- Retrieve RBA daily rates: https://www.rba.gov.au/statistics/tables/csv/f11.1-data.csv . USD field is USD per AUD: divide USD amounts by it. Convert basis at valuation and proceeds at disposal separately, not the combined broker USD gain once. Avoid double-counting fees netted in proceeds.
- Compute each lot and aggregate in code. Verify workbook counts/totals. Distinguish total gains, total losses and return-wide net capital gain after other CGT events. Capital losses are not salary deductions; check current ss102-10 and102-15. Do not apply discounts to losses or use US long-term labels for Australian eligibility after deemed acquisition.
- Load grounded-citations and xlsx. If ATO web_extract fails, try direct urllib/curl with HTML parsing; its legal database may work even when the scraping service fails. Preserve archive timestamps when citing snapshots.
