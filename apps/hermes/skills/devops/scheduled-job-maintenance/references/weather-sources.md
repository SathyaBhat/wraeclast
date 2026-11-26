# Weather data sources for cron briefings

The weather jobs (morning and afternoon, Acacia Gardens) share `$HERMES_HOME/scripts/weather_acacia_gardens.sh`. Use the BOM API; the user explicitly chose it for private, non-shared use. The previous Open-Meteo version is at `weather_acacia_gardens.sh.openmeteo.bak`.

## BOM API (api.weather.bom.gov.au/v1), no key needed

- Location search: `/locations?search=Acacia%20Gardens` returns geohash `r652455` (7 chars).
- Data endpoints require a 6-char geohash. Truncate the code to `r65245`, otherwise you get `WEATHER-400 Invalid Geohash`.
- `/locations/r65245/observations` returns the nearest station automatically (currently Horsley Park, about 14 km away): `temp`, `temp_feels_like`, `humidity`, `wind{direction,speed_kilometre}`, `gust`, `rain_since_9am`, `max_temp`/`min_temp` so far today, and `station{name,distance}`.
- `/locations/r65245/forecasts/daily`: `date` is UTC midnight local (13:00Z), so convert to Australia/Sydney. Fields: `temp_min`, `temp_max`, `rain{chance, amount{lower_range,upper_range}}`, `short_text`, `extended_text`, `icon_descriptor`, `uv`. Day 0 often has `temp_min: null` (and a null max late in the day); its `now` block gives `now_label`/`temp_now` and `later_label` ('Overnight min')/`temp_later`.
- `/forecasts/hourly` is also available.
- Send a browser-like `User-Agent`.

## Fallback: BOM public anonymous feeds (if the API breaks)

- Town forecasts: `ftp://ftp.bom.gov.au/anon/gen/fwo/IDN11060.xml`. Use `<area description="Blacktown">` (the nearest forecast town). `forecast_icon_code` 1-19 maps to Sunny/Clear/Partly cloudy/Cloudy/…/Storms.
- Observations: `https://reg.bom.gov.au/fwo/IDN60901/IDN60901.<wmo>.json`, Richmond 95753 or Badgerys Creek 94752. `local_date_time_full` is in `YYYYmmddHHMMSS` format.
