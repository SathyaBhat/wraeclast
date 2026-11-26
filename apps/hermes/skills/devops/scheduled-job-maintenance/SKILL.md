---
name: scheduled-job-maintenance
description: "Use for creating or repairing Hermes cron jobs. Verify runs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, cron, scheduled-jobs, troubleshooting, provider-routing]
    related_skills: [hermes-agent]
---

# Scheduled Job Maintenance

## Create a recurring report job

1. `cronjob_manage(action='list')` first; update an existing job rather than creating a near-duplicate.
2. Resolve the delivery target to an explicit ID: Discord channel IDs are in `$HERMES_HOME/channel_directory.json` (#ynab-finance = `699249623281303604`). Use `deliver: discord:<channel_id>`; a bare `discord` goes to the home channel (#hermes-alerts), not the channel the user named.
3. Set `timezone: Australia/Sydney` for day/time schedules, `wrap_response: off` for clean reports, and `enabled_toolsets: ["web"]` for research jobs.
4. Write a self-contained prompt with source URLs, the baseline facts the user gave, a fixed output shape, "cite only retrieved figures; write n/a when missing", and "Always post; never reply [SILENT]". The cron wrapper lets the model answer [SILENT] when it thinks nothing is new, and with `continuity: true` a rerun that finds the same figures as the previous output gets suppressed.
5. Keep the channel post short by default. The user rejected an ~800-word report as too long and wordy. The format that was accepted is ≤120 words in a fixed labelled-line shape (headline, last month, past year, why, changes, bottom line, one link), with no tables, arithmetic or caveat paragraphs. When the user also wants the detail, it goes in a threaded reply under the summary message, not in a second flat post or a standalone thread (see `references/report-jobs.md`).
6. Ask before a test run (it posts to a real channel), then verify it: read the newest `cron/output/<job_id>/*.md` response and check `executions.db` `delivery_outcome` is `delivered`, not `suppressed`. Show the user the posted text.

Short-summary plus threaded-reply pattern (posting tool plugin, `deliver: local`, `failure_deliver`), and Discord threading pitfalls: `references/report-jobs.md`.

## Diagnose before changing a job

1. Identify the exact job with `hermes cron list` and read its complete record from `$HERMES_HOME/cron/jobs.json`; CLI listings can omit routing snapshots and error detail.
2. Record the job's explicit `provider`, `model`, and `base_url`, then its `provider_snapshot`, `model_snapshot`, last status/error, and next run. An unset explicit provider is not proof that the job follows the live default: a snapshot can act as an effective pin.
3. Read the error log around the failing run and compare the job's effective routing with the current `model` configuration. State the distinction clearly: a job-level override, a stale creation snapshot, and missing runtime credentials are different faults.
4. Test the intended provider/model with a minimal one-shot `hermes chat --provider … --model … --quiet --query …` before mutating the job. Do not claim a routing repair works solely because its config write succeeded.

## Explain the latest run before attempting repairs

1. List jobs to identify the exact watch, then read the newest saved response under `$HERMES_HOME/cron/output/<job_id>/`. Read the preceding output too when the latest run appears to be a retry; distinguish the initial failure from the later outcome.
2. Inspect `$HERMES_HOME/cron/executions.db` read-only for that job, ordered by `claimed_at DESC`. Use execution start/finish, error, and `delivery_outcome` to distinguish execution from notification delivery; the job record alone can hide a failed attempt behind a later completed retry.
3. If the final response is a loop-stop message or omits the change summary, inspect the matching cron session in `$HERMES_HOME/state.db`. Find it by job ID and run timestamp, then inspect tool results in message order. Do not assume a stopped search made no tracker changes: writes can precede the guardrail. Deduplicate stored tool calls by their call ID before counting executions or repeated queries; context-history persistence can store the same call ID more than once, which is not evidence of another execution. Compare the failing run's model/provider and task prompt with preceding runs, and inspect auxiliary routing and compression failures before attributing a new loop solely to the prompt.
4. Reconstruct changes from write results and subsequent readbacks of each exact target. Distinguish verified additions/moves from successful write acknowledgements without a post-write readback. Read live targets if historical readbacks are absent and a definitive current-state claim is needed.
5. Report the outcome first, then concrete tracker changes, the unresolved blocker, and the next scheduled time in the user's timezone. Separate scheduler status from task completion and delivery. Do not modify or rerun a job merely because the user asked what happened.

For reusable read-only SQL recipes, see `references/run-forensics.md`.

## Audit tool access for work jobs

1. For a job that is expected to search, verify, or update an external tracker, inspect the saved output for actual tool calls or concrete tool-derived evidence. A scheduler `ok` result with a plausible no-change response is not proof that the work ran.
2. Inspect `enabled_toolsets`. When it is unset, cron inherits the `platform_toolsets.cron` allowlist, which can omit the required tools. For job watches that need live discovery plus an MCP-backed tracker, set `enabled_toolsets: ["web"]`; cron then layers enabled MCP servers onto that allowlist.
3. Preflight the externally hosted search endpoint separately before a retry. Then trigger the normal job unchanged where possible; use transient run context only to require a degraded report instead of an unearned no-change result.

## Repair provider snapshot drift

- Resnapshot an unpinned job only when the current global resolution is valid and distinct from the stale snapshot. Verify the stored snapshot afterward; runtime aliases such as `custom` can make resnapshot ineffective.
- When a stale provider snapshot resolves to an alias without the endpoint credentials required by a cron worker, pin the affected job explicitly with `hermes cron edit JOB_ID --provider PROVIDER --model MODEL`. Use the provider/model proven by the one-shot test.
- Verify the post-write record directly: explicit provider and model must be present, provider/model snapshots should be cleared, and the job must remain enabled and scheduled.

## Change a script-backed job's data source

1. List jobs and find every job sharing the same `script`; one script edit changes all of them, so update each job's prompt together.
2. Read the script under `$HERMES_HOME/scripts/` and each full prompt in `cron/jobs.json`. Back up the script (`<name>.<oldsource>.bak`) before rewriting it.
3. Use the source the user named. If you have a licensing or ToS concern, mention it in one line and ask; do not quietly swap to a different feed, because the user may already have accepted the terms for private use and will just tell you to redo it.
4. Have the script pre-format the data into labelled plain text (with `ERROR: … unavailable` markers on failure, and retries) instead of piping raw JSON, so the pinned small model only formats and never parses codes or guesses.
5. Rewrite only the source-specific prompt paragraph (e.g. code tables). Keep the delivery format block byte-identical, and add rules for missing values and ERROR sections.
6. Run the script directly to verify it with live data. Ask before calling `cronjob_manage run` when the job delivers to a shared chat, because a test run posts a real message.

Source recipes: `references/weather-sources.md` (BOM API for Acacia Gardens).

For creating or repairing an inbox-summary job (Gmail/Workspace), including the user's output spec, access-option decisions, OAuth pitfalls and delivery-target checks: `references/inbox-digest-jobs.md`.

## Verify completion

1. Trigger one normal verification run with `cronjob_manage(action='run', job_id=...)`; do not alter the job's task prompt or bypass its write/deduplication logic.
2. Wait for the asynchronous result rather than assuming dispatch means success.
3. Read the job record after completion. Require `last_status: ok`, an empty `last_error`, and a reset failure streak, but also inspect the final response and tool evidence before declaring task success: a returned loop-stop response can still be recorded as `ok`. Include the next scheduled time.
4. If the job makes external writes, verify each exact target and distinguish completed changes from degraded coverage or unfinished work. Treat an autonomous run asking for `continue` as incomplete, not as a healthy completion or proof of no changes.

## Pitfalls

- Inspect the full stored record before resnapshotting — the job's visible provider fields can be null while a hidden creation snapshot still overrides global routing.
- Pin both provider and model together after a snapshot-routing failure — swapping only the provider can pair it with an unintended paid or incompatible model.
- Treat a successful configuration edit as unverified until a real cron session completes, because cron has its own fresh-session provider resolution path.
