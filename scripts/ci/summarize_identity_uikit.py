#!/usr/bin/env python3
"""Keep bounded UIKit failure diagnostics without raw process or fixture data."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET

from library_tests import NoDtdBuilder


MODULES = ("nativecmpkit-webview", "nativecmpkit-ui", "nativecmpkit-file-picker", "nativecmpkit-share")
HOSTS = ("native-webview-application", "native-ui-application", "native-picker-application", "native-share-application")
OWNED_ROOT = Path("build/ci-verification")
MAX_BYTES = 4 * 1024 * 1024
TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,90}\Z")
FRAME = re.compile(r"\b([A-Za-z0-9_]+\.kt):(\d{1,5})\b")
RESTORE_PHASE = re.compile(r"\bNATIVECMPKIT_WK_RESTORE:(?:(?:url|html|navigator|redirect|null):(?:initial|saved|remount)|wire:counters)\b")
RESTORE_STAGES = ("url", "html-recovery", "navigator", "redirect", "final", "null-recovery")


def restore_stages(fixture):
    stages = fixture.get("methods", {}).get("restore", {}).get("stages", {})
    return {name: {key: value for key in ("get", "page", "redirect", "closed", "pending")
                   if type(value := stages[name].get(key)) is int and 0 <= value <= 120}
            for name in RESTORE_STAGES if isinstance(stages.get(name), dict)}


def labels(document, fields):
    return {key: value for key in fields if isinstance(value := document.get(key), str) and TOKEN.fullmatch(value)}


def receipt_rows():
    for parent in (OWNED_ROOT, *(OWNED_ROOT / name for name in ("wk-identity", "identity-picker", "identity-share"))):
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
                    "crash": labels(crash, ("status", "error_type")) | labels(crash.get("exception") or {}, ("type", "signal")),
                    "fixture": {
                        **{key: fixture[key] for key in ("connections", "control_requests", "refusals", "owned_sockets", "fixture_error")
                           if type(fixture.get(key)) in {int, bool}},
                        "methods": {name: {"claimed": case.get("claimed") is True, "done": case.get("done") is True}
                                    for name, case in fixture.get("methods", {}).items() if name in {"restore", "replay", "headers", "resources"}},
                        "restore_stages": restore_stages(fixture),
                    },
                }


def failure_rows():
    for module in MODULES:
        results = Path(module) / "build/test-results/iosSimulatorArm64ApplicationTest"
        for path in sorted(results.glob("TEST-*.xml")):
            if not 0 < path.stat().st_size <= MAX_BYTES:
                continue
            raw = path.read_bytes()
            xml = ET.fromstring(raw, parser=ET.XMLParser(target=NoDtdBuilder()))
            for case in xml.iter("testcase"):
                failed = next((child for child in case if child.tag in {"failure", "error"}), None)
                name = case.get("name", "").removesuffix("[iosSimulatorArm64]")
                if failed is not None and TOKEN.fullmatch(name):
                    yield {
                        "module": module, "case": name, "status": failed.tag,
                        "original_xml_sha256": hashlib.sha256(raw).hexdigest(),
                        "source_frames": list(dict.fromkeys(FRAME.findall(failed.text or "")))[:8],
                        "restore_phases": list(dict.fromkeys(RESTORE_PHASE.findall(
                            failed.get("message", "") + "\n" + (failed.text or ""))))[:4],
                    }


def main():
    output = Path("build/ci-identity/uikit-diagnostics.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    summary = {"application_receipts": list(receipt_rows()), "junit_failures": list(failure_rows())}
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
