#!/usr/bin/env python3
"""Print the read-only NativeCmpKit publication plan for an exact release tag."""
import argparse
import json
from pathlib import Path
import re
import subprocess

from verify_migration import DESTINATION, ROOT

MAVEN_GROUP = "io.github.apdelrahman1911.nativecmpkit"
TAG_REF = re.compile(r"refs/tags/v((?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*)){2}(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?)")
PROJECT_NAME = re.compile(r"nativecmpkit-[a-z]+(?:-[a-z0-9]+)*")


def publication_roots(root):
    manifest = json.loads((root / "docs/migration/current-identity.json").read_text(encoding="utf-8"))
    if manifest["github_repository"] != DESTINATION or manifest["maven_group"] != MAVEN_GROUP:
        raise ValueError("The manifest must target the NativeCmpKit repository and Maven group")
    names = set()
    paths = set()
    settings = (root / "settings.gradle.kts").read_text(encoding="utf-8")
    renamed_projects = dict(re.findall(r'^project\("([^"]+)"\)\.name = "([^"]+)"$', settings, re.M))
    for module in manifest["modules"]:
        name = module["new_artifact"]
        source = Path(module["source_directory"])
        original_project = ":" + ":".join(source.parts)
        parent, _, local_name = original_project.rpartition(":")
        project = parent + ":" + renamed_projects.get(original_project, local_name)
        if (not PROJECT_NAME.fullmatch(name) or source.is_absolute() or ".." in source.parts or
                not source.parts or not PROJECT_NAME.fullmatch(source.parts[0]) or
                module["new_group"] != MAVEN_GROUP or module["gradle_project"] != project or
                project.rsplit(":", 1)[-1] != name or
                name in names or source in paths):
            raise ValueError("Invalid or duplicate NativeCmpKit publication root")
        names.add(name)
        paths.add(source)
    build_files = {file for project in root.glob("nativecmpkit-*") if project.is_dir()
                   for pattern in ("build.gradle.kts", "*/build.gradle.kts") for file in project.glob(pattern)}
    configured = {file.parent.relative_to(root) for file in build_files
                  if 'id("module.publication")' in file.read_text(encoding="utf-8")}
    if not configured or configured != paths:
        raise ValueError("The identity manifest and configured publication roots differ")
    return [f"{MAVEN_GROUP}:{name}" for name in sorted(names)]


def tag_version(ref):
    match = TAG_REF.fullmatch(ref)
    if match is None or match[1].upper().endswith("-SNAPSHOT"):
        raise ValueError("An exact non-snapshot vMAJOR.MINOR.PATCH release tag is required")
    return match[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", required=True)
    args = parser.parse_args()
    version = tag_version(args.ref)
    head, tagged = subprocess.check_output(
        ["git", "rev-parse", "--verify", "HEAD"], cwd=ROOT, text=True
    ).strip(), subprocess.check_output(
        ["git", "rev-parse", "--verify", args.ref + "^{commit}"], cwd=ROOT, text=True
    ).strip()
    if head != tagged:
        raise ValueError("The tag must identify the checked-out revision")
    print(json.dumps({"repository": DESTINATION, "version": version, "revision": head,
                      "publication_roots": publication_roots(ROOT), "publication_enabled": False}, indent=2))


if __name__ == "__main__":
    main()
