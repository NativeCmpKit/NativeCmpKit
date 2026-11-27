from pathlib import Path
from subprocess import CompletedProcess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from jvm_abi import compare, parse_javap, snapshot_jars
from verify_artifacts import GROUP, InvalidArtifact


SAMPLE = '''Compiled from "Example.kt"
public final class io.github.apdelrahman1911.nativecmpkit.Example {
  public static final int FIELD = 3;
    descriptor: I
  public final java.lang.Object read(kotlin.coroutines.Continuation<? super byte[]>);
    descriptor: (Lkotlin/coroutines/Continuation;)Ljava/lang/Object;
  protected io.github.apdelrahman1911.nativecmpkit.Example();
    descriptor: ()V
}
Compiled from "Example.kt"
final class io.github.apdelrahman1911.nativecmpkit.Hidden {
  public final void hidden();
    descriptor: ()V
}
'''


class JvmAbiTest(unittest.TestCase):
    def snapshot(self):
        return {"expected_source_revision": "1" * 40, "artifacts": {"nativecmpkit-core-desktop": {"classes": parse_javap(SAMPLE)}}}

    def test_extracts_public_and_protected_descriptors_and_constants(self):
        classes = parse_javap(SAMPLE)
        self.assertEqual(["io.github.apdelrahman1911.nativecmpkit.Example"], list(classes))
        self.assertEqual(3, len(classes["io.github.apdelrahman1911.nativecmpkit.Example"]["members"]))
        self.assertTrue(any("FIELD = 3" in member["declaration"] for member in classes["io.github.apdelrahman1911.nativecmpkit.Example"]["members"]))

    def test_missing_descriptor_rejected(self):
        with self.assertRaises(InvalidArtifact):
            parse_javap('public class a.X {\npublic void f();\n}\n')

    def test_duplicate_class_rejected(self):
        with self.assertRaises(InvalidArtifact):
            parse_javap(SAMPLE + SAMPLE)

    def test_snapshot_selects_the_current_namespace_from_staged_jar_entries(self):
        with TemporaryDirectory() as temporary:
            jar = Path(temporary) / "nativecmpkit-core-desktop.jar"
            with ZipFile(jar, "w") as archive:
                archive.writestr(GROUP.replace(".", "/") + "/Example.class", b"")
                archive.writestr("outside/vendor/Foreign.class", b"")
            with patch("jvm_abi.subprocess.run", side_effect=[
                CompletedProcess([], 0, stdout="17"), CompletedProcess([], 0, stdout=SAMPLE),
            ]) as javap:
                result = snapshot_jars({"nativecmpkit-core-desktop": jar}, "1" * 40, "synthetic class entries")
        self.assertEqual([GROUP + ".Example"], javap.call_args.args[0][6:])
        artifact = result["artifacts"]["nativecmpkit-core-desktop"]
        self.assertEqual(1, artifact["class_count_inspected"])
        self.assertEqual(1, artifact["exported_class_count"])

    def test_identical_snapshot_no_compatibility_overclaim(self):
        result = compare(self.snapshot(), self.snapshot())
        self.assertTrue(result["no_removed_or_changed_exported_surface"])
        self.assertFalse(result["binary_compatibility_certified"])

    def test_removed_artifact_fails(self):
        after = self.snapshot()
        after["artifacts"] = {}
        self.assertFalse(compare(self.snapshot(), after)["no_removed_or_changed_exported_surface"])

    def test_removed_class_fails(self):
        after = self.snapshot()
        after["artifacts"]["nativecmpkit-core-desktop"]["classes"].clear()
        self.assertFalse(compare(self.snapshot(), after)["no_removed_or_changed_exported_surface"])

    def test_removed_method_fails(self):
        after = self.snapshot()
        after["artifacts"]["nativecmpkit-core-desktop"]["classes"]["io.github.apdelrahman1911.nativecmpkit.Example"]["members"].pop()
        self.assertFalse(compare(self.snapshot(), after)["no_removed_or_changed_exported_surface"])

    def test_changed_descriptor_fails(self):
        after = self.snapshot()
        after["artifacts"]["nativecmpkit-core-desktop"]["classes"]["io.github.apdelrahman1911.nativecmpkit.Example"]["members"][0]["descriptor"] = "J"
        self.assertFalse(compare(self.snapshot(), after)["no_removed_or_changed_exported_surface"])

    def test_changed_class_hierarchy_requires_review(self):
        after = self.snapshot()
        after["artifacts"]["nativecmpkit-core-desktop"]["classes"]["io.github.apdelrahman1911.nativecmpkit.Example"]["declaration"] += " extends Other"
        self.assertFalse(compare(self.snapshot(), after)["no_removed_or_changed_exported_surface"])

    def test_additive_api_keeps_old_surface(self):
        after = self.snapshot()
        after["artifacts"]["nativecmpkit-core-desktop"]["classes"]["io.github.apdelrahman1911.nativecmpkit.Example"]["members"].append({"declaration": "public void added();", "descriptor": "()V"})
        result = compare(self.snapshot(), after)
        self.assertTrue(result["no_removed_or_changed_exported_surface"])
        self.assertEqual(1, len(result["additions"]))


if __name__ == "__main__":
    unittest.main()
