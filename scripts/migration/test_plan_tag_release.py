import json
from pathlib import Path
import tempfile
import unittest

from plan_tag_release import MAVEN_GROUP, ROOT, publication_roots, tag_version


class TagPreflightTests(unittest.TestCase):
    def test_current_roots_match_the_in_scope_gradle_publications(self):
        roots = publication_roots(ROOT)
        self.assertEqual(21, len(roots))
        for module in ("core", "file-picker", "permissions-location", "share", "webview"):
            self.assertIn(f"{MAVEN_GROUP}:nativecmpkit-{module}", roots)
        for module in ("geo", "maps", "navigation"):
            self.assertNotIn(f"{MAVEN_GROUP}:nativecmpkit-{module}", roots)

    def test_configured_root_drift_refuses_even_if_the_manifest_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "settings.gradle.kts").write_text('rootProject.name = "NativeCmpKit"')
            manifest = root / "docs/migration/current-identity.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({
                "github_repository": "NativeCmpKit/NativeCmpKit",
                "maven_group": MAVEN_GROUP,
                "modules": [{"new_artifact": "nativecmpkit-core", "source_directory": "nativecmpkit-core",
                             "new_group": MAVEN_GROUP, "gradle_project": ":nativecmpkit-core"}],
            }))
            for name in ("nativecmpkit-core", "nativecmpkit-extra"):
                project = root / name
                project.mkdir()
                (project / "build.gradle.kts").write_text('plugins { id("module.publication") }')
            with self.assertRaisesRegex(ValueError, "configured publication roots differ"):
                publication_roots(root)

    def test_only_non_snapshot_release_tag_refs_are_admitted(self):
        self.assertEqual("0.1.0-preview.2", tag_version("refs/tags/v0.1.0-preview.2"))
        for ref in ("refs/heads/main", "v0.1.0", "refs/tags/v0.1.0-SNAPSHOT", "refs/tags/v0.1.0^{commit}"):
            with self.subTest(ref=ref), self.assertRaises(ValueError):
                tag_version(ref)
