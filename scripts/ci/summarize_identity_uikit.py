#!/usr/bin/env python3
"""Keep bounded platform failure diagnostics without raw process or fixture data."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET

from library_tests import NoDtdBuilder, safe_path
from ios_ui_application import PRE26_CUSTOMIZATION_PHASES, PRE26_NEGATIVE_STEPS_PHASES, WK_RESTORE_STEPS


MODULES = ("nativecmpkit-webview", "nativecmpkit-ui", "nativecmpkit-file-picker", "nativecmpkit-share", "nativecmpkit-camera-picker")
HOSTS = ("native-webview-application", "native-ui-application", "native-picker-application", "native-share-application", "native-camera-application")
OWNED_ROOT = Path("build/ci-verification")
MAX_BYTES = 4 * 1024 * 1024
TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,90}\Z")
FRAME = re.compile(r"\b([A-Za-z0-9_]+\.kt):(\d{1,5})\b")
RESTORE_PHASE = re.compile(r"\bNATIVECMPKIT_WK_RESTORE:(?:(?:url|html|navigator|redirect|null):(?:initial|saved|remount)|wire:counters)\b")
RESTORE_STAGES = ("url", "html-recovery", "navigator", "redirect", "final", "null-recovery")
ANDROID_RESTORE_TITLE = re.compile(r"\bNATIVECMPKIT_ANDROID_RESTORE_TITLE:(blank-dom|different-dom|evaluation-failed)\b")


def restore_stages(fixture):
    stages = fixture.get("methods", {}).get("restore", {}).get("stages", {})
    return {name: {key: value for key in ("get", "page", "redirect", "closed", "pending")
                   if type(value := stages[name].get(key)) is int and 0 <= value <= 120}
            for name in RESTORE_STAGES if isinstance(stages.get(name), dict)}


def labels(document, fields):
    return {key: value for key in fields if isinstance(value := document.get(key), str) and TOKEN.fullmatch(value)}


def receipt_rows():
    for parent in (OWNED_ROOT, *(OWNED_ROOT / name for name in (
        "wk-identity", "identity-picker", "identity-share", "identity-camera", "identity-main-ui",
        "identity-ui-pre26-customization", "identity-ui-pre26-remaining", "identity-ui-pre26-negative-steps",
        "identity-ui-pre26-toolbar",
    ))):
        for host in HOSTS:
            for path in sorted((parent / host).glob("*/receipt.json")):
                if not re.fullmatch(r"[a-f0-9]{32}", path.parent.name) or not 0 < path.stat().st_size <= MAX_BYTES:
                    continue
                raw = path.read_bytes()
                data = json.loads(raw)
                protocol = data.get("application_protocol") or data.get("application_protocol_partial") or {}
                transport = data.get("application_transport") or {}
                crash = data.get("owned_crash_diagnostics") or {}
                fixture = data.get("webview_content_policy_fixture") or {}
                yield {
                    "host": host,
                    "original_receipt_sha256": hashlib.sha256(raw).hexdigest(),
                    "transport_passed": data.get("transport_passed") is True,
                    "error": labels(data.get("error") or {}, ("phase", "type")),
                    "transport_failure": labels(transport, ("failure_stage", "failure_reason")),
                    "finished_case_counts": dict(Counter(case["status"] for case in protocol.get("testcases", [])
                                                        if case.get("status") in {"passed", "failed", "error", "skipped"})),
                    "unfinished_testcase": labels(protocol.get("unfinished_testcase") or {}, ("name",)),
                    "wk_restore_progress": [step for step in protocol.get("wk_restore_progress", [])[:len(WK_RESTORE_STEPS)]
                                            if step in WK_RESTORE_STEPS],
                    "pre26_customization_progress": [
                        step for step in protocol.get("pre26_customization_progress", [])[:len(PRE26_CUSTOMIZATION_PHASES)]
                        if step in PRE26_CUSTOMIZATION_PHASES
                    ],
                    "pre26_customization_host_confirmed": protocol.get("pre26_customization_host_confirmed") is True,
                    "pre26_negative_steps_progress": [
                        step for step in protocol.get("pre26_negative_steps_progress", [])[:len(PRE26_NEGATIVE_STEPS_PHASES)]
                        if step in PRE26_NEGATIVE_STEPS_PHASES
                    ],
                    "crash": labels(crash, ("status", "error_type")) | labels(crash.get("exception") or {}, ("type", "signal")),
                    "fixture": {
                        **{key: fixture[key] for key in ("connections", "control_requests", "refusals", "owned_sockets", "fixture_error")
                           if type(fixture.get(key)) in {int, bool}},
                        "methods": {name: {"claimed": case.get("claimed") is True, "done": case.get("done") is True}
                                    for name, case in fixture.get("methods", {}).items() if name in {"restore", "replay", "headers", "resources"}},
                        "restore_stages": restore_stages(fixture),
                    },
                }


def failure_rows(module, path, expected_digest=None):
    if not 0 < path.stat().st_size <= MAX_BYTES:
        return
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if expected_digest is not None and expected_digest != digest:
        raise ValueError("JUnit XML differs from its recorded digest")
    xml = ET.fromstring(raw, parser=ET.XMLParser(target=NoDtdBuilder()))
    for case in xml.iter("testcase"):
        failed = next((child for child in case if child.tag in {"failure", "error"}), None)
        name = case.get("name", "").removesuffix("[iosSimulatorArm64]")
        if failed is not None and TOKEN.fullmatch(name):
            failure_text = failed.get("message", "") + "\n" + (failed.text or "")
            yield {
                "module": module, "case": name, "status": failed.tag,
                "original_xml_sha256": digest,
                "source_frames": list(dict.fromkeys(FRAME.findall(failed.text or "")))[:8],
                "restore_phases": list(dict.fromkeys(RESTORE_PHASE.findall(failure_text)))[:4],
                "android_restore_title": list(dict.fromkeys(ANDROID_RESTORE_TITLE.findall(failure_text))),
            }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--android-webview", action="store_true")
    args = parser.parse_args()
    if args.android_webview:
        output = Path("build/ci-identity/android-webview-diagnostics.json")
        receipt = OWNED_ROOT / "identity-android-webview-device/library/receipt.json"
        failures = []
        if receipt.is_file() and 0 < receipt.stat().st_size <= MAX_BYTES:
            for module in json.loads(receipt.read_bytes())["modules"]:
                if module["task"] == ":nativecmpkit-webview:connectedAndroidDeviceTest":
                    for report in module["reports"]:
                        xml = safe_path(Path.cwd(), report["path"])
                        failures.extend(failure_rows(module["module"], xml, report["sha256"]))
        summary = {"junit_failures": failures}
    else:
        output = Path("build/ci-identity/uikit-diagnostics.json")
        failures = []
        for module in MODULES:
            results = Path(module) / "build/test-results/iosSimulatorArm64ApplicationTest"
            for path in sorted(results.glob("TEST-*.xml")):
                failures.extend(failure_rows(module, path))
        summary = {"application_receipts": list(receipt_rows()), "junit_failures": failures}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
