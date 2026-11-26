#!/usr/bin/env bash
# Cron pre-run for the monthly YNAB wrap. The job fires at 01:00 and 02:00 UTC on the 1st;
# only the run that lands at 12:00 Australia/Sydney (AEDT or AEST) proceeds.
set -euo pipefail
hour=$(TZ=Australia/Sydney date +%H)
if [[ "${FORCE_WRAP:-0}" != "1" && "$hour" != "12" ]]; then
  echo '{"wakeAgent": false}'
  exit 0
fi
cd /opt/data/cache/scratch
exec uv run --quiet --with matplotlib python3 /opt/data/skills/productivity/monthly-financial-wrap/scripts/build_wrap_data.py "$@"
