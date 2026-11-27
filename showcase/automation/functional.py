#!/usr/bin/env python3
"""Functional (not screenshot-only) UI checks for the live showcase session."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tour  # noqa: E402


def assert_text(ui, text: str, timeout_ms: int = 6000):
    observation = tour.soft_find(ui, {"text_contains": text}, timeout_ms=timeout_ms)
    if not observation.get("satisfied"):
        raise AssertionError(f"missing visible text {text!r}")
    return observation


def assert_absent(ui, text: str, timeout_ms: int = 6000):
    try:
        observation = tour.find(ui, {"text_contains": text}, state="absent", timeout_ms=timeout_ms)
    except Exception as error:
        raise AssertionError(f"text {text!r} is still present") from error
    if not observation.get("satisfied"):
        raise AssertionError(f"text {text!r} is still present")


def text_value(ui, needle: str) -> str:
    observation = tour.soft_find(ui, {"text_contains": needle}, timeout_ms=4000)
    for node in observation.get("nodes", []):
        value = node.get("text") or node.get("name")
        if value and needle in value:
            return value
    raise AssertionError(f"no text containing {needle!r}")


def click_switch(ui):
    for role in ("switch", "AXSwitch", "togglebutton"):
        observation = tour.soft_find(ui, {"role": role}, timeout_ms=1500)
        if observation.get("satisfied") and observation.get("nodes"):
            node = tour.choose_clickable(observation, observation["nodes"])
            ui.action("element.click", {"id": node["id"], "snapshot_id": observation["snapshot_id"]})
            return
    raise AssertionError("no switch role exposed")


def drag_slider(ui, needle: str):
    for role in ("slider", "AXSlider"):
        observation = tour.soft_find(ui, {"role": role}, timeout_ms=1500)
        if observation.get("satisfied") and observation.get("nodes"):
            node = observation["nodes"][0]
            bounds = node.get("bounds")
            if not bounds:
                continue
            x, y, width, height = bounds["x"], bounds["y"], bounds["width"], bounds["height"]
            ui.action("pointer.drag", {
                "x": x + max(8, width // 5), "y": y + height // 2,
                "end_x": x + width - max(8, width // 5), "end_y": y + height // 2,
                "duration_ms": 500,
            })
            return
    raise AssertionError("no slider role exposed")


FLOWS = [
    ("buttons", "Adaptive Buttons", lambda ui, p: (
        assert_text(ui, "Clicked 0 times"),
        tour.click_text(ui, "Clicked 0 times"),
        assert_text(ui, "Clicked 1 times"),
    )),
    ("switch", "Adaptive Switch", lambda ui, p: (
        assert_text(ui, "Wi-Fi: off"),
        click_switch(ui),
        assert_text(ui, "Wi-Fi: on"),
    )),
    ("slider", "Adaptive Slider", lambda ui, p: (
        (lambda before: (
            drag_slider(ui, "Brightness"),
            (lambda after: (_ for _ in ()).throw(AssertionError("slider did not move"))
             if after == before else None)(text_value(ui, "Brightness")),
        ))(text_value(ui, "Brightness")),
    )),
    ("dropdown", "Adaptive Drop Down", lambda ui, p: (
        tour.click_text(ui, "More options"),
        assert_text(ui, "Duplicate"),
        tour.click_text(ui, "Duplicate"),
        assert_text(ui, "Duplicated!"),
    )),
    ("alert-cancel", "Adaptive Alert Dialog", lambda ui, p: (
        tour.click_text(ui, "Show Alert Dialog"),
        assert_text(ui, "This is a native alert dialog from Kira"),
        tour.click_text(ui, "Cancel"),
        assert_absent(ui, "This is a native alert dialog from Kira"),
    )),
    ("action-sheet", "Adaptive Alert Dialog", lambda ui, p: (
        tour.click_text(ui, "Show ActionSheet"),
        assert_text(ui, "Alert Dialog"),
        assert_text(ui, "Cancel"),
        tour.click_text(ui, "Cancel"),
        assert_absent(ui, "This is a native alert dialog from Kira"),
    )),
    ("permissions-bulk-deny", "Permissions", lambda ui, p: (
        tour.click_text(ui, "Request permissions"),
        (tour.click_text(ui, "Don't allow") if p == "android" else tour.click_text(ui, "Don’t Allow")),
        assert_text(ui, "All permissions granted: false"),
    )),
    ("sheet", "Adaptive Bottom Sheet", lambda ui, p: (
        tour.click_text(ui, "Show Bottom Sheet"),
        assert_text(ui, "Bottom Sheet"),
        tour.click_text(ui, "Close"),
        assert_absent(ui, "Allow swipe to hide"),
    )),
    ("topbar", "Adaptive Top Bar", lambda ui, p: (
        tour.click_text(ui, "Share"),
        assert_text(ui, "Last action: Share tapped"),
    )),
    ("toolbar", "Adaptive Toolbar", lambda ui, p: (
        tour.click_text(ui, "Share"),
        assert_text(ui, "Share tapped"),
    )),
    ("navbar", "Adaptive Navigation Bar", lambda ui, p: (
        tour.click_text(ui, "Profile"),
        assert_text(ui, "Profile"),
    )),
    ("icons-category", "Cupertino Icons", lambda ui, p: (
        assert_text(ui, "1322 icons"),
        tour.click_text(ui, "Arrows"),
        assert_absent(ui, "1322 icons"),
        assert_text(ui, "icons"),
    )),
    ("geo-math", "Geo Maths", lambda ui, p: (
        assert_text(ui, "111.19"),
        assert_text(ui, "Live tracking: unavailable"),
    )),
    ("limitations", "Known Limitations", lambda ui, p: (
        assert_text(ui, "Expandable FAB is internal"),
        assert_text(ui, "No determinate circular progress"),
    )),
    ("liquidglass", "Liquid Glass", lambda ui, p: (
        assert_text(ui, "LiquidGlassButton") if p == "ios" else assert_text(ui, "Liquid Glass is iOS 26 only"),
        (tour.click_text(ui, "Glass click 0"), assert_text(ui, "Glass click 1")) if p == "ios" else None,
    )),
    ("webview", "Web View", lambda ui, p: (
        assert_text(ui, "Kira WebView Demo"),
        tour.click_text(ui, "Load second HTML page" if p == "android" else "embed code"),
        assert_text(ui, "Kira Second Page"),
        tour.click_text(ui, "Evaluate JavaScript title"),
        assert_text(ui, "JS:"),
        tour.click_text(ui, "Set and read cookie"),
        assert_text(ui, "kira=1"),
        tour.click_text(ui, "Clear cookies"),
        assert_text(ui, "Cookies cleared"),
        tour.click_text(ui, "Load invalid URL"),
        assert_text(ui, "errors 1"),
    )),
]

BLOCKED = [
    ("permission-camera", "Permissions", "OS permission dialog targeting is not enabled in the baseline"),
    ("file-picker", "File Picker", "system document picker; no seeded file selection in this run"),
    ("file-saver", "File Saver", "system export dialog; no save destination in this run"),
    ("share", "Content Sharing", "system share sheet; no external recipient"),
    ("camera", "Camera Picker", "emulator camera source is not seeded"),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-dir", type=Path, required=True)
    parser.add_argument("--connection", type=Path, required=True)
    parser.add_argument("--token-file", type=Path, required=True)
    parser.add_argument("--platform", choices=("android", "ios"), required=True)
    parser.add_argument("--output-root", type=Path, default=Path("screenshots"))
    parser.add_argument("--only", default="")
    args = parser.parse_args()

    LiveUI = tour.load_client(args.client_dir)
    ui = LiveUI.open(args.connection, args.token_file)
    identity = ui.identify()
    selected = {item.strip() for item in args.only.split(",") if item.strip()}
    result = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "target": identity.get("target"),
        "session": identity.get("id"),
        "flows": [],
    }

    def save(flow: str, phase: str, png: bytes):
        directory = args.output_root / args.platform / "functional" / flow
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{phase}.png"
        path.write_bytes(png)
        return path.as_posix()

    for flow_id, screen, action in FLOWS:
        if selected and flow_id not in selected:
            continue
        entry = {"id": flow_id, "screen": screen, "status": "failed", "before": None, "after": None}
        try:
            ui.action("app.restart", {"id": tour.ANDROID_APP_ID})
            tour.find(ui, {"text_contains": "component screens"}, timeout_ms=10000)
            tour.open_screen(ui, screen)
            entry["before"] = save(flow_id, "before", ui.screenshot())
            action(ui, args.platform)
            entry["after"] = save(flow_id, "after", ui.screenshot())
            entry["status"] = "passed"
        except Exception as error:  # noqa: BLE001
            entry["error"] = repr(error)
            try:
                entry["after"] = save(flow_id, "failed-after", ui.screenshot())
            except Exception:
                pass
        result["flows"].append(entry)
        print(f"{entry['status']}: {flow_id} {entry.get('error', '')}")

    for flow_id, screen, reason in BLOCKED:
        if selected and flow_id not in selected:
            continue
        result["flows"].append({
            "id": flow_id, "screen": screen, "status": "blocked", "reason": reason,
            "before": None, "after": None,
        })
        print(f"blocked: {flow_id} ({reason})")

    passed = sum(1 for item in result["flows"] if item["status"] == "passed")
    failed = sum(1 for item in result["flows"] if item["status"] == "failed")
    blocked = sum(1 for item in result["flows"] if item["status"] == "blocked")
    result["summary"] = {"passed": passed, "failed": failed, "blocked": blocked}
    out = args.output_root / args.platform / "functional.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"]))
    raise SystemExit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
