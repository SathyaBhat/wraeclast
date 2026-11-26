#!/usr/bin/env bash
# Fetch Bureau of Meteorology (BOM) weather for Acacia Gardens, NSW via api.weather.bom.gov.au
# Location geohash r65245 (Acacia Gardens r652455 truncated to the 6 chars the API requires).
# Prepends current Sydney date/time so the agent has the correct local time context.
set -u
SYDNEY_DATETIME=$(TZ="Australia/Sydney" date "+%A, %d %B %Y %I:%M %p %Z")
echo "Current Sydney date/time: $SYDNEY_DATETIME"
echo "Source: Bureau of Meteorology"
echo ""

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
BASE="https://api.weather.bom.gov.au/v1/locations/r65245"
UA="Mozilla/5.0 (hermes-weather-cron)"
for ep in observations forecasts/daily; do
  for i in 1 2 3; do
    curl -sf --max-time 30 -A "$UA" "$BASE/$ep" -o "$TMP/${ep//\//_}.json" && break
    sleep 5
  done
done

python3 - "$TMP" <<'PY'
import json, sys, os
from datetime import datetime
from zoneinfo import ZoneInfo
tmp, tz = sys.argv[1], ZoneInfo("Australia/Sydney")
def load(n): return json.load(open(os.path.join(tmp, n)))["data"]
def local(ts): return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(tz)

print("== CURRENT CONDITIONS (BOM observation) ==")
try:
    o = load("observations.json")
    st = o["station"]
    print(f"Station: {st['name']} ({st['distance']/1000:.0f} km away)")
    print(f"Temperature: {o['temp']} C | Feels like: {o['temp_feels_like']} C | Humidity: {o['humidity']}%")
    print(f"Wind: {o['wind']['direction']} {o['wind']['speed_kilometre']} km/h (gusts {o['gust']['speed_kilometre']} km/h)")
    print(f"Rain since 9am: {o['rain_since_9am']} mm")
    if o.get("max_temp"): print(f"Highest so far today: {o['max_temp']['value']} C")
    if o.get("min_temp"): print(f"Lowest so far today: {o['min_temp']['value']} C")
except Exception as e:
    print(f"ERROR: observations unavailable ({e})")

print("\n== DAILY FORECAST (BOM, Acacia Gardens) ==")
try:
    days = load("forecasts_daily.json")
    for i, d in enumerate(days[:4]):
        date = local(d["date"]).strftime("%A %d %B")
        tmax, tmin = d.get("temp_max"), d.get("temp_min")
        if i == 0 and d.get("now"):   # today: BOM's "now" block carries today's max / overnight min
            n = d["now"]
            if n.get("now_label") == "Max" and tmax is None: tmax = n.get("temp_now")
            if "min" in (n.get("later_label") or "").lower(): print(f"(Tonight's overnight min: {n.get('temp_later')} C)")
        r = d["rain"]; a = r["amount"]
        rng = f"{a['lower_range']} to {a['upper_range']} mm" if a.get("upper_range") else "0 mm"
        parts = [date, f"Max {tmax} C" if tmax is not None else "Max n/a",
                 f"Min {tmin} C" if tmin is not None else "Min n/a",
                 f"Chance of rain {r['chance']}%", f"Rain {rng}",
                 f"Icon: {d['icon_descriptor']}", f"Summary: {d['short_text']}"]
        if d.get("uv", {}).get("max_index"): parts.append(f"UV {d['uv']['max_index']} ({d['uv']['category']})")
        print(" | ".join(parts))
        if d.get("extended_text"): print(f"  Detail: {d['extended_text']}")
    print("(First line is today.)")
except Exception as e:
    print(f"ERROR: forecast unavailable ({e})")
PY
