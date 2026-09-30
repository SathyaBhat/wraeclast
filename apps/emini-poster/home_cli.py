#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Drive emini Home from a computer on the same network: the note, the screen, the picture.

    python3 tools/home_cli.py --host 192.168.1.50 note "Bins out tonight" --show
    python3 tools/home_cli.py show weather
    python3 tools/home_cli.py convert photo.jpg frame.bin      # needs Pillow
    python3 tools/home_cli.py picture frame.bin --show         # needs Picture firmware
    python3 tools/home_cli.py frame now.png                    # what the display shows

The host is --host or $EMINI_HOST: the device's address or its name.local, exactly as the phone
panel reaches it. This firmware has no pairing: anything on the local network is let in. (Against
firmware that still pairs, `pair CODE` with the code shown after holding OK keeps the token in
~/.config/emini-home/<host>.token, readable only by you, and it is sent from then on.)

In Breath mode (the default) Wi-Fi is off between fetches, so the device answers for about five
minutes after a press of OK. Anything unattended - a Home Assistant automation - needs Open mode.
Only the standard library is used, except that `convert` needs Pillow.
"""

import argparse
import json
import os
import struct
import sys
import urllib.error
import urllib.request
import zlib
from pathlib import Path

WIDTH, HEIGHT = 400, 300
FRAME_BYTES = WIDTH * HEIGHT // 4
NOTE_BYTES = 240
SCREENS = ["weather", "feed", "note", "sky", "air", "picture"]
# Two-bit codes 0..3 are black, white, yellow, red; the RGB is how the paper looks, as in
# firmware/ui/core.js, so an image is matched against the colours it will actually get.
PALETTE = [(26, 26, 22), (230, 229, 219), (247, 173, 1), (123, 0, 1)]


class HomeError(Exception):
    pass


def token_path(host):
    return Path.home() / ".config" / "emini-home" / (host + ".token")


def request(host, method, path, body=None, token=None, raw=False):
    headers = {}
    data = None
    if body is not None:
        if isinstance(body, bytes):
            data = body
            headers["Content-Type"] = "application/octet-stream"
        else:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request("http://%s%s" % (host, path), data, headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            payload = r.read()
    except urllib.error.HTTPError as e:
        try:
            message = json.loads(e.read()).get("error", "")
        except ValueError:
            message = ""
        raise HomeError("%s %s: %d %s" % (method, path, e.code, message or e.reason)) from None
    except OSError as e:
        raise HomeError(
            "%s: %s (in Breath mode, press OK on the device first)" % (host, e)
        ) from None
    return payload if raw else json.loads(payload or b"{}")


def load_token(host):
    try:
        return token_path(host).read_text().strip()
    except OSError:
        return None


def pair(host, code):
    token = request(host, "POST", "/api/pair", {"code": code})["token"]
    p = token_path(host)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(token + "\n")
    print("Paired; token saved to %s" % p)


def update_config(host, token, change):
    """Read, change and write back the settings. The revision read is sent back, so a change made
    in the phone panel in between is refused (409) rather than overwritten."""
    config = request(host, "GET", "/api/config", token=token)
    change(config)
    return request(host, "PUT", "/api/config", config, token=token)


def enable(config, screen):
    config["enabled"][SCREENS.index(screen)] = True


def show(host, token, screen):
    request(host, "POST", "/api/show", {"screen": screen}, token=token)
    print("Showing %s; the paper takes about 25 seconds" % screen)


def check_frame(data):
    if len(data) != FRAME_BYTES:
        raise HomeError("A frame is exactly %d bytes, this is %d" % (FRAME_BYTES, len(data)))


def to_png(frame, out):
    rows = bytearray()
    for y in range(HEIGHT):
        rows.append(0)
        for x in range(WIDTH):
            code = (frame[y * WIDTH // 4 + x // 4] >> (6 - 2 * (x % 4))) & 3
            rows += bytes(PALETTE[code])

    def chunk(kind, body):
        return (
            struct.pack(">I", len(body))
            + kind
            + body
            + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0)
    Path(out).write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(bytes(rows)))
        + chunk(b"IEND", b"")
    )


def convert(src, dither):
    try:
        from PIL import Image, ImageOps
    except ImportError:
        raise HomeError("convert needs Pillow: python3 -m pip install Pillow") from None
    image = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    image = ImageOps.fit(image, (WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    palette = Image.new("P", (1, 1))
    palette.putpalette([v for rgb in PALETTE for v in rgb] + [0, 0, 0] * 252)
    mode = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return pack(image.quantize(palette=palette, dither=mode).tobytes())


def pack(codes):
    """One two-bit code per pixel, row by row, into a frame: four pixels a byte, first one on top."""
    frame = bytearray(FRAME_BYTES)
    for i, code in enumerate(codes):
        frame[i // 4] |= (code & 3) << (6 - 2 * (i % 4))
    return bytes(frame)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--host", default=os.environ.get("EMINI_HOST"))
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("pair", help="pair with firmware that still asks for it")
    p.add_argument("code")
    p = sub.add_parser("note", help="set the note")
    p.add_argument("text")
    p.add_argument("--show", action="store_true", help="switch Note on and show it now")
    p = sub.add_parser("show", help="show a screen now")
    p.add_argument("screen", choices=SCREENS)
    p = sub.add_parser("picture", help="send a frame (.bin, or an image with Pillow)")
    p.add_argument("file")
    p.add_argument("--show", action="store_true", help="switch Picture on and show it now")
    p.add_argument("--dither", action="store_true", help="dither an image instead of flat colours")
    p = sub.add_parser("frame", help="save what the display shows (.bin or .png)")
    p.add_argument("out")
    p = sub.add_parser("convert", help="turn an image into a frame (.bin or .png preview)")
    p.add_argument("src")
    p.add_argument("out")
    p.add_argument("--dither", action="store_true")
    p = sub.add_parser("topng", help="preview a .bin frame as PNG")
    p.add_argument("src")
    p.add_argument("out")
    a = parser.parse_args()

    if a.command == "convert":
        frame = convert(a.src, a.dither)
        (to_png(frame, a.out) if a.out.lower().endswith(".png") else Path(a.out).write_bytes(frame))
        return
    if a.command == "topng":
        frame = Path(a.src).read_bytes()
        check_frame(frame)
        to_png(frame, a.out)
        return
    if not a.host:
        raise HomeError("Give --host or set EMINI_HOST")
    if a.command == "pair":
        return pair(a.host, a.code)
    token = load_token(a.host)
    if a.command == "note":
        size = len(a.text.encode())
        if size > NOTE_BYTES:
            raise HomeError("The note holds %d bytes of UTF-8, this is %d" % (NOTE_BYTES, size))

        def change(c):
            c["note"] = a.text
            if a.show:
                enable(c, "note")

        update_config(a.host, token, change)
        print("Note saved")
        if a.show:
            show(a.host, token, "note")
    elif a.command == "show":
        show(a.host, token, a.screen)
    elif a.command == "picture":
        data = Path(a.file).read_bytes()
        if not a.file.lower().endswith(".bin"):
            data = convert(a.file, a.dither)
        check_frame(data)
        request(a.host, "POST", "/api/picture", data, token=token)
        print("Picture saved")
        if a.show:
            config = request(a.host, "GET", "/api/config", token=token)
            if not config["enabled"][SCREENS.index("picture")]:
                update_config(a.host, token, lambda c: enable(c, "picture"))
            show(a.host, token, "picture")
    elif a.command == "frame":
        frame = request(a.host, "GET", "/api/frame", token=token, raw=True)
        check_frame(frame)
        (to_png(frame, a.out) if a.out.lower().endswith(".png") else Path(a.out).write_bytes(frame))


if __name__ == "__main__":
    try:
        main()
    except HomeError as e:
        sys.exit("error: %s" % e)
