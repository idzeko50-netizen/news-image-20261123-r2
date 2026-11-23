#!/usr/bin/env python3
"""Entrypoint for news-image-20261123 round 2.

Copies the pre-drawn front page (entry/entry.png, made by compose.py) to
MAKEFUN_OUTPUT_DIR (default /output) as entry.png, verifying the PNG
signature, size and SHA-256 after the copy. Standard library only, no
network, deterministic: the same bytes every run.
"""

import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry", "entry.png")
EXPECTED_SHA256 = "411af0b47205d6ce1cc1762fd653c8dcad3d5779f14a547eef11fbcbaef9f089"
MAX_BYTES = 1048576


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(SRC, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("entry.png is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    if width > 1024 or height > 1024:
        sys.exit("entry.png exceeds 1024x1024")
    if len(data) > MAX_BYTES:
        sys.exit("entry.png exceeds 1 MiB")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png sha256 mismatch")
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if hashlib.sha256(back).hexdigest() != EXPECTED_SHA256:
        sys.exit("written entry.png sha256 mismatch")
    os.chmod(dst, 0o644)


if __name__ == "__main__":
    main()
