"""Minimal Home Assistant WebSocket client.

Usage: python3 ha_ws.py '[{"type":"get_states"}, {"type":"lovelace/config","url_path":"home-overview"}]'
Prints a JSON list of responses (one per message). Token from $HOME_ASSISTANT_API_TOKEN.
"""
import asyncio, json, os, sys
import websockets

URL = os.environ.get("HA_WS_URL", "ws://homeassistant.bishop-bass.ts.net/api/websocket")


async def call(msgs):
    async with websockets.connect(URL, max_size=None) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": os.environ["HOME_ASSISTANT_API_TOKEN"]}))
        r = json.loads(await ws.recv())
        assert r["type"] == "auth_ok", r.get("type")
        out = []
        for i, m in enumerate(msgs, 1):
            await ws.send(json.dumps(dict(m, id=i)))
            while True:
                r = json.loads(await ws.recv())
                if r.get("id") == i:
                    out.append(r)
                    break
        return out


if __name__ == "__main__":
    print(json.dumps(asyncio.run(call(json.loads(sys.argv[1])))))
