# SPDX-License-Identifier: Apache-2.0
"""Finite Camera source/selection admission, not native acceptance.

Only NEW5 in one independently owned UIApplication. Controlled 24x16 UIImage,
real PNG/JPEG writes and GC/ownership checks are not physical capture, consent,
12/48MP profiling, native callback-throw, disk-full or observed write cancellation.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re

from ios_popover_anchor_plan import _ordinary_bytes, _unique_object

FOCUS = "ios-camera-ownership-memory-callback"
DISPOSAL_FOCUS = "ios-camera-ownership-memory-callback-disposal"
FOCUSES = (FOCUS, DISPOSAL_FOCUS)
PROFILE = FOCUS
MODULE = "nativecmpkit-camera-picker"
TASK_NAME = "iosSimulatorArm64ApplicationTest"
TASK = ":" + MODULE + ":" + TASK_NAME
COMPILER_TASK = ":" + MODULE + ":compileTestKotlinIosSimulatorArm64"
FOCUS_PROPERTY = "nativecmpkitCameraIosFocus"
INIT_SCRIPT = "scripts/ci/ios_camera_ownership_native.init.gradle.kts"
CONTRACT_KEY = "camera_ios_ownership_source_contract"
PHOTO_FIXTURE = "scripts/ci/ios_camera_photo_fixture.py"
CLASS = "io.github.apdelrahman1911.nativecmpkit.camerapicker.IosCameraOwnershipAcceptanceTest"
TEST_SOURCE = "nativecmpkit-camera-picker/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/camerapicker/IosCameraOwnershipAcceptanceTest.kt"
HOST_SOURCE = "nativecmpkit-camera-picker/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/camerapicker/internal/NativeCameraApplicationHost.kt"
IDENTITY_SOURCE = "nativecmpkit-camera-picker/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/camerapicker/internal/NativeCameraObjectIdentity.kt"
SOURCES = (TEST_SOURCE, HOST_SOURCE, IDENTITY_SOURCE)
DISPOSAL_METHOD = "compositionDisposalDuringObservedPresentingAndPresentedPhasesFinishesOwnedTeardown"
METHODS = (
    "publicOwnerSurvivesOrdinaryRecompositionAndNativeGcAndDeliversToLatestCallback",
    "doubleLaunchDuplicateTerminalInputAndReentrantReplacementKeepOneNativeOwner",
    DISPOSAL_METHOD,
    "actualSimulatorUnavailableAndCompetingModalOutcomesPreserveForeignPresenter",
    "controlledOriginalNativeImageWritesRealPngAndJpegAndSuccessOutlivesOwner",
)
SCOPE = ("Only NEW5 genuine Camera UIApplication/Worker/library methods. Controlled tiny 24x16 UIImage, "
         "actual source availability, GC and real Foundation PNG/JPEG/public file lifetime; terminal inputs "
         "are deliberately controlled, not physical capture/user gestures or recipient outcomes. One "
         "uniquely owned disposable app gets official photos grant/reset and an actual Main PHPhotoLibrary "
         "Authorized readback; this is controlled fallback setup, never denial, consent or security acceptance. "
         "No accepted Camera/picker/Share/WebView/UI/common/native replay, 12/48MP latency/RSS, native "
         "callback-throw, disk-full/cache eviction, observed worker-entry cancellation, other platform/OS, "
         "consumer/API-ABI/dependency/legal/security/readiness/publishing or issue closure claim.")
SOURCE_SHA256 = {'nativecmpkit-camera-picker/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/camerapicker/IosCameraOwnershipAcceptanceTest.kt': 'e4ee440103a9ad26a31259c45d29ff21d7a542f0cb52f5c43276528a469bf795', 'nativecmpkit-camera-picker/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/camerapicker/internal/NativeCameraApplicationHost.kt': 'fc6ddb7e7531ef9500388fceaeda04a4aa346f4a9c7601b13c67593c9c8352c5', 'nativecmpkit-camera-picker/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/camerapicker/internal/NativeCameraObjectIdentity.kt': '77ef5f5037b621f1c6cfe4c92c9d469bdbd3d56ba7318632106c2907c9234379'}
OTHER_SOURCE_SHA256 = {'nativecmpkit-camera-picker/build.gradle.kts': '44a82f78c4b35e0b9c63c964398c107e64ebd5756b5aa983e4016ebbff103ea4', 'nativecmpkit-camera-picker/src/commonMain/kotlin/io.github.apdelrahman1911.nativecmpkit/camerapicker/CameraPickerLauncher.kt': 'ded6bd6767cb25ed00a1f628028479a912f37111f9f7403b0e2b4757cdd1e332', 'nativecmpkit-camera-picker/src/commonMain/kotlin/io.github.apdelrahman1911.nativecmpkit/camerapicker/CameraPickerResult.kt': '5b67083ca39c46669b119c99e6cb3ac405bf5f4d4205343986d43f56f7f646a9', 'nativecmpkit-camera-picker/src/iosMain/kotlin/io.github.apdelrahman1911.nativecmpkit/camerapicker/CameraPickerLauncher.ios.kt': '036fd1b3e1b47721419be509812401f128ed2917a4c151bd7b847f2db7ac41d6', 'scripts/ci/ios_camera_ownership_native.init.gradle.kts': '03de60691aa7dfbf2e71f7f73380288ebbd1cfcf24fb6aa788b38dea235467a1', 'scripts/ci/ios_camera_photo_fixture.py': '0cae6165e230445944dc59c2aabbcc7b8a1d3c16e156eae9bf8c074e3465d752'}
ADMISSION = "build/ci-verification/camera-ios-native-source-admission.json"
COMPILE_ADMISSION = "build/ci-verification/camera-ios-precompiler-source-admission.json"


def selected_methods(focus: str) -> tuple[str, ...]:
    if focus not in FOCUSES:
        raise ValueError("Unknown exact Camera ownership focus")
    return METHODS if focus == FOCUS else (DISPOSAL_METHOD,)


def selectors(focus: str = FOCUS) -> tuple[str, ...]:
    return tuple(CLASS + "." + method for method in selected_methods(focus))


def focus_spec(focus: str = FOCUS) -> dict:
    return {"module": MODULE, "groups": ({"classname": CLASS, "source": TEST_SOURCE,
             "methods": selected_methods(focus), "declared_methods": METHODS},),
            "scope": SCOPE if focus == FOCUS else "Only the remaining Camera disposal method on the same owned UIKit host."}


def identities(focus: str = FOCUS) -> list[dict]:
    return [{"classname": TASK_NAME + "." + CLASS, "name": method + "[iosSimulatorArm64]"}
            for method in selected_methods(focus)]


def native_request(focus: str = FOCUS) -> list[str]:
    return [TASK, *(argument for selector in selectors(focus) for argument in ("--tests", selector))]


def _source_hashes(root: Path) -> dict[str, str]:
    wanted = SOURCE_SHA256 | OTHER_SOURCE_SHA256
    actual = {name: hashlib.sha256(_ordinary_bytes(root, name)[0]).hexdigest() for name in wanted}
    if actual != wanted:
        raise ValueError("Camera requires each exact ordinary reviewed source/build/init/privacy input")
    return actual


def validate_sources(root: Path, test_sources: list[str] | None = None) -> bool:
    if test_sources is not None and (type(test_sources) is not list or test_sources != sorted(SOURCES)):
        raise ValueError("Camera requires exactly three compiler test inputs, never common or an accepted host superset")
    _source_hashes(root)
    source = _ordinary_bytes(root, TEST_SOURCE)[0].decode("utf-8")
    if (re.findall(r"@Test\s+fun\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*\)", source) != list(METHODS) or
            re.search(r"@(Ignore|Disabled|IgnoredTest)\b", source) or
            "package " + CLASS.rsplit(".", 1)[0] not in source or "class " + CLASS.rsplit(".", 1)[1] not in source):
        raise ValueError("All exact enabled NEW5 declarations must remain authored")
    if any(re.search(r"@(Test|Ignore|Disabled|IgnoredTest)\b", _ordinary_bytes(root, name)[0].decode("utf-8"))
           for name in (HOST_SOURCE, IDENTITY_SOURCE)):
        raise ValueError("Camera ownership/privacy/identity helpers must remain zero-test")
    return True


def _contract(focus: str) -> dict:
    return {"schema_version": 1, "focus": focus, "module": MODULE, "task": TASK,
            "compiler_task": COMPILER_TASK, "init_script": INIT_SCRIPT,
            "focus_property": FOCUS_PROPERTY, "selected_methods": list(selectors(focus)),
            "effective_sources": list(SOURCES), "common_sources": [],
            "source_sha256": SOURCE_SHA256, "other_source_sha256": OTHER_SOURCE_SHA256,
            "required_testcases": identities(focus), "required_original_xml": 1,
            "privacy_setup": "owned-photos-grant-reset-and-actual-main-authorized-readback",
            "image_scope": "controlled-24x16-three-real-PNG-JPEG-PNG-writes-not-physical-or-profiling",
            "compiler_executions_attested": 0, "apple_links_attested": 0, "native_tests_executed": 0}


def source_contract(root: Path, focus: str = FOCUS) -> dict:
    validate_sources(root)
    return _contract(focus)


def validate_plan(plan: dict) -> bool:
    expected = plan.get("expected") if type(plan) is dict else None
    focus = plan.get("explicit_test_focus") if type(plan) is dict else None
    if (type(plan) is not dict or plan.get("suite") != "ios" or
            focus not in FOCUSES or plan.get("explicit_module_subset") != [MODULE] or
            plan.get("complete_suite_requested") is not False or type(expected) is not list or len(expected) != 1):
        raise ValueError("Camera requires exactly one explicit NEW5 iOS application plan")
    item = expected[0]
    if (type(item) is not dict or item.get("module") != MODULE or item.get("project") != ":" + MODULE or
            item.get("task") != TASK or item.get("report_directory") != MODULE + "/build/test-results/" + TASK_NAME or
            item.get("native_test_host") != "genuine-uikit-application" or
            item.get("test_source_sets") != ["iosTest"] or item.get("test_source_files") != sorted(SOURCES) or
            type(item.get("required_original_xml")) is not int or item["required_original_xml"] != 1 or
            item.get("test_filter") != ",".join(selectors(focus)) or item.get("required_testcases") != identities(focus) or
            item.get(CONTRACT_KEY) != _contract(focus) or
            type(item[CONTRACT_KEY].get("schema_version")) is not int or
            any(type(item[CONTRACT_KEY].get(key)) is not int for key in
                ("compiler_executions_attested", "apple_links_attested", "native_tests_executed", "required_original_xml")) or
            any(key in item for key in ("test_filter_argument", "test_exclusion_annotation", "ui_related_source_contract"))):
        raise ValueError("Camera exact test/source/build/privacy/selector contract must match without aliases")
    return True


def admission_document(*, native_task: bool, focus: str = FOCUS) -> dict:
    if type(native_task) is not bool:
        raise ValueError("Source admission must name its exact compiler or native-task boundary")
    return {"schema_version": 1, "task": TASK if native_task else COMPILER_TASK, "focus": focus,
            "phase": "native-task-source-admission" if native_task else "precompiler-source-admission",
            "selected_methods": list(selectors(focus)), "effective_sources": list(SOURCES), "common_sources": [],
            "source_sha256": SOURCE_SHA256, "excluded_unrelated_test_sources": True,
            "production_source_sets_changed": False, "compiler_executions_attested": 0,
            "apple_links_attested": 0, "native_tests_executed": 0,
            "scope": "Source/selection admission only; compiler result and fresh native XML/runtime/cleanup decide results"}


def validate_admission(root: Path, started_ns: int, ended_ns: int, focus: str = FOCUS) -> bool:
    if type(started_ns) is not int or type(ended_ns) is not int or started_ns <= 0 or ended_ns < started_ns:
        return False
    try:
        raw, info = _ordinary_bytes(root, ADMISSION)
        if not started_ns - 2_000_000_000 <= info.st_mtime_ns <= ended_ns + 2_000_000_000:
            return False
        validate_sources(root)
        document = json.loads(raw, object_pairs_hook=_unique_object,
                              parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Nonfinite Camera admission")))
        return (type(document) is dict and document == admission_document(native_task=True, focus=focus) and
                all(type(document.get(key)) is int for key in
                    ("schema_version", "compiler_executions_attested", "apple_links_attested", "native_tests_executed")) and
                all(type(document.get(key)) is bool for key in
                    ("excluded_unrelated_test_sources", "production_source_sets_changed")))
    except (OSError, ValueError, UnicodeError, TypeError, RecursionError):
        return False


def outcomes(cases: list[dict], host_system: str, *, cases_by_report: list[list[dict]], focus: str = FOCUS) -> tuple[list[dict], list[str]]:
    selected = identities(focus)
    wanted = Counter((case["classname"], case["name"]) for case in selected)
    shape = type(cases) is list and all(type(case) is dict and
            all(type(case.get(key)) is str for key in ("classname", "name", "status")) for case in cases)
    exact = shape and Counter((case["classname"], case["name"]) for case in cases) == wanted
    reports = type(cases_by_report) is list and len(cases_by_report) == 1 and cases_by_report == [cases]
    host = type(host_system) is str and host_system.lower() in {"darwin", "macos", "mac os x"}
    errors = [] if exact and reports and host else ["Camera requires the exact selected methods in one fresh original class XML on actual Apple host"]
    scenarios = []
    for identity in selected:
        matching = [case for case in cases if (case.get("classname"), case.get("name")) ==
                    (identity["classname"], identity["name"])] if shape else []
        passed = exact and reports and host and len(matching) == 1 and matching[0]["status"] == "passed"
        if not passed:
            errors.append("Required Camera method must pass exactly once: " + identity["name"])
        scenarios.append({**identity, "source": TEST_SOURCE, "task": TASK_NAME, "required_on_host": True,
                          "disposition": "required-executed" if passed else "required-not-passed"})
    return scenarios, errors
