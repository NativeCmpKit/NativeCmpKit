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
    "tests/consumer/jvm_abi.py",
    "tests/consumer/test_jvm_abi.py",
}
HISTORICAL_REJECTION_FIXTURES = {
    "scripts/ci/core_io_consumer.py",
    "tests/consumer/build.gradle.kts",
    "tests/consumer/io-desktop/build.gradle.kts",
    "tests/consumer/webview-desktop/build.gradle.kts",
    "tests/consumer/verify_artifacts.py",
}
ANDROID_PACKAGE_FIXTURE = "nativecmpkit-webview/src/androidHostTest/kotlin/android/webkit/NativeCmpKitControlledResourceError.kt"
ACTIVE_ROOTS = {"sample", "scripts", "tests", "tools", "gradle", "convention-plugins", ".github"}
ACTIVE_DOCS = {"README.md", "CONTRIBUTING.md", "NOTICE", "THIRD_PARTY_NOTICES.md", "docs/index.md",
               "docs/testing/nativecmpkit-webview-content-policy-focuses.json"}
SOURCE_SUFFIXES = {".kt", ".kts", ".java", ".rs", ".swift", ".c", ".cc", ".cpp", ".h", ".mm", ".js", ".mjs", ".cjs"}
CONFIG_SUFFIXES = {".py", ".toml", ".lock", ".yaml", ".yml", ".json", ".properties", ".xml", ".plist",
                   ".pbxproj", ".sh", ".bat", ".html", ".css", ".pro", ".def", ".gradle", ".xcconfig"}
# Avoid treating longer ordinary words as names when matching camel-case symbols.
OLD_IDENTITY = re.compile(
    r"com[./_]mohamedrejeb[./_](?:calf|nativecmpkit)\b|\b(?i:calf)[-_]|\b(?:Experimental)?Calf[A-Z]|\bcalf[A-Z]"
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
        if re.match(r"(?i)^calf-", root):
            errors.append(f"{relative}: legacy module path")
            continue
        if relative == "scripts/development/verify_namespace.py" or relative in ARCHIVE_TOOLS:
            continue
        if relative.startswith(("tests/consumer/binary/", "scripts/ci/fixtures/")):
            continue
        if not (root in ACTIVE_ROOTS or root.startswith("nativecmpkit-") or len(path.parts) == 1 or relative in ACTIVE_DOCS):
            continue
        if path.suffix not in SOURCE_SUFFIXES | CONFIG_SUFFIXES and relative not in ACTIVE_DOCS:
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
            if relative in HISTORICAL_REJECTION_FIXTURES and "Calf" in line and "!=" in line:
                continue
            if relative == "tests/consumer/verify_artifacts.py" and line.startswith("UPSTREAM_GROUP = "):
                continue
            if OLD_IDENTITY.search(line.replace(r"\.", ".")):
                errors.append(f"{relative}:{number}: superseded identity")
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Identity audit: {checked} active source/configuration files, {len(errors)} findings")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
