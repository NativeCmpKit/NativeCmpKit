"""Offline source-remote safety checks; no Git/GitHub mutation or network calls."""
import unittest
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import call, patch

import verify_migration as module


class VerificationActionsPolicyTests(unittest.TestCase):
    def setUp(self):
        self.actions = {"enabled": True, "allowed_actions": "selected", "sha_pinning_required": True}
        self.token = {"default_workflow_permissions": "read", "can_approve_pull_request_reviews": False}
        self.pin = "actions/checkout@" + "a" * 40
        self.required = {self.pin}
        self.selected = {"github_owned_allowed": False, "verified_allowed": False, "patterns_allowed": [self.pin]}
        self.workflow = """name: verification
on:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  checks:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v6
        with:
          persist-credentials: false
      - run: python3 scripts/audit/validate_audit.py
"""

    def test_explicit_owner_settings_pass(self):
        self.assertTrue(module.approved_actions_configuration(self.actions, self.token, self.selected, self.required))

    def test_disabled_unrestricted_or_unpinned_policy_is_rejected(self):
        for name, value in (("enabled", False), ("allowed_actions", "all"),
                            ("allowed_actions", "local_only"), ("sha_pinning_required", False)):
            with self.subTest(name=name, value=value):
                self.assertFalse(module.approved_actions_configuration(
                    {**self.actions, name: value}, self.token, self.selected, self.required))

    def test_missing_or_wrong_typed_api_settings_fail_closed(self):
        for name in self.actions:
            with self.subTest(name=name):
                self.assertFalse(module.approved_actions_configuration(
                    {key: value for key, value in self.actions.items() if key != name}, self.token, self.selected, self.required))
        for name, value in (("enabled", "true"), ("enabled", 1),
                            ("sha_pinning_required", "true"), ("sha_pinning_required", 1)):
            with self.subTest(name=name, value=value):
                self.assertFalse(module.approved_actions_configuration(
                    {**self.actions, name: value}, self.token, self.selected, self.required))
        for name in self.token:
            self.assertFalse(module.approved_actions_configuration(
                self.actions, {key: value for key, value in self.token.items() if key != name}, self.selected, self.required))

    def test_write_default_or_pull_request_approval_is_rejected(self):
        for name, value in (("default_workflow_permissions", "write"),
                            ("can_approve_pull_request_reviews", True),
                            ("can_approve_pull_request_reviews", "false")):
            self.assertFalse(module.approved_actions_configuration(
                self.actions, {**self.token, name: value}, self.selected, self.required))

    def test_selected_allowlist_must_match_every_required_pin_exactly(self):
        for name, value in (("github_owned_allowed", True), ("verified_allowed", True),
                            ("verified_allowed", 0), ("patterns_allowed", []),
                            ("patterns_allowed", [self.pin, self.pin]),
                            ("patterns_allowed", [self.pin, "owner/action@" + "b" * 40]),
                            ("patterns_allowed", [self.pin, "actions/*"]),
                            ("patterns_allowed", [None])):
            with self.subTest(name=name, value=value):
                self.assertFalse(module.approved_actions_configuration(
                    self.actions, self.token, {**self.selected, name: value}, self.required))

    def test_pinned_action_and_checkout_local_references_are_accepted(self):
        for reference in (self.pin, "gradle/actions/setup-gradle@" + "a" * 40,
                          "owner/repository/.github/workflows/check.yml@" + "a" * 40,
                          "./.github/actions/verify", "docker://alpine@sha256:" + "a" * 64):
            with self.subTest(reference=reference):
                self.assertTrue(module.pinned_action_reference(reference))

    def test_mutable_missing_or_interpolated_action_references_are_rejected(self):
        for reference in ("actions/checkout", "actions/checkout@", "${{ inputs.action }}",
                          "./../outside", "docker://alpine", "docker://alpine:3.22", "actions/checkout@v6",
                          "owner/action@main", "owner/action@release/v2", "owner/action@aabbcc", "owner/action@v1\nother", ""):
            with self.subTest(reference=reference):
                self.assertFalse(module.pinned_action_reference(reference))

    def test_read_only_tag_based_workflow_is_allowed(self):
        self.assertTrue(module.read_only_verification_workflow(self.workflow))

    def test_write_scopes_cannot_hide_in_job_or_inline_permissions(self):
        for scope in ("contents", "packages", "pages", "id-token", "deployments", "issues", "pull-requests"):
            for permission in (f"    permissions:\n      {scope}: write\n", f'    permissions: {{"{scope}": "write"}}\n'):
                with self.subTest(scope=scope, permission=permission):
                    self.assertFalse(module.read_only_verification_workflow(self.workflow + permission))
        self.assertFalse(module.read_only_verification_workflow(self.workflow + "    permissions: write-all\n"))

    def test_missing_explicit_read_only_default_does_not_pass(self):
        self.assertFalse(module.read_only_verification_workflow(self.workflow.replace("permissions:\n  contents: read\n", "")))
        self.assertFalse(module.read_only_verification_workflow(self.workflow.replace("permissions:\n  contents: read\n", "# permissions:\n#   contents: read\n")))

    def test_known_publication_deployment_and_privileged_triggers_are_rejected(self):
        for command in ("./gradlew publishAndReleaseToMavenCentral", "mkdocs gh-deploy", "cargo publish",
                        "npm publish", "gh release create preview", "gh api --method POST repos/x/y/deployments"):
            with self.subTest(command=command):
                self.assertFalse(module.read_only_verification_workflow(self.workflow + "      - run: " + command + "\n"))
        for action in ("actions/deploy-pages@v4", "nwtgck/actions-netlify@v3"):
            self.assertFalse(module.read_only_verification_workflow(self.workflow + "      - uses: " + action + "\n"))
        for event in ("pull_request_target", "workflow_run"):
            self.assertFalse(module.read_only_verification_workflow(self.workflow.replace("workflow_dispatch:", event + ":")))

    def test_in_progress_approved_run_is_not_a_control_policy_failure(self):
        run = {"path": ".github/workflows/gradle.yml", "event": "workflow_dispatch", "status": "in_progress"}
        self.assertTrue(module.approved_verification_run(run))
        for status in ("queued", "completed", "waiting", "pending", "requested"):
            self.assertTrue(module.approved_verification_run({**run, "status": status}))
        self.assertFalse(module.approved_verification_run({**run, "status": "unknown"}))

    def test_unreviewed_workflow_or_event_remains_rejected(self):
        run = {"path": ".github/workflows/gradle.yml", "event": "workflow_dispatch", "status": "completed"}
        self.assertFalse(module.approved_verification_run({**run, "path": ".github/workflows/deploy.yml"}))
        self.assertFalse(module.approved_verification_run({**run, "event": "pull_request_target"}))
        self.assertFalse(module.approved_verification_run({**run, "event": "push"}))

    def test_dependency_push_registration_is_limited_to_its_development_branch(self):
        run = {"path": ".github/workflows/javafx-library-candidate.yml", "event": "push", "status": "completed",
               "head_branch": "development/preview-hardening"}
        self.assertTrue(module.approved_verification_run(run))
        self.assertFalse(module.approved_verification_run({**run, "head_branch": "main"}))

    def test_preview_release_requires_exact_record_and_preserved_tag(self):
        release = module.PUBLISHED_KIRA_PREVIEW
        tag = "refs/tags/" + release["tag_name"]
        refs = {tag: module.KIRA_PREVIEW_DEPLOYMENT["sha"]}
        self.assertTrue(module.matches_kira_preview([release], refs))
        self.assertFalse(module.matches_kira_preview([release, {"id": 1}], refs))
        self.assertFalse(module.matches_kira_preview([{**release, "prerelease": False}], refs))
        self.assertFalse(module.matches_kira_preview([release], {tag: "a" * 40}))


class HistoricalRefCustodyTests(unittest.TestCase):
    branch, tip, archive = "refs/heads/imported-feature", "a" * 40, "b" * 40

    def index(self, *, scope="origin", ref=None, tip=None):
        return {"schema_version": 1, "repository": module.DESTINATION, "entries": [{
            "scope": scope, "ref": ref or self.branch, "tip": tip or self.tip,
            "purpose": "Original branch", "recovery": "git branch restored <tip>",
        }]}

    def test_published_ref_is_checked_directly(self):
        result = module.historical_ref_custody({self.branch: self.tip}, {self.branch: self.tip})
        self.assertEqual(result["preserved"], 1)
        self.assertEqual(result["indexed_in_archive"], [])

    def test_index_and_git_ancestry_are_both_required_for_a_retired_ref(self):
        remote = {module.ARCHIVE_BRANCH: self.archive}
        for exit_code in (0, 1, 128):
            with self.subTest(exit_code=exit_code), \
                 patch.object(module, "command", return_value=json.dumps(self.index())) as git, \
                 patch.object(module.subprocess, "run", return_value=subprocess.CompletedProcess([], exit_code)) as ancestry:
                result = module.historical_ref_custody({self.branch: self.tip}, remote)
                git.assert_any_call("git", "show", self.archive + ":" + module.ARCHIVE_INDEX)
                ancestry.assert_called_once_with(["git", "merge-base", "--is-ancestor", self.tip, self.archive],
                                                 cwd=module.ROOT, capture_output=True)
                self.assertEqual(result["indexed_in_archive"], [self.branch] if exit_code == 0 else [])
                self.assertEqual(result["missing_refs"], [] if exit_code == 0 else [self.branch])

    def test_an_archive_cannot_hide_a_moved_remote_branch(self):
        remote = {module.ARCHIVE_BRANCH: self.archive, self.branch: "c" * 40}
        with patch.object(module, "command") as git:
            result = module.historical_ref_custody({self.branch: self.tip}, remote)
        git.assert_not_called()
        self.assertEqual(result["changed_refs"], [self.branch])

    def test_tags_and_the_protected_pages_head_require_their_live_refs(self):
        expected = {"refs/tags/v1": self.tip, module.PAGES_BRANCH: self.tip}
        with patch.object(module, "command") as git:
            result = module.historical_ref_custody(expected, {module.ARCHIVE_BRANCH: self.archive})
        git.assert_not_called()
        self.assertEqual(result["missing_refs"], list(expected))

    def test_local_only_rows_and_duplicate_or_malformed_archive_records(self):
        self.assertEqual(module.archived_origin_heads(self.index(scope="local")), {})
        duplicate = self.index()
        duplicate["entries"] *= 2
        for index in (duplicate, self.index(ref="refs/tags/v1"), self.index(tip="no-sha"),
                      self.index(ref=module.PAGES_BRANCH), {**self.index(), "schema_version": True}):
            with self.subTest(index=index), self.assertRaises(ValueError):
                module.archived_origin_heads(index)


class PagesResolutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        names = ["pages.json", "public-http-checks.json", "gh-pages.json"]
        for name in names:
            (self.root / name).write_text("{}\n")
        self.receipt = {
            "repository": "Apdelrahman1911/nativeCmpkit", "verified": True,
            "owner_reported_unpublish_complete": True,
            "checks": dict.fromkeys(["correct_independent_repository", "pages_endpoint_accessible",
                "no_current_pages_build", "legacy_publishing_disabled", "published_routes_return_404",
                "preserved_historical_branch", "actions_disabled_at_observation"], True),
            "evidence_sha256": {name: module.digest(self.root / name) for name in names},
        }

    def evaluate(self, current=None):
        path = self.root / "verification.json"
        path.write_text(json.dumps(self.receipt))
        incident = {"resolution": {"verified": True, "receipt": path.name,
                                   "receipt_sha256": module.digest(path)}}
        with patch.object(module, "ROOT", self.root):
            return module.verified_pages_resolution(incident, {"status": None} if current is None else current)

    def test_hashed_complete_receipt_and_null_current_status_pass(self):
        self.assertTrue(self.evaluate())

    def test_new_build_or_missing_status_is_not_unpublished(self):
        self.assertFalse(self.evaluate({"status": "built"}))
        self.assertFalse(self.evaluate({}))

    def test_unresolved_migration_snapshot_is_not_assumed_complete(self):
        self.assertFalse(module.verified_pages_resolution({}, {"status": None}))

    def test_missing_owner_confirmation_fails(self):
        self.receipt["owner_reported_unpublish_complete"] = False
        self.assertFalse(self.evaluate())

    def test_false_or_missing_required_check_fails(self):
        self.receipt["checks"]["published_routes_return_404"] = False
        self.assertFalse(self.evaluate())
        del self.receipt["checks"]["published_routes_return_404"]
        self.assertFalse(self.evaluate())

    def test_changed_evidence_is_not_accepted(self):
        (self.root / "pages.json").write_text('{"status":"built"}')
        self.assertFalse(self.evaluate())

    def test_missing_evidence_hash_is_not_accepted(self):
        del self.receipt["evidence_sha256"]["public-http-checks.json"]
        self.assertFalse(self.evaluate())

    def test_path_escape_rejected(self):
        self.receipt["evidence_sha256"]["../outside.json"] = "0" * 64
        with self.assertRaises(ValueError):
            self.evaluate()


class UpstreamPushSafetyTests(unittest.TestCase):
    def test_fresh_clone_without_upstream_passes_without_url_lookup(self):
        with patch.object(module, "command", return_value="origin\n") as command:
            safe, detail = module.upstream_push_safety()
        self.assertTrue(safe)
        self.assertIn("No local upstream", detail)
        command.assert_called_once_with("git", "remote")

    def test_existing_explicit_interlock_passes(self):
        with patch.object(module, "command", side_effect=["origin\nupstream\n", "DISABLED_READ_ONLY_UPSTREAM\n"]) as command:
            safe, detail = module.upstream_push_safety()
        self.assertTrue(safe)
        self.assertIn("Every configured upstream push URL is disabled", detail)
        self.assertEqual(command.call_args_list, [call("git", "remote"), call("git", "remote", "get-url", "--push", "--all", "upstream")])

    def test_second_unsafe_push_url_is_not_hidden_by_first_interlock(self):
        url = "https://example.invalid/source.git"
        with patch.object(module, "command", side_effect=["origin\nupstream\n", "DISABLED_READ_ONLY_UPSTREAM\n" + url + "\n"]):
            safe, detail = module.upstream_push_safety()
        self.assertFalse(safe)
        self.assertNotIn(url, detail)

    def test_multiple_interlocked_push_urls_pass(self):
        with patch.object(module, "command", side_effect=["upstream\n", "DISABLED_READ_ONLY_UPSTREAM\nDISABLED_READ_ONLY_UPSTREAM\n"]):
            safe, _ = module.upstream_push_safety()
        self.assertTrue(safe)

    def test_empty_push_url_list_does_not_vacuously_pass(self):
        with patch.object(module, "command", side_effect=["upstream\n", ""]):
            safe, _ = module.upstream_push_safety()
        self.assertFalse(safe)

    def test_configured_unsafe_upstream_fails_without_echoing_url(self):
        url = "https://example.invalid/source.git"
        with patch.object(module, "command", side_effect=["upstream\norigin\n", url + "\n"]):
            safe, detail = module.upstream_push_safety()
        self.assertFalse(safe)
        self.assertNotIn(url, detail)
        self.assertIn("URL omitted", detail)

    def test_lookup_failure_is_not_silently_accepted(self):
        with patch.object(module, "command", side_effect=["origin\nupstream\n", RuntimeError("lookup failed")]):
            with self.assertRaisesRegex(RuntimeError, "lookup failed"):
                module.upstream_push_safety()


if __name__ == "__main__":
    unittest.main()
