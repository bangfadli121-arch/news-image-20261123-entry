#!/usr/bin/env python3
"""Copy the pre-drawn front page to the output directory.

The entry image is drawn at build time by draw.py (Pillow) and stored
in this repository as entry.png. This program only copies those bytes
to /output/entry.png, so every run writes identical bytes and the
result is fully deterministic. Standard library only, no network.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    # The output directory is /output in the harness container; the
    # MAKEFUN_OUTPUT_DIR variable lets a local run point elsewhere.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
