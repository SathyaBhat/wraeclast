# Interim local plugins (remove when upstream catches up)

## Adding one: rules that apply to every interim plugin

- Write `plugin.yaml` and `__init__.py` under `/opt/data/plugins/<name>/`, then `chmod 755` the directory and `644` the files.
- Enable it with `/opt/hermes/.venv/bin/python -m hermes_cli.main plugins enable <name>`. The agent file tools refuse to edit `config.yaml`, so use the CLI and never patch the file directly.
- Tools registered by a plugin load only in new sessions ("deferred: tools (next session)"). A fresh process proves the tool exists: `discover_plugins(force=True)`, then `tools.registry.registry.get_entry("<tool>")` and `toolsets.resolve_toolset("<toolset>")`. Cron runs start fresh sessions, so they pick the tool up without a restart.
- To reach a platform API, reuse the core helpers in-process (e.g. `tools.discord_tool._get_bot_token()` + `_discord_request`). That way the token is read through the gateway's secret scope and never reaches the model, logs or a subprocess environment. Hard-code the destination (channel ID) instead of making it a tool argument, so the tool can't be pointed elsewhere.
- Back up `config.yaml` and `cron/jobs.json` to `/opt/data/backups/<UTC timestamp>/` before enabling the plugin or rewiring jobs to use it.

## kiro-credits

- Path: `/opt/data/plugins/kiro-credits` (`plugin.yaml` + `__init__.py`), listed in `config.yaml` `plugins.enabled`.
- Why: Hermes 0.23.0 fetches Kiro credits (kiro-provider `fetch_account_usage`) but only shows them in `/usage` and the model-picker payload. The desktop picker chip appears only at <=20% remaining, the status-bar `plan_gauge` reads Nous window plans only (`gateway/session_usage.py::plan_gauge`), and the gateway runtime footer (`gateway/runtime_footer.py`) has no credits field.
- How: a `transform_llm_output` hook appends `_Kiro credits: N/1000 used (P%) · resets D Mon_` to the final reply while the main provider is `kiro`. It skips the `subagent`, `cron`, `batch` and `eval` platforms, and skips replies that already end with the line. It reads `agent.account_usage_cache`, refreshes in the background when stale (>15 min), and blocks (~2 s) only on the first fetch in a process.
- Caveat: the hook runs before the assistant row is persisted, so the line is stored in the transcript and the model sees it in later turns.
- Verify: run `discover_plugins(force=True)`, then `hermes_cli.lifecycle.invoke_hook("transform_llm_output", response_text=..., platform="telegram", ...)`. The live app needs a restart to load it.
- Replace with: an upstream `credits` field in `display.runtime_footer.fields` plus a plugin-provider status-bar gauge. The related open PR is NousResearch/hermes-agent#103095 (desktop account usage in the status bar). Then delete the plugin dir and its `plugins.enabled` entry.

## super-report-discord

- Path: `/opt/data/plugins/super-report-discord`. It registers the tool `post_super_report` in toolset `super_report`, which the AustralianSuper monthly cron job uses.
- Why: cron can't post a summary with an anchored public-thread reply. Its `attach_to_session` thread is a standalone thread, created private on Discord because `create_handoff_thread` omits the thread type.
- How: the tool posts the summary to #ynab-finance (hard-coded `CHANNEL_ID`), starts a public thread from that message, and posts the details in chunks. Usage pattern: `scheduled-job-maintenance` → `references/report-jobs.md`.
- Replace with: core cron support for an anchored public reply thread on Discord (and a `type=public_thread` fix in `create_handoff_thread`). Then move the job back to normal delivery and remove the plugin.
