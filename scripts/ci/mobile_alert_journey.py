#!/usr/bin/env python3
"""Drive the existing Adaptive Alert Dialog sample with the released UI Test Actions SDK."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
from tempfile import TemporaryDirectory
import threading
import time
from urllib.parse import urlsplit


RELEASE = "e22f6c35fe6ca50a83890f54e4a6ec29ef0e2951"
APP = "io.github.apdelrahman1911.nativecmpkit.sample"
HOME = "NativeCmpKit"
SCREEN = "Adaptive Alert Dialog"
ALERT_MESSAGE = "This is a native alert dialog from NativeCmpKit"
SINGLE_MESSAGE = "This dialog only has a confirm button."


def selector(label):
    return {"label": label, "visible": True}


def exercise(ui, output, platform, device):
    commands = ui.capabilities()["commands"]
    required = {"app.restart", "app.wait_ready", "device.info", "element.assert", "element.click", "element.wait",
                "screenshot.capture", "tree.diff", "tree.snapshot", "ui.settle"}
    if not required.issubset(commands):
        raise ValueError(f"The native driver lacks these journey commands: {required - set(commands)}")
    info = ui.device_info()["result"]
    hardware = "emulator" if platform == "android" else "simulator"
    if info["platform"] != platform or info["device_id"] != device or info["form_factor_hardware"] != hardware:
        raise ValueError("The native driver is not attached to the owned hosted device")
    ui.wait_ready(APP, timeout_ms=20000)
    ui.settle(mode="target", target_selector=selector(HOME), timeout_ms=7000)
    events = []

    def click(label, *, ref=None):
        target = {"ref": ref} if ref else {"selector": selector(label)}
        since = time.monotonic()
        change = ui.click(**target, settle="fast", return_diff=True)
        events.append({"action": label, "elapsed_seconds": time.monotonic() - since, "observation": change["result"]})

    def open_sample():
        snapshot = ui.inspect(format="compact", visible_only=True)["result"]
        references = [node["ref"] for node in snapshot["nodes"] if node.get("ref") and
                      (node.get("label") or "").split(" · ", 1)[0] == SCREEN]
        if len(references) != 1:
            raise ValueError("Expected one actionable Adaptive Alert Dialog entry in the current sample menu")
        click(SCREEN, ref=references[0])
        ui.wait(selector("Show Alert Dialog"), state="visible", timeout_ms=8000)

    def assert_closed(message):
        ui.wait(selector(message), state="absent", timeout_ms=7000)
        ui.assert_element(selector("Show Alert Dialog"), state="visible")

    open_sample()
    click("Show Alert Dialog")
    ui.wait(selector(ALERT_MESSAGE), state="visible", timeout_ms=8000)
    dialog = ui.inspect(format="compact", visible_only=True)["result"]
    engine = "a11y_daemon" if platform == "android" else "axe_serve"
    if dialog.get("performance", {}).get("engine") != engine:
        raise ValueError(f"The alert was not observed through the persistent {engine} engine")
    screenshot = ui.screenshot(wait_stable_ms=200, bind_snapshot=True)
    png = screenshot.pop("png")
    if (not png.startswith(b"\x89PNG\r\n\x1a\n") or not screenshot.get("snapshot_id") or
            screenshot.get("sha256") != hashlib.sha256(png).hexdigest()):
        raise ValueError("Expected a PNG matching its bound alert screenshot metadata")
    (output / "alert.png").write_bytes(png)
    click("Cancel")
    assert_closed(ALERT_MESSAGE)

    click("Show Alert Dialog")
    ui.wait(selector(ALERT_MESSAGE), state="visible", timeout_ms=8000)
    click("Ok")
    assert_closed(ALERT_MESSAGE)

    click("Show Single Button Dialog")
    ui.wait(selector(SINGLE_MESSAGE), state="visible", timeout_ms=8000)
    ui.assert_element(selector("Cancel"), state="absent")
    click("Got it")
    assert_closed(SINGLE_MESSAGE)

    ui.action("app.restart", {"id": APP, "wait_ready": True, "timeout_ms": 20000})
    ui.wait(selector(HOME), state="visible", timeout_ms=10000)
    open_sample()
    ui.assert_element(selector(ALERT_MESSAGE), state="absent")
    return {"cases_passed": ["cancel", "confirm_after_reopen", "confirm_without_cancel", "restart_and_reenter"],
            "device": info, "dialog_snapshot": dialog, "screenshot": screenshot, "actions": events}


def run(upstream, platform, device, output, axe):
    actual = subprocess.check_output(["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True).strip()
    if actual != RELEASE:
        raise ValueError("UI Test Actions must match the verified v4.1.0 release commit")
    sys.path.insert(0, str(upstream))
    from lease import HoldLease
    from ui_sdk import LiveUI

    output.mkdir(parents=True)
    with TemporaryDirectory(prefix="nativecmpkit-ui-", dir=os.environ["RUNNER_TEMP"]) as scratch:
        control = Path(scratch)
        token = secrets.token_hex(32)
        token_file = control / "token"
        descriptor = os.open(token_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="ascii") as secret:
            secret.write(token)
        env = {name: os.environ[name] for name in (
            "PATH", "HOME", "TMPDIR", "LANG", "LC_ALL", "JAVA_HOME", "ANDROID_HOME", "ANDROID_SDK_ROOT",
            "ANDROID_AVD_HOME", "RUNNER_TEMP", "GITHUB_STEP_SUMMARY", "XCODE_SELECT_PATH", "DEVELOPER_DIR",
        ) if name in os.environ}
        if platform == "android":
            platform_tools = Path(env["ANDROID_HOME"]) / "platform-tools"
            if not os.access(platform_tools / "adb", os.X_OK):
                raise ValueError("The hosted Android SDK does not contain an executable adb")
            env["PATH"] = os.pathsep.join((str(platform_tools), env["PATH"]))
        env.update(UI_TEST_TARGET=platform, UI_TEST_DEVICE=device, UI_TEST_APP_IDS=APP,
                   UI_TEST_TOKEN_SHA256=hashlib.sha256(token.encode("ascii")).hexdigest(),
                   UI_TEST_TRANSPORT="local", UI_TEST_TRANSPORT_FALLBACK="none", UI_TEST_DURATION="5",
                   UI_TEST_STARTUP_TIMEOUT="45", UI_TEST_ANDROID_A11Y_DAEMON="1", UI_TEST_ANDROID_IME="0",
                   UI_TEST_DEVICE_ISOLATION="1",
                   UI_TEST_AGENT_ID="nativecmpkit-alert-journey")
        if axe is not None:
            env["UI_TEST_IOS_AXE"] = str(axe)
        done = threading.Event()

        def renew():
            while not done.is_set():
                (control / HoldLease.heartbeat).touch()
                done.wait(2)

        connection = control / "connection.json"
        with (output / "driver.log").open("xb") as log, subprocess.Popen(
            [sys.executable, str(upstream / "session.py"), str(control)], cwd=upstream, env=env,
            stdout=log, stderr=subprocess.STDOUT,
        ) as server:
            heartbeat = threading.Thread(target=renew)
            heartbeat.start()
            try:
                started = time.monotonic()
                while not connection.is_file():
                    if server.poll() is not None or time.monotonic() - started >= 180:
                        raise RuntimeError("The owned native UI session did not start")
                    done.wait(0.25)
                metadata = json.loads(connection.read_text(encoding="utf-8"))
                address = urlsplit(metadata["url"])
                if metadata["transport"] != "local" or address.scheme != "http" or address.hostname != "127.0.0.1":
                    raise ValueError("The native UI journey requires a runner-local listener")
                ui = LiveUI.open(connection, token_file)
                try:
                    result = exercise(ui, output, platform, device)
                except Exception:
                    try:
                        observed = ui.inspect(format="compact", visible_only=True, limit=80)
                        (output / "failure-observation.json").write_text(
                            json.dumps(observed, indent=2) + "\n", encoding="utf-8"
                        )
                    except Exception as diagnostic:
                        print(f"Unable to capture a compact failure observation: {diagnostic}", file=sys.stderr)
                    raise
                ui.close_session()
                (control / "stop").touch()
                if server.wait(timeout=20) != 0 or (control / "outcome").read_text() != "success":
                    raise RuntimeError("The owned native UI session did not close cleanly")
                result.update(repository_revision=os.environ["GITHUB_SHA"], ui_test_actions_revision=actual,
                              platform=platform, transport="local", elapsed_seconds=time.monotonic() - started)
                (output / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
            finally:
                (control / "stop").touch()
                done.set()
                heartbeat.join()
                if server.poll() is None:
                    try:
                        server.wait(timeout=15)
                    except subprocess.TimeoutExpired:
                        server.terminate()
                        try:
                            server.wait(timeout=10)
                        except subprocess.TimeoutExpired:
                            server.kill()
                            server.wait(timeout=10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", required=True, type=Path)
    parser.add_argument("--platform", required=True, choices=("android", "ios"))
    parser.add_argument("--device", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--axe", type=Path)
    options = parser.parse_args()
    if (options.platform == "ios") != (options.axe is not None):
        parser.error("The iOS profile requires the pinned native AXe driver")
    run(options.upstream.resolve(strict=True), options.platform, options.device,
        options.output.resolve(), options.axe.resolve(strict=True) if options.axe else None)
