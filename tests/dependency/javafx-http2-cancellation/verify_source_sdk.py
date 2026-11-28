#!/usr/bin/env python3
"""Prepare the pinned full-source SDK and test its unmodified runtime classpath."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import time
from zipfile import ZipFile

from probe_runner import CASES, HERE, case_results, compare_patch, document, need, patch_source


LOCK = HERE / "source-sdk-lock.json"
LOADER = "modules/javafx.web/src/main/java/com/sun/webkit/network/HTTP2Loader.java"
PATCH = HERE / "cancel-response-future.patch"
WRAPPER = "gradle/wrapper/gradle-wrapper.properties"
CONSUMER_VERSION = "21.0.13.1-nativecmpkit-verification.1"
CONSUMER_MODULES = ("base", "graphics", "controls", "media", "web", "swing")
CLASSIFIERS = {
    ("linux", "x64"): ("linux", "linux"), ("linux", "arm64"): ("linux", "linux-aarch64"),
    ("macos", "x64"): ("mac", "mac"), ("macos", "arm64"): ("mac", "mac-aarch64"),
    ("windows", "x64"): ("win", "win"),
}


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write_json(path, data):
    with path.open("x", encoding="utf-8") as file:
        json.dump(data, file, indent=2, sort_keys=True)
        file.write("\n")


def git(source, *args):
    return subprocess.check_output(["git", "-C", str(source), *args], timeout=120)


def source_identity(source, lock, *, patched):
    for ref, expected in (("HEAD", lock["revision"]), ("HEAD^{tree}", lock["tree"]),
                          (f"refs/tags/{lock['tag']}", lock["tag_object"]),
                          (f"refs/tags/{lock['tag']}^{{commit}}", lock["revision"])):
        need(git(source, "rev-parse", "--verify", ref).decode().strip() == expected, f"Unexpected source {ref}")
    status = git(source, "status", "--porcelain", "--untracked-files=no").decode().splitlines()
    need(status == ([f" M {LOADER}"] if patched else []), "Unexpected OpenJFX source changes")
    need(sha256(source / WRAPPER) == lock["gradle_wrapper_properties_sha256"], "Wrapper properties differ")
    need(sha256(PATCH) == lock["patch_sha256"], "Cancellation patch differs")
    original = git(source, "show", f"HEAD:{LOADER}")
    need(hashlib.sha256(original).hexdigest() == lock["loader_sha256"], "Pinned upstream loader differs")
    changed = patch_source(original)
    compare_patch(original, changed)
    need((source / LOADER).read_bytes() == (changed if patched else original), "Working loader differs")


def material_path(output, row):
    return output / ("ivy" if row["ivy_input"] else "sources") / row["file"]


def verify_materials(output, lock):
    for row in lock["materials"]:
        file = material_path(output, row)
        need(file.stat().st_size == row["bytes"] and sha256(file) == row["sha256"],
             f"Source build material differs: {file.name}")


def prepare(source, output, lock, materials):
    source_identity(source, lock, patched=False)
    output.mkdir(parents=True)
    for folder in ("ivy", "sources"):
        (output / folder).mkdir()
    for row in lock["materials"]:
        file = material_path(output, row)
        if materials:
            shutil.copyfile(materials / file.name, file)
        else:
            subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location",
                            "--proto", "=https", "--proto-redir", "=https", "--retry", "2",
                            "--max-time", "100", "--max-filesize", str(row["bytes"]),
                            "--output", str(file), row["url"]], check=True, timeout=240)
    verify_materials(output, lock)
    subprocess.run(["git", "-C", str(source), "apply", "--check", "--", str(PATCH)], check=True)
    subprocess.run(["git", "-C", str(source), "apply", "--", str(PATCH)], check=True)
    source_identity(source, lock, patched=True)

    # A Git tree inventory holds every byte via its blob ID, including legal and build sources.
    full_manifest = git(source, "ls-tree", "-r", "HEAD")
    rows = full_manifest.splitlines()
    native_counts = {}
    for module in ("web", "media", "graphics"):
        prefix = f"modules/javafx.{module}/src/main/native".encode()
        native_counts[module] = sum(row.split(b"\t", 1)[1].startswith(prefix) for row in rows)
    need(all(native_counts.values()), "Upstream native source trees are incomplete")
    (output / "source-tree.tsv").write_bytes(full_manifest)
    write_json(output / "source.json", {
        "repository": lock["repository"], "tag": lock["tag"], "tag_object": lock["tag_object"],
        "revision": lock["revision"], "tree": lock["tree"], "native_source_entries": native_counts,
        "tree_entries": len(rows), "manifest_sha256": sha256(output / "source-tree.tsv"),
        "patch_sha256": lock["patch_sha256"], "loader_sha256": sha256(source / LOADER),
        "materials": lock["materials"], "check": "full Git tree identity and one reproducible source patch",
        "production_qualified": False,
    })


def run_probe(sdk, classes, output, evidence_name, class_name, *options):
    command = ["java", "--module-path", str(sdk),
               "--add-modules", "javafx.controls,javafx.web,jdk.management", "-cp", str(classes), class_name, *options]
    if platform.system() == "Linux":
        command = ["timeout", "--kill-after=5s", "120s", "xvfb-run", "-a", *command]
    started = time.monotonic()
    stdout_file = output / f"{evidence_name}.stdout"
    status, timed_out = None, False
    with stdout_file.open("xb") as stdout, (output / f"{evidence_name}.stderr").open("xb") as stderr:
        try:
            result = subprocess.run(command, cwd=output, stdout=stdout, stderr=stderr, timeout=130)
            status = result.returncode
            timed_out = platform.system() == "Linux" and status == 124
            result.check_returncode()
        except subprocess.TimeoutExpired:
            timed_out = True
            raise
        finally:
            write_json(output / f"{evidence_name}-execution.json", {
                "argv": command, "exit_code": status, "timed_out": timed_out,
                "elapsed_seconds": time.monotonic() - started,
                "repository_revision": os.environ.get("GITHUB_SHA"),
            })
    return stdout_file.read_text(encoding="utf-8")


def linux_binary_inventory(sdk, binaries, architecture):
    expected_cpu, elf_machine = {"x64": ("x86_64", "Advanced Micro Devices X86-64"),
                                 "arm64": ("aarch64", "AArch64")}[architecture]
    need(platform.system() == "Linux" and platform.machine() == expected_cpu, "Linux runtime architecture differs")
    need((sdk / "libjfxwebkit.so").is_file(), "The upstream build emitted no native WebKit library")
    native_files = [str(path) for path in binaries if path.suffix == ".so"]
    inventory = subprocess.check_output(["readelf", "-h", "-d", "--version-info", *native_files],
                                        timeout=60, text=True)
    rows = [line for line in inventory.splitlines() if line.strip().startswith("Machine:")]
    need(len(rows) == len(native_files) and all(elf_machine in line for line in rows),
         "An SDK native library uses the wrong architecture")
    return inventory


def macos_binary_inventory(sdk, binaries, architecture):
    expected_cpu = {"x64": "x86_64", "arm64": "arm64"}[architecture]
    need(platform.system() == "Darwin" and platform.machine() == expected_cpu, "macOS runtime architecture differs")
    need((sdk / "libjfxwebkit.dylib").is_file(), "The upstream build emitted no native WebKit library")
    native_files = [str(path) for path in binaries if path.suffix == ".dylib"]
    for path in native_files:
        cpu = subprocess.check_output(["xcrun", "lipo", "-archs", path], timeout=15, text=True).strip()
        need(cpu == expected_cpu, "An SDK native library uses the wrong architecture")
    return subprocess.check_output(["xcrun", "otool", "-l", "-L", *native_files], timeout=60, text=True)


def windows_binary_inventory(sdk, binaries, architecture):
    need(platform.system() == "Windows" and platform.machine().lower() == "amd64" and architecture == "x64",
         "Windows runtime architecture differs")
    need((sdk / "bin/jfxwebkit.dll").is_file(), "The upstream build emitted no native WebKit library")
    native_files = [str(path) for path in binaries if path.suffix == ".dll"]
    inventory = subprocess.check_output(["llvm-readobj", "--file-headers", "--coff-imports", *native_files],
                                        timeout=60, text=True)
    rows = [line for line in inventory.splitlines() if line.strip().startswith("Machine:")]
    need(len(rows) == len(native_files) and all("IMAGE_FILE_MACHINE_AMD64" in line for line in rows),
         "An SDK native library uses the wrong architecture")
    return inventory


def stage_consumer_jars(source, output, target, architecture, sdk_hashes):
    """Stage upstream Gradle's exact modular JARs for an isolated artifact-only consumer."""
    upstream_classifier, consumer_classifier = CLASSIFIERS[target, architecture]
    publications = source / "build/publications"
    webkit = {"linux": "libjfxwebkit.so", "macos": "libjfxwebkit.dylib", "windows": "jfxwebkit.dll"}[target]
    rows = []
    for module in CONSUMER_MODULES:
        artifact = f"javafx-{module}"
        original = publications / f"javafx.{module}-{upstream_classifier}.jar"
        original_empty = publications / f"javafx.{module}.jar"
        sdk_jar = source / f"build/sdk/lib/javafx.{module}.jar"
        with ZipFile(original) as jar, ZipFile(sdk_jar) as sdk:
            leaves = [entry for entry in jar.infolist() if not entry.is_dir()]
            need(len({entry.filename for entry in leaves}) == len(leaves), "Repeated entry in generated OpenJFX JAR")
            need("module-info.class" in jar.namelist(), f"Missing module descriptor: {original.name}")
            if module == "web":
                loader = "com/sun/webkit/network/HTTP2Loader.class"
                need(jar.read(loader) == sdk.read(loader), "Maven WebView uses different cancellation code from the SDK")
            natives = [entry for entry in leaves if Path(entry.filename).suffix in {".dll", ".dylib", ".so"}]
            if module == "web":
                need([Path(entry.filename).name for entry in natives] == [webkit], "Expected the host WebKit in the Maven JAR")
            for entry in natives:
                with jar.open(entry) as native_file:
                    digest = hashlib.file_digest(native_file, "sha256").hexdigest()
                need(sdk_hashes.get(Path(entry.filename).name) == digest,
                     f"Generated native JAR payload differs from the tested SDK: {entry.filename}")
        relative = Path("org/openjfx") / artifact / CONSUMER_VERSION
        stage = output / "javafx-maven" / relative
        stage.mkdir(parents=True)
        for jar, suffix in ((original_empty, ""), (original, f"-{consumer_classifier}")):
            name = f"{artifact}-{CONSUMER_VERSION}{suffix}.jar"
            destination = stage / name
            shutil.copyfile(jar, destination)
            digest = sha256(destination)
            need(digest == sha256(jar), "Staging changed the OpenJFX modular JAR")
            rows.append({"file": (relative / name).as_posix(), "sha256": digest, "bytes": destination.stat().st_size})
    write_json(output / "javafx-consumer-jars.json", {
        "version": CONSUMER_VERSION, "classifier": consumer_classifier, "source_classifier": upstream_classifier,
        "artifacts": rows, "artifact_only_consumer": True, "production_qualified": False,
    })


def verify_sdk(source, output, lock, target, architecture):
    source_identity(source, lock, patched=True)
    verify_materials(output, lock)
    sdk = source / "build/sdk"
    module_path = sdk / "lib"
    modules = ["javafx.base", "javafx.controls", "javafx.graphics", "javafx.media", "javafx.web"]
    binaries = sorted([path for path in module_path.iterdir() if path.suffix in {".jar", ".so", ".dylib"}]
                      + (list((sdk / "bin").glob("*.dll")) if target == "windows" else []))
    need(all((module_path / f"{module}.jar").is_file() for module in modules), "SDK modules missing")
    need(all(path.name.startswith("javafx") for path in binaries if path.suffix == ".jar"),
         "A build-only dependency appeared in the SDK runtime")
    inspector, native_root = {
        "linux": (linux_binary_inventory, module_path), "macos": (macos_binary_inventory, module_path),
        "windows": (windows_binary_inventory, sdk),
    }[target]
    native_inventory = inspector(native_root, binaries, architecture)
    bytecode = subprocess.check_output(["javap", "-p", "-c", "-classpath", str(module_path / "javafx.web.jar"),
                                        "com.sun.webkit.network.HTTP2Loader"], timeout=15, text=True)
    cancel_method = bytecode.split("public void fwkCancel();", 1)[1].split("private void callBackIfNotCanceled", 1)[0]
    need("java/util/concurrent/CompletableFuture.cancel:(Z)Z" in cancel_method, "Source change absent from SDK")
    before = {path.name: sha256(path) for path in binaries}
    write_json(output / "sdk-binaries.json", before)
    (output / "native-binary-inventory.txt").write_text(native_inventory, encoding="utf-8")
    (output / "loader-cancellation.txt").write_text(cancel_method, encoding="utf-8")

    classes = output / "probe-classes"
    classes.mkdir()
    subprocess.run(["javac", "--module-path", str(module_path), "--add-modules", "javafx.controls,javafx.web,jdk.management",
                    "-d", str(classes), str(HERE / "JavaFxPublicCancellationProbe.java"),
                    str(HERE / "JavaFxCancellationLifecycleProbe.java")], check=True, timeout=60)
    stdout = run_probe(module_path, classes, output, "probe", "JavaFxPublicCancellationProbe", ",".join(CASES))
    write_json(output / "case-results.json", case_results(stdout, list(CASES)))
    stdout = run_probe(module_path, classes, output, "lifecycle", "JavaFxCancellationLifecycleProbe")
    summaries = [line for line in stdout.splitlines() if line.startswith('{"replacementNavigation":')]
    need(len(summaries) == 1, "Expected one lifecycle summary")
    lifecycle = document(summaries[0])
    need(lifecycle["replacementNavigation"] is True and lifecycle["detachAfterCancel"] is True
         and lifecycle["repeatPeerEofs"] == 16 and lifecycle["worstCancelNanos"] > 0
         and lifecycle["resourceMetric"] == ("win32-process-handles" if target == "windows" else "unix-file-descriptors")
         and 0 < lifecycle["openResourcesAfter"] <= lifecycle["openResourcesBefore"] + 4,
         "Incomplete lifecycle or socket resource observations")
    write_json(output / "lifecycle-results.json", lifecycle)
    need(before == {path.name: sha256(path) for path in binaries}, "SDK binaries changed during execution")
    source_identity(source, lock, patched=True)
    verify_materials(output, lock)
    stage_consumer_jars(source, output, target, architecture, before)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["prepare", "verify"])
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--arch", choices=["x64", "arm64"], default="x64")
    parser.add_argument("--platform", choices=["linux", "macos", "windows"], default="linux")
    parser.add_argument("--materials", type=Path, help="Verify pre-fetched copies of the pinned build materials")
    options = parser.parse_args()
    checkout, evidence = options.source.resolve(strict=True), options.output.absolute()
    pin = json.loads(LOCK.read_text(encoding="utf-8"))
    pin["materials"] = [item for item in pin["materials"] if item.get("platform", options.platform) == options.platform]
    if options.operation == "prepare":
        prepare(checkout, evidence, pin, options.materials)
    else:
        verify_sdk(checkout, evidence, pin, options.platform, options.arch)
