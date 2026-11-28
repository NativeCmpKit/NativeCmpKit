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
| Android | Pixel 6 API 35, 1080×2400 | [46099102700](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46099102700) | **23 passed / 2 failed / 5 blocked** (`date-display`, `webview-js`) | `screenshots/android/functional-api35-phone.json` |
| iOS | iPhone 17 Pro, iOS 26.5, 402×874 | [46108448068](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46108448068) | **19 passed / 3 failed / 0 blocked** (`slider`, `sheet-veto`, `date-display`) | `screenshots/ios/functional-iphone-simulator.json` |
| iPad | iPad Pro 13-inch (M4), iOS 26.5 | [46099392157](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46099392157) | tour: 30 captures + 3 manual recaptures; functional: **18 passed / 8 failed / 5 blocked** | `screenshots/ios/functional-ipad-simulator.json` |

Machine-readable results: `screenshots/android/functional-api35-phone.json`
(partial rerun file) and `screenshots/ios/functional-iphone-simulator.json`.
The Android full-pass counts are only in the linked evidence note; that session's
driver wrote results at the end and its rerun file is partial.

## Visual matrix

- Android: 34 canonical high-res captures from run `45957524569` plus icon
  recapture from `45973585586`.
- iOS: 31 canonical captures from run `45968953555` (the workflow run was
  cancelled at session teardown after the captures were taken; the PNGs are the
  device bytes), including recovered Alert Dialog and WebView JS/cookie/error
  states. Icon recapture run `45973585586` was cancelled the same way.
- Both matrices are scheduled for a fresh full recapture on the next successful
  phone sessions; captured status will then cite a non-cancelled run.
- 24 paired comparison sheets under `screenshots/compare/`.
- Missing visual states: iOS Time Picker, iOS action-sheet capture (functional
  verdict exists), WebView second page on iOS after the toolbar-label change.

Executable dispatch and recording steps: [session-runbook.md](session-runbook.md).

## Tablet findings (run 46099392157)

- The iPad ActionSheet popover shows **Ok** and **Remove** but exposes **no Cancel**
  action; both the tour and the functional flow failed to find it. `UI-ALERT-006`
  is recorded `failed` with the iPad screenshot and defect note.
- The in-sheet veto switch (`sheet-veto`) is not reachable in the iPad sheet
  presentation; `UI-SHEET-002` stays failed on iPad.
- `webview-js` passed on iPad, including the JavaScript-off/on evaluation.
- iPad tour failures (`Adaptive Navigation Bar`, `Web View`, `Known Limitations`)
  were recaptured manually; their images exist but are not recorded as canonical
  tour captures.

Android tablet: run [46107087160](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46107087160),
**24 passed / 1 failed / 5 blocked**; details in
[functional-tablet-2026-11-28.md](functional-tablet-2026-11-28.md).

## Outstanding verification

1. Remaining flow defects:
   - iPhone/Android phone `date-display`: the switch toggles the inline picker but
     the readout leaves the viewport at phone width (passes at tablet width).
   - `webview-js` on both Android windows: the JavaScript switch readout did not
     reach `off` before evaluation; passes on iPad.
   - iPhone `slider` and `sheet-veto`: slider is an unnamed AX group; the sheet
     switch is not exposed.
   - iPad `action-sheet`: no Cancel action (recorded as a defect for `UI-ALERT-006`).
2. iPhone Time Picker visual: image captured at 05:15 on 2026-11-28 but the tour
   process timed out before writing `tour.json`, so it is not yet a recorded
   canonical capture.
3. Android phone tour: current canonical phone captures are from the earlier
   session; the fresh phone tour was not run in the 90-minute window.

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
