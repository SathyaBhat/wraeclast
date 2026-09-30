#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Draw a Home Assistant battery graph and weather forecast, and send it to emini Home's Picture.

    HA_TOKEN=... EMINI_HOST=192.168.0.49 python3 ha_poster.py            # every hour, forever
    HA_TOKEN=... python3 ha_poster.py --once --out poster.png           # draw only, to look at
    HA_TOKEN=... python3 ha_poster.py --list                            # battery-like sensors

Settings come from the environment, so the same image runs anywhere:

    HA_URL          default http://homeassistant.bishop-bass.ts.net
    HA_TOKEN        a long-lived access token (HA: Profile -> Security), required
    BATTERY_ENTITY  default sensor.battery_state_of_charge; see --list
    WEATHER_ENTITY  default weather.forecast_home
    EMINI_HOST      the device's address or name.local, required unless --out; in a container
                    use the address, as .local names are mDNS only
    HOURS           hours of battery history on the graph, default 24
    SHOW            1 (default) puts Picture on the display each hour, 0 only updates it

Times are shown in Home Assistant's own time zone. The device must be in Open mode: in Breath its
Wi-Fi is off between fetches and an hour's push is simply missed (and logged).
"""

import argparse
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

# home_cli.py from emini-home's tools/, next to this file or one directory up.
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import home_cli  # noqa: E402

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

W, H = home_cli.WIDTH, home_cli.HEIGHT
BLACK, WHITE, YELLOW, RED = 0, 1, 2, 3
LOW = 20  # percent: below this the battery is drawn red
HEARTBEAT = Path(os.environ.get("HEARTBEAT", "/tmp/emini-poster-ok"))
CONDITIONS = {
    "clear-night": "Clear",
    "cloudy": "Cloudy",
    "exceptional": "Unusual",
    "fog": "Fog",
    "hail": "Hail",
    "lightning": "Storm",
    "lightning-rainy": "Storm",
    "partlycloudy": "Partly cloudy",
    "pouring": "Pouring",
    "rainy": "Rain",
    "snowy": "Snow",
    "snowy-rainy": "Sleet",
    "sunny": "Sunny",
    "windy": "Windy",
    "windy-variant": "Windy",
}
FONTS = {
    False: ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/Library/Fonts/Arial.ttf"],
    True: [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ],
}


def log(message):
    print("%s %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message), flush=True)


class HomeAssistant:
    def __init__(self, url, token):
        self.url, self.token = url.rstrip("/"), token

    def call(self, method, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            self.url + path,
            data,
            {"Authorization": "Bearer " + self.token, "Content-Type": "application/json"},
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read() or b"null")
        except urllib.error.HTTPError as e:
            raise RuntimeError("HA %s %s: %d %s" % (method, path, e.code, e.reason)) from None
        except OSError as e:
            raise RuntimeError("HA %s: %s" % (self.url, e)) from None

    def zone(self):
        return ZoneInfo(self.call("GET", "/api/config")["time_zone"])

    def state(self, entity):
        return self.call("GET", "/api/states/" + entity)

    def history(self, entity, hours):
        start = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        rows = self.call(
            "GET",
            "/api/history/period/%s?filter_entity_id=%s&minimal_response&no_attributes"
            % (urllib.request.quote(start), entity),
        )
        points = []
        for row in rows[0] if rows else []:
            try:
                value = float(row["state"])
            except (KeyError, ValueError):
                continue  # unavailable, unknown
            points.append((datetime.fromisoformat(row["last_changed"]), value))
        return points

    def forecast(self, entity):
        for kind in ("hourly", "daily"):
            try:
                reply = self.call(
                    "POST",
                    "/api/services/weather/get_forecasts?return_response",
                    {"entity_id": entity, "type": kind},
                )
            except RuntimeError:
                continue  # this entity has no forecast of that kind
            items = reply.get("service_response", {}).get(entity, {}).get("forecast", [])
            if items:
                return kind, items
        return None, []


def font(size, bold=False):
    for path in [os.environ.get("FONT_BOLD" if bold else "FONT")] + FONTS[bold]:
        if path and Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def draw_poster(battery, points, weather, kind, forecast, zone, now):
    image = Image.new("P", (W, H), WHITE)
    image.putpalette([v for rgb in home_cli.PALETTE for v in rgb])
    d = ImageDraw.Draw(image)
    d.fontmode = "1"  # no anti-aliasing: grey edges have no colour to become on the paper
    small, label, big = font(13), font(15, True), font(46, True)

    # Header: the battery's name and the time of this picture.
    name = battery["attributes"].get("friendly_name", "Battery")
    d.text((8, 5), name[:34], font=label, fill=BLACK)
    d.text((W - 8, 5), now.strftime("%H:%M"), font=label, fill=BLACK, anchor="ra")
    d.line([(0, 26), (W, 26)], fill=BLACK, width=2)

    # The battery now, and which way it is going over the last hour.
    try:
        level = float(battery["state"])
    except ValueError:
        level = None
    d.text(
        (8, 34),
        "%d%%" % round(level) if level is not None else "--",
        font=big,
        fill=RED if level is not None and level < LOW else BLACK,
    )
    hour_ago = [v for t, v in points if t <= now - timedelta(hours=1)]
    if level is not None and hour_ago:
        change = level - hour_ago[-1]
        trend = "charging" if change > 0.5 else "discharging" if change < -0.5 else "steady"
        d.text((10, 88), trend, font=small, fill=BLACK)
        d.text((10, 106), "%+.0f%% last hour" % change, font=small, fill=BLACK)

    # The graph: level over the last hours, filled yellow (red below LOW), 0/50/100 lines.
    x0, x1, y0, y1 = 130, W - 8, 36, 168
    start = now - timedelta(hours=int(os.environ.get("HOURS", "24")))

    def xy(t, v):
        f = (t - start).total_seconds() / (now - start).total_seconds()
        return x0 + f * (x1 - x0), y1 - max(0.0, min(100.0, v)) / 100 * (y1 - y0)

    series = [(max(t, start), v) for t, v in points]
    if series:
        series.append((now, series[-1][1]))  # the state holds until now
        # History is a step function: a value lasts until the next change.
        steps = []
        for (t, v), (t2, _) in zip(series, series[1:]):
            steps += [xy(t, v), xy(t2, v)]
        for (ax, ay), (bx, by) in zip(steps, steps[1:]):
            colour = RED if (y1 - ay) / (y1 - y0) * 100 < LOW else YELLOW
            if bx > ax:
                d.rectangle([ax, ay, bx, y1], fill=colour)
        d.line(steps, fill=BLACK, width=2)
    for pct in (0, 50, 100):
        y = y1 - pct / 100 * (y1 - y0)
        for x in range(x0, x1, 6):
            d.point((x, y), fill=BLACK)
        d.text((x0 - 4, y), str(pct), font=small, fill=BLACK, anchor="rm")
    tick = start.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    while tick < now:
        if tick.hour % 6 == 0:
            x = xy(tick, 0)[0]
            d.line([(x, y1), (x, y1 + 4)], fill=BLACK)
            d.text((x, y1 + 6), tick.strftime("%H:%M"), font=small, fill=BLACK, anchor="ma")
        tick += timedelta(hours=1)
    d.line([(0, 190), (W, 190)], fill=BLACK, width=2)

    # Weather: now in the strip, then the next six hours (or days) in columns.
    if weather:
        a = weather["attributes"]
        unit = a.get("temperature_unit", "°C").lstrip("°")
        now_text = "Now %s°%s  %s" % (
            round(a["temperature"]) if a.get("temperature") is not None else "--",
            unit,
            CONDITIONS.get(weather["state"], weather["state"]),
        )
        d.text((8, 196), now_text, font=label, fill=BLACK)
    columns = [f for f in forecast if datetime.fromisoformat(f["datetime"]) > now][:6]
    width = (W - 16) / 6
    for i, f in enumerate(columns):
        cx = 8 + width * (i + 0.5)
        when = datetime.fromisoformat(f["datetime"]).astimezone(zone)
        d.text(
            (cx, 222),
            when.strftime("%H:%M" if kind == "hourly" else "%a"),
            font=small,
            fill=BLACK,
            anchor="ma",
        )
        temp = f.get("temperature")
        d.text(
            (cx, 239),
            "%d°" % round(temp) if temp is not None else "--",
            font=font(22, True),
            fill=BLACK,
            anchor="ma",
        )
        words = CONDITIONS.get(f.get("condition"), f.get("condition") or "").split()
        d.text((cx, 266), words[0] if words else "", font=small, fill=BLACK, anchor="ma")
        rain = f.get("precipitation_probability")
        if rain:
            d.text((cx, 282), "%d%%" % rain, font=small, fill=RED if rain >= 50 else BLACK,
                   anchor="ma")
    return image


def make(ha, battery_entity, weather_entity):
    zone = ha.zone()
    now = datetime.now(zone)
    battery = ha.state(battery_entity)
    points = [(t.astimezone(zone), v)
              for t, v in ha.history(battery_entity, int(os.environ.get("HOURS", "24")))]
    try:
        weather = ha.state(weather_entity)
        kind, forecast = ha.forecast(weather_entity)
    except RuntimeError as e:
        log("weather skipped: %s" % e)
        weather, kind, forecast = None, None, []
    return draw_poster(battery, points, weather, kind, forecast, zone, now)


def resolve(host):
    """The device's address for this push. A .local name is answered by the device itself over
    mDNS, and with its Wi-Fi in power save it misses a query now and then, so ask a few times."""
    name = host.split(":")[0]
    for attempt in range(5):
        try:
            return socket.gethostbyname(name) + host[len(name) :]
        except OSError as e:
            if attempt == 4:
                raise RuntimeError("cannot resolve %s: %s" % (name, e)) from None
            time.sleep(3)


def push(host, image, show):
    host = resolve(host)
    frame = home_cli.pack(image.tobytes())
    home_cli.request(host, "POST", "/api/picture", frame)
    if not show:
        return host
    status = home_cli.request(host, "GET", "/api/status")
    if status.get("displayed_screen") == "picture":
        return host  # the upload has already redrawn it
    config = home_cli.request(host, "GET", "/api/config")
    if not config["enabled"][home_cli.SCREENS.index("picture")]:
        home_cli.update_config(host, None, lambda c: home_cli.enable(c, "picture"))
    home_cli.request(host, "POST", "/api/show", {"screen": "picture"})
    return host


def list_batteries(ha):
    for s in ha.call("GET", "/api/states"):
        a = s.get("attributes", {})
        if s["entity_id"].startswith("sensor.") and a.get("unit_of_measurement") == "%" and (
            a.get("device_class") == "battery" or "battery" in s["entity_id"]
        ):
            print("%-60s %6s%%  %s" % (s["entity_id"], s["state"], a.get("friendly_name", "")))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--once", action="store_true", help="one picture, then exit")
    parser.add_argument("--out", help="save the picture (.png) instead of sending it")
    parser.add_argument("--list", action="store_true", help="list battery-like sensors")
    a = parser.parse_args()
    token = os.environ.get("HA_TOKEN")
    if not token:
        sys.exit("error: set HA_TOKEN to a Home Assistant long-lived access token")
    ha = HomeAssistant(os.environ.get("HA_URL", "http://homeassistant.bishop-bass.ts.net"), token)
    if a.list:
        return list_batteries(ha)
    battery = os.environ.get("BATTERY_ENTITY", "sensor.battery_state_of_charge")
    weather = os.environ.get("WEATHER_ENTITY", "weather.forecast_home")
    host = os.environ.get("EMINI_HOST")
    show = os.environ.get("SHOW", "1") != "0"
    if not a.out and not host:
        sys.exit("error: set EMINI_HOST to the device's address")
    while True:
        try:
            image = make(ha, battery, weather)
            if a.out:
                image.convert("RGB").save(a.out)
                log("saved %s" % a.out)
            else:
                log("sent to %s (%s)" % (host, push(host, image, show)))
                HEARTBEAT.touch()  # the container's healthcheck reads its age
        except (RuntimeError, home_cli.HomeError, KeyError, ValueError) as e:
            if a.once:
                sys.exit("error: %s" % e)
            log("skipped this hour: %s" % e)  # HA restarting, device asleep: try next hour
        if a.once or a.out:
            return
        # A few seconds past the next full hour, so the graph ends on a round time.
        time.sleep(3600 - time.time() % 3600 + 5)


if __name__ == "__main__":
    main()
