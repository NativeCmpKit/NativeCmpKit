#!/usr/bin/env python3
"""Read-only migration verification. Network reads require --remote or --actions-policy.

Never executes archived code/attachments or modifies project refs/GitHub state.
Bundle restoration uses a temporary, disposable bare repository only.
Run from any directory; stdout is a machine-readable verification receipt.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib
from github_json import json_pages

ROOT = Path(__file__).resolve().parents[2]
SHA = re.compile(r"^[0-9a-f]{40}$")
HEX256 = re.compile(r"^[0-9a-f]{64}$")
DESTINATION = "NativeCmpKit/NativeCmpKit"
TRANSFER_SNAPSHOT = "docs/migration/upstream-updates/20261024T183300Z/destination/repository.json"
DEPENDENCY_WORKFLOWS = frozenset({".github/workflows/javafx-dependency-regression.yml",
                                 ".github/workflows/javafx-library-candidate.yml"})
VERIFICATION_WORKFLOWS = DEPENDENCY_WORKFLOWS | {
    ".github/workflows/gradle.yml", ".github/workflows/build-native-libs.yml", ".github/workflows/release.yml",
}
REMOTE_ACTION = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*@[0-9a-f]{40}")
PUBLISHED_KIRA_PREVIEW = {"id": 449677531, "tag_name": "v0.1.0-preview.1", "draft": False,
                          "prerelease": True, "published_at": "2026-11-18T08:02:22Z"}
KIRA_PREVIEW_DEPLOYMENT = {"id": 7877162495, "ref": PUBLISHED_KIRA_PREVIEW["tag_name"],
                           "sha": "6fac2815a6e3e7cdb1d1d5dd5259ac59e8663eaa", "environment": "maven-central",
                           "creator": "Apdelrahman1911", "created_at": "2026-11-18T07:38:09Z"}


def approved_actions_configuration(actions: dict, token: dict, selected: dict, required: set[str]) -> bool:
    """Check the currently authorized repository controls.

    Missing fields and truthy strings/integers are not authenticated booleans.
    This is a control observation, not action-code or release verification.
    """
    patterns = selected.get("patterns_allowed")
    return (actions.get("enabled") is True
            and actions.get("allowed_actions") == "selected"
            and actions.get("sha_pinning_required") is True
            and token.get("default_workflow_permissions") == "read"
            and token.get("can_approve_pull_request_reviews") is False
            and selected.get("github_owned_allowed") is False
            and selected.get("verified_allowed") is False
            and isinstance(patterns, list)
            and all(isinstance(pattern, str) and REMOTE_ACTION.fullmatch(pattern) for pattern in patterns)
            and len(patterns) == len(required) and set(patterns) == required)


def pinned_action_reference(reference: str) -> bool:
    """Require immutable references for dependencies outside the checkout."""
    if reference.startswith("./"):
        return bool(re.fullmatch(r"\./[A-Za-z0-9_./-]+", reference)) and all(
            part not in {"", ".", ".."} for part in reference[2:].split("/"))
    if reference.startswith("docker://"):
        return bool(re.fullmatch(r"docker://[a-z0-9][a-z0-9./_-]*@sha256:[0-9a-f]{64}", reference))
    return bool(REMOTE_ACTION.fullmatch(reference))


def read_only_verification_workflow(source: str) -> bool:
    """Lexical guard for reviewed workflows, NOT a YAML parser or shell sandbox.

    Manual source/action review remains required, including transitive behavior.
    Historical read-only workflows need not satisfy newer cache/test conventions.
    """
    text = re.sub(r"(?m)^\s*#.*$", "", source)
    explicit_default = re.search(r"(?m)^permissions:\s*\n\s+contents:\s*read\s*$", text)
    writes = re.search(r"[\w-]+[\"']?\s*:\s*[\"']?(?:write|write-all)\b", text)
    forbidden = re.search(
        r"publishAndRelease|gh-deploy|actions-netlify|actions/deploy-pages|"
        r"\bcargo\s+publish\b|\bnpm\s+publish\b|\bgh\s+release\s+create\b|"
        r"\bgh\s+api[^\n]*\bdeployments\b|\bpull_request_target\s*:|\bworkflow_run\s*:", text)
    return bool(explicit_default) and not writes and not forbidden


def approved_verification_run(run: dict) -> bool:
    """Safe entry-point observation, not a claim of completed/passing execution."""
    workflow = run.get("path")
    event = run.get("event")
    registration = (event == "push" and workflow in DEPENDENCY_WORKFLOWS
                    and run.get("head_branch") == "development/preview-hardening")
    return (workflow in VERIFICATION_WORKFLOWS and (event == "workflow_dispatch" or registration)
            and run.get("status") in {"queued", "in_progress", "completed", "waiting", "pending", "requested"})


def matches_kira_preview(releases: list[dict], remote_refs: dict[str, str]) -> bool:
    tag = "refs/tags/" + PUBLISHED_KIRA_PREVIEW["tag_name"]
    return (len(releases) == 1
            and all(releases[0].get(key) == value for key, value in PUBLISHED_KIRA_PREVIEW.items())
            and remote_refs.get(tag) == KIRA_PREVIEW_DEPLOYMENT["sha"])


def command(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"{args[0]} {args[1] if len(args)>1 else ''} failed (exit {result.returncode}): {result.stderr.strip()[:2000]}")
    return result.stdout


def verify_checkout_workflows(check) -> set[str]:
    required = set()
    for workflow in sorted((ROOT / ".github/workflows").iterdir()):
        if workflow.suffix not in {".yml", ".yaml"}:
            continue
        source = workflow.read_text()
        check("read_only_workflow_" + workflow.name, read_only_verification_workflow(source),
              "Lexical read-only/publication guard; executed source and actions still require review")
        for action in re.findall(r"(?m)^\s*(?:-\s*)?uses:\s*[\"']?([^\s\"']+)", source):
            check("pinned_action_reference_" + action, pinned_action_reference(action), {"workflow": workflow.name})
            if REMOTE_ACTION.fullmatch(action):
                required.add(action)
    return required


def verify_actions_policy(check, repo: str, required: set[str]) -> None:
    prefix = f"repos/{repo}/actions/permissions"
    actions = json.loads(command("gh", "api", prefix))
    token = json.loads(command("gh", "api", prefix + "/workflow"))
    selected = json.loads(command("gh", "api", prefix + "/selected-actions"))
    check("github_actions_owner_policy", approved_actions_configuration(actions, token, selected, required),
          {"actions": actions, "default_token": token, "selected_actions": selected,
           "required_action_pins": sorted(required)})


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_child(parent: Path, relative: str) -> Path:
    path = parent / relative
    if path.is_symlink() or not path.resolve().is_relative_to(parent.resolve()):
        raise ValueError(f"Unsafe archive path: {relative}")
    return path


def upstream_push_safety() -> tuple[bool, str]:
    """A fresh independent clone need not configure the optional source remote.

    Never include a configured URL in evidence: it could contain credentials.
    Existing upstream remotes must still have the explicit migration interlock.
    """
    if "upstream" not in command("git", "remote").splitlines():
        return True, "No local upstream remote configured; no source push URL is needed"
    push_urls = command("git", "remote", "get-url", "--push", "--all", "upstream").splitlines()
    disabled = bool(push_urls) and all(url == "DISABLED_READ_ONLY_UPSTREAM" for url in push_urls)
    return disabled, "Every configured upstream push URL is disabled" if disabled else "An upstream push URL lacks the migration interlock, or none was returned (URL omitted)"


def verified_pages_resolution(incident: dict, current_pages: dict) -> bool:
    """Accept an additive, hashed unpublishing receipt, never a mere closed issue.

    GitHub retains the Pages configuration and old deployment success after
    Unpublish site. A present configuration is therefore not itself a failure.
    The current authenticated response must still have an explicitly null status.
    """
    resolution = incident.get("resolution", {})
    if not resolution.get("verified") or "status" not in current_pages or current_pages["status"] is not None:
        return False
    path = safe_child(ROOT, resolution["receipt"])
    if digest(path) != resolution.get("receipt_sha256"):
        return False
    receipt = json.loads(path.read_text())
    required = {"correct_independent_repository", "pages_endpoint_accessible",
                "no_current_pages_build", "legacy_publishing_disabled",
                "published_routes_return_404", "preserved_historical_branch",
                "actions_disabled_at_observation"}
    checks = receipt.get("checks", {})
    if (receipt.get("repository") != "Apdelrahman1911/nativeCmpkit"
            or receipt.get("verified") is not True
            or receipt.get("owner_reported_unpublish_complete") is not True
            or not required <= checks.keys()
            or not all(checks[key] is True for key in required)):
        return False
    hashes = receipt.get("evidence_sha256", {})
    if not {"pages.json", "public-http-checks.json", "gh-pages.json"} <= hashes.keys():
        return False
    return all(digest(safe_child(path.parent, name)) == expected for name, expected in hashes.items())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--remote", action="store_true", help="Also read destination refs/settings using git and gh; no writes")
    scope.add_argument("--actions-policy", action="store_true", help="Check workflow pins and the live repository Actions policy only")
    parser.add_argument("--remote-ref", default="refs/heads/main", help="Explicit destination head to compare with this checkout (default: refs/heads/main)")
    parser.add_argument("--output", type=Path, help="Write the same receipt to this explicit output path")
    args = parser.parse_args()
    checks: list[dict] = []
    report = {"checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "remote_reads": args.remote or args.actions_policy, "checks": checks,
              "verification_script_sha256": digest(Path(__file__).resolve()),
              "required_owner_followups": [],
              "receipt_scope": "Verifies the observed checkout/remote SHA and current files, not the later commit storing this receipt."}

    def check(name, condition, detail):
        checks.append({"name": name, "passed": bool(condition), "detail": detail})
        if not condition:
            raise AssertionError(f"{name}: {detail}")

    try:
        identity = json.loads((ROOT / "docs/migration/current-identity.json").read_text())
        report["observed_checkout_sha"] = command("git", "rev-parse", "HEAD").strip()
        if args.actions_policy:
            if identity["github_repository"] != DESTINATION:
                raise ValueError("Unexpected destination repository")
            report["receipt_scope"] = "Checks workflow source in this checkout and the destination's live Actions settings."
            verify_actions_policy(check, DESTINATION, verify_checkout_workflows(check))
            report["passed"] = True
            return write_report(report, args.output)
        report["worktree_porcelain"] = command("git", "status", "--porcelain", "--", ".",
                                              ":(exclude)scripts/ci/test_javafx_ordinary_success_trace.py").splitlines()
        baseline = identity["source_baseline"]
        check("baseline_sha_shape", bool(SHA.fullmatch(baseline)), baseline)
        command("git", "cat-file", "-e", baseline + "^{commit}")
        command("git", "merge-base", "--is-ancestor", baseline, "HEAD")
        check("baseline_ancestry", True, "Original main is an ancestor of the checked-out migration branch")
        original_license = subprocess.check_output(["git", "show", baseline + ":LICENSE"], cwd=ROOT)
        check("apache_license_unchanged", (ROOT / "LICENSE").read_bytes() == original_license,
              "LICENSE is byte-identical to the upstream baseline")
        for name in ("NOTICE", "THIRD_PARTY_NOTICES.md", "AGENTS.md"):
            check("required_notice_" + name, (ROOT / name).is_file(), name)
        check("root_identity", identity.get("project") == "NativeCmpKit" and
              'rootProject.name = "NativeCmpKit"' in (ROOT / "settings.gradle.kts").read_text(),
              "Current owner-requested root Gradle/library name; archived migration identity remains historical")
        check("maven_identity", 'group = "io.github.apdelrahman1911.nativecmpkit"' in (ROOT / "build.gradle.kts").read_text(), "Prospective independent Maven group (not publication validation)")
        resource_package = "io.github.apdelrahman1911.nativecmpkit.nativecmpkit_cupertino_icons.generated.resources"
        check("resource_namespace_pinned", identity["compose_resource_package"] == resource_package and
              f'packageOfResClass = "{resource_package}"' in (ROOT / "nativecmpkit-cupertino-icons/build.gradle.kts").read_text(), resource_package)
        namespace = "io.github.apdelrahman1911.nativecmpkit"
        opt_in = (ROOT / "nativecmpkit-core/src/commonMain/kotlin" / namespace /
                  "core/ExperimentalNativeCmpKitApi.kt").read_text()
        check("public_opt_in_annotation", identity["opt_in_annotation"] == f"{namespace}.core.ExperimentalNativeCmpKitApi" and
              f"package {namespace}.core" in opt_in and "annotation class ExperimentalNativeCmpKitApi" in opt_in,
              identity["opt_in_annotation"])
        framework = identity["swift_framework"]
        sample = (ROOT / "sample/common/build.gradle.kts").read_text()
        swift = (ROOT / "sample/ios/NativeCmpKit/NativeCmpKitApp.swift").read_text()
        check("sample_framework_source_identity", framework == {"name": "NativeCmpKit", "bundle_identifier": f"{namespace}.framework"} and
              'baseName = "NativeCmpKit"' in sample and f'binaryOption("bundleId", "{namespace}.framework")' in sample and
              "import NativeCmpKit" in swift.splitlines(), "Framework name, bundle identifier and Swift import in source")
        native = identity["native_libraries"]
        check("native_library_source_inventory", set(native) == {"nativecmpkit-file-picker", "nativecmpkit-share"}, "Desktop JNI modules")
        for module, names in native.items():
            module_root = safe_child(ROOT, module)
            crate = tomllib.loads((module_root / "native/Cargo.toml").read_text())
            bridge_package, bridge_class = names["bridge"].rsplit(".", 1)
            platform = module_root / "src/desktopMain/kotlin" / bridge_package.replace(".", "/")
            loader = (platform / "NativeLibLoader.kt").read_text()
            bridge = (platform / f"{bridge_class}.kt").read_text()
            rust = (module_root / "native/src/lib.rs").read_text()
            methods = set(re.findall(r"\bexternal\s+fun\s+(\w+)\s*\(", bridge))
            exports = set(re.findall(r'pub extern "system" fn (Java_\w+)\(', rust))
            jni_prefix = "Java_" + names["bridge"].replace(".", "_") + "_"
            check("native_library_identity_" + module, names["crate"].startswith("nativecmpkit-") and
                  names["loader_name"] == names["crate"].replace("-", "_") and crate["package"]["name"] == names["crate"] and
                  names["bridge"].startswith(namespace + ".") and f"package {bridge_package}" in bridge and
                  f'LIB_NAME = "{names["loader_name"]}"' in loader and bool(methods) and
                  exports == {jni_prefix + method for method in methods}, "Cargo, loader, Kotlin and JNI source identities agree")
        check("no_git_alternates", not (ROOT / ".git/objects/info/alternates").exists(), "Local checkout does not require another clone's object store")
        check("coordinate_uniqueness", len({m['new_artifact'] for m in identity['modules']}) == len(identity['modules']), f"{len(identity['modules'])} planned artifacts; no publication implied")
        for module in identity["modules"]:
            source = safe_child(ROOT, module["source_directory"]) / "build.gradle.kts"
            check("publishable_module_" + module["new_artifact"], 'id("module.publication")' in source.read_text(), module["source_directory"])

        archive = ROOT / "docs/migration/git"
        expected = {}
        kinds = {}
        for line in (archive / "upstream-refs.txt").read_text().splitlines():
            oid, typ, ref = line.split()
            check("ref_shape_" + ref, bool(SHA.fullmatch(oid)) and ref.startswith("refs/"), typ)
            expected[ref] = oid
            kind = ref.split("/")[1]
            kinds[kind] = kinds.get(kind, 0) + 1
        advertised_bundle = archive / "upstream.bundle"
        checksum = (archive / "upstream.bundle.sha256").read_text().split()[0]
        check("git_bundle_sha256", digest(advertised_bundle) == checksum, checksum)
        bundled = {}
        for line in command("git", "bundle", "list-heads", str(advertised_bundle)).splitlines():
            oid, ref = line.split()
            bundled[ref] = oid
        check("all_advertised_refs_bundled", all(bundled.get(ref) == oid for ref, oid in expected.items()), kinds)
        command("git", "bundle", "verify", str(advertised_bundle))
        check("git_bundle_complete", True, "Git verified the self-contained advertised-ref bundle")
        command("git", "fsck", "--full", "--no-dangling")
        check("git_objects_integrity", True, "git fsck --full --no-dangling passed for local repository")

        metadata = ROOT / "docs/migration/upstream-metadata"
        sums_file = metadata / "SHA256SUMS"
        check("metadata_integrity_manifest_present", sums_file.is_file(), "SHA256SUMS required; exporter must have finished")
        seen = set()
        for line in sums_file.read_text().splitlines():
            if not line.strip():
                continue
            expected_hash, filename = line.split(maxsplit=1)
            filename = filename.lstrip("*")
            if filename.startswith("./"):
                filename = filename[2:]
            if not HEX256.fullmatch(expected_hash):
                raise ValueError("Invalid metadata checksum format")
            path = safe_child(metadata, filename)
            if not path.is_file() or digest(path) != expected_hash:
                raise AssertionError("Metadata checksum mismatch: " + filename)
            seen.add(filename)
        actual = {str(p.relative_to(metadata)) for p in metadata.rglob("*") if p.is_file() and p != sums_file}
        check("metadata_all_files_verified", actual == seen, {"hashed_files": len(seen), "unlisted": sorted(actual-seen)[:20], "missing": sorted(seen-actual)[:20]})
        for f in ("issues.json", "pull-requests.json", "issue-comments.json", "review-comments.json", "releases.json", "repository.json", "manifest.json", "validation.json", "referenced-commits.json"):
            json.loads((metadata / f).read_text())
        check("metadata_json_readable", True, "Required raw datasets and final exporter manifest parse")

        required_actions = verify_checkout_workflows(check)

        supplemental = archive / "referenced-commits.bundle"
        recovery = json.loads((archive / "referenced-commits-verification.json").read_text())
        dataset = metadata / "referenced-commits.json"
        candidates = json.loads(dataset.read_text())
        check("referenced_commit_recovery_complete", bool(recovery.get("completed_at_utc")) and recovery.get("candidate_count") == len(candidates),
              {"candidates": len(candidates), "statuses": recovery.get("statuses"), "completed_at_utc": recovery.get("completed_at_utc")})
        check("referenced_commit_dataset_hash", recovery["source_dataset_sha256"] == digest(dataset), digest(dataset))
        check("supplemental_bundle_checksum", supplemental.is_file() and digest(supplemental) == recovery["bundle_sha256"] ==
              (archive / "referenced-commits.bundle.sha256").read_text().split()[0], recovery["bundle_sha256"])
        supplemental_refs = {}
        for line in (archive / "referenced-commit-refs.txt").read_text().splitlines():
            oid, typ, ref = line.split()
            if not SHA.fullmatch(oid) or typ != "commit" or not ref.startswith("refs/archive/upstream/referenced-commits/"):
                raise ValueError("Invalid supplemental ref")
            supplemental_refs[ref] = oid
        bundled_supplemental = dict(line.split()[::-1] for line in command("git", "bundle", "list-heads", str(supplemental)).splitlines())
        check("supplemental_refs_complete", bundled_supplemental == supplemental_refs and len(supplemental_refs) == recovery["archival_refs_count"], len(supplemental_refs))
        # A check inside the existing project could accidentally satisfy missing
        # prerequisites. Restore both archives into an empty object database.
        with tempfile.TemporaryDirectory(prefix="nativecmpkit-bundle-verify-") as temp:
            command("git", "init", "--bare", temp)
            for bundle in (advertised_bundle, supplemental):
                command("git", "--git-dir=" + temp, "bundle", "verify", str(bundle))
                command("git", "--git-dir=" + temp, "fetch", "--no-write-fetch-head", str(bundle), "+refs/*:refs/*")
            restored = dict(line.split()[::-1] for line in command("git", "--git-dir=" + temp, "for-each-ref", "--format=%(objectname) %(refname)").splitlines())
            check("offline_restored_refs_identical", all(restored.get(ref) == oid for ref, oid in {**expected, **supplemental_refs}.items()), len(restored))
            missing = []
            for item in candidates:
                sha = item["sha"]
                if not SHA.fullmatch(sha): raise ValueError("Malformed candidate commit")
                result = subprocess.run(["git", "--git-dir=" + temp, "cat-file", "-t", sha], capture_output=True, text=True)
                if result.returncode or result.stdout.strip() != "commit": missing.append(sha)
            check("all_metadata_commits_restored_offline", not missing, {"candidates": len(candidates), "missing": missing})
            command("git", "--git-dir=" + temp, "fsck", "--full", "--no-dangling")
            check("offline_bundle_restore_integrity", True, {"commits": int(command("git", "--git-dir=" + temp, "rev-list", "--all", "--count")), "network_required": False})

        if args.remote:
            repo = identity["github_repository"]
            if repo != DESTINATION:
                raise ValueError("Unexpected destination repository")
            if not args.remote_ref.startswith("refs/heads/"):
                raise ValueError("--remote-ref must be an explicit refs/heads/ reference")
            command("git", "check-ref-format", args.remote_ref)
            remote = dict(line.split()[::-1] for line in command("git", "ls-remote", "--refs", f"https://github.com/{repo}.git").splitlines())
            state = json.loads(command("gh", "api", "repos/" + repo))
            check("independent_github_repository", state.get("fork") is False and state["full_name"] == repo, {"full_name": state["full_name"], "fork": state.get("fork"), "default_branch": state["default_branch"]})
            incident = json.loads((ROOT / "docs/migration/pages-incident.json").read_text())
            archive_destination = json.loads((ROOT / TRANSFER_SNAPSHOT).read_text())
            check("legacy_pages_incident_disclosed", type(state.get("id")) is int
                  and state["id"] == archive_destination["id"]
                  and incident["repository"] == archive_destination["full_name"] and incident["schema_version"] == 1,
                  {"historical_repository": archive_destination["full_name"], "repository_id": state.get("id")})
            report["pages_configuration_present"] = state.get("has_pages")
            if state.get("has_pages"):
                pages = json.loads(command("gh", "api", f"repos/{repo}/pages"))
                check("legacy_pages_publishing_disabled", pages.get("build_type") == "workflow",
                      "Legacy branch publishing is off; this does not unpublish an existing deployment")
                report["pages_unpublishing_verified"] = verified_pages_resolution(incident, pages)
                if not report["pages_unpublishing_verified"]:
                    report["required_owner_followups"].append(incident["owner_followup"])
                else:
                    check("pages_unpublishing_resolution_verified", True,
                          "Hashed owner/API/HTTP resolution evidence and current null Pages status; historical deployment/configuration retained")
            else:
                check("github_pages_configuration_removed", state.get("has_pages") is False,
                      "No Pages configuration reported; CDN/cache expiration is not tested")
                report["pages_unpublishing_verified"] = True
            verify_actions_policy(check, repo, required_actions)
            release_pages = json_pages(command("gh", "api", "--paginate", f"repos/{repo}/releases?per_page=100"))
            releases = [release for page in release_pages for release in page]
            check("only_recorded_kira_preview_release", matches_kira_preview(releases, remote),
                  {"observed_release_ids": [release["id"] for release in releases],
                   "recorded_prior_release": PUBLISHED_KIRA_PREVIEW})
            deployment_pages = json_pages(command("gh", "api", "--paginate", f"repos/{repo}/deployments?per_page=100"))
            if not all(isinstance(page, list) for page in deployment_pages):
                raise ValueError("Unexpected deployment response shape")
            deployments = [deployment for page in deployment_pages for deployment in page]
            known = {item["id"]: item for item in [*incident["disclosed_deployments"], KIRA_PREVIEW_DEPLOYMENT]}
            check("no_undisclosed_deployments", all(
                deployment["id"] in known and
                all(deployment[field] == known[deployment["id"]][field] for field in ("ref", "sha", "environment", "created_at")) and
                deployment["creator"]["login"] == known[deployment["id"]]["creator"]
                for deployment in deployments),
                {"observed_ids": [d["id"] for d in deployments], "disclosed_incident_ids": sorted(known),
                 "scope": "The historical Pages incident and the earlier Maven Central preview are both recorded"})
            branch = args.remote_ref.removeprefix("refs/heads/")
            planned_revision = report["observed_checkout_sha"]
            pages = json_pages(command("gh", "api", "--paginate", "--method", "GET", f"repos/{repo}/actions/runs", "-F", "per_page=100",
                                       "-f", f"branch={branch}", "-f", f"head_sha={planned_revision}"))
            runs = [run for page in pages for run in page["workflow_runs"]]
            report["verification_workflow_run_scope"] = {"branch": branch, "head_sha": planned_revision}
            for run in runs:
                check("approved_verification_run_" + str(run["id"]), run.get("head_sha") == planned_revision
                      and run.get("head_branch") == branch and approved_verification_run(run),
                      {k: run[k] for k in ("id", "path", "head_sha", "event", "status", "conclusion")})
                workflow = command("git", "show", planned_revision + ":" + run["path"])
                check("read_only_executed_workflow_" + str(run["id"]), read_only_verification_workflow(workflow),
                      "Approved workflow source at its executed revision; report artifacts are not releases/packages")
            report["verification_workflow_runs"] = [run["id"] for run in runs]
            report["unfinished_verification_runs"] = [run["id"] for run in runs if run["status"] != "completed"]
            report["completed_nonsuccess_verification_runs"] = [run["id"] for run in runs if run["status"] == "completed" and run["conclusion"] != "success"]
            preserved = {ref: oid for ref, oid in expected.items() if ref.startswith(("refs/heads/", "refs/tags/")) and ref != "refs/heads/main"}
            check("historical_remote_refs_identical", all(remote.get(ref) == oid for ref, oid in preserved.items()), f"{len(preserved)} non-main heads/tags are byte-identical object IDs")
            report["observed_remote_main_sha"] = remote.get("refs/heads/main")
            check("remote_ref_matches_checkout", remote.get(args.remote_ref) == report["observed_checkout_sha"],
                  {"ref": args.remote_ref, "sha": remote.get(args.remote_ref)})
            source_push_safe, source_push_detail = upstream_push_safety()
            check("source_remote_push_disabled", source_push_safe, source_push_detail)
        report["passed"] = True
    except Exception as exc:
        report["passed"] = False
        report["error"] = str(exc)
    return write_report(report, args.output)


def write_report(report: dict, output_path: Path | None) -> int:
    output = json.dumps(report, indent=2) + "\n"
    if output_path:
        output_path.write_text(output)
    sys.stdout.write(output)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
