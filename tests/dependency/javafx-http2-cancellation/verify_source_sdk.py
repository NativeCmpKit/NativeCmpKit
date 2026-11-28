#!/usr/bin/env python3
"""Prepare the pinned full-source SDK and test its unmodified runtime classpath."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

from probe_runner import CASES, HERE, case_results, compare_patch, document, need, patch_source


LOCK = HERE / "source-sdk-lock.json"
LOADER = "modules/javafx.web/src/main/java/com/sun/webkit/network/HTTP2Loader.java"
PATCH = HERE / "cancel-response-future.patch"
WRAPPER = "gradle/wrapper/gradle-wrapper.properties"


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
    command = ["timeout", "--kill-after=5s", "120s", "xvfb-run", "-a", "java", "--module-path", str(sdk),
               "--add-modules", "javafx.controls,javafx.web,jdk.management", "-cp", str(classes), class_name, *options]
    started = time.monotonic()
    stdout_file = output / f"{evidence_name}.stdout"
    with stdout_file.open("xb") as stdout, (output / f"{evidence_name}.stderr").open("xb") as stderr:
        result = subprocess.run(command, cwd=output, stdout=stdout, stderr=stderr)
    write_json(output / f"{evidence_name}-execution.json", {
        "argv": command, "exit_code": result.returncode, "elapsed_seconds": time.monotonic() - started,
        "repository_revision": os.environ.get("GITHUB_SHA"),
    })
    result.check_returncode()
    return stdout_file.read_text(encoding="utf-8")


def verify_sdk(source, output, lock):
    source_identity(source, lock, patched=True)
    verify_materials(output, lock)
    sdk = source / "build/sdk/lib"
    modules = ["javafx.base", "javafx.controls", "javafx.graphics", "javafx.media", "javafx.web"]
    binaries = sorted(path for path in sdk.iterdir() if path.suffix in {".jar", ".so"})
    need(all((sdk / f"{module}.jar").is_file() for module in modules), "SDK modules missing")
    need((sdk / "libjfxwebkit.so").is_file(), "The upstream build emitted no native WebKit library")
    native_arch = subprocess.check_output(["readelf", "-h", str(sdk / "libjfxwebkit.so")], timeout=10, text=True)
    need("Advanced Micro Devices X86-64" in native_arch, "Expected a Linux x86-64 WebKit library")
    native_inventory = subprocess.check_output(["readelf", "-h", "-d", *(str(path) for path in binaries
                                                        if path.suffix == ".so")], timeout=60, text=True)
    bytecode = subprocess.check_output(["javap", "-p", "-c", "-classpath", str(sdk / "javafx.web.jar"),
                                        "com.sun.webkit.network.HTTP2Loader"], timeout=15, text=True)
    cancel_method = bytecode.split("public void fwkCancel();", 1)[1].split("private void callBackIfNotCanceled", 1)[0]
    need("java/util/concurrent/CompletableFuture.cancel:(Z)Z" in cancel_method, "Source change absent from SDK")
    before = {path.name: sha256(path) for path in binaries}
    write_json(output / "sdk-binaries.json", before)
    (output / "webkit-elf.txt").write_text(native_arch, encoding="utf-8")
    (output / "native-elf-inventory.txt").write_text(native_inventory, encoding="utf-8")
    (output / "loader-cancellation.txt").write_text(cancel_method, encoding="utf-8")

    classes = output / "probe-classes"
    classes.mkdir()
    subprocess.run(["javac", "--module-path", str(sdk), "--add-modules", "javafx.controls,javafx.web,jdk.management",
                    "-d", str(classes), str(HERE / "JavaFxPublicCancellationProbe.java"),
                    str(HERE / "JavaFxCancellationLifecycleProbe.java")], check=True, timeout=60)
    stdout = run_probe(sdk, classes, output, "probe", "JavaFxPublicCancellationProbe", ",".join(CASES))
    write_json(output / "case-results.json", case_results(stdout, list(CASES)))
    stdout = run_probe(sdk, classes, output, "lifecycle", "JavaFxCancellationLifecycleProbe")
    summaries = [line for line in stdout.splitlines() if line.startswith('{"replacementNavigation":')]
    need(len(summaries) == 1, "Expected one lifecycle summary")
    lifecycle = document(summaries[0])
    need(lifecycle["replacementNavigation"] is True and lifecycle["detachAfterCancel"] is True
         and lifecycle["repeatPeerEofs"] == 16 and lifecycle["worstCancelNanos"] > 0
         and 0 < lifecycle["openDescriptorsAfter"] <= lifecycle["openDescriptorsBefore"] + 4,
         "Incomplete lifecycle or socket resource observations")
    write_json(output / "lifecycle-results.json", lifecycle)
    need(before == {path.name: sha256(path) for path in binaries}, "SDK binaries changed during execution")
    source_identity(source, lock, patched=True)
    verify_materials(output, lock)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["prepare", "verify"])
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--materials", type=Path, help="Verify pre-fetched copies of the pinned build materials")
    options = parser.parse_args()
    checkout, evidence = options.source.resolve(strict=True), options.output.absolute()
    pin = json.loads(LOCK.read_text(encoding="utf-8"))
    if options.operation == "prepare":
        prepare(checkout, evidence, pin, options.materials)
    else:
        verify_sdk(checkout, evidence, pin)
