#!/usr/bin/env bash
set -euo pipefail

# Soft-archive weather cron sessions older than one day.  Keep stdout empty
# when there is nothing to archive so this local-only cron stays quiet.
/opt/hermes/bin/hermes sessions archive --title "Weather" --older-than 1d --yes
