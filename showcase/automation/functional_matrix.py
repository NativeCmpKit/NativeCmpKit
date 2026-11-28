#!/usr/bin/env python3
"""Render a readable functional-verdict matrix from coverage.json."""

from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    document = json.loads((ROOT / "showcase" / "coverage.json").read_text(encoding="utf-8"))
    rows = document["rows"]
    per_flow: "OrderedDict[str, dict]" = OrderedDict()
    for row in rows:
        for entry in row.get("functional", []):
            flow = entry.get("flow", "?")
            bucket = per_flow.setdefault(flow, {"rows": [], "android": set(), "ios": set()})
            bucket["rows"].append(row["id"])
            platform = entry.get("platform", "android")
            bucket.setdefault(platform, set()).add(entry.get("status", "?"))

    lines = [
        "# Functional verdict matrix",
        "",
        "Generated from `showcase/coverage.json`; regenerate with",
        "`python3 showcase/automation/functional_matrix.py`.",
        "",
        "| Flow | Coverage rows | Android | iOS |",
        "| --- | --- | --- | --- |",
    ]
    for flow, data in per_flow.items():
        lines.append(
            "| `{flow}` | {rows} | {android} | {ios} |".format(
                flow=flow,
                rows=", ".join(sorted(set(data["rows"]))),
                android=", ".join(sorted(data["android"])) or "—",
                ios=", ".join(sorted(data["ios"])) or "—",
            )
        )
    lines.extend([
        "",
        "## Row verdicts without a flow record",
        "",
        "These rows carry a passed/failed execution status without a matching",
        "machine-readable flow entry: either a manual assertion in an earlier session",
        "or a result file from before the driver wrote after every flow.",
        "",
        "| Row | Platform | Status | Run |",
        "| --- | --- | --- | --- |",
    ])
    for row in rows:
        for platform in ("android", "ios"):
            execution = row["execution"][platform]
            if execution["status"] not in ("passed", "failed"):
                continue
            has_record = any(
                entry.get("platform") == platform and entry.get("run") == execution.get("run")
                for entry in row.get("functional", [])
            )
            if not has_record:
                lines.append(
                    f"| {row['id']} | {platform} | {execution['status']} | {execution.get('run', '—')} |"
                )

    lines.append("")
    (ROOT / "showcase" / "evidence" / "functional-matrix.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
    print(f"wrote {len(per_flow)} flows")


if __name__ == "__main__":
    main()
