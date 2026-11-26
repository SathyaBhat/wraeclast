# Read-only cron run forensics

Use when scheduler status and the saved final response disagree, or a stopped run may have made partial external changes.

## 1. Inspect execution history

Open SQLite without permitting writes:

```python
import sqlite3
from pathlib import Path

home = Path(HERMES_HOME)  # use the discovered active profile home
conn = sqlite3.connect(f"file:{home / 'cron/executions.db'}?mode=ro", uri=True)
conn.row_factory = sqlite3.Row
rows = conn.execute(
    "SELECT * FROM executions WHERE job_id=? ORDER BY claimed_at DESC LIMIT 3",
    (job_id,),
).fetchall()
```

Compare `status`, `error`, `started_at`, `finished_at`, and `delivery_outcome`. A completed retry can supersede a failed scheduled attempt in `jobs.json`; report them separately. Do not equate `delivered` with successful task execution.

## 2. Locate and inspect the cron transcript

Connect to `state.db` with the same read-only URI pattern. Query cron sessions around the execution interval and match job ID and timestamp; do not hard-code a session ID format as the only lookup method.

```sql
SELECT id, started_at, ended_at, end_reason
FROM sessions
WHERE source='cron'
ORDER BY started_at DESC LIMIT 20;

SELECT id, role, tool_name, content, tool_calls
FROM messages
WHERE session_id=?
ORDER BY id;

SELECT tool_name, COUNT(*)
FROM messages
WHERE session_id=? AND role='tool'
GROUP BY tool_name;
```

Filter before printing large transcripts. Inspect final messages for the exact guardrail code and reason. Count recorded tool responses separately from successful searches: blocked attempts can inflate the transcript count beyond the guardrail's successful-call budget.

Use a short multiline Python script rather than deeply nested shell quoting for SQLite queries and JSON parsing; quoting failures obscure the actual evidence.

## 3. Recover partial external changes

Collect all tracker write results, then find later reads of the exact returned IDs or URLs. Classify each as added, updated, or moved using before/after state and source fields, not merely the number of write calls.

Tool-result content may wrap a JSON object inside an untrusted-result envelope and encode the provider payload as a JSON string in `result`. Parse the envelope payload and then decode `result` when it is a string. Support both a single-card object and a `cards` array. A matching card in a pre-write board enumeration is not a post-write verification: compare message ordering.

For every reported change, retain its exact target ID/URL, expected destination, and readback evidence. When a write acknowledgement has no later exact-target readback, read the live target or explicitly label the change as not verified. Do not infer a duplicate count from search or write totals.

## 4. Explain the result

Lead with one of: completed, partially completed, or failed before work began. List verified useful changes before discussing the blocker. Explain when scheduler `ok` means only that the agent returned text. Include delivery status only when supported by execution evidence, and convert execution/next-run timestamps with `zoneinfo` rather than mental arithmetic.
