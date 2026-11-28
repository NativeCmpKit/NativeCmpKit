#!/usr/bin/env python3
"""Check current source, build files and test consumers for superseded identities."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
NAMESPACE = "io.github.apdelrahman1911.nativecmpkit"
EXCLUDED = "scripts/ci/test_javafx_ordinary_success_trace.py"
ARCHIVE_TOOLS = {
    "scripts/audit/io_original_tests.py",
    "scripts/audit/source_inventory.py",
    "tests/consumer/binary_linkage.py",
    "tests/consumer/test_binary_linkage.py",
}
HISTORICAL_REJECTION_FIXTURES = {
    "scripts/ci/core_io_consumer.py",
    "tests/consumer/build.gradle.kts",
    "tests/consumer/io-desktop/build.gradle.kts",
    "tests/consumer/webview-desktop/build.gradle.kts",
    "tests/consumer/verify_artifacts.py",
}
ARCHIVED_CARRIAGE_METADATA = (
    "docs/development/evidence/current-platform-recovery-20261101/native-stage-prerequisites20261104/metadata-current606/"
    "calf-file-picker.json",
    "docs/development/evidence/current-platform-recovery-20261101/native-stage-prerequisites20261104/metadata-current606/"
    "calf-share.json",
)
ANDROID_PACKAGE_FIXTURE = "nativecmpkit-webview/src/androidHostTest/kotlin/android/webkit/NativeCmpKitControlledResourceError.kt"
ACTIVE_ROOTS = {"sample", "scripts", "tests", "tools", "gradle", "convention-plugins", ".github"}
ACTIVE_DOCS = {
    "README.md", "CONTRIBUTING.md", "NOTICE", "THIRD_PARTY_NOTICES.md", "docs/index.md",
    "docs/installation.md", "docs/ui.md", "docs/webview.md", "docs/filepicker.md", "docs/share.md",
    "docs/sf-symbols.md", "docs/permissions.md",
    "docs/development/android-io-default-decode.md", "docs/development/android-io-named-system-providers.md",
    "docs/development/android-io-provider-lifecycle.md", "docs/development/android-permission-lifecycle-compatibility.md",
    "docs/development/compatibility.md",
    "docs/development/ios-share-presentation-disposal.md", "docs/development/navigation-unknown-routes.md",
    "docs/development/share-clipboard-native-contexts.md",
    "docs/testing/adaptive-controls-native-matrix.md", "docs/testing/android-camera-callback-substitution.md",
    "docs/testing/ios-camera-ownership-native-routing.md", "docs/testing/ios-popover-geometry.md",
    "docs/testing/native-license-schema4.md",
    "docs/testing/ui-drag-shader-lifecycle.md",
    "docs/testing/webview-content-policy.md", "docs/testing/webview-content-policy-native-routing.md",
    "docs/testing/nativecmpkit-webview-content-policy-focuses.json",
}
SOURCE_SUFFIXES = {".kt", ".kts", ".java", ".rs", ".swift", ".c", ".cc", ".cpp", ".h", ".mm", ".js", ".mjs", ".cjs"}
CONFIG_SUFFIXES = {".py", ".toml", ".lock", ".yaml", ".yml", ".json", ".properties", ".xml", ".plist",
                   ".pbxproj", ".sh", ".bat", ".html", ".css", ".pro", ".def", ".gradle", ".xcconfig"}
# Avoid treating longer ordinary words as names when matching camel-case symbols.
OLD_IDENTITY = re.compile(
    r"com[./_]mohamedrejeb[./_](?:calf|nativecmpkit)(?:[./_]|\b)|\b(?i:calf)[-_]|\b(?:Experimental)?Calf[A-Z]|\bcalf[A-Z]"
    r"|io[./_]github[./_]apdelrahman1911[./_]kira(?:[./_]|\b)|\bkira-"
    r"|\b(?i:github\.com/apdelrahman1911/nativecmpkit)\b"
)
PACKAGE = re.compile(r"^package\s+([\w.]+)", re.M)


def main():
    paths = subprocess.check_output(
        ["git", "ls-files", "-z", "--", ".", f":(exclude){EXCLUDED}"], cwd=ROOT
    ).decode().split("\0")
    checked = 0
    errors = []
    for relative in filter(None, paths):
        path = Path(relative)
        root = path.parts[0]
        if re.match(r"(?i)^(?:calf|kira)-", root):
            errors.append(f"{relative}: legacy module path")
            continue
        if relative == "scripts/development/verify_namespace.py" or relative in ARCHIVE_TOOLS:
            continue
        if relative.startswith(("tests/consumer/binary/", "scripts/ci/fixtures/")):
            continue
        current_doc = relative in ACTIVE_DOCS or (relative.startswith("docs/ui/") and path.suffix == ".md")
        if not (root in ACTIVE_ROOTS or root.startswith("nativecmpkit-") or len(path.parts) == 1 or current_doc):
            continue
        if path.suffix not in SOURCE_SUFFIXES | CONFIG_SUFFIXES and not current_doc:
            continue
        raw = (ROOT / path).read_bytes()
        if b"\0" in raw:
            continue
        source = raw.decode("utf-8")
        checked += 1
        if path.suffix == ".kt" and (root.startswith("nativecmpkit-") or root in {"sample", "tests"}):
            package = PACKAGE.search(source)
            if relative != ANDROID_PACKAGE_FIXTURE and (package is None or not (
                package[1] == NAMESPACE or package[1].startswith(NAMESPACE + ".")
            )):
                errors.append(f"{relative}: Kotlin package is outside the project namespace")
        for number, line in enumerate(source.splitlines(), 1):
            if relative == "tests/consumer/build.gradle.kts" and line.strip() == (
                'check(id.group != "com.mohamedrejeb.calf" && id.group != "io.github.apdelrahman1911.kira") {'
            ):
                continue
            if relative in HISTORICAL_REJECTION_FIXTURES and "Calf" in line and "!=" in line:
                continue
            if relative == "tests/consumer/verify_artifacts.py" and line.startswith(
                ("UPSTREAM_GROUP = ", "SUPERSEDED_PREVIEW_GROUP = ")
            ):
                continue
            if relative == "tests/consumer/native_consumer_carriage.py":
                for archived_path in ARCHIVED_CARRIAGE_METADATA:
                    line = line.replace(archived_path, "")
            if OLD_IDENTITY.search(line.replace(r"\.", ".")):
                errors.append(f"{relative}:{number}: superseded identity")
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Identity audit: {checked} active source/configuration files, {len(errors)} findings")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
