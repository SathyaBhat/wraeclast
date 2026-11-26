---
name: job-search
description: "Use when finding, vetting, comparing, or monitoring job opportunities for a user. Covers live-status verification, compensation and location filters, duplicate-safe tracking, and recurring searches."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [jobs, careers, research, monitoring, cron]
    related_skills: [research, hermes-agent]
---

# Job search and monitoring

Use for one-off job searches, curated shortlists, and recurring job-watch workflows.

## 1. Establish the search contract

Record the user's target functions, seniority, preferred location/remote arrangement, and compensation floor. Treat compensation as a filter only when it is explicitly listed on a trustworthy source; do not infer a salary from title or market averages.

For current-job research, search broadly but report only roles that meet the user's stated filters. State where work arrangement or compensation is not disclosed.

## 2. Discover broadly, verify narrowly

1. Search across job boards and search indexes to surface candidates.
2. For every candidate to be presented, open the employer's official career page or the employer's live ATS page.
3. Include a role only after verifying that it is active and accepting applications.
4. Prefer the canonical employer/ATS URL in the final shortlist.
5. Explicitly exclude stale results, reposts, expired listings, or pages marked closed/no longer accepting applications.

### Pitfall: indexed results go stale

Search results and third-party aggregators routinely retain closed jobs. A title/snippet or LinkedIn/SEEK index result is discovery evidence, not proof that a job is open. Check the original listing immediately before presentation and remove a candidate when the user identifies it as closed.

## 3. Assess fit without overselling

For each viable role, briefly cover:
- title, employer, location and work arrangement;
- disclosed compensation, or "not disclosed";
- concrete overlap with the user's experience;
- meaningful gaps or constraints (for example, mandatory language depth, people management, office cadence, or different cloud stack).

Keep title and seniority calibration explicit. A role may be a good technical fit but still be below the user's current level.

## 4. Recurring job watches

Use a durable tracker when the user asks for monitoring. A Markdown note, database, or Notion page should contain at least:

| First seen | Company | Role | Work arrangement | Compensation | Why it matches | Source |
| --- | --- | --- | --- | --- | --- | --- |

### Duplicate-safe update algorithm

1. Read the entire existing tracker before searching.
2. Use `employer + normalised role title + canonical source URL` as the duplicate key.
3. Search and verify a fresh batch of roles.
4. Append only newly verified active roles; never re-add an existing key.
5. Preserve existing entries. If status tracking is requested, record closure/status separately rather than silently deleting rows.
6. Append a concise run-history record, including zero-result runs when the user wants an audit trail.

### Cron-job requirements

When configuring a recurring Hermes job:
- make the prompt fully self-contained: criteria, verification requirements, tracker location, duplicate key, and output schema;
- bound each run explicitly: set a discovery-search budget, prohibit repeated identical queries, cap canonical-page recovery attempts per candidate, and rotate source groups across runs instead of interpreting a broad source catalogue as an exhaustive per-run obligation; reserve capacity for tracker write/readback and the final report, and report unresolved candidates as unverified rather than continuing discovery indefinitely;
- require incomplete-run reports to preserve and enumerate any verified changes already made; never hard-code `no changes made` for all failures, since a later search or verification failure can occur after successful tracker writes;
- use web/file tools for a Markdown tracker, plus the relevant external integration toolset for a remote database;
- schedule by interval when exact local clock times are not required, avoiding daylight-saving ambiguity;
- run the job once immediately after creation and verify its actual output, tool health, and duplicate behaviour;
- require every run to report operational health separately from tracker changes: a `healthy` result only when all tools used succeeded; otherwise a concise `DEGRADED` line naming the failed/blocked/rate-limited capability, any fallback, and whether discovery or verification coverage was reduced;
- never treat a scheduler `completed` status or a no-change tracker result as proof that the web search was exhaustive; surface search, extraction, browser, credential, billing, or verification failures in the delivery;
- add an explicit completion gate to job-watch prompts: require a board/tracker read, multiple discovery searches, canonical verification, and deduplication before a normal no-change or duplicate-count report; otherwise require a degraded/incomplete result rather than an invented zero count;
- when using self-hosted Firecrawl for discovery, test a representative `/v2/search` request separately from `/v2/scrape` before relying on it: a working scraper does not prove that search has an upstream provider, and an empty successful payload must reduce coverage rather than count as a zero-result market;
- remember that TUI-local cron delivery is saved locally, not delivered to the active chat.

### Trello-backed watches

Use Trello when the user wants a visual pipeline rather than a database. Before creating or migrating a watch:

1. Read the target board and enumerate **all** open lists; record the board and destination-list ARIs verbatim.
2. If the board holds multiple people’s pipelines, name the permitted lists explicitly in the cron prompt. New roles should enter that person’s `Todo` list; later confirmed closures should move only that person’s cards to their `Done` list. Never rely on a generic list name such as `To Do` when an owner-specific list exists.
3. Inspect existing cards across the board before writing. Deduplicate first by the canonical employer/ATS URL stored in the card description; use employer plus normalised role title only as a legacy fallback.
4. Create one card per verified role. Include stable labelled fields in the description: `Owner`, `Source`, `Work arrangement`, `Compensation`, `Fit`, and `First seen`. Read the card back after creation and verify its name, destination list, and canonical source URL.
5. Set the cron job’s `deliver` independently from the tracking destination. Trello is where cards are written; a Telegram/Discord `deliver` target remains necessary when the user wants run notifications. Pause old relay jobs only when the main job now sends both success summaries and failures to the intended notification target.

### Notion-backed watches and notification routing

1. Fetch the destination data source before creating the watch. If it lacks a canonical-source URL field, add a `URL` property (for example, `Source URL`) and, where useful, a date-only `First seen` property. Re-fetch the schema before creating records.
2. Store the canonical employer/ATS URL in that URL property and query it before every write. This makes cross-run deduplication reliable; title-only matching is a fallback for legacy rows, not the primary key.
3. Put the job's normal cron `deliver` target on the default/error channel. In the prompt, require an empty response for zero-result and duplicate-only runs, and require a concise failure response so cron routes failures to that default channel.
4. For success notifications that belong in a different chat/topic, require the cron agent to use its messaging tool only when it creates one or more records. Include the explicit `platform:chat_id:thread_id` destination in the self-contained prompt. This prevents routine no-op reports and ensures the careers notification reaches the intended topic rather than the cron origin.
5. Give a scheduled job the `messaging` toolset when it must send conditional notifications; keep the external database integration available as well.

## 5. Migration between trackers

Before migrating a watch from a local file/wiki to Notion or another database:
1. inspect the configured integration and confirm its tools are exposed in the current runtime;
2. obtain the destination database or page URL and inspect its schema;
3. define the unique key in the destination before importing;
4. import existing rows once, then update the cron prompt and enabled toolsets;
5. run a test tick and verify the destination contains each entry exactly once;
6. pause or repurpose the old tracker only after the destination is verified.

## Standing criteria
- Targets: Staff/Principal/Lead Cloud Engineering, Cloud Platform, Platform Engineering, SRE and FinOps roles.
- Prefers remote; will consider Sydney hybrid with 2-3 office days weekly.
- Exclude any role with listed compensation below AUD 250,000.
- The recurring cloud/platform/FinOps job watch lives in the Trello "Oz Job Hunt" board, not Notion or Obsidian. Move confirmed-closed jobs to the closed list rather than leaving them among active leads.

Do not assume that an MCP server installed in one desktop/profile context is usable from the current chat or from cron. Verify tool exposure first.
