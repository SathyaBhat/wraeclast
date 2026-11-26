#!/usr/bin/env python3
"""Rebuild the live YNAB spending-bar view from current category entities."""
import base64
import json
import os
import socket
import struct
import urllib.request

BASE_URL = "http://homeassistant.bishop-bass.ts.net"
HOST = "homeassistant.bishop-bass.ts.net"
DASHBOARD = "finance-overview"
VIEW_PATH = "spending-bars"
TARGET_GROUPS = {
    "food bills": "Food Bills",
    "variable expenses": "Variable Expenses",
    "just for fun": "Just For Fun",
}
# Use an MDI icon matching the category-name emoji; unknown/new emoji get a tag.
EMOJI_ICONS = {
    "🍌": "mdi:fruit-banana",
    "🥡": "mdi:food-takeout-box",
    "🍞": "mdi:bread-slice",
    "👩‍💼": "mdi:office-building",
    "👓": "mdi:glasses",
    "🛠": "mdi:hammer-screwdriver",
    "👕": "mdi:tshirt-crew",
    "🧴": "mdi:bottle-tonic-plus",
    "💸": "mdi:cash-fast",
    "🕐": "mdi:clock-outline",
    "😖": "mdi:emoticon-sad-outline",
    "🤷‍♀️": "mdi:emoticon-confused-outline",
    "🤷‍♂️": "mdi:emoticon-confused-outline",
    "🌅": "mdi:weather-sunset",
    "🧘": "mdi:yoga",
    "🛍️": "mdi:shopping",
}


def receive(sock, buffered):
    def take(count):
        nonlocal buffered
        while len(buffered) < count:
            chunk = sock.recv(4096)
            if not chunk:
                raise RuntimeError("WebSocket closed unexpectedly")
            buffered += chunk
        value, buffered = buffered[:count], buffered[count:]
        return value

    header = take(2)
    length = header[1] & 127
    if length == 126:
        length = struct.unpack("!H", take(2))[0]
    elif length == 127:
        length = struct.unpack("!Q", take(8))[0]
    return json.loads(take(length)), buffered


def send(sock, payload):
    data = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
    mask = os.urandom(4)
    length = len(data)
    if length < 126:
        header = bytes([129, 128 | length])
    elif length < 65536:
        header = bytes([129, 128 | 126]) + struct.pack("!H", length)
    else:
        header = bytes([129, 128 | 127]) + struct.pack("!Q", length)
    sock.sendall(header + mask + bytes(value ^ mask[i % 4] for i, value in enumerate(data)))


def category_name(attributes):
    return attributes["friendly_name"].replace("YNAB Australia - Categories ", "").replace(" YNAB Australia", "").strip()


def icon_for(name):
    return next((icon for emoji, icon in EMOJI_ICONS.items() if emoji in name), "mdi:tag")


def main():
    token = os.environ.get("HOME_ASSISTANT_API_TOKEN")
    if not token:
        raise RuntimeError("HOME_ASSISTANT_API_TOKEN is not set")

    request = urllib.request.Request(f"{BASE_URL}/api/states", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(request, timeout=30) as response:
        states = json.load(response)

    groups = {label: [] for label in TARGET_GROUPS.values()}
    for state in states:
        attributes = state.get("attributes", {})
        group = str(attributes.get("category_group", "")).casefold()
        if not state["entity_id"].startswith("sensor.ynab_australia_categories_") or group not in TARGET_GROUPS:
            continue
        try:
            budgeted = float(attributes.get("budgeted") or 0)
            activity = float(attributes.get("activity") or 0)
        except (TypeError, ValueError):
            continue
        if budgeted <= 0:
            continue
        name = category_name(attributes)
        groups[TARGET_GROUPS[group]].append({
            "entity": state["entity_id"],
            "name": f"{name} — used A${max(0, -activity):.2f} of A${budgeted:.2f}",
            "icon": icon_for(name),
            "max": round(budgeted, 2),
        })

    for entries in groups.values():
        entries.sort(key=lambda entry: entry["name"].casefold())

    sock = socket.create_connection((HOST, 80), timeout=30)
    key = base64.b64encode(os.urandom(16)).decode()
    sock.sendall(
        f"GET /api/websocket HTTP/1.1\r\nHost: {HOST}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode()
    )
    buffered = b""
    while b"\r\n\r\n" not in buffered:
        buffered += sock.recv(4096)
    response_headers, buffered = buffered.split(b"\r\n\r\n", 1)
    if b"101 Switching Protocols" not in response_headers:
        raise RuntimeError("Home Assistant did not accept the WebSocket connection")

    result, buffered = receive(sock, buffered)
    if result.get("type") != "auth_required":
        raise RuntimeError(f"Unexpected auth response: {result}")
    send(sock, {"type": "auth", "access_token": token})
    result, buffered = receive(sock, buffered)
    if result.get("type") != "auth_ok":
        raise RuntimeError(f"Home Assistant authentication failed: {result}")

    send(sock, {"id": 1, "type": "lovelace/config", "url_path": DASHBOARD})
    result, buffered = receive(sock, buffered)
    if not result.get("success"):
        raise RuntimeError(f"Could not load Finance dashboard: {result}")
    config = result["result"]
    config["views"] = [view for view in config["views"] if view.get("path") != VIEW_PATH]

    sections = []
    for group, entities in groups.items():
        if not entities:
            continue
        sections.append({
            "type": "grid",
            "cards": [
                {"type": "heading", "heading": group},
                {
                    "type": "custom:bar-card",
                    "title": f"{group} — used this month",
                    "entities": entities,
                    "min": 0,
                    "max": 100,
                    "direction": "right-reverse",
                    "height": "32px",
                    "stack": "vertical",
                    "limit_value": True,
                },
            ],
        })
    config["views"].append({
        "title": "Spending bars",
        "path": VIEW_PATH,
        "icon": "mdi:chart-bar",
        "type": "sections",
        "max_columns": 1,
        "sections": sections,
    })

    send(sock, {"id": 2, "type": "lovelace/config/save", "url_path": DASHBOARD, "config": config})
    result, buffered = receive(sock, buffered)
    if not result.get("success"):
        raise RuntimeError(f"Could not save Finance dashboard: {result}")

    send(sock, {"id": 3, "type": "lovelace/config", "url_path": DASHBOARD})
    result, buffered = receive(sock, buffered)
    saved_view = next(view for view in result["result"]["views"] if view.get("path") == VIEW_PATH)
    cards = [card for section in saved_view["sections"] for card in section["cards"] if card.get("type") == "custom:bar-card"]
    saved_entities = sum(len(card["entities"]) for card in cards)
    saved_icons = sum(bool(entity.get("icon")) for card in cards for entity in card["entities"])
    if len(cards) != len(sections) or saved_entities != sum(len(entries) for entries in groups.values()) or saved_icons != saved_entities:
        raise RuntimeError("Saved spending-bar view did not match the generated category set or icons")
    print(json.dumps({"saved": True, "groups": list(groups), "categories": saved_entities, "icons": saved_icons}, ensure_ascii=False))


if __name__ == "__main__":
    main()
