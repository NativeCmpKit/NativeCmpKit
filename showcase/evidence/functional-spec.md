# Functional UI flow specification

Implemented in `showcase/automation/functional.py`. Each flow restarts the app,
opens its screen through the real Home index, performs a user action, and asserts
observable state. A flow is `passed` only when the assertion succeeds; otherwise
it is `failed` or explicitly `blocked`.

| Flow | Screen | Action | Assertion |
| --- | --- | --- | --- |
| `buttons` | Adaptive Buttons | tap the filled counter | text changes from 0 to 1 |
| `switch` | Adaptive Switch | toggle the Wi-Fi switch | row text changes off → on |
| `slider` | Adaptive Slider | drag the brightness slider | readout changes |
| `dropdown` | Adaptive Drop Down | iOS: top-bar UIMenu → Duplicate; Android: simple menu → Copy | readout becomes `Duplicated!` / `Copied!` |
| `alert-cancel` | Alert Dialog | show, cancel | dialog body disappears |
| `alert-confirm` | Alert Dialog | show, confirm | dialog body disappears |
| `alert-text-field` | Alert Dialog | show text-field dialog | iOS-only section: `Enter Name` field, then Cancel |
| `action-sheet` | Alert Dialog | show ActionSheet, cancel (iOS only) | action sheet dismisses |
| `sheet` | Bottom Sheet | show, close | sheet content disappears |
| `topbar` | Adaptive Top Bar | tap Share | `Last action: Share tapped` |
| `toolbar` | Adaptive Toolbar | tap Share | `Share tapped` |
| `navbar` | Adaptive Navigation Bar | select Profile | Profile content visible |
| `scaffold-tab` | Adaptive Scaffold | select Favorites | tab title and content update (two `Favorites` nodes) |
| `date-bounds` | Date Picker | select `From today` | chip is selected |
| `time-24h` | Time Picker | scroll to 24-hour state | `24-hour state: 19:20` |
| `icons-category` | Cupertino Icons | select Arrows | count no longer 1,322 |
| `geo-math` | Geo Maths | read fixed values | `111.19` and unavailable tracker |
| `limitations` | Known Limitations | read unsupported list | FAB and determinate progress limits |
| `liquidglass` | Liquid Glass | tap glass button (iOS 26) | click count increments; Android shows fallback |
| `webview` | Web View | second HTML, JS, cookie, clear, invalid | title, `JS:`, `kira=1`, cleared, one error |
| `permissions-bulk-deny` | Permissions | bulk request, deny OS prompts | `All permissions granted: false` |
| `permissions-sms-rows` | Permissions | read the three SMS rows | `ReadSms`, `ReceiveSms`, `SendSms` |
| `alert-text-field` | Alert Dialog | — | not-applicable on Android: sample section is iOS-only |
| `action-sheet` | Alert Dialog | — | not-applicable on Android: sample section is iOS-only |
| `file-picker` | File Picker | — | blocked: seeded file selection not driven |
| `file-saver` | File Saver | — | blocked: no save destination |
| `share` | Content Sharing | — | blocked: no external recipient |
| `camera` | Camera Picker | — | blocked: emulator camera not seeded |

The workflow seeds `showcase/fixtures/kira-fixture.txt` and
`showcase/fixtures/kira-fixture.png` into Android Downloads and the iOS photo
library. A future flow can select those fixtures deterministically; until then
the system picker flows remain blocked rather than claimed as passed.

Compile validation: Android build `45990755404` at `05513774` succeeded after the
Liquid Glass, SMS, native-bar-label and functional-driver changes. Functional
execution is still pending the next Android/iOS phone sessions and the tablet
sessions.
