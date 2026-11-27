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
    parser.add_argument("--android-device", default="api35-phone")
    parser.add_argument("--ios-device", default="iphone-simulator")
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    android_root = args.root / "android"
    ios_root = args.root / "ios"
    pairs = []
    for android in sorted(android_root.rglob(f"{args.android_device}.png")):
        relative = android.parent.relative_to(android_root)
        ios = ios_root / relative / f"{args.ios_device}.png"
        if ios.is_file():
            pairs.append((android, ios, relative))
        else:
            print(f"missing iOS counterpart: {relative}")

    for android, ios, relative in pairs:
        target = args.output / relative
        if args.label:
            target = target / args.label
        target = target.with_suffix(".png")
        compose(android, ios, target)
        print(f"wrote {target}")
    print(f"{len(pairs)} comparison sheets")


if __name__ == "__main__":
    main()
