#!/usr/bin/env python3
"""Drive one deterministic NativeCmpKit showcase smoke flow on a live session.

This is the first end-to-end proof used before the wider tour. It uses the
pinned ui-test-actions Python client from the same commit as the runner.

    python3 showcase/automation/smoke.py \
      --client-dir /path/to/ui-test-actions \
      --connection live/connection.json \
      --token-file /private/token \
      --output screenshots/_smoke/android

The token file is private and must never be committed.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_client(client_dir: Path):
    sys.path.insert(0, str(client_dir))
    from ui_sdk import LiveUI  # type: ignore

    return LiveUI


def find(ui, selector: dict, *, state: str = "present", timeout_ms: int = 8000):
    return ui.action(
        "element.wait",
        {"selector": selector, "state": state, "timeout_ms": timeout_ms},
    )


SEARCH_SELECTORS = (
    {"properties": {"editable": True}},
    {"role": "textbox"},
    {"text_contains": "Search components"},
    {"name": "Search components"},
)


def find_search(ui, timeout_ms: int = 2500):
    for selector in SEARCH_SELECTORS:
        observation = find(ui, selector, timeout_ms=timeout_ms)
        if observation.get("satisfied") and observation.get("nodes"):
            return observation
    return None


def click_text(ui, text: str):
    observation = find(ui, {"text": text})
    if not observation.get("satisfied"):
        observation = find(ui, {"name": text})
    if not observation.get("satisfied") or not observation.get("nodes"):
        raise RuntimeError(f"No visible element for {text!r}")
    node = next(
        (item for item in observation["nodes"] if item.get("properties", {}).get("clickable")),
        observation["nodes"][0],
    )
    ui.action("element.click", {"id": node["id"], "snapshot_id": observation["snapshot_id"]})


def open_screen(ui, title: str):
    search = find_search(ui, timeout_ms=8000)
    if not search:
        raise RuntimeError("The Home search field was not found")
    node = search["nodes"][0]
    ui.action("element.click", {"id": node["id"], "snapshot_id": search["snapshot_id"]})
    ui.action("text.insert", {"text": title, "replace": True})
    click_result(ui, title)
    find(ui, {"text": title}, timeout_ms=10000)


def click_result(ui, text: str):
    observation = find(ui, {"text": text})
    if not observation.get("satisfied"):
        observation = find(ui, {"name": text})
    nodes = [
        node for node in observation.get("nodes", [])
        if not node.get("properties", {}).get("editable")
    ]
    if not nodes:
        raise RuntimeError(f"No non-editable result for {text!r}")
    node = next(
        (item for item in nodes if item.get("properties", {}).get("clickable")),
        nodes[0],
    )
    ui.action("element.click", {"id": node["id"], "snapshot_id": observation["snapshot_id"]})


def back(ui, platform: str):
    try:
        click_text(ui, "Back")
    except RuntimeError:
        keys = ["BACK"] if platform == "android" else ["ESCAPE"]
        ui.action("keyboard.press", {"keys": keys})
    find(ui, {"text_contains": "component screens"}, timeout_ms=8000)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-dir", type=Path, required=True)
    parser.add_argument("--connection", type=Path, required=True)
    parser.add_argument("--token-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--platform", choices=("android", "ios"), required=True)
    args = parser.parse_args()

    LiveUI = load_client(args.client_dir)
    ui = LiveUI.open(args.connection, args.token_file)
    identity = ui.identify()
    capabilities = ui.capabilities()
    args.output.mkdir(parents=True, exist_ok=True)

    record = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "target": identity.get("target"),
        "session": identity.get("id"),
        "commands": sorted(capabilities.get("commands", [])),
        "screenshots": [],
    }

    def shot(name: str) -> None:
        path = args.output / name
        path.write_bytes(ui.screenshot())
        record["screenshots"].append({"name": name, "bytes": path.stat().st_size})
        print(f"captured {path}")

    shot("01-home.png")
    open_screen(ui, "Adaptive Buttons")
    shot("02-buttons.png")

    # Interact with the production button and confirm the visible counter changes.
    click_text(ui, "Clicked 0 times")
    shot("03-buttons-after-tap.png")
    find(ui, {"text_contains": "Clicked 1 times"}, timeout_ms=5000)

    back(ui, args.platform)
    shot("04-home-after-back.png")

    (args.output / "smoke.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "screenshots": len(record["screenshots"])}))


if __name__ == "__main__":
    main()
