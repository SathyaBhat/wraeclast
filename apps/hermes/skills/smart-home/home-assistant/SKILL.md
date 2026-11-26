---
name: home-assistant
description: Use when configuring or debugging HA. Use the API.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [home-assistant, smart-home, lovelace, tuya]
    related_skills: [openhue]
---

# Home Assistant (Sathya's instance)

## When to Use
Use this for Home Assistant dashboard edits, broken or `unavailable` entities, integration reloads, entity-registry changes, or device diagnostics. To just turn a device on or off or read its live state, use the HA MCP tools.

Instance: `http://homeassistant.bishop-bass.ts.net` (Tailscale). Auth: `$HOME_ASSISTANT_API_TOKEN` (never print or persist it). The HA MCP tools cover live state and device control only; anything to do with configuration (dashboards, entity registry, integrations, diagnostics) goes through the REST/WebSocket API.

## Tools
- `scripts/ha_ws.py`: copy it to the scratch dir and run `python3 ha_ws.py '<json list of WS messages>'`. It authenticates, sends each message with an auto id, and prints a JSON list of responses. Needs the `websockets` package (already installed in this Python).
- REST: `curl -s -H "Authorization: Bearer $HOME_ASSISTANT_API_TOKEN" $B/api/...`.
- Save big dumps (get_states, registries, lovelace configs) to scratch files and filter them with Python. Don't print them.

Useful WS calls: `lovelace/dashboards/list`, `lovelace/config` (+`url_path`; the default dashboard returns `config_not_found` when it is auto-generated, so the user's "main dashboard" is usually a custom one such as `home-overview`), `lovelace/config/save`, `get_states`, `config/entity_registry/list`, `config/entity_registry/update`, `config/device_registry/list`, `config_entries/get` (+`domain`).
Useful REST calls: `/api/states/<entity>`, `POST /api/config/config_entries/entry/<entry_id>/reload`, `/api/diagnostics/config_entry/<entry_id>/device/<device_id>`.

## Dashboard "Entity not found" procedure
1. List the dashboards, fetch the config of the one the user means, and regex out every `domain.object_id` string. Diff that set against `get_states`. Ignore service names such as `light.turn_on`.
2. Look up each missing id in the entity registry. When `disabled_by` is set (`user`/`integration`), the entity exists but is disabled, so it has no state. When the id is absent, it was renamed or deleted: find the replacement by device or friendly name.
3. Report every place the entity is used (tiles, plus `target.entity_id` lists in button actions). Then ask whether to re-enable it or remove it from the dashboard. A user-disabled entity may have been disabled on purpose, for example a retired bulb.
4. Re-enable with `config/entity_registry/update` and `disabled_by: null`. HA reloads the integration after the returned `reload_delay` (about 30s), so wait for that before checking the state.
5. Treat `unavailable` after re-enabling as a different problem. Go to the device-offline triage below.

## Device `unavailable` triage
1. Compare it with a sibling device on the same integration. If the sibling works, the integration is fine and the device is at fault. Check that the config entry is `loaded`, then reload the entry once.
2. Pull the device diagnostics. For cloud integrations such as Tuya, check `online` and `update_time`/`active_time`. `online: False` with an old `update_time` means the vendor cloud has lost the device. HA cannot fix that. The device needs re-pairing in the vendor app (Smart Life/Tuya on the household@sathyasays.com account, 2.4 GHz Wi-Fi).
3. A bulb that lights up after a power cycle is not proof that it is online. Many bulbs default to on when powered.
4. If re-pairing stalls at "connecting to router" while a sibling Tuya device on the same Wi-Fi stays online and the network hasn't changed, the network is proven compatible. Try AP/compatibility-mode pairing next to the router once, then call it a failed bulb (Wi-Fi module) rather than iterating on router settings.

## Removing a dead device
- Strip it from dashboards first: drop tiles whose `entity` matches and remove the id from every `target.entity_id` list. Back up first, save, then confirm zero references remain.
- Tuya: once the user removes the device in the Smart Life app, HA drops the device and entity by itself on the next sync, and `config/device_registry/remove_config_entry` then returns `Unknown device`. Check the registries before treating that as an error.

## Household setup
- FoxESS KH10 (serial 60KB10305BMA125) cloud integration is set up. Entity IDs: SOC `sensor.60kb10305bma125_soc`; grid consumption `..._daily_grid_consumption`; feed-in `..._daily_feedin`; solar generation `..._daily_generation`; battery charged `..._daily_charged_energy_total`; battery discharged `..._daily_discharged_energy_total` (all prefixed `sensor.60kb10305bma125`).
- The Home Assistant MCP server is connected. It gives live context and device control, but not dashboard, Energy, HACS or integration configuration. Use the REST/WebSocket API with HOME_ASSISTANT_API_TOKEN for those.
- Planned e-paper project: the homeserver is headless Arch Linux with no hypervisor. Intended path is Home Assistant OS in a KVM/libvirt VM. Network changes need out-of-band recovery access.

## User preferences
- Dashboard layout: clean responsive Sections; Solar & Battery centred; show room temperatures but not humidity; all lights as quick controls; use FoxESS Meter 2 Power for live solar generation and include grid import in live/chart power flow.
- Dashboards: see the user profile (Sections layout, solar centred, finance bar charts). Keep these when editing dashboards.
- Back up a dashboard config to scratch before any `lovelace/config/save`.
