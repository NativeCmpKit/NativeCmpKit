# Showcase build failures and repairs

Original failures are retained here. They are not overwritten by later green
runs.

## iOS simulator architecture — run 45949914164 (attempt 1)

- Base: `c29dda2d`
- Job: `ios`
- First failure: `:sample:common:syncComposeResourcesForIos` rejected
  `Unknown iOS simulator arch: 'x86_64'` after the Kotlin framework linked.
- Cause: `xcodebuild -destination 'generic/platform=iOS Simulator'` passed both
  simulator architectures by default; this project declares only
  `iosSimulatorArm64`.
- Repair: pass `ARCHS=arm64 EXCLUDED_ARCHS=x86_64` to `xcodebuild` in
  `.github/workflows/showcase-ui.yml`.
- The original run remains failed; the repair is verified by a later run.

## Android common-code import — run 45951792460 (attempt 1)

- Base: `112847c8`
- Job: `android`
- First failure:
  `FilePickerScreen.kt:319:21 Unresolved reference 'readByteArray'`.
- Cause: the new whole-file readout called `KmpFile.readByteArray()` without
  importing `io.github.apdelrahman1911.kira.io.readByteArray`.
- Repair: add the explicit extension import.
- The original run remains failed; the repair is verified by a later run.

## Android emulator tool path — run 45953237281 (attempt 1)

- Base: `1c1c534b`
- Job: `android`
- APK build succeeded. The emulator step then failed with exit 127:
  `adb: command not found`.
- Cause: the hosted image had the SDK installed but `platform-tools` and
  `emulator` were not on `PATH`.
- Repair: export both SDK directories in the emulator step and append them to
  `$GITHUB_PATH` for the later launch/ready scripts.

## iOS AXe readiness and pyobjc fallback — run 45953237281 (attempt 1)

- Base: `1c1c534b`
- Job: `ios`
- The simulator `.app` built successfully and launched.
- AXe `describe-ui` actually returned a large application tree, but the step
  wrote `AXE_READY=1` only to `$GITHUB_ENV`, then read the unset shell variable
  and overwrote it with `0`.
- With `AXE_READY=0`, the session fell back to the visible-Simulator driver and
  tried to build `pyobjc-framework-Quartz==12.1`. That build fails on macOS 26 /
  Python 3.15 because `CGWindowListCreateImageFromArray` is unavailable.
- Repair: keep `axe_ready` in a shell variable for the current step and write
  the environment value after the probe. AXe mode then uses `simctl` device
  screenshots and needs no pyobjc wheel.

## Missing Cupertino icon font in the Android APK — runs 45957524569 / 45972040187

- Base: `1c1c534b` / `36382250`
- The Android catalog rendered every glyph as a missing-glyph box even though
  the bundled TTF contains all 1,322 codepoints.
- Cause: the Compose 1.12 `com.android.kotlin.multiplatform.library` AAR did not
  contribute `composeResources/.../font/sf_symbols.ttf` to the application APK.
  `unzip -l android-debug.apk` had no `.ttf` entry.
- First repair attempt used an Android `SourceSet.assets.srcDir(Provider)` and
  failed before the build with
  `You cannot add Provider instances to the Android SourceSet API`.
- Working repair: a `Copy` task stages the reviewed TTF under
  `build/generated/cupertinoAssets/composeResources/<resource-package>/font/`
  and the app adds that static directory to `main` assets. The built APK now
  contains the exact 257,628-byte `sf_symbols.ttf`.
- The icon catalog is recaptured from a session built with this repair. The
  original tofu screenshot remains in the failure record.

## Cancelled iterations

Two intermediate runs were cancelled after their commit was superseded by a
repair. Cancellation is not a build result and is not reported as a pass.
