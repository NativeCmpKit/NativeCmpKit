#!/usr/bin/env python3
"""Record reviewed hosted captures into showcase/coverage.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generate_coverage import render  # noqa: E402

CAPTURE_ROWS = {
    ("ui-adaptive-alert-dialog", "simple"): ["UI-ALERT-001", "UI-ALERT-002"],
    ("ui-adaptive-alert-dialog", "overview"): ["UI-ALERT-003", "UI-ALERT-004"],
    ("ui-adaptive-bottom-sheet", "expanded"): ["UI-SHEET-001"],
    ("ui-adaptive-dropdown", "menu"): ["UI-MENU-001", "UI-MENU-002"],
    ("ui-cupertino-icons", "search-chevron"): ["UI-ICON-001", "UI-ICON-003"],
    ("ui-cupertino-icons", "category-arrows"): ["UI-ICON-004"],
    ("webview", "second-page"): ["WEB-001", "WEB-002"],
    ("webview", "javascript-title"): ["WEB-004"],
    ("webview", "cookie-roundtrip"): ["WEB-005"],
    ("webview", "invalid-destination"): ["WEB-003"],
}

SCREEN_ROWS = {
    "ui-adaptive-button": ["UI-BUTTON-001", "UI-BUTTON-002", "UI-BUTTON-003", "UI-BUTTON-004"],
    "ui-adaptive-clickable": ["UI-CLICK-001"],
    "ui-adaptive-switch": ["UI-SWITCH-001", "UI-SWITCH-002"],
    "ui-adaptive-slider": ["UI-SLIDER-001", "UI-SLIDER-002", "UI-SLIDER-003"],
    "ui-adaptive-progress": ["UI-PROGRESS-001", "UI-PROGRESS-002"],
    "ui-adaptive-date-picker": ["UI-DATE-001", "UI-DATE-002", "UI-DATE-003", "UI-DATE-004",
                                "UI-DATE-005", "UI-DATE-006"],
    "ui-adaptive-time-picker": ["UI-TIME-001"],
    "ui-adaptive-alert-dialog": ["UI-ALERT-001", "UI-ALERT-002", "UI-ALERT-003",
                                 "UI-ALERT-004", "UI-ALERT-005"],
    "ui-adaptive-bottom-sheet": ["UI-SHEET-001", "UI-SHEET-002"],
    "ui-adaptive-dropdown": ["UI-MENU-001", "UI-MENU-002"],
    "ui-adaptive-scaffold": ["UI-BAR-001"],
    "ui-adaptive-top-bar": ["UI-BAR-002", "UI-BAR-005", "UI-ICON-002"],
    "ui-adaptive-navigation-bar": ["UI-BAR-003", "UI-BAR-006"],
    "ui-adaptive-toolbar": ["UI-BAR-004", "UI-BAR-007"],
    "ui-cupertino-icons": ["UI-ICON-001", "UI-ICON-003", "UI-ICON-004"],
    "io-file-picker": ["IO-CTX-001", "IO-FILE-001", "IO-PICK-001", "IO-PICK-002",
                       "IO-PICK-003", "IO-PICK-004"],
    "io-image-picker": ["IO-COIL-001"],
    "io-file-saver": ["IO-SAVE-001", "IO-SAVE-002"],
    "io-camera-picker": ["IO-CAMERA-001"],
    "share": ["SHARE-001", "SHARE-002", "SHARE-003"],
    "webview": ["WEB-001", "WEB-002", "WEB-003", "WEB-004", "WEB-005", "WEB-006"],
    "permissions": ["PERM-SINGLE-001", "PERM-BULK-001", "PERM-STATE-001", "PERM-NOTIF-001",
                    "PERM-LOC-001", "PERM-PIM-001", "PERM-BT-001", "PERM-CORE-001",
                    "PERM-SMS-001"],
    "geo-math": ["GEO-001", "GEO-003"],
    "home": ["NAV-001"],
    "ui-liquid-glass": ["UI-LIQUID-001", "UI-LIQUID-002", "UI-LIQUID-003", "UI-LIQUID-004"],
    "limitations": ["UI-PROGRESS-003", "UI-FAB-001", "PERM-STUB-001", "NAV-002", "GEO-002",
                    "EXCL-MAPS-001", "EXCL-MEDIA-001", "EXCL-NOTIF-001"],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coverage", type=Path, default=Path("showcase/coverage.json"))
    parser.add_argument("--tour", type=Path, required=True)
    parser.add_argument("--platform", choices=("android", "ios"), required=True)
    parser.add_argument("--run", required=True)
    parser.add_argument("--attempt", default="1")
    parser.add_argument("--job", required=True)
    parser.add_argument("--passed-ids", default="")
    parser.add_argument("--only-rows", default="")
    args = parser.parse_args()

    document = json.loads(args.coverage.read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in document["rows"]}
    passed = {item.strip() for item in args.passed_ids.split(",") if item.strip()}
    only = {item.strip() for item in args.only_rows.split(",") if item.strip()}
    tour = json.loads(args.tour.read_text(encoding="utf-8"))

    for capture in tour.get("captures", []):
        component = capture["component"]
        row_ids = CAPTURE_ROWS.get((component, capture["scenario"]), SCREEN_ROWS.get(component, []))
        for row_id in row_ids:
            if only and row_id not in only:
                continue
            row = rows[row_id]
            execution = row["execution"][args.platform]
            if execution["status"] not in ("not-applicable", "passed"):
                execution["status"] = "passed" if row_id in passed else "captured"
                execution["run"] = args.run
                execution["attempt"] = args.attempt
                execution["job"] = args.job
                execution["device"] = tour.get("device")
            row["screenshot"][args.platform] = capture["path"]
            row.setdefault("evidence", []).append({
                "platform": args.platform,
                "run": args.run,
                "attempt": args.attempt,
                "job": args.job,
                "capture": capture["path"],
            })

    for failure in tour.get("errors", []):
        component = failure.get("screen", "")
        for row_id in SCREEN_ROWS.get(component, []):
            if only and row_id not in only:
                continue
            row = rows[row_id]
            execution = row["execution"][args.platform]
            if execution["status"] != "not-applicable":
                execution["status"] = "failed"
                execution["run"] = args.run
                execution["attempt"] = args.attempt
                execution["job"] = args.job
                execution["device"] = tour.get("device")
            row.setdefault("defect", {})
            row["defect"] = {
                "platform": args.platform,
                "run": args.run,
                "attempt": args.attempt,
                "job": args.job,
                "error": failure.get("error"),
            }

    args.coverage.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    render(document)
    print(f"recorded {len(tour.get('captures', []))} captures; {len(tour.get('errors', []))} errors")


if __name__ == "__main__":
    main()
