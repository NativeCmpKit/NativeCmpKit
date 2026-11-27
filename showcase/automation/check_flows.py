#!/usr/bin/env python3
"""Static consistency checks for the functional flow tables.

No device is needed: this verifies that every flow in functional.py is mapped to
coverage rows (and vice versa), that row ids exist, and that statuses cannot be
written to the wrong device class.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import functional  # noqa: E402
import record_functional  # noqa: E402


def main() -> int:
    coverage = json.loads((HERE.parent / "coverage.json").read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in coverage["rows"]}
    flow_ids = [flow[0] for flow in functional.FLOWS]
    blocked_ids = [flow[0] for flow in functional.BLOCKED]
    mapped = record_functional.FLOW_ROWS
    problems: list[str] = []

    for duplicate in {item for item in flow_ids + blocked_ids if (flow_ids + blocked_ids).count(item) > 1}:
        problems.append(f"duplicate flow id: {duplicate}")

    for flow in flow_ids:
        if flow not in mapped:
            problems.append(f"flow without a coverage mapping: {flow}")

    for flow, row_ids in mapped.items():
        if flow not in flow_ids + blocked_ids:
            problems.append(f"mapping for an unknown flow: {flow}")
        for row_id in row_ids:
            row = rows.get(row_id)
            if row is None:
                problems.append(f"{flow}: unknown row {row_id}")
            elif row.get("windowClass") == "tablet":
                problems.append(f"{flow}: phone flow maps the tablet row {row_id}")

    for row_id, row in rows.items():
        if row["execution"]["android"]["status"] == "passed" or row["execution"]["ios"]["status"] == "passed":
            if not row.get("functional"):
                problems.append(f"{row_id}: passed without functional evidence")
        for platform in ("android", "ios"):
            status = row["execution"][platform]["status"]
            path = row.get("screenshot", {}).get(platform)
            if status in ("captured", "passed", "failed") and path and not Path(path).exists():
                problems.append(f"{row_id}: {platform} {status} screenshot missing: {path}")

    print(f"flows: {len(flow_ids)} (+{len(blocked_ids)} blocked), mapped flows: {len(mapped)}")
    for problem in problems:
        print(f"ERROR {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
