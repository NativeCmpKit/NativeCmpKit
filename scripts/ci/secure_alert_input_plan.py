#!/usr/bin/env python3
"""Exact isolated sample-callback source binding for ten finite library iOS methods.

This reads source only. No candidate Kotlin, Gradle, test process or sample app
is executed here. Actual native/stdout/stderr/keyboard/pixel evidence remains
mandatory; a source digest is not a runtime, physical-device or security proof.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import re
import stat

PROFILE = "ios-secure-alert-input"
FOCUS = "ios-native-secure-alert-input"
MODULE = "nativecmpkit-ui"
SOURCE_SET = "iosTest"
EXTERNAL_DIRECTORY = "sample/common/src/commonMain/kotlin/io.github.apdelrahman1911.nativecmpkit.sample/alertinput"
HELPER = EXTERNAL_DIRECTORY + "/SampleAlertDialogInputFields.kt"
SCREEN = "sample/common/src/commonMain/kotlin/io.github.apdelrahman1911.nativecmpkit.sample/screens/AlertDialogScreen.kt"
BUILD = "nativecmpkit-ui/build.gradle.kts"
NATIVE = "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/dialog/NativeSecureAlertInputTest.kt"
CAPTURE = "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/dialog/OwnedNativeConsoleCapture.kt"
CONTROLS = "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/dialog/OwnedNativeConsoleCaptureTest.kt"
BUILD_SEAM = 'sourceSets.getByName("iosTest").kotlin.srcDir(rootProject.file("' + EXTERNAL_DIRECTORY + '"))'
NATIVE_CLASS = "io.github.apdelrahman1911.nativecmpkit.ui.dialog.NativeSecureAlertInputTest"
CAPTURE_CLASS = "io.github.apdelrahman1911.nativecmpkit.ui.dialog.OwnedNativeConsoleCaptureTest"
NATIVE_METHODS = ("syntheticNativeInputKeepsRequestedKeyboardMaskedPixelsAndNoCapturedConsoleValues",)
CAPTURE_METHODS = (
    "bothRealSinksCapturePublicControlsAndRestoreOriginalDescriptorIdentity",
    "throwingBodyPreservesExactThrowableAndRestoresBothOriginalDescriptors",
    "nestedAndOversizeCapturesRefuseBeforeNoLogAcceptanceAndRestoreOriginalSinks",
    "inheritedCloseOnExecFlagsRestoreForBothRealDescriptors",
    "stderrOversizeRefusesWithoutTruncationAndRestoresBothOriginalSinks",
    "controlledShortReadsRefuseAndStillCloseEveryOwnedSink",
    "controlledPartialAcquisitionsRefuseBeforeActionAndReleaseEveryAcquiredHandle",
    "controlledRestoreFlagAndCloseRefusalsStillAttemptAllOtherOwnedCleanup",
    "bodyAndControlledCleanupFailurePreserveExactThrowableAndSuppressedRefusal",
)
QUALIFIED_SOURCE_SHA256 = {'sample/common/src/commonMain/kotlin/io.github.apdelrahman1911.nativecmpkit.sample/alertinput/SampleAlertDialogInputFields.kt': 'cf65d4231fc1cb3f83260224f2acb657634f89a1589e0f4aea56444c5af9ffec',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/dialog/NativeSecureAlertInputTest.kt': '4efc19fc6b031d7651bb92ebff1a56ab84cfdb49638aeb18d7e423ec30614e56',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/dialog/OwnedNativeConsoleCapture.kt': 'ce12478c3677910dd711293691b046b544103e72cfa3af3102152f03be526ec0',
 'nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/dialog/OwnedNativeConsoleCaptureTest.kt': '6afae03e21d48a033f0d0475d229c39299bb139cf4cd1d0c22a75e77a01536bc'}
ORIGINAL_DESCRIPTOR_EXPRESSION_SHA256 = "1adae899b3dd5da975e687a52f60b6f2af26dbadaa62b53af93aa8bbf094528e"
MAX_SOURCE_BYTES = 2 * 1024 * 1024
_NO_INPUT_LOG = re.compile(
    r"\b(?:println|print|NSLog|os_log|fprintf|fputs)\s*\(|"
    r"\bLog\.[diewv]\s*\(|\blogger\.|\bSystem\.(?:out|err)\.|\bconsole\.log\s*\("
)


def _path(root: Path, relative: str, *, optional: bool = False) -> Path | None:
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or any(part in {".", ".."} for part in parts):
        raise ValueError("Secure-input source must remain repository-relative")
    if root.is_symlink():
        raise ValueError("Secure-input source cannot use a symlink checkout")
    current = root
    for index, part in enumerate(parts):
        current = current / part
        try:
            shape = current.lstat()
        except FileNotFoundError:
            if optional:
                return None
            raise ValueError("The exact secure-input source is absent") from None
        if stat.S_ISLNK(shape.st_mode) or (index < len(parts) - 1 and not stat.S_ISDIR(shape.st_mode)):
            raise ValueError("Secure-input source cannot follow a symlink or non-directory ancestor")
    if not current.resolve().is_relative_to(root.resolve()):
        raise ValueError("Secure-input source escaped the owned checkout")
    return current


def _read(root: Path, relative: str, *, allow_empty_legacy_build: bool = False) -> bytes:
    path = _path(root, relative)
    assert path is not None
    before = path.lstat()
    minimum = 0 if allow_empty_legacy_build and relative == BUILD else 1
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or not minimum <= before.st_size <= MAX_SOURCE_BYTES:
        raise ValueError("Secure-input source requires one bounded owned regular file")
    data = path.read_bytes()
    after = path.lstat()
    identity = lambda value: (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size, value.st_mtime_ns)
    if identity(before) != identity(after) or len(data) != before.st_size:
        raise ValueError("Secure-input source changed during its bounded read")
    return data


def _external_directory(root: Path) -> None:
    directory = _path(root, EXTERNAL_DIRECTORY)
    assert directory is not None
    if not stat.S_ISDIR(directory.lstat().st_mode):
        raise ValueError("The isolated secure-input source directory is not owned")
    entries = directory.iterdir()
    first = next(entries, None)
    if first is None or first.name != "SampleAlertDialogInputFields.kt" or next(entries, None) is not None:
        raise ValueError("Compile only the exact single helper, never additional sample source")
    _read(root, HELPER)  # Reject symlink, hard link, empty/oversized or changed helper.


def _build_configured(root: Path, *, required: bool) -> bool:
    if _path(root, BUILD, optional=True) is None:
        if required:
            raise ValueError("The owning secure-input iosTest build is absent")
        return False
    text = _read(root, BUILD, allow_empty_legacy_build=not required).decode("utf-8")
    if BUILD_SEAM not in text:
        if required:
            raise ValueError("The exact isolated secure-input iosTest source seam is absent")
        return False  # Legacy/synthetic builds do not compile this external helper.
    if text.count(BUILD_SEAM) != 1:
        raise ValueError("The isolated secure-input source seam must be declared once")
    for line in text.splitlines():
        if "srcDir" in line and "sample" in line and line.strip() != BUILD_SEAM:
            raise ValueError("No broader or alternate sample source-set seam is permitted")
    if re.search(r"(?:implementation|api)\s*\(\s*(?:projects\.sample|project\s*\(\s*['\"]:sample)", text):
        raise ValueError("Library secure-input tests cannot depend on a sample module")
    _external_directory(root)
    return True


def external_test_sources(root: Path) -> tuple[str, ...]:
    """One actual iosTest source only, not all sample sources or a sample task."""
    return (HELPER,) if _build_configured(root, required=False) else ()


def held_provenance_sources(root: Path) -> tuple[str, ...]:
    """Hold compiled helper + originating screen identity; screen is NOT compiled."""
    return (HELPER, SCREEN) if _build_configured(root, required=False) else ()


def source_contract(root: Path) -> dict:
    _build_configured(root, required=True)
    source_hashes = {}
    for relative, expected in QUALIFIED_SOURCE_SHA256.items():
        actual = hashlib.sha256(_read(root, relative)).hexdigest()
        if actual != expected:
            raise ValueError("Secure-input source differs from its reviewed exact callbacks/native fixture/capture controls")
        source_hashes[relative] = actual
    screen_bytes = _read(root, SCREEN)
    screen = screen_bytes.decode("utf-8")
    helper = _read(root, HELPER).decode("utf-8")
    if (screen.count("textFields = sampleAlertDialogInputFields()") != 1 or
            screen.count("import io.github.apdelrahman1911.nativecmpkit.sample.alertinput.sampleAlertDialogInputFields") != 1 or
            _NO_INPUT_LOG.search(screen + "\n" + helper)):
        raise ValueError("The genuine sample must use the exact no-input-log callback seam")
    return {
        "schema_version": 1, "module": MODULE, "source_set": SOURCE_SET,
        "isolated_directory": EXTERNAL_DIRECTORY, "compiled_external_source": HELPER,
        "qualified_source_sha256": source_hashes,
        "originating_screen_source": SCREEN,
        "originating_screen_sha256": hashlib.sha256(screen_bytes).hexdigest(),
        "owning_build": BUILD, "owning_build_sha256": hashlib.sha256(_read(root, BUILD)).hexdigest(),
        "sample_screen_compiled": False, "sample_application_executed": False,
        "native_or_compile_success_inferred": False, "physical_device_verified": False,
        "capture_scope": "current-process-stdout-stderr-only",
    }


def validate_contract(contract: object, test_sources: list[str]) -> None:
    fixed = {
        "schema_version": 1, "module": MODULE, "source_set": SOURCE_SET,
        "isolated_directory": EXTERNAL_DIRECTORY, "compiled_external_source": HELPER,
        "qualified_source_sha256": QUALIFIED_SOURCE_SHA256,
        "originating_screen_source": SCREEN, "owning_build": BUILD,
        "sample_screen_compiled": False, "sample_application_executed": False,
        "native_or_compile_success_inferred": False, "physical_device_verified": False,
        "capture_scope": "current-process-stdout-stderr-only",
    }
    keys = set(fixed) | {"originating_screen_sha256", "owning_build_sha256"}
    if (not isinstance(contract, dict) or set(contract) != keys or
            any(type(contract.get(key)) is not type(value) or contract.get(key) != value for key, value in fixed.items()) or
            any(not isinstance(contract.get(key), str) or re.fullmatch(r"[0-9a-f]{64}", contract[key]) is None
                for key in ("originating_screen_sha256", "owning_build_sha256")) or
            any(test_sources.count(relative) != 1 for relative in QUALIFIED_SOURCE_SHA256) or
            SCREEN in test_sources):
        raise ValueError("Invalid exact secure-input source provenance or library-only build confinement")
