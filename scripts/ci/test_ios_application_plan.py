"""Synthetic plan contracts; no iOS application, native or library execution."""
from pathlib import Path
import tempfile
import unittest

import library_tests as r

HOST = "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeUiApplicationHost.kt"
FIXTURE = "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeUiApplicationHostTest.kt"
IDENTITY = "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeObjectIdentity.kt"
IMAGE = "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/utils/UIImageConversionTest.kt"
PROPERTIES = "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/dialog/RememberNativeAlertPropertiesTest.kt"
BARS = "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/navigation/NativeBarOwnershipTest.kt"
VECTOR_THEME = "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/utils/NativeVectorThemeAcceptanceTest.kt"
IMAGE_MEMORY = "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/utils/UIImageMemoryDiagnosticsTest.kt"


class IosApplicationPlanTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.write("settings.gradle.kts", 'include(\n    ":nativecmpkit-ui",\n    ":nativecmpkit-io",\n)\n')
        for module in ["nativecmpkit-ui", "nativecmpkit-io"]:
            self.write(module + "/build.gradle.kts", "// synthetic configuration")
            self.write(module + "/src/commonTest/kotlin/Common.kt", "// synthetic common test")
        self.write(HOST, "// synthetic application host")
        self.write(FIXTURE, "// synthetic genuine-host regression")
        self.write(IDENTITY, "// synthetic exact native identity helper")
        self.write(IMAGE, "// synthetic retained-image ownership regression")
        self.write(PROPERTIES, "// synthetic stable/changed text-field remember contract")
        self.write(BARS, "// synthetic current-membership native selection contract")
        self.write(VECTOR_THEME, "// synthetic real rendering/system-appearance acceptance input")
        self.write(IMAGE_MEMORY, "// synthetic real image-memory/profile-workload acceptance input")

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def plan(self, suite="ios"):
        return r.plan(self.root, suite, minimum_modules=("nativecmpkit-ui", "nativecmpkit-io"))

    def test_ui_ios_uses_app_task_and_distinct_actual_report_directory(self):
        item = next(i for i in self.plan()["expected"] if i["module"] == "nativecmpkit-ui")
        self.assertEqual(":nativecmpkit-ui:iosSimulatorArm64ApplicationTest", item["task"])
        self.assertEqual("nativecmpkit-ui/build/test-results/iosSimulatorArm64ApplicationTest", item["report_directory"])
        self.assertEqual("genuine-uikit-application", item["native_test_host"])

    def test_other_ios_modules_keep_their_existing_test_runner(self):
        item = next(i for i in self.plan()["expected"] if i["module"] == "nativecmpkit-io")
        self.assertEqual(":nativecmpkit-io:iosSimulatorArm64Test", item["task"])
        self.assertNotIn("native_test_host", item)

    def test_ui_application_sources_cannot_disappear_behind_common_tests(self):
        for source in [HOST, FIXTURE, IDENTITY, IMAGE, PROPERTIES, BARS, VECTOR_THEME, IMAGE_MEMORY]:
            with self.subTest(source=source):
                original = (self.root / source).read_bytes()
                (self.root / source).unlink()
                try:
                    with self.assertRaisesRegex(ValueError, "application"):
                        self.plan()
                finally:
                    (self.root / source).write_bytes(original)

    def test_diagnostic_subset_keeps_application_task_and_discloses_omitted_io(self):
        plan = r.plan(self.root, "ios", only_modules=("nativecmpkit-ui",))
        self.assertFalse(plan["complete_suite_requested"])
        self.assertEqual(["nativecmpkit-io"], plan["test_bearing_modules_not_requested"])
        self.assertEqual(":nativecmpkit-ui:iosSimulatorArm64ApplicationTest", plan["expected"][0]["task"])
        self.assertIn(HOST, plan["expected"][0]["test_source_files"])
        self.assertIn(FIXTURE, plan["expected"][0]["test_source_files"])
        self.assertIn(IDENTITY, plan["expected"][0]["test_source_files"])
        self.assertIn(IMAGE, plan["expected"][0]["test_source_files"])
        self.assertIn(PROPERTIES, plan["expected"][0]["test_source_files"])
        self.assertIn(BARS, plan["expected"][0]["test_source_files"])
        self.assertIn(VECTOR_THEME, plan["expected"][0]["test_source_files"])
        self.assertIn(IMAGE_MEMORY, plan["expected"][0]["test_source_files"])

    def test_ui_host_sources_do_not_change_other_platform_tasks(self):
        for suite in ["desktop", "android-host", "js", "wasm"]:
            item = next(i for i in self.plan(suite)["expected"] if i["module"] == "nativecmpkit-ui")
            self.assertEqual(":nativecmpkit-ui:" + r.SUITES[suite][0], item["task"])
            self.assertNotIn("native_test_host", item)
            self.assertNotIn(HOST, item["test_source_files"])


if __name__ == "__main__":
    unittest.main()
