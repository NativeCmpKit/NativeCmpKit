#!/usr/bin/env python3
"""Render screenshots/INDEX.md from canonical captures and reviewed run metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CAPTIONS = {
    "home": "Searchable component index, stable routes and per-screen reset.",
    "limitations": "Source-confirmed unsupported and internal APIs; not working parity.",
    "geo-math": "Deterministic LatLng distance/bearing plus the tracker-unavailable state.",
    "permissions": "Public permission status and request rows; OS dialogs are separate.",
    "share": "Native share payloads and terminal result state.",
    "webview": "Deterministic HTML, navigation/errors, JavaScript and cookie state.",
    "io-file-picker": "Platform file selection, filters, metadata and streaming readout.",
    "io-image-picker": "Picked image preview through the KmpFile Coil pipeline.",
    "io-file-saver": "Save/export entry point and result state.",
    "io-camera-picker": "Camera launch and the platform-specific unavailable fallback.",
}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("screenshots"))
    parser.add_argument("--coverage", type=Path, default=Path("showcase/coverage.json"))
    parser.add_argument("--runs", type=Path, default=Path("screenshots/runs.json"))
    parser.add_argument("--output", type=Path, default=Path("screenshots/INDEX.md"))
    args = parser.parse_args()

    coverage = json.loads(args.coverage.read_text(encoding="utf-8"))
    rows = coverage["rows"]
    runs = json.loads(args.runs.read_text(encoding="utf-8")) if args.runs.exists() else {}

    lines = [
        "# Showcase device screenshots",
        "",
        f"App revision: `{runs.get('appSha', 'pending')}`",
        f"Base handoff: `{coverage['base']['sha']}`",
        "",
        "Every image is a PNG captured from the live GitHub-hosted Android emulator or",
        "iOS Simulator through ui-test-actions. Host renders and mockups are not used.",
        "",
    ]

    for platform in ("android", "ios"):
        directory = args.root / platform
        if not directory.exists():
            continue
        meta = runs.get("platforms", {}).get(platform, {})
        lines.extend([
            f"## {platform}",
            "",
            f"- Run: {meta.get('runUrl', 'pending')}",
            f"- Job/attempt: `{meta.get('job', 'pending')}` / `{meta.get('attempt', 'pending')}`",
            f"- Device: {meta.get('device', 'pending')}",
            f"- Runtime: {meta.get('runtime', 'pending')}",
            f"- ui-test-actions: `{runs.get('uiTestActionsRef', '0c818c5d72e8c30c59bd1287c330a40392bf8e89')}`",
            "",
            "| Capture | Component / scenario | Expected observation | Image |",
            "| --- | --- | --- | --- |",
        ])
        for png in sorted(directory.rglob("*.png")):
            relative = png.as_posix()
            component = png.parts[-3] if len(png.parts) >= 3 else png.parent.name
            scenario = png.parts[-2] if len(png.parts) >= 2 else ""
            expected = CAPTIONS.get(component, "")
            if not expected:
                for row in rows:
                    if row.get("screenshot", {}).get(platform) == relative:
                        expected = " / ".join(row.get("expected", []))[:220]
                        break
            lines.append(
                f"| `{component}/{scenario}` | {component} | {expected or 'See coverage.json'} | "
                f"![{component} {scenario}]({platform}/{component}/{scenario}/{png.name}) |"
            )
        lines.append("")

    for name, title in (("compare", "Side-by-side Android / iOS"),
                        ("compare-tablet", "Side-by-side tablet windows")):
        compare = args.root / name
        if not compare.exists():
            continue
        lines.extend([f"## {title}", ""])
        for png in sorted(compare.rglob("*.png")):
            relative = png.relative_to(compare)
            lines.append(f"- [{relative.as_posix()}]({png.as_posix()})")
        lines.append("")

    lines.extend(["## Functional flows", ""])
    any_functional = False
    for platform in ("android", "ios"):
        for functional in sorted((args.root / platform).glob("functional-*.json")):
            data = json.loads(functional.read_text(encoding="utf-8"))
            summary = data.get("summary", {})
            flow_count = len(data.get("flows", []))
            suffix = " (partial result file; see showcase/evidence/)" if flow_count < 30 else ""
            lines.append(
                f"- `{platform}/{functional.name}` — device `{data.get('device', 'unknown')}`: "
                f"**{summary.get('passed', 0)} passed**, {summary.get('failed', 0)} failed, "
                f"{summary.get('blocked', 0)} blocked, {flow_count} flows{suffix}."
            )
            any_functional = True
    if not any_functional:
        lines.append("- No functional result files were recorded in this checkout.")
    lines.append("")

    lines.extend([
        "## Status",
        "",
        "The per-row execution state is maintained in",
        "[showcase/coverage.json](../showcase/coverage.json) and summarized in",
        "[showcase/COVERAGE.md](../showcase/COVERAGE.md). A capture proves the screen",
        "rendered on that device; interaction assertions are recorded separately and",
        "must name the run/attempt/job that produced them.",
        "",
        "Unsupported rows point at the Known Limitations screen and are marked",
        "`not-applicable`; they are not evidence of working functionality.",
        "",
    ])

    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
