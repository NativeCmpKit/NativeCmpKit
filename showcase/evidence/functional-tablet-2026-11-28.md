# Tablet functional evidence — 2026-11-28

Two large-screen sessions, one per platform. Neither result is a phone verdict.

## iPad (iPad Pro 13-inch (M4), iOS 26.5)

- Run: [46099392157](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46099392157)
- iOS job: `140838141915`
- Tour: 30 captures + 3 manual recaptures (Navigation Bar, Web View, Known
  Limitations) after their tour steps timed out.
- Functional: **18 passed / 8 failed / 5 blocked** (`screenshots/ios/functional-ipad-simulator.json`).

Failed flows and observations:

| Flow | Observation |
| --- | --- |
| `action-sheet` | the popover exposes Ok and Remove but **no Cancel**; `UI-ALERT-006` recorded failed with the popover screenshot |
| `sheet-veto` | the in-sheet “Allow swipe to hide” switch is not exposed by the iPad sheet |
| `date-display` | same viewport/readout issue as iPhone |
| `slider` | same unnamed-group slider limitation as iPhone |
| `sheet` | close path did not complete within the flow timeout |
| `topbar` | Home navigation timed out once (`HTTP 408`) |
| `webview-js` | **passed** on iPad |

## Android tablet (Pixel 6 AVD, 1600×2560 @ 320 dpi, API 35)

- Run: [46107087160](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46107087160)
- Android job: `140862145867`
- Tour: 37 captures (`api35-tablet.png`); one dropdown-menu step failed, overview captured.
- Functional: **24 passed / 1 failed / 5 blocked** (`screenshots/android/functional-api35-tablet.json`).

`date-display` **passed** on the tablet window while failing on the phone window:
the readout stays in view at 1600×2560. `nav-restore` passed after a
landscape/portrait rotation. The only failure is `webview-js`, where the
JavaScript switch readout did not reach `off` before evaluation.

## Tablet comparison sheets

`screenshots/compare-tablet/` holds 31 Android-tablet-left / iPad-right sheets
generated with `compare.py --android-device api35-tablet --ios-device ipad-simulator`.

## Contract rows

`NAV-004`, `UI-BAR-008`, `UI-SHEET-003` are recorded `captured` for both platforms
from these tours; `UI-ALERT-006` is `failed` with the iPad popover evidence.
