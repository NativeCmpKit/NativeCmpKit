#!/usr/bin/env python3
"""Build Android-left / iOS-right comparison sheets from canonical captures."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def compose(android: Path, ios: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    filter_graph = (
        "[0:v]scale=-2:1400,"
        "drawtext=fontfile={font}:text='Android':x=20:y=20:fontsize=34:fontcolor=white:"
        "box=1:boxcolor=black@0.65:boxborderw=10[a];"
        "[1:v]scale=-2:1400,"
        "drawtext=fontfile={font}:text='iOS':x=20:y=20:fontsize=34:fontcolor=white:"
        "box=1:boxcolor=black@0.65:boxborderw=10[i];"
        "[a][i]hstack=inputs=2"
    ).format(font=FONT)
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-i", str(android), "-i", str(ios),
         "-filter_complex", filter_graph, "-frames:v", "1", str(output)],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("screenshots"))
    parser.add_argument("--output", type=Path, default=Path("screenshots/compare"))
    args = parser.parse_args()

    android_root = args.root / "android"
    ios_root = args.root / "ios"
    pairs = []
    for android in sorted(android_root.rglob("*.png")):
        relative = android.parent.relative_to(android_root)
        ios_dir = ios_root / relative
        candidates = sorted(ios_dir.glob("*.png")) if ios_dir.is_dir() else []
        if candidates:
            pairs.append((android, candidates[0], relative))
        else:
            print(f"missing iOS counterpart: {relative}")

    for android, ios, relative in pairs:
        output = args.output / relative.with_suffix(".png")
        compose(android, ios, output)
        print(f"wrote {output}")
    print(f"{len(pairs)} comparison sheets")


if __name__ == "__main__":
    main()
