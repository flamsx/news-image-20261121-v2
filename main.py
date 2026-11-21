#!/usr/bin/env python3
"""Entry point: copy the pre-rendered front page to the output dir.

The image is drawn by draw.py (run locally when building); this program
only copies it, so the graded run is deterministic and needs no network.
Standard library only.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get(
        "OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    shutil.copyfile(src, os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
    sys.exit(0)
