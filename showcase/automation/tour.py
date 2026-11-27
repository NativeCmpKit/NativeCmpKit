#!/usr/bin/env python3
"""Capture the NativeCmpKit showcase screens on a live Android or iOS session.

The tour navigates only through the production Home search and real screens.
It writes canonical PNG paths consumed by screenshots/INDEX.md and the coverage
manifest. A failed screen is reported; it is never replaced with a mock image.

    python3 showcase/automation/tour.py \
      --client-dir /path/to/ui-test-actions \
      --connection live/connection.json --token-file /private/token \
      --platform android \
      --output-root screenshots
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


# title, component directory, default scenario
SCREENS = [
    ("Adaptive Buttons", "ui-adaptive-button", "overview"),
    ("Adaptive Clickable", "ui-adaptive-clickable", "overview"),
    ("Adaptive Switch", "ui-adaptive-switch", "overview"),
    ("Adaptive Slider", "ui-adaptive-slider", "overview"),
    ("Adaptive Progress Bar", "ui-adaptive-progress", "overview"),
    ("Adaptive Date Picker", "ui-adaptive-date-picker", "overview"),
    ("Adaptive Time Picker", "ui-adaptive-time-picker", "overview"),
    ("Adaptive Alert Dialog", "ui-adaptive-alert-dialog", "overview"),
    ("Adaptive Bottom Sheet", "ui-adaptive-bottom-sheet", "overview"),
    ("Adaptive Drop Down", "ui-adaptive-dropdown", "overview"),
    ("Adaptive Scaffold", "ui-adaptive-scaffold", "overview"),
    ("Adaptive Top Bar", "ui-adaptive-top-bar", "overview"),
    ("Adaptive Navigation Bar", "ui-adaptive-navigation-bar", "overview"),
    ("Adaptive Toolbar", "ui-adaptive-toolbar", "overview"),
    ("Cupertino Icons", "ui-cupertino-icons", "overview"),
    ("File Picker", "io-file-picker", "overview"),
    ("Image Picker", "io-image-picker", "overview"),
    ("File Saver", "io-file-saver", "overview"),
    ("Camera Picker", "io-camera-picker", "overview"),
    ("Content Sharing", "share", "overview"),
    ("Web View", "webview", "overview"),
    ("Permissions", "permissions", "overview"),
    ("Geo Maths", "geo-math", "overview"),
    ("Liquid Glass", "ui-liquid-glass", "overview"),
    ("Known Limitations", "limitations", "known-limitations"),
]


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
    parser.add_argument("--platform", choices=("android", "ios"), required=True)
    parser.add_argument("--output-root", type=Path, default=Path("screenshots"))
    parser.add_argument("--device", default=None)
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()

    device = args.device or ("api35-phone" if args.platform == "android" else "iphone-simulator")
    LiveUI = load_client(args.client_dir)
    ui = LiveUI.open(args.connection, args.token_file)
    identity = ui.identify()
    capabilities = ui.capabilities()
    record = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "target": identity.get("target"),
        "session": identity.get("id"),
        "device": device,
        "commands": sorted(capabilities.get("commands", [])),
        "captures": [],
        "errors": [],
    }

    def shot(component: str, scenario: str) -> str:
        directory = args.output_root / args.platform / component / scenario
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{device}.png"
        path.write_bytes(ui.screenshot())
        record["captures"].append(
            {"component": component, "scenario": scenario, "path": path.as_posix(),
             "bytes": path.stat().st_size}
        )
        print(f"captured {path}")
        return path.as_posix()

    # Home is the index and the reset entry point.
    if not home_visible(ui):
        ui.action("app.restart", {"id": ANDROID_APP_ID})
    find(ui, {"text_contains": "component screens"}, timeout_ms=10000)
    scroll_to_top(ui)
    shot("home", "index")

    for title, component, scenario in SCREENS:
        try:
            open_screen(ui, title)
            shot(component, scenario)

            if title == "Adaptive Alert Dialog":
                click_text(ui, "Show Alert Dialog")
                shot("ui-adaptive-alert-dialog", "simple")
                click_text(ui, "Cancel")
                if args.platform == "ios":
                    click_text(ui, "Show ActionSheet")
                    shot("ui-adaptive-alert-dialog", "action-sheet")
                    click_text(ui, "Cancel")
            elif title == "Adaptive Bottom Sheet":
                click_text(ui, "Show Bottom Sheet")
                shot("ui-adaptive-bottom-sheet", "expanded")
                click_text(ui, "Close")
            elif title == "Adaptive Drop Down":
                click_text(ui, "More options")
                shot("ui-adaptive-dropdown", "menu")
                ui.action("keyboard.press", {"keys": ["BACK"] if args.platform == "android" else ["ESCAPE"]})
            elif title == "Web View":
                click_text(ui, "Load second HTML page")
                find(ui, {"text": "Kira Second Page"}, timeout_ms=10000)
                shot("webview", "second-page")
                click_text(ui, "Navigate Back")
                shot("webview", "after-back")
                click_text(ui, "Navigate Forward")
                shot("webview", "after-forward")
                click_text(ui, "Evaluate JavaScript title")
                find(ui, {"text_contains": "JS:"}, timeout_ms=5000)
                shot("webview", "javascript-title")
                click_text(ui, "Set and read cookie")
                find(ui, {"text_contains": "kira=1"}, timeout_ms=5000)
                shot("webview", "cookie-roundtrip")
                click_text(ui, "Clear cookies")
                find(ui, {"text_contains": "Cookies cleared"}, timeout_ms=5000)
                shot("webview", "cookies-cleared")
                click_text(ui, "Load invalid URL")
                shot("webview", "invalid-destination")
            elif title == "Cupertino Icons":
                for category in ("Arrows", "Communication"):
                    click_text(ui, category)
                    shot("ui-cupertino-icons", "category-" + category.lower())

            back(ui, args.platform)
        except Exception as error:  # noqa: BLE001 - the run record must retain the real failure
            record["errors"].append({"screen": title, "error": repr(error)})
            print(f"FAILED {title}: {error}", file=sys.stderr)
            if not args.continue_on_error:
                break
            try:
                back(ui, args.platform)
            except Exception as recovery:  # noqa: BLE001
                record["errors"].append({"screen": title, "recovery": repr(recovery)})
                break

    record["ok"] = not record["errors"]
    out = args.output_root / args.platform / "tour.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": record["ok"], "captures": len(record["captures"]), "errors": len(record["errors"])}))
    raise SystemExit(0 if record["ok"] or args.continue_on_error else 1)


if __name__ == "__main__":
    main()
