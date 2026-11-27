# Showcase verification status

Updated 2026-11-27. This page separates evidence levels; a lower level never
implies a higher one. The contract now has 88 rows, including four tablet-window
rows (`UI-ALERT-006`, `NAV-004`, `UI-BAR-008`, `UI-SHEET-003`).

## Source and build

| Level | Evidence | Result |
| --- | --- | --- |
| Repository invariants | `verify_migration.py`, `validate_audit.py`, `source_inventory.py --check` on `4de926fd` | pass (inventory matches `af388bd3`) |
| iOS app build | run [46014167086](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46014167086), revision `94a93ef8` | `success` (Kotlin/Native framework + simulator app) |
| Android app build | run [45993784178](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/45993784178), revision `e751b57f` | `success` (debug APK) |
| Newest sample changes | sheet veto, date display mode, WebView JS toggle, row-targeted switches | compiled on iOS at `94a93ef8`; Android compile pending the next session |

## Functional UI (asserted state, not screenshots)

| Platform | Device | Run | Result | Record |
| --- | --- | --- | --- | --- |
| Android | Pixel 6 API 35, 1080×2400 | [45993784178](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/45993784178) | 17 passed / 6 failed / 5 blocked in the full pass; failures were flow-targeting bugs (fixed) and one iOS-only section | [functional-android-2026-11-27.md](functional-android-2026-11-27.md) |
| iOS | iPhone 17 Pro, iOS 26.5, 402×874 | [46014167086](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46014167086) | 16 passed / 6 failed / 0 blocked | [functional-ios-2026-11-27.md](functional-ios-2026-11-27.md) |

Machine-readable results: `screenshots/android/functional-api35-phone.json`
(partial rerun file) and `screenshots/ios/functional-iphone-simulator.json`.
The Android full-pass counts are only in the linked evidence note; that session's
driver wrote results at the end and its rerun file is partial.

## Visual matrix

- Android: 34 canonical high-res captures from run `45957524569` plus icon
  recapture from `45973585586`.
- iOS: 31 canonical captures from run `45968953555`, including recovered Alert
  Dialog and WebView JS/cookie/error states.
- 24 paired comparison sheets under `screenshots/compare/`.
- Missing visual states: iOS Time Picker, iOS action-sheet capture (functional
  verdict exists), WebView second page on iOS after the toolbar-label change.

## Outstanding verification

1. Android full functional re-run on the current branch (all flows, including the
   new veto/display-mode/JS/rotation flows) and Android tour recapture.
2. Six iOS retests: `clickable`, `slider`, `date-bounds`, `sheet-veto`,
   `date-display`, `webview-js`.
3. iPad session: tour, functional, action-sheet popover (`UI-ALERT-006`).
4. Android tablet session (1600×2560 / 320 dpi), tour, functional, tablet sheets.
5. iOS Time Picker capture.

## Blocked, not passed

- System document/photo pickers, share sheet and camera: fixtures are seeded, but
  the OS dialogs are not driven; verdicts stay `blocked`.
- Desktop/web runtime behavior: out of this device matrix.

## Defects already fixed in the showcase branch

- Android APK shipped no Cupertino icon font (tofu glyphs); app-level staging now
  includes `sf_symbols.ttf` (SHA-256 `67c44fe…823c`).
- Duplicate `More options` accessibility labels made menu targeting ambiguous.
- Bottom-sheet content had no padding on Android.
- Native bar buttons exposed no stable labels for image-only items.
