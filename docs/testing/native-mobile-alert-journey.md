# Hosted NativeCmpKit alert journey

The NativeCmpKit sample runs on an owned Android API 35 phone emulator and an
owned iPhone simulator. The tests use the verified UI Test Actions v4.1.0 commit
`e22f6c35fe6ca50a83890f54e4a6ec29ef0e2951` through its Python SDK. The job uses a
runner-local listener and per-device ownership. The Android accessibility daemon
and persistent iOS AXe driver provide the semantic observations. The repository's
allowlisted checkout action fetches the source at the verified commit.
[UI Test Actions release](https://github.com/ui-test-actions/ui-test-actions/releases/tag/v4.1.0)

Use the `identity-linux-sample-automation` or `identity-apple-sample-automation`
profile in the manual native verification workflow. Both profiles build the
normal sample, open **Adaptive Alert Dialog** from its home screen, and verify
four outcomes.

1. Open the alert, press **Cancel**, and verify that the alert closes and the sample still responds.
2. Reopen the same alert, press **Ok**, and verify that it closes again.
3. Open the single-button alert and verify that no Cancel control is present. Confirm and check the screen is still usable.
4. Restart the app, reenter the sample, and verify that the previously closed alert remains closed.

The SDK settles after mutations and requests snapshot diffs. The artifact
retains the compact alert observation, a snapshot-bound screenshot, action
timings, device provenance, and the exact NativeCmpKit and driver revisions.
The screenshot and its `alert-evidence.json` receipt are available if a later
interaction fails. Runtime counts come from the completed assertions. The device
tests for file providers, popover anchoring and permission dialogs, and the release's
physical-device checklist retain their own procedures.
[Workflow](../../.github/workflows/build-native-libs.yml) · [Physical-device procedure](nativecmpkit-physical-device-verification.md)
