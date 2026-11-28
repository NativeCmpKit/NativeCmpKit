#!/usr/bin/env python3
"""Probe native system surfaces (pickers/share/camera) on a live v4 session.

Read-only exploration for deciding whether a surface can become a functional
flow. Prints window owners and matching labels; never asserts a product result.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tour  # noqa: E402


def dump(ui, title):
    print(f"--- { title } ---")
    try:
        windows = ui.action("ui.windows")["result"].get("windows", [])
    except Exception as error:  # noqa: BLE001
        print("ui.windows failed:", error)
        windows = []
    for window in windows:
        print("window", window.get("id"), window.get("owner_app"), window.get("type"), window.get("modal"))
    try:
        tree = ui.action("tree.snapshot", {"include_hidden": False})["result"]
    except Exception as error:  # noqa: BLE001
        print("tree failed:", error)
        return
    labels = []
    for node in tree.get("nodes", []):
        value = node.get("label") or node.get("text") or node.get("name")
        if value:
            labels.append(value)
    print("labels", json.dumps(labels[:40], ensure_ascii=False))


def probe(ui, platform):
    ui.action("app.restart", {"id": tour.ANDROID_APP_ID, "wait_ready": True})
    tour.find(ui, {"text_contains": "component screens"}, timeout_ms=15000)

    tour.open_screen(ui, "File Picker", use_search=False)
    tour.click_text(ui, "Pick Files")
    dump(ui, "file picker")
    tour.back(ui, platform)

    tour.open_screen(ui, "Image Picker", use_search=False)
    tour.click_text(ui, "Pick Image")
    dump(ui, "image picker")
    tour.back(ui, platform)

    tour.open_screen(ui, "Content Sharing", use_search=False)
    tour.click_text(ui, "Share Text")
    dump(ui, "share sheet")
    try:
        ui.action("alert.dismiss", {"timeout_ms": 3000})
    except Exception:
        tour.back(ui, platform)

    tour.open_screen(ui, "Camera Picker", use_search=False)
    tour.click_text(ui, "Open Camera")
    dump(ui, "camera")
    try:
        ui.action("alert.dismiss", {"timeout_ms": 2000})
    except Exception:
        tour.back(ui, platform)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-dir", type=Path, required=True)
    parser.add_argument("--connection", type=Path, required=True)
    parser.add_argument("--token-file", type=Path, required=True)
    parser.add_argument("--platform", choices=("android", "ios"), required=True)
    args = parser.parse_args()
    LiveUI = tour.load_client(args.client_dir)
    ui = LiveUI.open(args.connection, args.token_file)
    probe(ui, args.platform)


if __name__ == "__main__":
    main()
