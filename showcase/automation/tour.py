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
    ("Known Limitations", "limitations", "known-limitations"),
]


def load_client(client_dir: Path):
    sys.path.insert(0, str(client_dir))
    from ui_sdk import LiveUI  # type: ignore

    return LiveUI


def find(ui, selector: dict, *, state: str = "present", timeout_ms: int = 8000):
    return ui.action(
        "element.wait",
        {"selector": selector, "state": state, "timeout_ms": timeout_ms},
    )


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


def scroll_up(ui):
    ui.action("pointer.scroll", {"x": 200, "y": 450, "dx": 0, "dy": -8})


def ensure_home(ui):
    for _ in range(6):
        search = find(ui, {"properties": {"editable": True}}, timeout_ms=2500)
        if search.get("satisfied") and search.get("nodes"):
            return
        scroll_up(ui)
    raise RuntimeError("Could not return to the Home search field")


def open_screen(ui, title: str):
    ensure_home(ui)
    search = find(ui, {"properties": {"editable": True}})
    node = search["nodes"][0]
    ui.action("element.click", {"id": node["id"], "snapshot_id": search["snapshot_id"]})
    ui.action("text.insert", {"text": title, "replace": True})
    click_text(ui, title)
    find(ui, {"text": title}, timeout_ms=12000)


def back(ui, platform: str):
    try:
        click_text(ui, "Back")
    except RuntimeError:
        ui.action("keyboard.press", {"keys": ["BACK"] if platform == "android" else ["ESCAPE"]})
    ensure_home(ui)


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
    shot("home", "index")

    for title, component, scenario in SCREENS:
        try:
            open_screen(ui, title)
            shot(component, scenario)

            if title == "Adaptive Alert Dialog":
                click_text(ui, "Show Simple Dialog")
                shot("ui-adaptive-alert-dialog", "simple")
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
                click_text(ui, "Load invalid URL")
                shot("webview", "invalid-destination")
            elif title == "Cupertino Icons":
                search = find(ui, {"properties": {"editable": True}})
                if search.get("satisfied") and search.get("nodes"):
                    node = search["nodes"][0]
                    ui.action("element.click", {"id": node["id"], "snapshot_id": search["snapshot_id"]})
                    ui.action("text.insert", {"text": "chevron", "replace": True})
                    shot("ui-cupertino-icons", "search-chevron")

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
