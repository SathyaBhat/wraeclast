# Checking upstream for a Hermes / plugin fix

Use the GitHub REST API from `execute_code` (urllib with `User-Agent` and `Accept: application/vnd.github+json`); no auth needed for light use. `gh` is not installed in the container.

1. **Search issues/PRs:** `https://api.github.com/search/issues?q=<terms>+repo:NousResearch/hermes-agent`. Search by the exact log string (e.g. `"not directly supported"`), the provider name, and the subsystem (`auxiliary oauth plugin provider`). For plugins, list `https://api.github.com/repos/<owner>/<repo>/issues?state=all`.
2. **Read main's code, not just issues:** fetch `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/<path>` and look for the branch that failed locally. Fixes often land without a matching issue.
3. **Find the fixing commit:** `.../commits?path=<file>&per_page=10`.
4. **Find which releases contain it:** for each tag in `.../releases?per_page=15`, call `.../compare/<sha>...<tag>`; `ahead`/`identical` means the release includes the fix.
5. **Compare with the deployed version:** the image tag is `image:` in `/opt/data/wraeclast/apps/hermes/docker-compose.yml`; the in-container version is `/opt/hermes/.venv/bin/python -c "import hermes_cli; print(hermes_cli.__version__)"`. Calendar tags (`v2026.x.y`) and semver tags (`v0.2x.y`) coexist; use compare, not string ordering.
6. Report one of: fixed upstream (release X; upgrade via `hermes-docker-updates`), open PR (number + status), or unreported (offer to draft the issue/PR).
