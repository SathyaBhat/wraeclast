---
name: productivity
description: "Productivity umbrella: databases, documents, presentations, spreadsheets, maps, email-to-meetings — route to the right tool."
version: 1.0.0
author: Hermes Agent (curator)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [productivity, airtable, notion, google-workspace, teams, powerpoint, pdf, maps, documents, spreadsheets, databases, presentations]
    related_skills: [airtable, notion, google-workspace, teams-meeting-pipeline, powerpoint, pdf-tools, maps]
---

# Productivity Umbrella

Seven sibling skills cover the productivity stack — from no-code databases to office documents to geospatial lookups. Load this umbrella to orient; load the specific skill for execution.

## Skill Map

| Skill | Load when… |
|---|---|
| **airtable** | Read, write, filter, or upsert records in an Airtable base via the REST API |
| **notion** | Read, search, create, or edit Notion pages and databases; export to markdown |
| **google-workspace** | Gmail, Google Calendar, Drive, Docs, or Sheets — via `gws` CLI or Python client |
| **teams-meeting-pipeline** | Operate the Teams meeting summary pipeline (transcripts → summaries → delivery) |
| **powerpoint** | Create, read, edit `.pptx` decks — slides, notes, charts, templates |
| **pdf-tools** | Edit, extract, annotate, merge, or convert PDFs via natural-language prompts |
| **maps** | Geocode addresses, find POIs, calculate routes, look up timezones via OpenStreetMap/OSRM |

## Routing Guide

**"I need to manage structured data / a relational database without code"** → **airtable**

**"I need to read/write/search Notion pages or databases"** → **notion**

**"I need to send email / check calendar / read a Google Doc / Sheet"** → **google-workspace**

**"I need to summarise a Teams meeting / process a meeting transcript"** → **teams-meeting-pipeline**

**"I need to create or edit a PowerPoint deck"** → **powerpoint**

**"I need to work with a PDF (edit, extract text, merge, annotate)"** → **pdf-tools**

**"I need a map, route, distance, or timezone for an address"** → **maps**

## Shared Auth Patterns

### Airtable
Requires `AIRTABLE_API_KEY` (personal access token) and `AIRTABLE_BASE_ID`. Store in `${HERMES_HOME:-~/.hermes}/.env`.

### Notion
Requires `NOTION_TOKEN` (integration token). Store in `${HERMES_HOME:-~/.hermes}/.env`. Pages must be shared with the integration.

### Google Workspace
Requires OAuth2 credentials (`credentials.json`) and a `gws` CLI setup, or a Python service account. Run `gws setup` on first use.

### Teams
Requires M365 credentials configured for the meeting pipeline. See `teams-meeting-pipeline` skill for full setup.

## Pitfalls

- **Airtable field types matter** — writing a string to a number field fails silently in some clients; confirm field types before bulk writes
- **Notion shared pages** — the Notion API only returns pages that have been shared with your integration; "page not found" almost always means the sharing step was skipped
- **Google Workspace scopes** — OAuth scopes are granted at setup time; if a new capability (e.g. Calendar write) fails with a 403, re-run `gws setup` to expand scopes
- **PowerPoint compatibility** — python-pptx writes valid `.pptx` but may not render identically in all PowerPoint versions; always preview before sharing
- **PDF edits are destructive** — always keep the original; work on a copy
- **Maps / geocoding accuracy** — OpenStreetMap coverage varies by region; for obscure addresses, try multiple search strategies before concluding the address doesn't geocode
