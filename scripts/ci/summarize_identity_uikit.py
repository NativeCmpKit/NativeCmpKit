#!/usr/bin/env python3
"""Keep bounded platform failure diagnostics without raw process or fixture data."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET

from library_tests import IOS_DEFAULT_ACTION_SHEET_METHOD, NoDtdBuilder, safe_path
from camera_ios_ownership_native_focus import DISPOSAL_METHOD
from ios_popover_geometry_plan import METHODS as POPOVER_GEOMETRY_METHODS
from native_ui_input import ACTION_SHEET_FOCUS
from ios_ui_application import (
    CAMERA_DISPOSAL_PHASES, DEFAULT_ACTION_SHEET_PHASES, IPAD_ROTATION_PHASES, IPAD_ROTATION_STACK_MARKERS,
    PRE26_CUSTOMIZATION_PHASES, PRE26_MISSING_THUMB_PIXELS, PRE26_NEGATIVE_STEPS_PHASES,
    PRE26_STACK_MARKERS, PRE26_TOOLBAR_PHASES, WK_RESTORE_STEPS,
)


MODULES = ("nativecmpkit-webview", "nativecmpkit-ui", "nativecmpkit-file-picker", "nativecmpkit-share", "nativecmpkit-camera-picker")
HOSTS = ("native-webview-application", "native-ui-application", "native-picker-application", "native-share-application", "native-camera-application")
OWNED_ROOT = Path("build/ci-verification")
MAX_BYTES = 4 * 1024 * 1024
TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,90}\Z")
FRAME = re.compile(r"\b([A-Za-z0-9_]+\.(?:kt|java)):(\d{1,5})\b")
RESTORE_PHASE = re.compile(r"\bNATIVECMPKIT_WK_RESTORE:(?:(?:url|html|navigator|redirect|null):(?:initial|saved|remount)|wire:counters)\b")
RESTORE_STAGES = ("url", "html-recovery", "navigator", "redirect", "final", "null-recovery")
IPAD_ROTATION_PHASE = re.compile(
    r"\bNATIVECMPKIT_IPAD_ROTATION:(" + "|".join(map(re.escape, IPAD_ROTATION_PHASES)) + r")(?![A-Za-z0-9_-])"
)
DEFAULT_ACTION_SHEET_PHASE = re.compile(
    r"\bNATIVECMPKIT_DEFAULT_ACTION_SHEET:(" + "|".join(map(re.escape, (*DEFAULT_ACTION_SHEET_PHASES, "ipad-anchor"))) +
    r")(?![A-Za-z0-9_-])"
)
ANDROID_RESTORE_TITLE = re.compile(r"\bNATIVECMPKIT_ANDROID_RESTORE_TITLE:(blank-dom|different-dom|evaluation-failed)\b")
ANDROID_REMOTE_IO_FAILURE_MARKERS = {
    "held-open-admission": "genuine HTTP held pending-open admission",
    "awaiting-terminal-cleanup": "cancellation socket/native producer terminal",
    "provider-cancellation": "OperationCanceledException",
    "provider-file-not-found": "FileNotFoundException",
    "timeout": "TimeoutException",
    "assertion": "AssertionError",
}
CAMERA_DISPOSAL_FAILURE_MARKERS = {
    "terminal-before-disposal": "Camera returned a result before disposal admission",
    "presenting-at-launch": "The first disposal variant requires an observed real animated presentation",
    "presenting-at-disposal": "Composition disposal must occur in the actually observed requested UIKit phase",
    "unexpected-late-delivery": "Disposed owners suppress their late controlled terminal inputs",
    "native-timeout": "Timed out awaiting",
    "incorrect-picker-type": "UIImagePickerController",
}
ANDROID_ASSEMBLY_LOGS = {
    "camera-test-apk": "identity-android-camera/apk-assembly.log",
    "remote-io-helper-apk": "identity-android-remote-io/io-remote-documents/source-apk-build.log",
    "remote-io-test-apk": "identity-android-remote-io/apk-assembly.log",
}
GRADLE_FAILED_TASK = re.compile(r"^> Task ((?::[A-Za-z0-9_-]+){1,6}) FAILED\s*$", re.M)
GRADLE_SOURCE_ERROR = re.compile(
    r"^(?:e: [^\r\n]{0,500}[/\\]([A-Za-z0-9_.-]+\.kts?):(\d{1,5}):\d{1,5} "
    r"|[^\r\n]{0,500}[/\\]([A-Za-z0-9_.-]+\.java):(\d{1,5}): error: )", re.M
)
GRADLE_FAILURE_MARKERS = {
    "dependency-resolution": ("Could not resolve", "Could not find", "Could not download"),
    "repository-rate-limit": ("429 Too Many Requests", "status code 429"),
    "repository-policy": ("settings repositories over project repositories",),
    "android-sdk": ("SDK location not found", "Failed to find target", "Build Tools revision", "Failed to install the following Android SDK"),
    "signing": ("Failed to read key", "Keystore file", "keystore password was incorrect"),
    "java-toolchain": ("Cannot find a Java installation", "No matching toolchains found"),
    "compilation": ("Compilation error", "Compilation failed"),
    "android-resources": ("Manifest merger failed", "Android resource linking failed"),
}
PRE26_SAMPLE_STATUSES = (
    "owned-pid-not-observed", "owned-process-mismatch", "owned-process-unavailable", "sample-tool-refused",
    "sample-output-refused", "owned-process-changed",
    "observed", "sample-tool-unavailable",
)


def restore_stages(fixture):
    stages = fixture.get("methods", {}).get("restore", {}).get("stages", {})
    return {name: {key: value for key in ("get", "page", "redirect", "closed", "pending")
                   if type(value := stages[name].get(key)) is int and 0 <= value <= 120}
            for name in RESTORE_STAGES if isinstance(stages.get(name), dict)}


def labels(document, fields):
    return {key: value for key in fields if isinstance(value := document.get(key), str) and TOKEN.fullmatch(value)}


def observed_exit(document, key="exit_code"):
    value = document.get(key) if isinstance(document, dict) else None
    return value if type(value) is int and -(2**31) <= value < 2**31 else None


def camera_photo_summary(data, protocol):
    lease = data.get("camera_photos") or {}
    observation = protocol.get("camera_photo_authorization") or {}
    status = observation.get("status")
    outcomes = {f"{action}_exit": value for action in ("grant", "reset")
                if type(value := (lease.get(action) or {}).get("exit_code")) is int and -255 <= value <= 255}
    if status in ("authorized", "limited", "not-determined", "denied", "restricted", "unknown"):
        process_id = observation.get("process_id")
        launch_pid = protocol.get("observed_launch_pid")
        outcomes["actual_status"] = status
        outcomes["main_thread"] = observation.get("main_thread") is True
        outcomes["matches_observed_launch"] = type(process_id) is int and type(launch_pid) is int and process_id == launch_pid
    return outcomes


def stall_sample_summary(transport, field, markers):
    sample = transport.get(field)
    if not isinstance(sample, dict) or sample.get("status") not in PRE26_SAMPLE_STATUSES:
        return {}
    summary = {"status": sample["status"]}
    if sample["status"] == "observed":
        frames = sample.get("known_frames")
        summary["known_frames"] = [name for name in markers if isinstance(frames, list) and name in frames]
    return {field: summary}


def pre26_sample_summary(transport):
    return stall_sample_summary(transport, "pre26_stall_sample", PRE26_STACK_MARKERS)


def receipt_rows():
    for parent in (OWNED_ROOT, *(OWNED_ROOT / name for name in (
        "wk-identity", "identity-picker", "identity-share", "identity-camera", "identity-main-ui",
        "identity-ui-pre26-customization", "identity-ui-pre26-remaining", "identity-ui-pre26-negative-steps",
        "identity-ui-pre26-toolbar", "identity-ui-action-sheet", "identity-ui-ipad-rotation",
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
                native_input = data.get("native_xctest_input") or {}
                yield {
                    "host": host,
                    "original_receipt_sha256": hashlib.sha256(raw).hexdigest(),
                    "transport_passed": data.get("transport_passed") is True,
                    "error": labels(data.get("error") or {}, ("phase", "type")),
                    "transport_failure": labels(transport, ("failure_stage", "failure_reason")),
                    **pre26_sample_summary(transport),
                    **stall_sample_summary(transport, "ipad_rotation_stall_sample", IPAD_ROTATION_STACK_MARKERS),
                    "finished_case_counts": dict(Counter(case["status"] for case in protocol.get("testcases", [])
                                                        if case.get("status") in {"passed", "failed", "error", "skipped"})),
                    "unfinished_testcase": labels(protocol.get("unfinished_testcase") or {}, ("name",)),
                    "wk_restore_progress": [step for step in protocol.get("wk_restore_progress", [])[:len(WK_RESTORE_STEPS)]
                                            if step in WK_RESTORE_STEPS],
                    "pre26_customization_progress": [
                        step for step in protocol.get("pre26_customization_progress", [])[:len(PRE26_CUSTOMIZATION_PHASES)]
                        if step in PRE26_CUSTOMIZATION_PHASES or step == PRE26_MISSING_THUMB_PIXELS
                    ],
                    "pre26_customization_host_confirmed": protocol.get("pre26_customization_host_confirmed") is True,
                    "pre26_negative_steps_progress": [
                        step for step in protocol.get("pre26_negative_steps_progress", [])[:len(PRE26_NEGATIVE_STEPS_PHASES)]
                        if step in PRE26_NEGATIVE_STEPS_PHASES
                    ],
                    "pre26_toolbar_progress": [step for step in protocol.get("pre26_toolbar_progress", [])[:len(PRE26_TOOLBAR_PHASES)]
                                               if step in PRE26_TOOLBAR_PHASES],
                    "ipad_rotation_progress": [step for step in protocol.get("ipad_rotation_progress", [])[:len(IPAD_ROTATION_PHASES)]
                                               if step in IPAD_ROTATION_PHASES],
                    "default_action_sheet_progress": [
                        step for step in protocol.get("default_action_sheet_progress", [])[:len(DEFAULT_ACTION_SHEET_PHASES)]
                        if step in DEFAULT_ACTION_SHEET_PHASES
                    ],
                    **({"default_action_sheet_input": {
                        "ready": native_input.get("runner_ready") is True,
                        "verified": native_input.get("verified") is True,
                        "phase": labels(native_input, ("phase",)).get("phase"),
                        "build_exit_code": observed_exit(native_input.get("build")),
                        "startup_exit_code": observed_exit(native_input.get("runner_startup"), "process_exit_code"),
                        "startup_deadline": (native_input.get("runner_startup") or {}).get("deadline_reached") is True,
                        "swift_error_lines": [
                            line for line in native_input.get("swift_error_lines", [])[:24]
                            if type(line) is int and 1 <= line <= 99999
                        ],
                        "startup_phases": [
                            labels(step, ("phase", "domain")) |
                            ({"code": step["code"]} if type(step.get("code")) is int and
                             -(2**31) <= step["code"] < 2**31 else {})
                            for step in native_input.get("startup_diagnostics", [])[:24]
                        ],
                        "operations": [labels(operation, ("operation", "status", "reason"))
                                       for operation in native_input.get("operations", [])[:1]],
                    }} if native_input.get("focus") == ACTION_SHEET_FOCUS else {}),
                    **({"camera_photos": camera_photo_summary(data, protocol),
                        "camera_disposal_progress": [step for step in protocol.get("camera_disposal_progress", [])[:len(CAMERA_DISPOSAL_PHASES)]
                                                     if step in CAMERA_DISPOSAL_PHASES]}
                       if host == "native-camera-application" else {}),
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
            diagnostics = {}
            if module == "nativecmpkit-io":
                diagnostics["android_remote_io_failure_categories"] = [
                    key for key, marker in ANDROID_REMOTE_IO_FAILURE_MARKERS.items() if marker in failure_text
                ]
            if module == "nativecmpkit-camera-picker" and name == DISPOSAL_METHOD:
                diagnostics["camera_disposal_failure_categories"] = [
                    key for key, marker in CAMERA_DISPOSAL_FAILURE_MARKERS.items() if marker in failure_text
                ]
            if module == "nativecmpkit-ui" and name == POPOVER_GEOMETRY_METHODS[1]:
                diagnostics["ipad_rotation_phases"] = list(dict.fromkeys(IPAD_ROTATION_PHASE.findall(failure_text)))[:2]
                diagnostics["ipad_geometry_request_refused"] = "Owned public OS geometry request failed:" in failure_text
            if module == "nativecmpkit-ui" and name == IOS_DEFAULT_ACTION_SHEET_METHOD:
                diagnostics["default_action_sheet_phases"] = list(dict.fromkeys(DEFAULT_ACTION_SHEET_PHASE.findall(failure_text)))[:2]
            yield {
                "module": module, "case": name, "status": failed.tag,
                "original_xml_sha256": digest,
                "source_frames": list(dict.fromkeys(FRAME.findall(failed.text or "")))[:8],
                "restore_phases": list(dict.fromkeys(RESTORE_PHASE.findall(failure_text)))[:4],
                "android_restore_title": list(dict.fromkeys(ANDROID_RESTORE_TITLE.findall(failure_text))),
                **diagnostics,
            }


def android_assembly_summaries():
    rows = []
    for stage, relative in ANDROID_ASSEMBLY_LOGS.items():
        path = safe_path(Path.cwd(), (OWNED_ROOT / relative).as_posix())
        if not path.is_file() or path.is_symlink() or not 0 < path.stat().st_size <= MAX_BYTES:
            continue
        payload = path.read_bytes()
        document = payload.decode("utf-8", errors="replace")
        sources = ((kotlin or java, kotlin_line or java_line)
                   for kotlin, kotlin_line, java, java_line in GRADLE_SOURCE_ERROR.findall(document))
        rows.append({"stage": stage, "original_log_sha256": hashlib.sha256(payload).hexdigest(),
                     "failed_tasks": list(dict.fromkeys(GRADLE_FAILED_TASK.findall(document)))[:12],
                     "source_errors": list(dict.fromkeys(sources))[:12],
                     "categories": [key for key, variants in GRADLE_FAILURE_MARKERS.items()
                                    if any(marker in document for marker in variants)]})
    return rows


def android_receipt_failures(output_name, module_name):
    root = Path.cwd()
    receipt = safe_path(root, (OWNED_ROOT / output_name / "library/receipt.json").as_posix())
    if not receipt.is_file() or not 0 < receipt.stat().st_size <= MAX_BYTES:
        return []
    failures = []
    for module in json.loads(receipt.read_bytes())["modules"]:
        if module["task"] != f":{module_name}:connectedAndroidDeviceTest":
            continue
        for report in module["reports"]:
            xml = safe_path(root, report["path"])
            if not xml.is_relative_to(root / module_name / "build/outputs/androidTest-results/connected"):
                raise ValueError("Android JUnit report must belong to the selected module's connected test task")
            digest = report["sha256"]
            if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
                raise ValueError("Android JUnit report must have an exact SHA-256 witness")
            failures.extend(failure_rows(module_name, xml, digest))
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    platform = parser.add_mutually_exclusive_group()
    platform.add_argument("--android-webview", action="store_true")
    platform.add_argument("--android-ownership", action="store_true")
    args = parser.parse_args()
    if args.android_ownership:
        output = Path("build/ci-identity/android-ownership-diagnostics.json")
        summary = {"assembly": android_assembly_summaries(),
                   "junit_failures": android_receipt_failures("identity-android-remote-io", "nativecmpkit-io")}
    elif args.android_webview:
        output = Path("build/ci-identity/android-webview-diagnostics.json")
        summary = {"junit_failures": android_receipt_failures("identity-android-webview-device", "nativecmpkit-webview")}
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
