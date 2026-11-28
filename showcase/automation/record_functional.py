#!/usr/bin/env python3
"""Record functional flow results into the coverage manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generate_coverage import render  # noqa: E402

FLOW_ROWS = {
    "buttons": ["UI-BUTTON-001"],
    "switch": ["UI-SWITCH-001"],
    "clickable": ["UI-CLICK-001"],
    "slider": ["UI-SLIDER-001"],
    "dropdown": ["UI-MENU-001"],
    "alert-cancel": ["UI-ALERT-001"],
    "alert-confirm": ["UI-ALERT-001"],
    "alert-text-field": ["UI-ALERT-003", "UI-ALERT-005"],
    "action-sheet": ["UI-ALERT-004", "UI-ALERT-006"],
    "sheet": ["UI-SHEET-001"],
    "sheet-veto": ["UI-SHEET-002"],
    "date-display": ["UI-DATE-006"],
    "webview-js": ["WEB-006"],
    "topbar": ["UI-BAR-002"],
    "toolbar": ["UI-BAR-004"],
    "navbar": ["UI-BAR-003"],
    "scaffold-tab": ["UI-BAR-001"],
    "icons-category": ["UI-ICON-004"],
    "geo-math": ["GEO-001"],
    "nav-restore": ["NAV-003"],
    "liquidglass": ["UI-LIQUID-001", "UI-LIQUID-002", "UI-LIQUID-003", "UI-LIQUID-004"],
    "webview": ["WEB-001", "WEB-002", "WEB-003", "WEB-004", "WEB-005"],
    "permissions-bulk-deny": ["PERM-BULK-001"],
    "permissions-sms-rows": ["PERM-SMS-001"],
    "time-24h": ["UI-TIME-002"],
    "date-bounds": ["UI-DATE-004"],
    "limitations": ["UI-PROGRESS-003", "UI-FAB-001", "PERM-STUB-001", "NAV-002",
                    "GEO-002", "EXCL-MAPS-001", "EXCL-MEDIA-001", "EXCL-NOTIF-001"],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coverage", type=Path, default=Path("showcase/coverage.json"))
    parser.add_argument("--functional", type=Path, required=True)
    parser.add_argument("--platform", choices=("android", "ios"), required=True)
    parser.add_argument("--run", required=True)
    parser.add_argument("--attempt", default="1")
    parser.add_argument("--job", required=True)
    parser.add_argument("--allow-device", action="store_true")
    parser.add_argument("--tablet-rows", action="store_true")
    args = parser.parse_args()

    result = json.loads(args.functional.read_text(encoding="utf-8"))
    canonical = ("api35-phone", "iphone-simulator")
    if (result.get("device") not in canonical and not args.allow_device
            and not args.tablet_rows):
        raise SystemExit(
            f"{args.functional} is from device {result.get('device')!r}; the "
            "coverage execution slots are bound to the canonical phone devices. "
            "Keep tablet/large-screen results as separate evidence or pass "
            "--allow-device explicitly."
        )
    document = json.loads(args.coverage.read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in document["rows"]}
    for flow in result.get("flows", []):
        for row_id in FLOW_ROWS.get(flow["id"], []):
            row = rows[row_id]
            if args.tablet_rows and row.get("windowClass") != "tablet":
                continue
            if not args.tablet_rows and row.get("windowClass") == "tablet":
                continue
            execution = row["execution"][args.platform]
            if execution["status"] == "not-applicable":
                continue
            execution["status"] = flow["status"]
            if flow["status"] == "passed" and (row.get("defect") or {}).get("platform") == args.platform:
                row["defect"] = None
            execution["run"] = args.run
            execution["attempt"] = args.attempt
            execution["job"] = args.job
            execution["device"] = result.get("device")
            if flow.get("after"):
                row["screenshot"][args.platform] = flow["after"]
            entries = [
                item for item in row.setdefault("functional", [])
                if not (item.get("flow") == flow["id"] and item.get("run") == args.run)
            ]
            entries.append({
                "flow": flow["id"],
                "platform": args.platform,
                "status": flow["status"],
                "run": args.run,
                "attempt": args.attempt,
                "job": args.job,
                "before": flow.get("before"),
                "after": flow.get("after"),
                "error": flow.get("error"),
                "reason": flow.get("reason"),
            })
            row["functional"] = entries
    args.coverage.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    render(document)
    print(f"recorded {len(result.get('flows', []))} functional flows")


if __name__ == "__main__":
    main()
