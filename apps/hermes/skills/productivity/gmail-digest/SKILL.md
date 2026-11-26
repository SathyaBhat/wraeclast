---
name: gmail-digest
description: "Use when fixing the Gmail inbox digest cron or its OAuth."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [gmail, email, cron, digest]
---

# Gmail digest

Google Workspace inbox summarised twice daily to Sathya's Telegram DM.

## Components
- Cron job `769091d129af` "Gmail digest": `0 7,19 * * *` (7am and 7pm), Australia/Sydney, `script=gmail_digest.py`, `enabled_toolsets=[]`, deliver `telegram:7342383`.
- `/opt/data/scripts/gmail_auth.py`: one-time sign-in, user runs it in a terminal. Scope `gmail.readonly` only.
- `/opt/data/scripts/gmail_digest.py`: lists messages since last run (state `/opt/data/secrets/gmail_state.json`, max 48h lookback, first run 14h). Counts promotions, social and List-Unsubscribe bulk mail without listing them; prints the rest as sender/subject/snippet inside UNTRUSTED markers. `--dry` does not advance the state.
- Gig roll-up: emails whose From matches `GIG_SENDERS` (Bandsintown, Whatslively, ticketing sites) AND whose Subject matches `GIG_SUBJECT` bypass the promotions count. The script fetches their body (first 500 chars, links stripped) because snippets lack dates and venues, and prints them under `--- GIG ANNOUNCEMENTS ---`. The prompt renders them as a separate "Gigs" section. Add new gig senders to `GIG_SENDERS`.
- Secrets in `/opt/data/secrets/` (700): `gmail_client.json` (Desktop OAuth client), `gmail_token.json`. All must be owned by hermes with mode 600.

## Pitfalls
- Catalog skill `panthrocorp-google-workspace` fails Hermes security review and pulls an unsigned binary. Do not force it.
- Google's Gmail MCP (gmailmcp.googleapis.com) needs compose/modify scopes, Developer Preview membership and may re-prompt hourly. Rejected for the unattended job; fine for interactive use later.
- `gmail_auth.py` needs `OAUTHLIB_INSECURE_TRANSPORT=1` (already set) because the redirect is http://localhost. Auth codes are single use; rerun for a fresh URL.
- If the user runs auth as root, the token is root-owned and unreadable; ask them to `chown hermes:hermes` it. hermes has no sudo.
- Snippets contain HTML entities and zero-width characters; `clean()` in the script strips them.
- Two Telegram users are allowed (7342383 Sathya, 25822233 other). Confirm which is Sathya before delivering personal mail anywhere.
- The 'Cronjob Response / job_id / To stop or manage this job' header and footer come from the global `cron.wrap_response` config (set false at user's request; affects all jobs).
- Cron tool is reached via `tool_call` name `cronjob_manage`, not directly.
