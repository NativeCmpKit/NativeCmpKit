#!/usr/bin/env python3
"""Validate the hosted-session dispatch surface without contacting GitHub.

Checks the workflow inputs/artifact names against the runbook commands and the
CLI flags of the automation scripts, so a typo is caught before a runner slot is
spent.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "showcase-ui.yml"
RUNBOOK = ROOT / "showcase" / "evidence" / "session-runbook.md"
SCRIPTS = {
    name: ROOT / "showcase" / "automation" / f"{name}.py"
    for name in ("tour", "functional", "record", "record_functional", "compare", "index",
                 "functional_matrix", "check_flows")
}
DEVICES = {"api35-phone", "api35-tablet", "iphone-simulator", "ipad-simulator"}


def problems() -> list[str]:
    issues: list[str] = []
    workflow = WORKFLOW.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")

    # workflow_dispatch inputs
    block = workflow.split("  workflow_dispatch:", 1)[1].split("\npermissions:", 1)[0]
    inputs = set(re.findall(r"^      ([a-z_]+):", block, re.MULTILINE))
    for expected in ("mode", "platform", "device_class", "duration_minutes"):
        if expected not in inputs:
            issues.append(f"workflow is missing input {expected!r}")
    for option in ("build", "session"):
        if f"options: [build, session]" not in block and f"- {option}" not in block:
            issues.append(f"workflow mode is missing option {option!r}")
    if "options: [both, android, ios]" not in block:
        issues.append("workflow platform options drifted")
    if "options: [phone, tablet]" not in block:
        issues.append("workflow device_class options drifted")

    # artifact names must include the device class
    for platform in ("android", "ios"):
        pattern = rf"ui-session-{platform}-\$\{{\{{ steps\.mode\.outputs\.device_class \}}\}}"
        if not re.search(pattern, workflow):
            issues.append(f"{platform} session artifact omits the device class")

    # runbook dispatch commands
    for match in re.finditer(r"gh workflow run ([^\n]+)\n((?:  [^\n]*\n)+)", runbook):
        command, args = match.group(1).split(" \\")[0].strip(), match.group(2)
        if command != "showcase-ui.yml -R NativeCmpKit/NativeCmpKit":
            issues.append(f"unexpected workflow in runbook: {command}")
        for flag in ("-f mode=", "-f platform=", "-f device_class=", "-f duration_minutes="):
            if flag not in args:
                issues.append(f"runbook dispatch misses {flag}")
        mode = re.search(r"-f mode=(\w+)", args)
        platform = re.search(r"-f platform=(\w+)", args)
        device = re.search(r"-f device_class=(\w+)", args)
        duration = re.search(r"-f duration_minutes=(\d+)", args)
        if mode and mode.group(1) not in ("build", "session"):
            issues.append(f"runbook mode {mode.group(1)!r} is not an input option")
        if platform and platform.group(1) not in ("both", "android", "ios"):
            issues.append(f"runbook platform {platform.group(1)!r} is not an input option")
        if device and device.group(1) not in ("phone", "tablet"):
            issues.append(f"runbook device class {device.group(1)!r} is not an input option")
        if duration:
            value = int(duration.group(1))
            if value < 5 or value > 150:
                issues.append(f"runbook duration {value} is outside the job timeout")

    # artifact download patterns
    for name in re.findall(r"-n (ui-session-[^\s]+)", runbook):
        if not re.match(r"ui-session-(android|ios)-(phone|tablet)-", name):
            issues.append(f"runbook artifact pattern drifts: {name}")

    # script flags named in the runbook
    for match in re.finditer(r"showcase/automation/(\w+)\.py((?: [^\n\\]+)?)", runbook):
        name, line = match.group(1), match.group(2)
        if name not in SCRIPTS:
            issues.append(f"runbook calls unknown script {name!r}")
            continue
        known = set(re.findall(r'"--([a-z0-9-]+)"', SCRIPTS[name].read_text(encoding="utf-8")))
        for flag in re.findall(r"--([a-z0-9-]+)", line):
            if flag not in known:
                issues.append(f"{name}.py has no --{flag} flag used in the runbook")

    # device names used by the automation and comparison steps
    for device in re.findall(r"--device ([\w-]+)", runbook):
        if device not in DEVICES:
            issues.append(f"unknown device name in runbook: {device}")
    for device in re.findall(r"--(?:android|ios)-device ([\w-]+)", runbook):
        if device not in DEVICES:
            issues.append(f"unknown comparison device in runbook: {device}")

    # canonical guard devices
    guard = (ROOT / "showcase" / "automation" / "record_functional.py").read_text(encoding="utf-8")
    for device in ("api35-phone", "iphone-simulator"):
        if f'"{device}"' not in guard:
            issues.append(f"record_functional canonical device {device} missing")

    # workflow YAML must at least be structurally closed (consistent indentation)
    for line_no, line in enumerate(workflow.splitlines(), 1):
        if "\t" in line:
            issues.append(f"workflow line {line_no} contains a tab")
    return issues


def main() -> int:
    issues = problems()
    for issue in issues:
        print(f"ERROR {issue}")
    print(f"dispatch checks: {'ok' if not issues else f'{len(issues)} problems'}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
