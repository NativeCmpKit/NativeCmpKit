"""Current branding guards; not compilation, ABI or publication evidence."""
from pathlib import Path
import json
import plistlib
import unittest

from verify_namespace import OLD_IDENTITY


ROOT = Path(__file__).resolve().parents[2]


class CurrentIdentityTest(unittest.TestCase):
    def test_legacy_detection_covers_compiler_and_publication_spellings(self):
        old_jni = 'Java_' + '_'.join(('com', 'mohamedrejeb', 'calf', 'picker', 'abiVersion'))
        alternate_namespace = '.'.join(('io', 'github', 'apdelrahman1911', 'kira', 'picker'))
        alternate_artifact = '-'.join(('kira', 'file', 'picker'))
        old_repository_path = '/'.join(('', 'Apdelrahman1911', 'nativeCmpkit', 'blob', 'main'))
        for obsolete in (old_jni, alternate_namespace, alternate_artifact, old_repository_path):
            with self.subTest(value=obsolete):
                self.assertIsNotNone(OLD_IDENTITY.search(obsolete))
        for current in ('Java_io_github_apdelrahman1911_nativecmpkit_picker_abiVersion',
                        'io.github.apdelrahman1911.nativecmpkit.picker', 'nativecmpkit-file-picker'):
            with self.subTest(value=current):
                self.assertIsNone(OLD_IDENTITY.search(current))

    def test_library_and_exact_producer_root_use_the_owner_requested_name(self):
        identity = json.loads((ROOT / "docs/migration/current-identity.json").read_bytes())
        self.assertEqual("NativeCmpKit", identity["project"])
        self.assertIn('rootProject.name = "NativeCmpKit"', (ROOT / "settings.gradle.kts").read_text())
        self.assertIn('check(root.name == "NativeCmpKit")', (ROOT / "scripts/ci/stage-core-io.init.gradle.kts").read_text())

    def test_current_docs_and_publication_display_use_the_same_brand(self):
        for name in ("README.md", "docs/index.md", "AGENTS.md"):
            with self.subTest(path=name):
                self.assertTrue((ROOT / name).read_text().startswith("# NativeCmpKit"))
        self.assertIn("site_name: 'NativeCmpKit'", (ROOT / "mkdocs.yml").read_text())
        self.assertIn('name.set("NativeCmpKit - "', (ROOT / "convention-plugins/src/main/kotlin/module.publication.gradle.kts").read_text())

    def test_sample_display_names_and_packages_use_the_current_identity(self):
        self.assertIn('title = "NativeCmpKit"', (ROOT / "sample/desktop/src/jvmMain/kotlin/io/github/apdelrahman1911/nativecmpkit/sample/desktop/Main.kt").read_text())
        self.assertIn('android:label="NativeCmpKit"', (ROOT / "sample/android/src/main/AndroidManifest.xml").read_text())
        for name in ("sample/web-js/src/jsMain/resources/index.html", "sample/web-wasm/src/wasmJsMain/resources/index.html"):
            with self.subTest(path=name):
                self.assertIn("<title>NativeCmpKit Demo</title>", (ROOT / name).read_text())
        info = plistlib.loads((ROOT / "sample/ios/NativeCmpKit/Info.plist").read_bytes())
        self.assertEqual("NativeCmpKit", info["CFBundleDisplayName"])
        show = (ROOT / "sample/common/src/commonMain/kotlin/io.github.apdelrahman1911.nativecmpkit.sample/screens/ShowcaseScreen.kt").read_text()
        self.assertIn('title = "About NativeCmpKit"', show)

    def test_coordinates_and_public_names_share_the_current_identity(self):
        identity = json.loads((ROOT / "docs/migration/current-identity.json").read_bytes())
        self.assertEqual("io.github.apdelrahman1911.nativecmpkit", identity["maven_group"])
        self.assertEqual("io.github.apdelrahman1911.nativecmpkit", identity["public_kotlin_namespace"])
        self.assertEqual(23, len(identity["modules"]))
        self.assertLessEqual({"nativecmpkit-geo", "nativecmpkit-navigation"},
                             {module["new_artifact"] for module in identity["modules"]})
        self.assertTrue(all(m["new_artifact"].startswith("nativecmpkit-") and m["gradle_project"].startswith(":nativecmpkit-")
                            for m in identity["modules"]))
        self.assertFalse(identity["binary_compatibility_verified"])
        build = (ROOT / "build.gradle.kts").read_text()
        self.assertIn('gradleProperty("nativeCmpkit.version")', build)
        self.assertIn('gradleProperty("nativeCmpkit.allowPublishing")', build)
        resources = (ROOT / "nativecmpkit-cupertino-icons/build.gradle.kts").read_text()
        self.assertIn('packageOfResClass = "io.github.apdelrahman1911.nativecmpkit.nativecmpkit_cupertino_icons.generated.resources"', resources)

    def test_original_upstream_attribution_is_present(self):
        notice = (ROOT / "NOTICE").read_text()
        self.assertIn("Mohamed Rejeb", notice)
        self.assertIn("NativeCmpKit", notice)
        self.assertIn('publish = false', (ROOT / "nativecmpkit-share/native/Cargo.toml").read_text())
        self.assertIn('publish = false', (ROOT / "nativecmpkit-file-picker/native/Cargo.toml").read_text())


if __name__ == "__main__":
    unittest.main()
