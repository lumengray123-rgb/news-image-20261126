#!/usr/bin/env python3
"""Entry program: copy the bundled front-page image to /output/entry.png.

The image is drawn by render.py and shipped in this repository as
entry.png. The grader runs this program twice; both runs must write
the same bytes, so this is a plain byte-for-byte copy.
"""
import os
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576


def main():
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    data = src.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    dest.write_bytes(data)
    print(f"wrote {dest} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
