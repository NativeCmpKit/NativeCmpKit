# Public API and component inventory

Source baseline: `a2c48c0b9ebf3524192e680ecd4becc1f2880bb8`.
Raw declaration extract: [public-api.json](public-api.json) (759 declarations,
including expect/actual duplicates and test sources). This page is the curated
component/variant view; the executable matrix is [coverage.json](coverage.json).

Status meanings:

- **passed** — a real UI action changed observable state and the assertion passed.
- **captured** — a live device screenshot exists; the behavior may not be driven.
- **pending** — implemented in the worktree, not yet built/captured.
- **blocked** — requires system UI, a seeded external file, or an unavailable host.
- **unsupported** — public API is absent/internal or the module is excluded.

## kira-core / context

| Public API | Variants / states | Android | iOS | Desktop | Web | Screen | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PlatformContext` / `LocalPlatformContext` | Android Context alias; opaque sentinel elsewhere | supported | supported | sentinel | sentinel | File Picker readout | captured |
| `ExperimentalKiraApi`, `InternalKiraApi`, `ExperimentalKiraUiApi` | opt-in markers | supported | supported | supported | supported | n/a | source-reviewed |

## kira-ui — controls

| Public API | Variants / states | Android | iOS | Desktop | Web | Screen | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `AdaptiveButton` | filled, disabled, custom shape/padding/colors, `liquidGlassColors` | supported | supported (Cupertino; Liquid Glass 26+) | supported | supported | Adaptive Buttons | captured; counter passed on Android |
| `AdaptiveIconButton` | enabled/disabled, custom colors, Liquid Glass on iOS 26 | supported | supported | supported | supported | Adaptive Buttons | captured |
| `CupertinoButton` | filled, bordered, plain, disabled | supported | supported | supported | supported | Adaptive Buttons | captured |
| `LiquidGlassButton` + colors/defaults | filled, bordered, plain, disabled | not public | supported on iOS 26 | not public | not public | Liquid Glass | captured; click asserted on iPhone |
| `Modifier.adaptiveClickable` | single, long, double, disabled, labels, role, shape, haptic | ripple | press scale 0.96 | ripple | ripple | Adaptive Clickable | captured |
| `AdaptiveSwitch` | on/off, disabled, thumbContent, colors | Material | Cupertino <26; Liquid Glass 26+ (drops thumb/colors) | Material | Material | Adaptive Switch | captured; toggled (on) on Android and iPhone |
| `CupertinoSwitch` | on/off, disabled, thumbContent | supported | supported | supported | supported | Adaptive Switch | captured |
| `LiquidGlassSwitch` + colors/defaults | on/off, disabled | not public | supported on iOS 26 | not public | not public | Liquid Glass | captured on iPhone; toggle not driven |
| `AdaptiveSlider` | continuous, range, steps, disabled, callback | Material | Cupertino <26; Liquid Glass 26+ (drops steps) | Material | Material | Adaptive Slider | captured |
| `LiquidGlassSlider` + colors/defaults | continuous, disabled | not public | supported on iOS 26 | not public | not public | Liquid Glass | captured on iPhone; drag not driven |
| `AdaptiveCircularProgressIndicator` | indeterminate sizes/color/stroke | supported | Cupertino spinner | supported | supported | Adaptive Progress Bar | captured; determinate unsupported |
| `CupertinoActivityIndicator` | spinner, color, size | supported | supported | supported | supported | Adaptive Progress Bar | captured |
| `AdaptiveExpandableFAB` / `UIKitExpandableFABItem` | expanded/collapsed | internal | internal | internal | internal | Known Limitations | unsupported (not public) |

## kira-ui — date and time

| Public API | Variants / states | Android | iOS | Desktop | Web | Screen | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `AdaptiveDatePicker` | inline, Material picker/input, iOS Picker/Wheels, bounds/rules, disabled | supported | supported | supported | supported | Adaptive Date Picker | captured |
| `AdaptiveCompactDatePicker` | open, confirm, cancel, enabled, placeholder | supported | supported | supported | supported | Adaptive Date Picker | captured |
| `AdaptiveDateRangePicker` | start/end/restart, bounded, Material fallback <16.2 | supported | supported | supported | supported | Adaptive Date Picker | captured |
| `AdaptiveDatePickerState` / `AdaptiveDateRangePickerState` | selected values, display mode, bounds, saver | supported | supported | supported | supported | Adaptive Date Picker | captured; state restoration not driven |
| `DateBounds`, `SelectableDates.and`, `UIKitDisplayMode` | min/max, combined rule, picker/wheels | supported | supported | supported | supported | Adaptive Date Picker | captured |
| `AdaptiveTimePicker` / state | 12h/24h, layoutType, Material/time wheels | supported | supported | supported | supported | Adaptive Time Picker | Android captured; iPhone 24-hour readout asserted; iOS visual capture pending |
| `AdaptiveTimePickerState.is24Hour` | accepted but ignored by UIKit | n/a | format follows locale | n/a | n/a | Adaptive Time Picker | documented unsupported on iOS |

## kira-ui — presentation

| Public API | Variants / states | Android | iOS | Desktop | Web | Screen | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `AdaptiveAlertDialog` | one/two button, confirm/dismiss, preferred, destructive | Material | UIAlertController | Material | Material | Alert Dialog | captured; Cancel and Ok asserted on Android and iPhone |
| `AdaptiveBasicAlertDialog` | alert/action sheet, severity, text fields, secure/number pad | Material content | UIKit properties | Material content | Material content | Alert Dialog | captured; text-field and action-sheet asserted on iPhone |
| `AlertDialogIosStyle.ActionSheet` | iPhone sheet, iPad centred popover | n/a | supported | n/a | n/a | Alert Dialog | iPhone sheet asserted; iPad popover **pending** |
| `AdaptiveBottomSheet` / `AdaptiveSheetState` | detents, drag handle, veto, insets, dismissal | Material | page sheet; insets/shape ignored | Material | Material | Bottom Sheet | captured |
| `AdaptiveDropDown` / `Item` / `Section` | simple, sections, disabled, destructive, iOS anchor parent | Material | UIMenu | Material | Material | Drop Down | captured |
| `UIKitUIBarButtonItem` + system items | title/image/system/flexible/fixed/withMenu | n/a | supported | n/a | n/a | Top Bar / Toolbar | captured; title, image, system Add and spacing driven |

## kira-ui — bars, navigation, icons

| Public API | Variants / states | Android | iOS | Desktop | Web | Screen | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `AdaptiveScaffold` | top/bottom bars, FAB, insets | Material | Material + native bar padding | Material | Material | Adaptive Scaffold | captured |
| `AdaptiveTopBar` | title/leading/trailing, large titles, menu | Material | UINavigationBar | Material | Material | Adaptive Top Bar | captured; Share and Add readouts asserted on iPhone |
| `AdaptiveNavigationBar` | 3/5 items, selected index, tint | Material | UITabBar | Material | Material | Adaptive Navigation Bar | captured |
| `AdaptiveToolbar` | expanded, leading/trailing, iOS items | Material | UIToolbar (empty items renders nothing) | Material | Material | Adaptive Toolbar | captured |
| `UIKitNavigationBarConfiguration` / `UIKitTabBarConfiguration` | large titles, translucent, tints | n/a | supported | n/a | n/a | Top Bar / Navigation Bar | captured visually |
| `CupertinoIcon` / `CupertinoIcons` | 1,322 codepoints, size, tint, label | font staged; renders | renders | renders | renders | Cupertino Icons | overview; Arrows filter asserted on Android and iPhone |
| `SFSymbol` / `UIKitImage` | SystemName, Vector, Bitmap | names only | UIImage | names only | names only | Top Bar / Toolbar | captured; Bitmap variant pending |
| `CupertinoIndication` | press alpha 0.33 | internal | internal | internal | internal | n/a | unsupported (not public) |

## kira-io / pickers / Coil / camera

| Public API | Variants / states | Android | iOS | Desktop | Web | Screen | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `KmpFile` | exists, readByteArray, source, name, path, file/directory | content URI | NSURL/temp copy | File | File/basename | File Picker | screen captured; seeded read **blocked** |
| `rememberFilePickerLauncher` | Single, Multiple(max), Folder, Custom, Extension, settings | SAF/photo picker | UIDocumentPicker/PHPicker | rfd | input file | File Picker | screen captured; real picker **blocked** |
| `rememberFileSaverLauncher` | bytes, KmpFile, baseName/extension | CreateDocument | export picker | save dialog | download | File Saver | screen captured; save **blocked** |
| `KmpFileFetcher` / Coil | stream, bounds, success/error | supported | supported | supported | supported | Image Picker | screen captured; seeded image **blocked** |
| `rememberCameraPickerLauncher` | launch, unavailable, simulator fallback | camera intent | camera/photo fallback | no-op | no-op | Camera Picker | screen captured; capture **blocked** |
| `ImageRepresentationMode` | Current, Compatible | ignored | supported | ignored | ignored | File Picker | source-reviewed |

## kira-permissions — 28 public permissions

All rows render on the Permissions screen. Android and iOS status is functional
only after an OS request; the current evidence is screen-level unless noted.

| Permission | Android mapping | iOS helper | Status |
| --- | --- | --- | --- |
| `Call` | `CALL_PHONE` | granted | captured |
| `ReadSms` | `READ_SMS` | NotGranted | row rendered; asserted on Android and iPhone |
| `ReceiveSms` | `RECEIVE_SMS` | NotGranted | row rendered; asserted on Android and iPhone |
| `SendSms` | `SEND_SMS` | granted | row rendered; asserted on Android and iPhone |
| `Camera` | `CAMERA` | AVCapture video | captured; OS dialog **blocked** |
| `RecordAudio` | `RECORD_AUDIO` | AVCapture audio | captured; OS dialog **blocked** |
| `Gallery` | legacy/media images | Photos | captured; **granted=true anomaly** |
| `ReadImage` | `READ_MEDIA_IMAGES` | Photos | captured |
| `ReadVideo` | `READ_MEDIA_VIDEO` | Photos | captured |
| `ReadAudio` | `READ_MEDIA_AUDIO` | granted | captured |
| `ReadStorage` | legacy storage | granted | captured |
| `WriteStorage` | legacy storage | granted | captured |
| `FineLocation` | fine location | when-in-use | captured |
| `CoarseLocation` | coarse location | when-in-use | captured |
| `BackgroundLocation` | background location | Always helper | captured |
| `Notification` | `POST_NOTIFICATIONS` (33+) | local notifications | captured |
| `RemoteNotification` | no Android mapping (Granted) | APNs | captured |
| `BluetoothLe` | legacy Bluetooth | CoreBluetooth | captured |
| `BluetoothScan` | scan (31+) | CoreBluetooth | captured |
| `BluetoothConnect` | connect (31+) | CoreBluetooth | captured |
| `BluetoothAdvertise` | advertise (31+) | CoreBluetooth | captured |
| `ReadContacts` | `READ_CONTACTS` | Contacts | captured |
| `WriteContacts` | `WRITE_CONTACTS` | Contacts | captured |
| `ReadCalendar` | `READ_CALENDAR` | events-only | captured |
| `WriteCalendar` | `WRITE_CALENDAR` | events-only | captured |
| `WifiAccessState` | `ACCESS_WIFI_STATE` | local-network probe | captured |
| `WifiChangeState` | `CHANGE_WIFI_STATE` | local-network probe | captured |
| `WifiNearbyDevices` | `NEARBY_WIFI_DEVICES` | local-network probe | captured |

Desktop and web permission states are permanent `Denied(false)` stubs; the
Known Limitations screen states this. No ordered/sequential request API exists.

## kira-share / kira-webview

| Public API | Variants / states | Android | iOS | Desktop | Web | Screen | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `rememberShareLauncher` / `ShareContent` | Text, Url, File, Files, subject | chooser; Success=opened | UIActivityViewController | clipboard/open/macOS picker | Web Share/clipboard | Content Sharing | screen captured; sheet **blocked** |
| `WebView` / `WebViewState` | Url, Data, NavigatorOnly; title/url/loading/errors | android.webkit | WKWebView | JavaFX | iframe | Web View | captured; JS/cookie/invalid passed on Android |
| `WebViewNavigator` | loadUrl/loadHtml/back/forward/reload/stop | supported | supported | supported | supported | Web View | Android second page/JS/cookies asserted; iOS JS/cookies captured; iOS second page **pending** |
| `WebSettings` | JavaScript off/on, platform knobs | supported | supported | supported | supported | Web View | JS toggle not driven |
| `CookieManager` / `Cookie` | set/get/removeAll | supported | supported | generic handler refusal | host cookies | Web View | Android cookie round-trip captured; iOS captured |

## kira-navigation / kira-geo

| Public API | Variants / states | Android | iOS | Desktop | Web | Screen | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `rememberNavController` / `AdaptiveNavHost` | routes, push/pop, saveable state | AndroidX back | in-app only | in-app only | in-app only | app shell | app navigation exercised |
| `NavArgument` / `AdaptiveNavType` / `AdaptiveBundle` | declarations, typed defaults | supported | supported | supported | supported | n/a | arguments are declarations only |
| Nested graphs / deep links / value arguments | not implemented | — | — | — | — | Known Limitations | unsupported |
| `LatLng` | distanceTo, getAngleTo | common | common | common | common | Geo Maths | captured; values asserted |
| `LocationTracker` | start/stop, State<LatLng>, ExtendedLocation | bind required; public states stay 0 | no-op | no-op | no-op | Geo Maths | unsupported in practice |
| `ExtendedLocation` / `Speed` / `Azimuth` / `Altitude` | data types | common | common | common | common | Geo Maths | data inspected |

## Excluded or build-only modules

| Module | State | Evidence |
| --- | --- | --- |
| `kira-maps` | build file only, no public API | `settings.gradle.kts`; only `build.gradle.kts` |
| `kira-media` | on disk, not included in settings | no active build |
| `kira-notifications` scheduler | on disk, not included | stale build + un-packaged iOS experiment |
| notification **permission** | included and supported | `kira-permissions/notifications` |

## Evidence status

- Android: 34 canonical PNGs, 53 rows captured, 1 passed, 12 not-applicable.
- iOS: 31 canonical PNGs, 57 rows captured, 1 not-run (Time Picker), 8 not-applicable.
- 31 paired sheets in `screenshots/compare/`.
- Real functional suite: `showcase/automation/functional.py` (implemented; run
  pending the next Android/iOS sessions).
- Only the Android button-counter flow is currently a functional pass; every
  other row is captured/visual unless explicitly marked otherwise.
