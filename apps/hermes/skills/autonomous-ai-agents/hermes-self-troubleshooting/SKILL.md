---
name: hermes-self-troubleshooting
description: "Use when a Hermes feature breaks here. Diagnose, keep Kiro."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, troubleshooting, auxiliary, vision, browser, kiro, plugins]
    related_skills: [hermes-agent, hermes-docker-updates]
---

# Troubleshooting Hermes on Sathya's install

## When to Use

A Hermes feature on this install is broken or missing (session titles, `vision_analyze`, browser tools, compression/other `auxiliary.*` tasks, a tool hidden by a failing `check_fn`), or the user wants a small Hermes behaviour added (e.g. showing Kiro credits in replies).

## Environment

Hermes runs in a Docker container (Wraeclast). Code is at `/opt/hermes` (read-only, no git), venv at `/opt/hermes/.venv/bin/python`, config/state at `/opt/data` (`HERMES_HOME`). The `hermes` CLI is not on PATH; drive internals through the venv python. Plugins in `/opt/data/plugins/` are writable (main model provider: `plugins/kiro-provider`).

## Standing user preferences

- **All model traffic goes through Kiro** (main model and every `auxiliary.*` task). Never fix an aux failure by pointing it at Bedrock, Bedrock Mantle, OpenRouter, or any other provider, even if that works. If Kiro can't serve a task, fix the Kiro path or report the blocker.
- **Check upstream before patching locally.** When the root cause is in Hermes core or a plugin, first search upstream issues/PRs and check whether a fix already shipped in a newer release; offer the upgrade before writing a local patch.
- Back up `config.yaml`, `.env`, `cron/jobs.json`, and any plugin dir you touch (timestamped under `/opt/data/backups/`) before editing. Ask before removing providers or credentials.
- **Local fixes go upstream too.** Any plugin or behaviour patch is paired with an upstream-ready diff in `/opt/data/patches/<plugin>-<topic>.patch` (made with `diff -u` against the backup, `a/provider/...` labels) and an offer to draft the issue/PR. When open upstream PRs already cover the area, propose building on the most active one rather than opening a competing PR. Never submit without the user's review.

## Procedure

1. **Find the gate that hid or broke the feature.** `grep -i '<feature>' /opt/data/logs/agent.log | tail` — look for `check_fn <name> returned False` (tool hidden) and `WARNING agent.<module>:` lines (call-time failure, e.g. `agent.title_generator: Title generation failed: ...`).
2. **Reproduce the check in the venv** with a small script in `$TMPDIR` (`cd /opt/hermes && .venv/bin/python script.py`), calling `hermes_cli.env_loader.load_hermes_dotenv()` first so `.env` keys are present. Useful probes:
   - Vision: `tools.vision_tools._should_use_native_vision_fast_path()`, `check_video_requirements()`, `agent.image_routing.decide_image_input_mode(provider, model, cfg)`, `agent.auxiliary_client.resolve_vision_provider_client()` under `aux_probe_mode()`.
   - Aux text tasks: `agent.auxiliary_client.call_llm(task="title_generation", messages=[...], max_tokens=30)`.
   - Browser: `tools.browser_tool_install.check_browser_requirements()`, `tools.browser_tool_cloud._get_cloud_provider()`, then end-to-end `tools.browser_use_cli.browser_exec(code, task_id="diag")`.
   Enable `logging.basicConfig(level=logging.DEBUG)` and grep the `agent.auxiliary_client` lines; they name the resolver branch that returned None.
3. **Test the provider directly** to separate "provider can't do it" from "Hermes can't route to it": import the plugin client and call it with a hand-built body. See `references/kiro-provider.md`. Do this before proposing any reroute: a provider that works directly means the fix is in routing or the plugin, never in switching providers.
4. **Check upstream** (`references/upstream-check.md`) before any local code patch.
5. **Fix in the right layer:** config in `/opt/data/config.yaml`; provider behaviour in the plugin; core bugs via image upgrade (`hermes-docker-updates`). Never try to edit `/opt/hermes`. When core/UI is read-only and the user wants a behaviour now, a small local plugin using a lifecycle hook is the interim layer (see `references/interim-plugins.md`); state its trade-offs and ask whether to also do the upstream patch.
6. **Verify in a fresh process.** The running session caches tool availability and the browser cloud-provider choice, so a correct config fix can still fail in-session. Prove it with the venv script, then tell the user a restart is needed for the live app.

## Pitfalls

- `auxiliary.<task>.provider: kiro` fails on Hermes 0.21.5 and older with "no credentials were found" even though Kiro is signed in: old core had no aux arm for plugin OAuth providers (debug log: `OAuth provider kiro not directly supported`). The plugin-OAuth aux arm (`agent/auxiliary_plugin_oauth.py`) shipped in v0.21.6+; upgrade rather than rerouting.
- `browser.cloud_provider: browser-use` with `use_gateway: true` routes through the Nous Tool Gateway; without a Nous subscription `browser_exec` errors "returned no CDP endpoint". Set `browser.cloud_provider: local`, `use_gateway: false` to use the packaged Chromium.
- A tool that fails in the current session right after a plugin edit (e.g. `vision_analyze` 400 `INVALID_MODEL_ID` from the old Kiro plugin) is usually the stale in-memory plugin, not the patch. Re-run the same tool function in a fresh venv process before debugging further; tell the user a restart is needed.
- Approval prompts time out after ~1 minute and block the command. Keep config-mutating steps (backup, `plugins.enabled` edit) in their own short command, separate from long verification scripts, so an unattended prompt does not stall the whole batch.
- Vision on Kiro needs both: the plugin must forward image parts (see reference) and the profile/model must be declared vision-capable; otherwise `vision_analyze` is hidden because native mode resolves to `text` and no aux vision backend resolves.
