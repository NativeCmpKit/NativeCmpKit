# NativeCmpKit showcase

A reusable, independently testable showcase for the public Kira components and
native services. It is the existing `sample` application extended with a
searchable component index, stable screen routes, semantic test tags and an
in-app Known Limitations screen. Nothing in the production components is mocked.

- Base commit: `a2c48c0b9ebf3524192e680ecd4becc1f2880bb8` (`origin/main`)
- Feature branch: `feature/showcase-ui-verification`
- Android application ID and iOS bundle ID:
  `io.github.apdelrahman1911.nativecmpkit.sample`
- Android launcher activity:
  `io.github.apdelrahman1911.kira.sample.MainActivity`
- Shared UI entry point:
  `sample/common/src/commonMain/kotlin/io.github.apdelrahman1911.kira.sample/App.kt`

## Use the app

Every screen is reachable from the Home index. Type in **Search components** to
filter by title, description or route name. Each result has a stable route name
from `sample/common/.../navigation/Screen.kt` and a root test tag such as
`screen.adaptive-buttons`. **Reset state** recreates the nav host and clears
screen-local demo state without reinstalling the app.

The app is the normal sample build. Test support is limited to:

- stable routes, test tags and the searchable index;
- the Known Limitations screen, which states source-confirmed unsupported and
  internal APIs instead of presenting them as working;
- deterministic, synthetic fixture text and the hosted session driver.

There is no alternate mock component implementation.

## Build and run

```sh
# Android debug APK (the hosted workflow uses this exact task)
./gradlew :sample:android:assembleDebug --no-configuration-cache

# Desktop sample, if a desktop host is available
./gradlew :sample:desktop:run

# iOS simulator app (macOS + Xcode only)
xcodebuild -project sample/ios/Kira.xcodeproj -scheme Kira \
  -configuration Debug -sdk iphonesimulator \
  -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath build CODE_SIGNING_ALLOWED=NO build
```

The iOS project embeds the shared `Common` framework through its existing
`embedAndSignAppleFrameworkForXcode` build phase. The shared scheme is
`sample/ios/Kira.xcodeproj/xcshareddata/xcschemes/Kira.xcscheme`.

## Hosted UI verification

`.github/workflows/showcase-ui.yml` builds the real APK and simulator `.app` on
GitHub-hosted runners. With `ci/showcase-mode` set to `session`, it opens a live
[ui-test-actions](https://github.com/ui-test-actions/ui-test-actions) session and
holds it for the external client.

```sh
# Build only
printf 'build\n' > ci/showcase-mode
printf '2\n' > ci/showcase-trigger
git add ci/showcase-mode ci/showcase-trigger
git commit -m 'ci(showcase): build'
git push

# Live session: replace both digests with a fresh token digest first.
printf 'session\n' > ci/showcase-mode
printf '3\n' > ci/showcase-trigger
```

The repository Actions allowlist does not include the ui-test-actions composite
action. The workflow therefore clones the reviewed commit
`0c818c5d72e8c30c59bd1287c330a40392bf8e89` and runs its `lifecycle.py` directly.
Only allowlisted actions (`checkout`, `setup-java`, `gradle/actions`,
`upload-artifact`) are referenced. This does not change repository settings.

The workflow uses the documented Cloudflare Quick Tunnel (`transport: auto`)
because the controller is the external agent host; runner-local loopback is not
reachable from there. No named tunnel, Access credential or private overlay is
required. The raw token stays on the controller; only its SHA-256 digest is in
Git.

The workflow records:

- the exact run/attempt/job and app revision;
- the selected emulator model/API/density and the selected simulator UDID;
- the pinned ui-test-actions commit;
- the build artifact and the live session connection artifact.

## Device matrix and functional testing

Phone is the baseline. `device_class: tablet` selects an iPad simulator on iOS
and a 1600×2560 / 320 dpi viewport on the Pixel 6 Android emulator.

```sh
# Android tablet session
gh workflow run showcase-ui.yml -R NativeCmpKit/NativeCmpKit \
  --ref feature/showcase-ui-verification \
  -f mode=session -f platform=android -f device_class=tablet -f duration_minutes=45

# iPad session
gh workflow run showcase-ui.yml -R NativeCmpKit/NativeCmpKit \
  --ref feature/showcase-ui-verification \
  -f mode=session -f platform=ios -f device_class=tablet -f duration_minutes=60
```

Use `--device` so tablet evidence never overwrites the phone captures:

```sh
python3 showcase/automation/tour.py ... --device api35-tablet
python3 showcase/automation/functional.py ... --device api35-tablet
python3 showcase/automation/compare.py --android-device api35-tablet \
  --ios-device ipad-simulator --output screenshots/compare-tablet --label tablet
```

`record_functional.py` refuses non-canonical devices unless `--allow-device` is
passed: the coverage execution slots are bound to `api35-phone` and
`iphone-simulator`. Tablet results are reported as separate large-screen evidence,
and `record.py --tablet` records only the tablet-window rows (iPad popover,
large-screen index, tablet scaffold and sheet) from the tablet tour.

Functional checks, not screenshots alone:

```sh
python3 showcase/automation/functional.py \
  --client-dir /path/to/ui-test-actions \
  --connection /tmp/showcase-session/connection.json \
  --token-file /tmp/showcase-token \
  --platform android --output-root screenshots
```

The driver asserts observable state (counter, switch, slider, menu selection,
dialog dismissal, sheet dismissal, top-bar/toolbar action, tab content, icon
filter, WebView title/JS/cookie/error, Geo values, Liquid Glass click) and records
`passed`, `failed`, or `blocked` in `screenshots/<platform>/functional-<device>.json`.
It seeds a synthetic text and image fixture for picker discovery; driving the
system file/photo picker remains explicitly blocked until a deterministic
selection path is added.

## Capture

See [automation/README.md](automation/README.md). The smoke flow proves Home →
Adaptive Buttons → counter change → Back. The tour captures every indexed screen
from the real emulator/simulator.

```sh
python3 showcase/automation/smoke.py \
  --client-dir /path/to/ui-test-actions \
  --connection /tmp/showcase-session/connection.json \
  --token-file /tmp/showcase-token \
  --output screenshots/_smoke/android --platform android

python3 showcase/automation/tour.py \
  --client-dir /path/to/ui-test-actions \
  --connection /tmp/showcase-session/connection.json \
  --token-file /tmp/showcase-token \
  --platform android --output-root screenshots --continue-on-error
```

Canonical captures live under `screenshots/android/<component>/<scenario>/` and
`screenshots/ios/<component>/<scenario>/`. The index is `screenshots/INDEX.md`.
Temporary sessions, logs and failure captures stay out of the canonical tree.

## Reset and fixtures

- Android: `adb shell pm clear io.github.apdelrahman1911.nativecmpkit.sample`
  resets app data and granted runtime permissions; uninstall/reinstall for a
  fully fresh state.
- iOS: `xcrun simctl uninstall <UDID> io.github.apdelrahman1911.nativecmpkit.sample`
  then reinstall; `xcrun simctl privacy <UDID> reset all <bundle>` resets
  permission decisions.
- Fixtures are synthetic: known text, generated bytes, seeded image fixtures and
  `https://example.test`-style destinations. No personal accounts, contacts,
  photos, calendars or real share recipients are used.
- The WebView starts from deterministic inline HTML. The remote-URL button is a
  separate, explicit action and is not part of the baseline capture.

## Coverage

Current evidence levels and gaps: [evidence/verification-status.md](evidence/verification-status.md).
Hosted dispatch and recording steps: [evidence/session-runbook.md](evidence/session-runbook.md).
The source-audited component/API view is [INVENTORY.md](INVENTORY.md)
([public-api.json](public-api.json) is the raw declaration extract). The
versioned contract is [coverage.json](coverage.json), with a readable
[COVERAGE.md](COVERAGE.md). It enumerates 66 component/service rows, their
platform support, route, steps, expected observations, screenshot path and
execution status. Rows are updated only from reviewed hosted runs.

Supported rows are not claimed as passed until their execution entry names the
run/attempt/job. Unsupported rows point at the Known Limitations screen and are
marked `not-applicable`; they are not presented as working features.

### Android icon font packaging

The stock Android APK built from `1c1c534b` did not contain
`sf_symbols.ttf`, so `CupertinoIcon` rendered tofu boxes. `sample/android` now
stages the reviewed 257,628-byte font at
`assets/composeResources/io.github.apdelrahman1911.kira.kira_cupertino_icons.generated.resources/font/sf_symbols.ttf`
through a deterministic `Copy` task; the rebuilt APK contains the same SHA-256
`67c44fe9183b002e79dde7f6977e2988661c9a3e4a3c5fce968787efdbed823c` and the
catalog renders. The underlying AAR packaging path still deserves a library-level
regression check.

Source-confirmed gaps that shape the showcase:

- `AdaptiveExpandableFAB` and `UIKitExpandableFABItem` are `internal`; there is
  no public FAB entry point.
- There is no determinate circular-progress API.
- Buttons have no size or selected state; variants are color factories.
- iOS 26 drops slider `steps` and switch `thumbContent`/custom colors.
- iOS time format follows the device locale; `is24Hour` is not applied.
- Dropdown offset/shape/elevation and sheet insets/shape are ignored on iOS.
- No public action-sheet source-view/bar-item anchor API exists.
- Navigation arguments are declarations only; nested graphs and non-Android
  system back handling are absent.
- `LocationTracker` never updates its public states; Android additionally needs
  an Android-only `bind(...)`.
- `kira-maps` is build-file-only; `kira-media` and the notification scheduler are
  excluded. The notification permission is supported and in scope.

## Reproduce a focused check

The app's production components are also covered by the existing library tests.
Use the module tasks, not the showcase, for component-level regressions:

```sh
./gradlew :kira-ui:desktopTest :kira-io:desktopTest :kira-file-picker:desktopTest
```

The showcase adds device-level evidence; it does not replace library tests,
consumer/ABI checks or release gates.
