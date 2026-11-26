#!/usr/bin/env python3
"""Emit the newest Hermes Agent GitHub release JSON only once per tag."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request, urlopen

API_URL = "https://api.github.com/repos/NousResearch/hermes-agent/releases/latest"
STATE_PATH = Path("/opt/data/cron/hermes-agent-release-watch.json")
BASELINE_TAG = "v2026.8.31"  # Latest release when this watch was created.


def main() -> None:
    try:
        request = Request(
            API_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "Hermes-Agent-release-watch",
            },
        )
        with urlopen(request, timeout=25) as response:
            release = json.load(response)
        tag = release["tag_name"]
    except Exception:
        # A transient fetch failure must not create a user-facing notification.
        return

    try:
        previous = json.loads(STATE_PATH.read_text(encoding="utf-8")).get("last_notified_tag")
    except Exception:
        previous = BASELINE_TAG

    if tag == previous:
        return

    # Advance only after a successfully retrieved, genuinely new release.
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps({"last_notified_tag": tag}) + "\n", encoding="utf-8")

    print(json.dumps({
        "name": release.get("name") or tag,
        "tag": tag,
        "published_at": release.get("published_at"),
        "url": release.get("html_url"),
        "body": (release.get("body") or "")[:40000],
    }))


if __name__ == "__main__":
    main()
