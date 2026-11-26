#!/usr/bin/env python3
"""Copy entry.png to the grader output directory.

Standard library only: the grader runs with no third-party packages,
so this file imports nothing but os and shutil.
"""
import os
import shutil


def main():
    # entry.png sits next to this file in the repo; the grader only
    # guarantees MAKEFUN_OUTPUT_DIR, never the current directory.
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))


if __name__ == "__main__":
    main()
