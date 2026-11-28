import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock

from mobile_alert_journey import exercise


PNG = b"\x89PNG\r\n\x1a\n"


class MobileAlertJourneyTests(unittest.TestCase):
    def setUp(self):
        self.ui = Mock(spec=["capabilities", "device_info", "wait_ready", "settle", "click", "wait",
                             "assert_element", "inspect", "screenshot", "action"])
        self.ui.capabilities.return_value = {"commands": {
            "app.restart", "app.wait_ready", "device.info", "element.assert", "element.click", "element.wait",
            "screenshot.capture", "tree.diff", "tree.snapshot", "ui.settle",
        }}
        self.ui.device_info.return_value = {"ok": True, "result": {
            "platform": "android", "device_id": "emulator-5554", "form_factor_hardware": "emulator",
        }}
        self.ui.click.return_value = {"ok": True, "result": {"mode": "diff"}}
        self.ui.inspect.side_effect = [
            {"ok": True, "result": {"nodes": [{"ref": "@e3", "label": "Adaptive Alert Dialog · Native alert"}]}},
            {"ok": True, "result": {"performance": {"engine": "a11y_daemon"}}},
            {"ok": True, "result": {"nodes": [{"ref": "@e7", "label": "Adaptive Alert Dialog · Native alert"}]}},
        ]
        self.ui.screenshot.return_value = {"png": PNG, "snapshot_id": "alert-snapshot",
                                           "sha256": hashlib.sha256(PNG).hexdigest()}

    def test_bound_screenshot_and_fresh_menu_references_follow_the_sdk_contract(self):
        with TemporaryDirectory() as folder:
            output = Path(folder)
            result = exercise(self.ui, output, "android", "emulator-5554")
            self.assertEqual((output / "alert.png").read_bytes(), PNG)
        self.assertEqual(result["screenshot"]["snapshot_id"], "alert-snapshot")
        self.assertNotIn("png", result["screenshot"])
        self.assertEqual(len(result["cases_passed"]), 4)
        clicks = self.ui.click.call_args_list
        self.assertEqual([call.kwargs["ref"] for call in clicks if "ref" in call.kwargs], ["@e3", "@e7"])
        self.assertTrue(all(call.kwargs["return_diff"] for call in clicks))

    def test_unbound_screenshot_does_not_pass_the_journey(self):
        del self.ui.screenshot.return_value["snapshot_id"]
        with TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "bound alert screenshot metadata"):
                exercise(self.ui, Path(folder), "android", "emulator-5554")
            self.assertFalse((Path(folder) / "alert-evidence.json").exists())

    def test_evidence_survives_a_later_interaction_failure(self):
        reply = self.ui.click.return_value
        self.ui.click.side_effect = [reply, reply, RuntimeError("Cancel failed")]
        with TemporaryDirectory() as folder:
            output = Path(folder)
            with self.assertRaisesRegex(RuntimeError, "Cancel failed"):
                exercise(self.ui, output, "android", "emulator-5554")
            evidence = json.loads((output / "alert-evidence.json").read_text(encoding="utf-8"))
            captured = (output / "alert.png").read_bytes()
        self.assertEqual(evidence["screenshot"]["sha256"], hashlib.sha256(captured).hexdigest())
        self.assertEqual(evidence["screenshot"]["snapshot_id"], "alert-snapshot")

    def test_an_unexpected_device_is_refused_before_mutation(self):
        self.ui.device_info.return_value["result"]["form_factor_hardware"] = "physical"
        with TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "owned hosted device"):
                exercise(self.ui, Path(folder), "android", "emulator-5554")
        self.ui.click.assert_not_called()
