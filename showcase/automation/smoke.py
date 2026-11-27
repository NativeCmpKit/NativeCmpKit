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


ANDROID_APP_ID = "io.github.apdelrahman1911.nativecmpkit.sample"


def load_client(client_dir: Path):
    sys.path.insert(0, str(client_dir))
    from ui_sdk import LiveUI  # type: ignore

    return LiveUI


def find(ui, selector: dict, *, state: str = "present", timeout_ms: int = 8000):
    response = ui.action(
        "element.wait",
        {"selector": selector, "state": state, "timeout_ms": timeout_ms},
    )
    return response.get("result", response)


SEARCH_SELECTORS = (
    {"properties": {"editable": True}},
    {"role": "textbox"},
    {"text_contains": "Search components"},
    {"name": "Search components"},
)


def find_search(ui, timeout_ms: int = 2500):
    for selector in SEARCH_SELECTORS:
        try:
            observation = find(ui, selector, timeout_ms=timeout_ms)
        except Exception:
            continue
        if observation.get("satisfied") and observation.get("nodes"):
            return observation
    return None


def click_text(ui, text: str):
    observation = soft_find(ui, {"text": text})
    if not observation.get("satisfied"):
        observation = soft_find(ui, {"name": text})
    if not observation.get("satisfied") or not observation.get("nodes"):
        raise RuntimeError(f"No visible element for {text!r}")
    node = choose_clickable(observation, observation["nodes"])
    ui.action("element.click", {"id": node["id"], "snapshot_id": observation["snapshot_id"]})


_SCREEN = None


def screen_size(ui):
    global _SCREEN
    if _SCREEN is None:
        screen = ui.capabilities()["screen"]
        _SCREEN = (screen["width"], screen["height"])
    return _SCREEN


def scroll_list(ui, dy: int):
    width, height = screen_size(ui)
    ui.action("pointer.scroll", {"x": width // 2, "y": height // 2, "dx": 0, "dy": dy})


def scroll_to_top(ui):
    for _ in range(20):
        if soft_find(ui, {"text_contains": "UI Components"}, timeout_ms=600).get("satisfied"):
            return
        scroll_list(ui, -5)


def ensure_home(ui):
    if home_visible(ui):
        return
    for _ in range(3):
        ui.action("keyboard.press", {"keys": ["BACK"]})
        if home_visible(ui):
            return
    ui.action("app.restart", {"id": ANDROID_APP_ID})
    find(ui, {"text_contains": "component screens"}, timeout_ms=10000)


def open_screen(ui, title: str):
    ensure_home(ui)
    try:
        ui.action("keyboard.press", {"keys": ["ESC"]})
    except Exception:
        pass
    scroll_to_top(ui)
    for _ in range(40):
        observation = soft_find(ui, {"text_contains": title}, timeout_ms=800)
        nodes = observation.get("nodes", [])
        if observation.get("satisfied") and nodes:
            node = choose_clickable(observation, nodes)
            ui.action("element.click", {"id": node["id"], "snapshot_id": observation["snapshot_id"]})
            find(ui, {"text_contains": "component screens"}, state="absent", timeout_ms=10000)
            return
        scroll_list(ui, 3)
    raise RuntimeError(f"Could not find the Home entry for {title!r}")


def soft_find(ui, selector: dict, timeout_ms: int = 2500):
    try:
        return find(ui, selector, timeout_ms=timeout_ms)
    except Exception:
        return {"satisfied": False, "nodes": []}


def choose_clickable(observation, nodes):
    by_id = {node.get("id"): node for node in observation.get("nodes", [])}
    for node in nodes:
        current = node
        seen = set()
        while current and current.get("id") not in seen:
            if current.get("properties", {}).get("clickable"):
                return current
            seen.add(current.get("id"))
            current = by_id.get(current.get("parent_id"))
    return nodes[0]


def click_result(ui, text: str):
    observation = soft_find(ui, {"text": text})
    if not observation.get("satisfied"):
        observation = soft_find(ui, {"name": text})
    nodes = [
        node for node in observation.get("nodes", [])
        if not node.get("properties", {}).get("editable")
        and str(node.get("role", "")).lower() not in ("textbox", "textfield", "edittext")
    ]
    if not nodes:
        raise RuntimeError(f"No non-editable result for {text!r}")
    node = choose_clickable(observation, nodes)
    ui.action("element.click", {"id": node["id"], "snapshot_id": observation["snapshot_id"]})


def home_visible(ui) -> bool:
    return bool(soft_find(ui, {"text_contains": "component screens"}, timeout_ms=1000).get("satisfied"))


def back(ui, platform: str):
    if platform == "android":
        for _ in range(3):
            ui.action("keyboard.press", {"keys": ["BACK"]})
            if home_visible(ui):
                return
    else:
        try:
            click_text(ui, "Back")
        except RuntimeError:
            ui.action("pointer.drag", {"x": 4, "y": 420, "end_x": 300, "end_y": 420, "duration_ms": 300})
    if home_visible(ui):
        return
    ui.action("app.restart", {"id": ANDROID_APP_ID})
    find(ui, {"text_contains": "component screens"}, timeout_ms=10000)


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

    if not home_visible(ui):
        ui.action("app.restart", {"id": ANDROID_APP_ID})
    find(ui, {"text_contains": "component screens"}, timeout_ms=10000)
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
