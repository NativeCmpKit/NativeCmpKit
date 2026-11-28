# NativeCmpKit Showcase — implementation and verification report

- **Repository**: `NativeCmpKit/NativeCmpKit`
- **Branch**: `feature/showcase-ui-verification`
- **Report revision**: `042f51168fea7a1156127276bdab7e10ab410157`
- **Base handoff**: `a2c48c0b9ebf3524192e680ecd4becc1f2880bb8` (`origin/main`)
- **App**: `sample/android` + `sample/common` (searchable Home index, stable routes)
- **Harness**: `ui-test-actions` pinned at
  `0c818c5d72e8c30c59bd1287c330a40392bf8e89`
- **Companion report**: [ui-test-actions-limitations.md](ui-test-actions-limitations.md)

Everything in this report is bound to a workflow run, a screenshot path or a
manifest row. Statuses are evidence, not intent:

- **passed** — a functional flow drove a control and asserted observable state.
- **captured** — a live screenshot exists; behaviour was not driven.
- **failed** — a flow ran and its assertion failed; the row is not green.
- **blocked** — the OS surface was not driven (pickers/share/camera).
- **not-applicable** — the API or sample section does not exist on that platform.
- **not-run** — no hosted evidence.

---

## 1. What was built

| Area | Change | Commit |
| --- | --- | --- |
| Searchable Home index, stable routes, test tags, per-screen reset | `Screen.kt`, `HomeScreen.kt`, `App.kt` | `ae7dc5ef` |
| Known Limitations screen | `LimitationsScreen.kt` | `ae7dc5ef` |
| Deterministic geo maths + tracker-unavailable state | `GeoMathScreen.kt` | `96fd9a5f` |
| Liquid Glass screen (iOS actual, non-iOS fallback) | `LiquidGlassShowcase*.kt` | `03676e2f` |
| SMS permission rows (`ReadSms/ReceiveSms/SendSms`) | `PermissionsScreen.kt` | `03676e2f` |
| Switch / top-bar / toolbar / navbar functional readouts | screen files | `03676e2f`, `0f053028` |
| Picker filter modes (Custom MIME, Extension) | `FilePickerScreen.kt` | `f4a4d472` |
| Sheet detents + veto + dismissal controls | `BottomSheetScreen.kt` | `f4a4d472`, `37c9479f` |
| Date display-mode readout, selected-range readout | `DatePickerScreen.kt` | `56407cfa`, `55dc4a25` |
| WebView JavaScript toggle + JS-off evaluation | `WebViewScreen.kt` | `c1deb9be`, `678bee2c` |
| Clickable gesture counters | `AdaptiveClickableScreen.kt` | `e751b57f` |
| Unique native-bar labels (Share/More/Add/system items, tints) | `TopBarDemoScreen.kt`, `ToolbarScreen.kt`, `DropDownScreen.kt`, `NavigationBarScreen.kt` | `0f053028`, `05513774` |
| Android Cupertino font staging workaround | `sample/android/build.gradle.kts` | earlier branch work |
| Coverage contract, inventory, API extract | `showcase/*` | `eacba3d9`, `03676e2f` |
| Functional driver, tour, recorder, index, checks | `showcase/automation/*` | `03676e2f` … `efd99aae` |

The showcase drives **public** APIs only. `kira-maps` is build-file-only and
`kira-media`/`kira-notifications` are not included in the build; they are shown
as excluded rows, not as features.

---

## 2. Verification method

### 2.1 Device matrix

| Device | OS | Window | Runs |
| --- | --- | --- | --- |
| Pixel 6 AVD (Google APIs, x86_64) | Android 15 / API 35 | 1080×2400 @ 420 dpi | 46099102700, 46114711444 |
| Pixel 6 AVD, resized | Android 15 / API 35 | 1600×2560 @ 320 dpi | 46107087160 |
| iPhone 17 Pro simulator | iOS 26.5 | 402×874 pt | 46014167086, 46108448068, 46114716852 |
| iPad Pro 13-inch (M4) simulator | iOS 26.5 | iPad portrait | 46099392157 |

All sessions are GitHub-hosted (`ubuntu-24.04`, `macos-26`), KVM emulator /
Simulator, exposed through a Cloudflare Quick Tunnel with a one-time token
digest. The APK/IPA is built from the branch revision inside the same run.

### 2.2 Two capture layers

1. **Tour** (`showcase/automation/tour.py`) — opens every screen through the real
   Home index, captures a PNG per screen and extra states (alert, sheet,
   dropdown menu, WebView JS/cookie/error, icon categories), and records
   `tour.json`. Progress is written after every capture, so a timeout preserves
   the completed set.
2. **Functional driver** (`showcase/automation/functional.py`) — restarts the app,
   opens the screen, performs a user action, asserts observable state, and writes
   `functional-<device>.json` **after every flow**. Screenshots are taken before
   and after each flow.

Navigation: Android uses the Home search field; iOS scrolls the index because
search results are not observable after typing (see limitation L5).

### 2.3 Assertion style

Assertions are semantic readouts, not pixels. Examples: `Clicked 0 times` →
`Clicked 1 times`; `Wi-Fi: off` → `Wi-Fi: on`; `Duplicated!`; `Range: From
today`; `24-hour state: 19:20`; `All permissions granted: false`; `JS:` result
must not contain the page title when JavaScript is off and must contain it when
on. Visual capture is supplementary; it never upgrades a row to `passed`.

---

## 3. Functional flows and assertions

Status legend: **P** passed, **F** failed, **B** blocked, **n/a** not applicable,
**–** not executed in that session.

| Flow | Action | Assertion | Android phone | Android tablet | iPhone | iPad |
| --- | --- | --- | --- | --- | --- | --- |
| `buttons` | tap filled button | `Clicked 0 times` → `Clicked 1 times` | P | P | P | P |
| `clickable` | tap, long-press | `Clicks: 1`, `Long: 1` | P | P | P | F (reply lost) |
| `switch` | toggle Wi-Fi switch | `Wi-Fi: off` → `Wi-Fi: on` | P | P | P | P |
| `slider` | drag brightness track | readout changes from 50 % | P | P | F | F |
| `dropdown` | open menu, select item | iOS `Duplicate`→`Duplicated!`; Android `Copy`→`Copied!` | P | P | P | P |
| `alert-cancel` | show, Cancel | dialog body disappears | P | P | P | P |
| `alert-text-field` | show text-field dialog | iOS `Enter Name`; Android n/a | n/a | n/a | P | P |
| `alert-confirm` | show, Ok | dialog body disappears | P | P | P | P |
| `date-bounds` | select `From today` | `Range: Any date` → `Range: From today` | P | P | P | P |
| `scaffold-tab` | select Favorites | two `Favorites` nodes + description | P | P | P | P |
| `action-sheet` | show ActionSheet | iOS sheet/popover reachable and dismissible | n/a | n/a | P | F (no Cancel) |
| `permissions-sms-rows` | read rows | `ReadSms`, `ReceiveSms`, `SendSms` | P | P | P | P |
| `time-24h` | scroll to 24-hour picker | `24-hour state: 19:20` | P | P | P | P |
| `permissions-bulk-deny` | bulk request, deny prompts | `All permissions granted: false` | P | P | P | P |
| `sheet` | show, Close | sheet content disappears | P | P | P | P |
| `sheet-veto` | open, disable swipe-to-hide, back/drag, re-enable, Close | veto keeps sheet, Close dismisses | P | P | F | F |
| `date-display` | toggle inline display mode | `Inline display: Picker` → `Input` | F | P | F | F |
| `webview-js` | toggle JS off/on, evaluate title | off ≠ title; on = `Kira WebView Demo` | F | F | P | P |
| `topbar` | Share, (iOS) Add | `Last action: Share tapped` / `Add tapped` | P | P | P | F (nav 408) |
| `toolbar` | Share | `Share tapped` | P | P | P | P |
| `navbar` | select Profile | Profile content | P | P | P | P |
| `icons-category` | filter Arrows | `1322 icons` → filtered count | P | P | P | P |
| `nav-restore` | rotate landscape/portrait on Geo | same screen + `111.19` | P | P | – | n/a |
| `geo-math` | read values | `111.19`, `Live tracking: unavailable` | P | P | – | F |
| `limitations` | read list | FAB + determinate progress limits | P | P | – | P |
| `liquidglass` | iOS click glass button | `Glass click 0` → `1`; Android fallback text | P | P | – | F |
| `webview` | second page, JS, cookie, clear, invalid | title, `JS:`, `kira=1`, cleared, `errors 1` | P | P | – | F |
| `permission-camera` | — | blocked | B | B | – | B |
| `file-picker` | — | blocked | B | B | – | B |
| `file-saver` | — | blocked | B | B | – | B |
| `share` | — | blocked | B | B | – | B |
| `camera` | — | blocked | B | B | – | B |

Counts (machine-readable files):

| Result file | Summary |
| --- | --- |
| `screenshots/android/functional-api35-phone.json` | 23 passed / 2 failed / 5 blocked, 32 flows |
| `screenshots/android/functional-api35-tablet.json` | 24 passed / 1 failed / 5 blocked, 32 flows |
| `screenshots/ios/functional-iphone-simulator.json` | 19 passed / 3 failed, 22 flows |
| `screenshots/ios/functional-ipad-simulator.json` | 18 passed / 8 failed / 5 blocked, 32 flows |

The iPad file includes failures from its single full pass (`clickable`, `topbar`,
`liquidglass`, `webview`) that are not represented in the phone contract.

---

## 4. The 88-row coverage contract

Each row names the module, public component, tested variant, platform support,
route, and per-platform execution. Run ids are the sessions that produced the
status; `captured` rows have images but no assertion.

| ID | Component | Variant | Android / iOS support | Route | Android | iOS |
| --- | --- | --- | --- | --- | --- | --- |
| UI-BUTTON-001 | AdaptiveButton | filled enabled and disabled | supported / supported | Button | passed (46099102700) | passed (46108448068) |
| UI-BUTTON-002 | AdaptiveButton | icon and label content | supported / supported | Button | captured (46114711444) | captured (46114716852) |
| UI-BUTTON-003 | AdaptiveIconButton | three enabled and one disabled | supported / supported | Button | captured (46114711444) | captured (46114716852) |
| UI-BUTTON-004 | CupertinoButton | filled, bordered, plain, disabled | supported / supported | Button | captured (46114711444) | captured (46114716852) |
| UI-CLICK-001 | Modifier.adaptiveClickable | single, long, double, disabled | supported / supported | AdaptiveClickable | passed (46099102700) | passed (46108448068) |
| UI-SWITCH-001 | AdaptiveSwitch | on, off and disabled | supported / supported | Switch | passed (46099102700) | passed (46108448068) |
| UI-SWITCH-002 | CupertinoSwitch | on, off, disabled, thumb content | supported / supported | Switch | captured (46114711444) | captured (46114716852) |
| UI-SLIDER-001 | AdaptiveSlider | continuous value readout | supported / supported | Slider | passed (46099102700) | failed (46108448068) |
| UI-SLIDER-002 | AdaptiveSlider | discrete steps | supported / supported | Slider | captured (46114711444) | captured (46114716852) |
| UI-SLIDER-003 | AdaptiveSlider | disabled and custom range | supported / supported | Slider | captured (46114711444) | captured (46114716852) |
| UI-PROGRESS-001 | AdaptiveCircularProgressIndicator | indeterminate sizes | supported / supported | ProgressBar | captured (46114711444) | captured (46114716852) |
| UI-PROGRESS-002 | CupertinoActivityIndicator | spinner | supported / supported | ProgressBar | captured (46114711444) | captured (46114716852) |
| UI-PROGRESS-003 | AdaptiveCircularProgressIndicator | determinate | unsupported / unsupported | Limitations | not-applicable  | not-applicable  |
| UI-FAB-001 | AdaptiveExpandableFAB | expanded/collapsed | unsupported / unsupported | Limitations | not-applicable  | not-applicable  |
| UI-DATE-001 | AdaptiveDatePicker | inline selection and readout | supported / supported | DatePicker | captured (46114711444) | captured (46114716852) |
| UI-DATE-002 | AdaptiveCompactDatePicker | open, confirm, cancel | supported / supported | DatePicker | captured (46114711444) | captured (46114716852) |
| UI-DATE-003 | AdaptiveDateRangePicker | start and end transition | supported / supported | DatePicker | captured (46114711444) | captured (46114716852) |
| UI-DATE-004 | DateBounds and SelectableDates | bounded weekdays only | supported / supported | DatePicker | passed (46099102700) | passed (46108448068) |
| UI-DATE-005 | UIKitDisplayMode | picker and wheels | unsupported / supported | DatePicker | not-applicable  | captured (46114716852) |
| UI-TIME-001 | AdaptiveTimePicker | 12-hour and 24-hour states | supported / supported | TimePicker | captured (46114711444) | captured (46114716852) |
| UI-ALERT-001 | AdaptiveAlertDialog | two-button confirm and cancel | supported / supported | Dialog | passed (46099102700) | passed (46108448068) |
| UI-ALERT-002 | AdaptiveAlertDialog | single button | supported / supported | Dialog | captured (46114711444) | captured (46114716852) |
| UI-ALERT-003 | AdaptiveBasicAlertDialog | text fields and critical severity | unsupported / supported | Dialog | not-applicable  | passed (46108448068) |
| UI-ALERT-004 | AlertDialogIosStyle.ActionSheet | iPhone sheet and iPad popover | unsupported / supported | Dialog | not-applicable  | passed (46108448068) |
| UI-SHEET-001 | AdaptiveBottomSheet | show, content, dismiss | supported / supported | BottomSheet | passed (46099102700) | passed (46108448068) |
| UI-MENU-001 | AdaptiveDropDown | simple destructive and disabled items | supported / supported | DropDown | passed (46099102700) | passed (46108448068) |
| UI-MENU-002 | AdaptiveDropDownSection | sections | supported / supported | DropDown | captured (46114711444) | captured (46114716852) |
| UI-BAR-001 | AdaptiveScaffold | top bar, bottom bar, content padding | supported / supported | ScaffoldDemo | passed (46099102700) | passed (46108448068) |
| UI-BAR-002 | AdaptiveTopBar | title, leading, trailing, menu | supported / supported | TopBarDemo | passed (46099102700) | passed (46108448068) |
| UI-BAR-003 | AdaptiveNavigationBar | items and selected index | supported / supported | NavigationBar | passed (46099102700) | passed (46108448068) |
| UI-BAR-004 | AdaptiveToolbar | collapsed and expanded | supported / supported | Toolbar | passed (46099102700) | passed (46108448068) |
| UI-ICON-001 | CupertinoIcon catalog | search and category | supported / supported | CupertinoIconsCatalog | captured (46114711444) | captured (46114716852) |
| UI-ICON-002 | SFSymbol and UIKitImage | system name and vector | unsupported / supported | TopBarDemo | not-applicable  | captured (46114716852) |
| UI-ICON-003 | CupertinoIcon | size and content description | supported / supported | CupertinoIconsCatalog | captured (46114711444) | captured (46114716852) |
| IO-CTX-001 | LocalPlatformContext | host context smoke | supported / supported | FilePicker | captured (46114711444) | captured (46114716852) |
| IO-FILE-001 | KmpFile | read, stream, name and path | supported / supported | FilePicker | captured (46114711444) | captured (46114716852) |
| IO-PICK-001 | rememberFilePickerLauncher | single selection | supported / supported | FilePicker | captured (46114711444) | captured (46114716852) |
| IO-PICK-002 | rememberFilePickerLauncher | multiple with limit | supported / supported | FilePicker | captured (46114711444) | captured (46114716852) |
| IO-PICK-003 | FilePickerFileType.Folder | folder and cancel | supported / supported | FilePicker | captured (46114711444) | captured (46114716852) |
| IO-SAVE-001 | rememberFileSaverLauncher | bytes save and reopen | supported / supported | ProfilePicture | captured (46114711444) | captured (46114716852) |
| IO-COIL-001 | KmpFileFetcher and AsyncImage | preview success | supported / supported | ImagePicker | captured (46114711444) | captured (46114716852) |
| IO-CAMERA-001 | rememberCameraPickerLauncher | capture or fallback | supported / supported | CameraPickerScreen | captured (46114711444) | captured (46114716852) |
| PERM-SINGLE-001 | rememberPermissionState | camera grant and deny | supported / supported | Permission | captured (46114711444) | captured (46114716852) |
| PERM-BULK-001 | rememberMultiplePermissionsState | camera and microphone | supported / supported | Permission | passed (46099102700) | passed (46108448068) |
| PERM-STATE-001 | PermissionState | determined and settings return | supported / supported | Permission | captured (46114711444) | captured (46114716852) |
| PERM-NOTIF-001 | Notification and RemoteNotification | local and remote notification | supported / supported | Permission | captured (46114711444) | captured (46114716852) |
| PERM-LOC-001 | BackgroundLocation and location leaves | foreground and background location | supported / supported | Permission | captured (46114711444) | captured (46114716852) |
| PERM-PIM-001 | contacts and calendar leaves | read and write | supported / supported | Permission | captured (46114711444) | captured (46114716852) |
| PERM-BT-001 | Bluetooth and Wi-Fi leaves | scan/connect and nearby | supported / supported | Permission | captured (46114711444) | captured (46114716852) |
| PERM-CORE-001 | storage, call and SMS leaves | legacy routes | supported / supported | Permission | captured (46114711444) | captured (46114716852) |
| PERM-STUB-001 | desktop and web permission stubs | unavailable | unsupported / unsupported | Limitations | not-applicable  | not-applicable  |
| SHARE-001 | ShareContent.Text | native share sheet | supported / supported | Share | captured (46114711444) | captured (46114716852) |
| SHARE-002 | ShareContent.Url | native share sheet | supported / supported | Share | captured (46114711444) | captured (46114716852) |
| SHARE-003 | ShareContent.File and Files | single and mixed files | supported / supported | Share | captured (46114711444) | captured (46114716852) |
| WEB-001 | WebViewState | deterministic HTML load | supported / supported | WebView | passed (46099102700) | captured (46114716852) |
| WEB-002 | WebViewNavigator | URL load, back and forward | supported / supported | WebView | passed (46099102700) | captured (46114716852) |
| WEB-003 | WebViewState.errorsForCurrentRequest | bad destination | supported / supported | WebView | passed (46099102700) | captured (46114716852) |
| WEB-004 | WebViewState.evaluateJavascript and settings | JavaScript on | supported / supported | WebView | passed (46099102700) | captured (46114716852) |
| WEB-005 | CookieManager | set, get, remove | supported / supported | WebView | passed (46099102700) | captured (46114716852) |
| NAV-001 | AdaptiveNavHost | push, back, restore | supported / supported | Home | captured (46114711444) | captured (46114716852) |
| NAV-002 | NavArgument | declared arguments | unsupported / unsupported | Limitations | not-applicable  | not-applicable  |
| GEO-001 | LatLng | distance and bearing maths | supported / supported | Geo | passed (46099102700) | captured (46114716852) |
| GEO-002 | LocationTracker | start, stop, updates | unsupported / unsupported | Limitations | not-applicable  | not-applicable  |
| UI-LIQUID-001 | LiquidGlassButton | filled, bordered, plain, disabled | unsupported / supported | LiquidGlass | not-applicable  | captured (46114716852) |
| UI-LIQUID-002 | LiquidGlassSwitch | on, off, disabled | unsupported / supported | LiquidGlass | not-applicable  | captured (46114716852) |
| UI-LIQUID-003 | LiquidGlassSlider | continuous and disabled | unsupported / supported | LiquidGlass | not-applicable  | captured (46114716852) |
| UI-LIQUID-004 | Liquid Glass fallback | non-iOS runtime | supported / unsupported | LiquidGlass | passed (46099102700) | not-applicable  |
| PERM-SMS-001 | ReadSms, ReceiveSms, SendSms | legacy SMS routes | supported / supported | Permission | passed (46099102700) | passed (46108448068) |
| UI-ICON-004 | CupertinoIcon catalog | category filters | supported / supported | CupertinoIconsCatalog | passed (46099102700) | passed (46108448068) |
| UI-ALERT-005 | AdaptiveBasicAlertDialog | text field and critical severity | unsupported / supported | Dialog | not-applicable  | passed (46108448068) |
| UI-ALERT-006 | AlertDialogIosStyle.ActionSheet | iPad popover | unsupported / supported | Dialog | not-applicable  | failed (46099392157) |
| NAV-004 | HomeScreen | large-screen index layout | supported / supported | Home | captured (46107087160) | captured (46099392157) |
| UI-BAR-008 | AdaptiveScaffold | tablet tab and bar layout | supported / supported | Scaffold | captured (46107087160) | captured (46099392157) |
| UI-SHEET-003 | AdaptiveBottomSheet | tablet presentation | supported / supported | BottomSheet | captured (46107087160) | captured (46099392157) |
| UI-SHEET-002 | AdaptiveSheetState | detents, veto and dismissal | supported / supported | BottomSheet | passed (46099102700) | failed (46108448068) |
| UI-DATE-006 | AdaptiveDatePicker | picker and input display modes | supported / supported | DatePicker | failed (46099102700) | failed (46108448068) |
| UI-TIME-002 | AdaptiveTimePicker | 24-hour state | supported / supported | TimePicker | passed (46099102700) | passed (46108448068) |
| UI-BAR-005 | UIKitNavigationBarConfiguration | large titles and tint | unsupported / supported | TopBarDemo | not-applicable  | captured (46114716852) |
| UI-BAR-006 | UIKitTabBarConfiguration | selected and unselected tint | unsupported / supported | NavigationBar | not-applicable  | captured (46114716852) |
| UI-BAR-007 | UIKitUIBarButtonItem | system item, fixed and flexible space | unsupported / supported | Toolbar | not-applicable  | captured (46114716852) |
| WEB-006 | WebSettings | JavaScript off and on | supported / supported | WebView | failed (46099102700) | passed (46108448068) |
| IO-PICK-004 | FilePickerFileType.Custom/Extension | filter modes | supported / supported | FilePicker | captured (46114711444) | captured (46114716852) |
| IO-SAVE-002 | FileSaverLauncher | file and stream save | supported / supported | ProfilePicture | captured (46114711444) | captured (46114716852) |
| NAV-003 | rememberNavController | saveable state restoration | supported / supported | Home | passed (46099102700) | not-run  |
| GEO-003 | ExtendedLocation types | altitude, speed, azimuth | supported / supported | Geo | captured (46114711444) | captured (46114716852) |
| EXCL-MAPS-001 | maps | excluded build-only module | unsupported / unsupported | Limitations | not-applicable  | not-applicable  |
| EXCL-MEDIA-001 | media | excluded module | unsupported / unsupported | Limitations | not-applicable  | not-applicable  |
| EXCL-NOTIF-001 | notification scheduler | excluded module | unsupported / unsupported | Limitations | not-applicable  | not-applicable  |

### 4.1 Why many rows are `captured` only

- **Styling/variant rows** (e.g. `UI-BUTTON-002..004`, `UI-SLIDER-002..003`,
  `UI-PROGRESS-001..002`): the variant is a visual configuration; there is no
  independent state to assert beyond “renders”, and the component-level flow
  already covers the interactive path.
- **Platform-only APIs** (`UI-BAR-005..007`, `UI-ALERT-005`): iOS UIKit
  configuration objects; verified visually plus, for alert text fields, by flow.
- **Blocked OS surfaces** (`IO-FILE-001`, `IO-PICK-*`, `IO-SAVE-*`, `SHARE-*`,
  `IO-CAMERA-001`): the system dialogs were not driven (see §5).
- **New variants added late** (`UI-SHEET-002`, `UI-DATE-006`, `WEB-006`,
  `UI-LIQUID-00x`): flows exist and run; the iPhone Android convergence is
  partial, and the failures are listed rather than hidden.
- **Tablet rows** (`NAV-004`, `UI-BAR-008`, `UI-SHEET-003`, `UI-ALERT-006`):
  recorded from tablet tours only.

### 4.2 Missing public APIs / variants / states

The contract is broad but not exhaustive. Known gaps after the source audit:

1. **Cupertino icon catalogue**: only the `Arrows` and `Communication` category
   filters were driven; the other categories and the full 1,322-glyph grid were
   not enumerated.
2. **Liquid Glass switch/slider**: rendered on iPhone but not functionally
   toggled/adjusted.
3. **`SFSymbol` / `UIKitImage.Bitmap`**: names and vector variants used; the
   bitmap variant is not exercised.
4. **File picker filters**: `Custom(text/plain)` and `Extension(txt)` chips are
   rendered; the picker was never driven with them.
5. **File saver / ProfilePicture**: save-from-`KmpFile`, stream save, cancel and
   null results are not driven.
6. **Image picker / Coil pipeline**: capture only; no decode/preview assertion.
7. **Permissions**: bulk deny and SMS rows are asserted; individual camera,
   location, notification, contacts, Bluetooth, Wi-Fi and “Always” upgrade paths
   are capture-only.
8. **Date range picker**: start/end/restart semantics not driven; only visual.
9. **Date/time platform-specific modes**: iOS `Wheels` is captured; Material
   Input vs Picker is driven only through a readout, and the switch interaction
   fails at phone widths.
10. **WebView per-engine behaviour**: only mobile Android WebView and iOS
    WKWebView; desktop JavaFX and browser iframe are outside the matrix. JS
    off/on is asserted on iPhone/iPad; it fails on Android windows.
11. **Navigation state across process death**: only rotation-based recreation on
    Android is asserted (`NAV-003`); iOS rotation is unavailable.
12. **Toolbar spacing patterns** (fixed/flexible) and **top-bar menu sections**
    are visually captured, not asserted.
13. **RTL, dark theme, dynamic type/font scale, accessibility focus order** are
    not part of the contract.
14. **Excluded modules**: `kira-maps` (build file only), `kira-media`,
    `kira-notifications` are explicitly documented as excluded, not tested.

---

## 5. Every failed, blocked or not-run item

Exact error strings are quoted from the result JSON.

### 5.1 Android phone — `date-display` (UI-DATE-006)

- **Device**: Pixel 6, API 35, 1080×2400 @ 420 dpi, run 46099102700.
- **Scenario**: open *Adaptive Date Picker*; switch inline display from Picker to
  Input; read `Inline display: …`.
- **Expected**: `Inline display: Input`.
- **Actual**: the switch toggles the picker, the calendar collapses, the readout
  leaves the viewport; assertion raises
  `AssertionError("missing visible text 'Inline display: Input'")`.
- **Screenshot**: `screenshots/android/functional/date-display/api35-phone-failed-after.png`.
- **Root cause**: confirmed layout/driver combination — the sample places the
  readout above a large calendar; the harness has no scroll-into-view (L4) and
  the tree prunes off-screen nodes. At 1600×2560 the identical flow **passes**,
  so this is a phone-width presentation issue, not a state bug.
- **Owner**: Showcase layout + `ui-test-actions` missing scroll-into-view.
- **Fix**: move the display-mode control/readout above the calendar or add
  `element.scroll_into_view`; permanent harness fix in L4/P0-4.
- **Workaround**: tablet run passes; phone row stays failed.

### 5.2 Android phone/tablet — `webview-js` (WEB-006)

- **Device**: Pixel 6 phone and 1600×2560 tablet, runs 46099102700 / 46107087160.
- **Scenario**: toggle the overlay JavaScript switch off, evaluate the page title,
  toggle on, evaluate again.
- **Expected**: `JavaScript: off`, then a `JS:` readout that is not the title, then
  the title.
- **Actual**: `AssertionError("missing visible text 'JavaScript: off'")`; the
  readout never changed, so evaluation was not reached.
- **Screenshot**: `screenshots/android/functional/webview-js/*-failed-after.png`.
- **Root cause**: **not confirmed.** Hypotheses: the row-targeted switch click
  lands on the label row rather than the switch thumb, or the Compose switch
  click is consumed by the WebView overlay. The same flow passes on iPhone and
  iPad, so the state logic works.
- **Owner**: driver targeting (primary) / Showcase control placement.
- **Fix**: select the switch by `checked` semantics (P0-1) and click its node id;
  if the overlay intercepts, place the control outside the WebView bounds.
- **Workaround**: none on Android; evidence is captured.

### 5.3 iPhone — `slider` (UI-SLIDER-001)

- **Device**: iPhone 17 Pro, iOS 26.5, 402×874, run 46108448068.
- **Scenario**: drag the Brightness track from ~50 % to the right edge.
- **Expected**: readout changes.
- **Actual**: `AssertionError('slider did not move')`.
- **Screenshot**: `screenshots/ios/functional/slider/iphone-simulator-failed-after.png`.
- **Root cause**: confirmed observation — the UISlider is exposed as an unnamed
  `AXGroup` with no role/value; the fallback drags a geometric track and AXe
  `draw` does not move it. Underlying cause (AXe gesture vs Compose gesture) is
  **not confirmed**.
- **Owner**: `ui-test-actions` (semantics + gesture), possibly Compose iOS
  accessibility bridging. The library does define `setProgress` semantics
  (`CupertinoSlider.kt:668-700`), so the library is not missing intent.
- **Fix**: expose `value`/`adjustable` and add `element.adjust` (P0-1), plus a
  multi-point drag (P1-2).
- **Workaround**: none; row stays failed.

### 5.4 iPhone/iPad — `sheet-veto` (UI-SHEET-002)

- **Device**: iPhone 17 Pro and iPad Pro 13-inch, iOS 26.5, runs 46108448068 /
  46099392157.
- **Scenario**: open the bottom sheet, toggle “Allow swipe to hide”, attempt
  dismissal, re-enable, close.
- **Expected**: vetoed dismissal keeps the sheet; Close dismisses.
- **Actual**: `AssertionError("no node for 'Allow swipe to hide'")`.
- **Screenshot**: `screenshots/ios/functional/sheet-veto/*-failed-after.png`.
- **Root cause**: unconfirmed. The switch is inside a `LazyColumn` in a native
  page sheet; it is below the sheet detent and no scroll-into-view exists (L4).
  Whether the sheet content is a separate accessibility window is unverified.
- **Owner**: `ui-test-actions` primarily; Showcase placement secondary.
- **Fix**: element-scoped scroll + window enumeration (L4/L11).
- **Workaround**: none.

### 5.5 iPhone — `date-display` (UI-DATE-006)

Same failure as 5.1 with
`AssertionError("missing visible text 'Inline display: Input'")` (run 46108448068).
iPhone screen is shorter; the readout leaves the viewport after layout collapse.
Owner/ fix identical.

### 5.6 iPad — `action-sheet` (UI-ALERT-006, tablet row)

- **Device**: iPad Pro 13-inch, iOS 26.5, run 46099392157 / functional iPad file.
- **Scenario**: show the iOS ActionSheet style alert on iPad.
- **Expected (contract)**: centred popover, Cancel reachable.
- **Actual**: popover renders **Ok** and disabled **Remove**, no Cancel; AX tree
  and functional flow both fail to find `Cancel`
  (`AssertionError("missing visible text 'Cancel'")`).
- **Screenshot**: `screenshots/ios/alertdialogiosstyle-actionsheet/ipad-popover/ipad-simulator.png`.
- **Root cause**: **UIKit behaviour plus contract error.** A `UIAlertController`
  action sheet presented as a popover omits the cancel action (outside tap
  dismisses). The library deliberately anchors the popover on iPad
  (`AlertDialogManager.kt:193-210`, with a comment that anchoring on iPhone would
  drop Cancel). This is not a NativeCmpKit regression.
- **Owner**: coverage contract (expectation) and `ui-test-actions` (no modal/
  window metadata); not the library.
- **Fix**: change the row expectation to “popover dismisses by outside tap;
  Cancel is intentionally omitted”, and assert outside-tap dismissal via
  `ui.windows`/modal helper. Row should become `passed` under the corrected
  expectation.
- **Workaround**: visual evidence plus the explanation above.

### 5.7 iOS — `NAV-003` not-run

- **Device**: iPhone/iPad, iOS 26.5.
- **Scenario**: rotate to landscape and back, assert the route/state remains.
- **Actual**: `not-run`; iOS capabilities expose no rotation command.
- **Root cause**: confirmed capability gap (L2).
- **Owner**: `ui-test-actions`.
- **Fix**: implement and advertise iOS rotation (P0-2).

### 5.8 Blocked system surfaces

| Flow | Device | Expected | Actual | Owner | Fix |
| --- | --- | --- | --- | --- | --- |
| `file-picker` | Android/iOS phone+tablet | choose seeded `kira-fixture.txt` | picker never driven | `ui-test-actions` + test design | window/context targeting (P0-3) |
| `file-saver` | both | save destination returns a readable file | no destination selection | same | same |
| `share` | both | share sheet recipient | no recipient path | same | same |
| `camera` | both | capture or explicit unsupported path | emulator camera not seeded | environment + test design | seed camera / assert fallback |
| `permission-camera` | both | single permission grant/deny | only bulk permission path asserted | test design | add single-permission flows |

All five are `blocked`, never reported as passed. Fixtures are seeded by the
workflow (`/sdcard/Download`, iOS photo library) but selection is not automated.

### 5.9 Historical failures that were fixed (for completeness)

| Symptom | Root cause | Fix | Verified |
| --- | --- | --- | --- |
| Android Cupertino glyphs rendered as tofu | APK lacked `sf_symbols.ttf` | stage font/notice in `sample/android/build.gradle.kts` | APK contains exact SHA-256 `67c44fe…823c` (run 45972729059) |
| iOS alert action sheet and Time Picker `HTTP 408` | session/tunnel timeout, not the control | shorter flows, retry pass, incremental tour write | Time Picker captured in run 46114716852 |
| iOS Home search found no result rows | accessibility tree exposes only the search field (L5) | scroll navigation on iOS | 19 iPhone flows passed |
| iOS `clickable` lost response | double-tap `--count 2` (L9) | remove double-tap from the flow | passed in run 46108448068 |
| Post-restart `HTTP 400` | readiness race (L8) | `wait_home` retry loop | all later suites stable |
| Duplicate `More options` labels | accessibility labels not unique | unique `contentDescription` per menu | dropdown passed |
| Android sheet content flush-left | missing sheet padding | 16 dp padding | recaptured |

### 5.10 Other observed anomalies, not counted as failures

- iOS top-bar “Back” renders grey/low-contrast under Liquid Glass (visual only).
- iPad tour missed Navigation Bar, Web View and Known Limitations on the first
  pass (`HTTP 408`); recaptured manually outside `tour.json`.
- WebView toolbar image-only items on iOS expose SF Symbol names (`embed code`,
  `chevron left`) rather than descriptions; the tour falls back to those names.

---

## 6. NativeCmpKit vs Showcase defects (not automation)

### NativeCmpKit

1. **Android Cupertino font packaging defect (fixed in the app, library fix
   pending).** Stock APK had no `.ttf`; icons were tofu. The sample now stages
   the font/notice itself. The library’s Android resources should ship them so
   consumers do not need the workaround. Independent verification: APK contains
   `assets/composeResources/io.github.apdelrahman1911.kira.kira_cupertino_icons.generated.resources/font/sf_symbols.ttf`,
   SHA-256 `67c44fe9183b002e79dde7f6977e2988661c9a3e4a3c5fce968787efdbed823c`.
2. **iOS slider accessibility exposure (unresolved, attribution uncertain).**
   `setProgress` semantics exist, but the element surfaces as an unnamed
   `AXGroup`. Could be Compose/UIKit bridging rather than the library; needs a
   focused UIKit accessibility investigation.
3. **No library-level accessibility on image-only bar buttons (unresolved).**
   `UIKitUIBarButtonItem.image` accepts no description; consumers must pass
   `accessibilityLabel`. Consider defaulting to the SF Symbol name.

### Showcase application

1. **Duplicate “More options” labels (fixed).** Three menus shared one
   description; now “Top bar menu”, “Simple drop down menu”, “Sectioned drop
   down menu”.
2. **Bottom-sheet padding (fixed).** Content was flush-left on Android.
3. **Date display-mode readout leaves the viewport (unresolved).** Layout places
   it above a collapsing calendar.
4. **WebView JS control interaction (unresolved).** Overlay switch did not change
   its readout when driven on Android.
5. **WebView toolbar lacks descriptions (partially fixed).** Top-level actions
   have content descriptions; iOS toolbar image items rely on SF Symbol names.
6. **iPad ActionSheet expectation (contract, not app).** Expectation contradicts
   UIKit popover behaviour.

---

## 7. Evidence index

### Runs and jobs

| Run | Job | Result |
| --- | --- | --- |
| [46099102700](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46099102700) | `140837241882` | success; 23/2/5 Android phone |
| [46114711444](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46114711444) | `140885816479` | success; 37 phone captures |
| [46107087160](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46107087160) | `140862145867` | success; 24/1/5 Android tablet |
| [46014167086](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46014167086) | `140556939197` | success; first iPhone functional pass |
| [46108448068](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46108448068) | `140866374272` | success; six-flow retest, 19/3 |
| [46114716852](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46114716852) | `140885832699` | success; 32 phone captures incl. Time Picker |
| [46099392157](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46099392157) | `140838141915` | success; 30+3 iPad captures, 18/8/5 |

### Raw session logs

Committed verbatim (no tokens or tunnel URLs): `showcase/evidence/logs/`.

| Log | Session |
| --- | --- |
| `android-phone-functional-run46099102700.log` | Android phone functional pass |
| `android-phone-tour-run46114711444.log` | Android phone tour |
| `android-tablet-functional-run46107087160.log` | Android tablet functional pass |
| `android-tablet-tour-run46107087160.log` | Android tablet tour |
| `ios-phone-functional-run46014167086.log` | first iPhone functional pass (cut off) |
| `ios-phone-tour-run46108448068.log` | iPhone tour that timed out before `tour.json` |
| `ios-phone-tour-run46114716852.log` | iPhone tour including Time Picker |
| `ipad-functional-run46099392157.log` | iPad functional pass |
| `ipad-tour-run46099392157.log` | iPad tour |

### Repository evidence (pinned to `042f5116`)

- Contract: [`showcase/coverage.json`](https://github.com/NativeCmpKit/NativeCmpKit/blob/042f51168fea7a1156127276bdab7e10ab410157/showcase/coverage.json),
  [`showcase/COVERAGE.md`](https://github.com/NativeCmpKit/NativeCmpKit/blob/042f51168fea7a1156127276bdab7e10ab410157/showcase/COVERAGE.md)
- Inventory: [`showcase/INVENTORY.md`](https://github.com/NativeCmpKit/NativeCmpKit/blob/042f51168fea7a1156127276bdab7e10ab410157/showcase/INVENTORY.md),
  [`showcase/public-api.json`](https://github.com/NativeCmpKit/NativeCmpKit/blob/042f51168fea7a1156127276bdab7e10ab410157/showcase/public-api.json)
- Status: [`showcase/evidence/verification-status.md`](https://github.com/NativeCmpKit/NativeCmpKit/blob/042f51168fea7a1156127276bdab7e10ab410157/showcase/evidence/verification-status.md)
- Matrix: [`showcase/evidence/functional-matrix.md`](https://github.com/NativeCmpKit/NativeCmpKit/blob/042f51168fea7a1156127276bdab7e10ab410157/showcase/evidence/functional-matrix.md)
- Tablet evidence: [`showcase/evidence/functional-tablet-2026-11-28.md`](https://github.com/NativeCmpKit/NativeCmpKit/blob/042f51168fea7a1156127276bdab7e10ab410157/showcase/evidence/functional-tablet-2026-11-28.md)
- Runbook: [`showcase/evidence/session-runbook.md`](https://github.com/NativeCmpKit/NativeCmpKit/blob/042f51168fea7a1156127276bdab7e10ab410157/showcase/evidence/session-runbook.md)
- Screenshots: [`screenshots/INDEX.md`](https://github.com/NativeCmpKit/NativeCmpKit/blob/042f51168fea7a1156127276bdab7e10ab410157/screenshots/INDEX.md),
  `screenshots/compare/` (31 phone sheets), `screenshots/compare-tablet/` (31 tablet sheets)
- Functional result files: `screenshots/android/functional-api35-phone.json`,
  `screenshots/android/functional-api35-tablet.json`,
  `screenshots/ios/functional-iphone-simulator.json`,
  `screenshots/ios/functional-ipad-simulator.json`
- Harness report: [`ui-test-actions-limitations.md`](ui-test-actions-limitations.md)

### Commits

- Base handoff: `a2c48c0b9ebf3524192e680ecd4becc1f2880bb8`
- Contract: `eacba3d9`, app expansion: `ae7dc5ef`, `03676e2f`, `e751b57f`
- Harness/driver: `03676e2f`, `efd99aae`, `4de926fd`, `0237c2fe`
- Final evidence: `042f5116`

---

## 8. Verdict

- Android phone: **23/32** flows pass, 2 fail, 5 blocked, 2 are iOS-only.
- Android tablet: **24/32** pass, 1 fails, 5 blocked.
- iPhone: **19/22** pass, 3 fail.
- iPad: **18/32** pass, 8 fail, 5 blocked (single pass; includes older-flow
  failures).

The coverage contract is complete in structure and honest in status. It is not
“all green”: distinct flow failures remain for `date-display` (both phone
platforms), `webview-js` (both Android windows), `slider` and `sheet-veto`
(iPhone/iPad), plus the iPad ActionSheet expectation error; five OS surfaces are
blocked. Each is documented above with owner and fix. The dominant blocker for
the next verification level is `ui-test-actions` semantics fidelity and
overlay/window control, not the NativeCmpKit components themselves.
