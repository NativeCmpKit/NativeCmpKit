# Showcase coverage

Base: `a2c48c0b9ebf3524192e680ecd4becc1f2880bb8` on `feature/showcase-ui-verification`.

The authoritative machine-readable manifest is [coverage.json](coverage.json).
Regenerate both files with `python3 showcase/generate_coverage.py`.

Statuses: **passed** = a functional flow asserted observable state; **captured** = a reviewed screenshot only; **failed** = flow ran and the assertion failed; **not-run** = no hosted evidence yet; **not-applicable** = the API or sample section does not exist on that platform.

- android: 38 captured, 2 failed, 20 not-applicable, 3 not-run, 25 passed
- ios: 45 captured, 4 failed, 9 not-applicable, 11 not-run, 19 passed

Functional flow evidence lives under [evidence/](evidence/) and `screenshots/<platform>/functional-<device>.json`.

| ID | Component | Variant | Android | iOS | Route | Android run | iOS run |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UI-BUTTON-001 | AdaptiveButton | filled enabled and disabled | supported | supported | Button | passed (46099102700) | passed (46108448068) |
| UI-BUTTON-002 | AdaptiveButton | icon and label content | supported | supported | Button | captured (45957524569) | captured (45968953555) |
| UI-BUTTON-003 | AdaptiveIconButton | three enabled and one disabled | supported | supported | Button | captured (45957524569) | captured (45968953555) |
| UI-BUTTON-004 | CupertinoButton | filled, bordered, plain, disabled | supported | supported | Button | captured (45957524569) | captured (45968953555) |
| UI-CLICK-001 | Modifier.adaptiveClickable | single, long, double, disabled | supported | supported | AdaptiveClickable | passed (46099102700) | passed (46108448068) |
| UI-SWITCH-001 | AdaptiveSwitch | on, off and disabled | supported | supported | Switch | passed (46099102700) | passed (46108448068) |
| UI-SWITCH-002 | CupertinoSwitch | on, off, disabled, thumb content | supported | supported | Switch | captured (45957524569) | captured (45968953555) |
| UI-SLIDER-001 | AdaptiveSlider | continuous value readout | supported | supported | Slider | passed (46099102700) | failed (46108448068) |
| UI-SLIDER-002 | AdaptiveSlider | discrete steps | supported | supported | Slider | captured (45957524569) | captured (45968953555) |
| UI-SLIDER-003 | AdaptiveSlider | disabled and custom range | supported | supported | Slider | captured (45957524569) | captured (45968953555) |
| UI-PROGRESS-001 | AdaptiveCircularProgressIndicator | indeterminate sizes | supported | supported | ProgressBar | captured (45957524569) | captured (45968953555) |
| UI-PROGRESS-002 | CupertinoActivityIndicator | spinner | supported | supported | ProgressBar | captured (45957524569) | captured (45968953555) |
| UI-PROGRESS-003 | AdaptiveCircularProgressIndicator | determinate | unsupported | unsupported | Limitations | not-applicable | not-applicable |
| UI-FAB-001 | AdaptiveExpandableFAB | expanded/collapsed | unsupported | unsupported | Limitations | not-applicable | not-applicable |
| UI-DATE-001 | AdaptiveDatePicker | inline selection and readout | supported | supported | DatePicker | captured (45957524569) | captured (45968953555) |
| UI-DATE-002 | AdaptiveCompactDatePicker | open, confirm, cancel | supported | supported | DatePicker | captured (45957524569) | captured (45968953555) |
| UI-DATE-003 | AdaptiveDateRangePicker | start and end transition | supported | supported | DatePicker | captured (45957524569) | captured (45968953555) |
| UI-DATE-004 | DateBounds and SelectableDates | bounded weekdays only | supported | supported | DatePicker | passed (46099102700) | passed (46108448068) |
| UI-DATE-005 | UIKitDisplayMode | picker and wheels | unsupported | supported | DatePicker | not-applicable | captured (45968953555) |
| UI-TIME-001 | AdaptiveTimePicker | 12-hour and 24-hour states | supported | supported | TimePicker | captured (45957524569) | not-run |
| UI-ALERT-001 | AdaptiveAlertDialog | two-button confirm and cancel | supported | supported | Dialog | passed (46099102700) | passed (46108448068) |
| UI-ALERT-002 | AdaptiveAlertDialog | single button | supported | supported | Dialog | captured (45957524569) | captured (45968953555) |
| UI-ALERT-003 | AdaptiveBasicAlertDialog | text fields and critical severity | unsupported | supported | Dialog | not-applicable | passed (46108448068) |
| UI-ALERT-004 | AlertDialogIosStyle.ActionSheet | iPhone sheet and iPad popover | unsupported | supported | Dialog | not-applicable | passed (46108448068) |
| UI-SHEET-001 | AdaptiveBottomSheet | show, content, dismiss | supported | supported | BottomSheet | passed (46099102700) | passed (46108448068) |
| UI-MENU-001 | AdaptiveDropDown | simple destructive and disabled items | supported | supported | DropDown | passed (46099102700) | passed (46108448068) |
| UI-MENU-002 | AdaptiveDropDownSection | sections | supported | supported | DropDown | captured (45957524569) | captured (45968953555) |
| UI-BAR-001 | AdaptiveScaffold | top bar, bottom bar, content padding | supported | supported | ScaffoldDemo | passed (46099102700) | passed (46108448068) |
| UI-BAR-002 | AdaptiveTopBar | title, leading, trailing, menu | supported | supported | TopBarDemo | passed (46099102700) | passed (46108448068) |
| UI-BAR-003 | AdaptiveNavigationBar | items and selected index | supported | supported | NavigationBar | passed (46099102700) | passed (46108448068) |
| UI-BAR-004 | AdaptiveToolbar | collapsed and expanded | supported | supported | Toolbar | passed (46099102700) | passed (46108448068) |
| UI-ICON-001 | CupertinoIcon catalog | search and category | supported | supported | CupertinoIconsCatalog | captured (45973585586) | captured (45968953555) |
| UI-ICON-002 | SFSymbol and UIKitImage | system name and vector | unsupported | supported | TopBarDemo | not-applicable | captured (45968953555) |
| UI-ICON-003 | CupertinoIcon | size and content description | supported | supported | CupertinoIconsCatalog | captured (45973585586) | captured (45968953555) |
| IO-CTX-001 | LocalPlatformContext | host context smoke | supported | supported | FilePicker | captured (45957524569) | captured (45968953555) |
| IO-FILE-001 | KmpFile | read, stream, name and path | supported | supported | FilePicker | captured (45957524569) | captured (45968953555) |
| IO-PICK-001 | rememberFilePickerLauncher | single selection | supported | supported | FilePicker | captured (45957524569) | captured (45968953555) |
| IO-PICK-002 | rememberFilePickerLauncher | multiple with limit | supported | supported | FilePicker | captured (45957524569) | captured (45968953555) |
| IO-PICK-003 | FilePickerFileType.Folder | folder and cancel | supported | supported | FilePicker | captured (45957524569) | captured (45968953555) |
| IO-SAVE-001 | rememberFileSaverLauncher | bytes save and reopen | supported | supported | ProfilePicture | captured (45957524569) | captured (45968953555) |
| IO-COIL-001 | KmpFileFetcher and AsyncImage | preview success | supported | supported | ImagePicker | captured (45957524569) | captured (45968953555) |
| IO-CAMERA-001 | rememberCameraPickerLauncher | capture or fallback | supported | supported | CameraPickerScreen | captured (45957524569) | captured (45968953555) |
| PERM-SINGLE-001 | rememberPermissionState | camera grant and deny | supported | supported | Permission | captured (45957524569) | captured (45968953555) |
| PERM-BULK-001 | rememberMultiplePermissionsState | camera and microphone | supported | supported | Permission | passed (46099102700) | passed (46108448068) |
| PERM-STATE-001 | PermissionState | determined and settings return | supported | supported | Permission | captured (45957524569) | captured (45968953555) |
| PERM-NOTIF-001 | Notification and RemoteNotification | local and remote notification | supported | supported | Permission | captured (45957524569) | captured (45968953555) |
| PERM-LOC-001 | BackgroundLocation and location leaves | foreground and background location | supported | supported | Permission | captured (45957524569) | captured (45968953555) |
| PERM-PIM-001 | contacts and calendar leaves | read and write | supported | supported | Permission | captured (45957524569) | captured (45968953555) |
| PERM-BT-001 | Bluetooth and Wi-Fi leaves | scan/connect and nearby | supported | supported | Permission | captured (45957524569) | captured (45968953555) |
| PERM-CORE-001 | storage, call and SMS leaves | legacy routes | supported | supported | Permission | captured (45957524569) | captured (45968953555) |
| PERM-STUB-001 | desktop and web permission stubs | unavailable | unsupported | unsupported | Limitations | not-applicable | not-applicable |
| SHARE-001 | ShareContent.Text | native share sheet | supported | supported | Share | captured (45957524569) | captured (45968953555) |
| SHARE-002 | ShareContent.Url | native share sheet | supported | supported | Share | captured (45957524569) | captured (45968953555) |
| SHARE-003 | ShareContent.File and Files | single and mixed files | supported | supported | Share | captured (45957524569) | captured (45968953555) |
| WEB-001 | WebViewState | deterministic HTML load | supported | supported | WebView | passed (46099102700) | captured (45968953555) |
| WEB-002 | WebViewNavigator | URL load, back and forward | supported | supported | WebView | passed (46099102700) | captured (45968953555) |
| WEB-003 | WebViewState.errorsForCurrentRequest | bad destination | supported | supported | WebView | passed (46099102700) | captured (45968953555) |
| WEB-004 | WebViewState.evaluateJavascript and settings | JavaScript on | supported | supported | WebView | passed (46099102700) | captured (45968953555) |
| WEB-005 | CookieManager | set, get, remove | supported | supported | WebView | passed (46099102700) | captured (45968953555) |
| NAV-001 | AdaptiveNavHost | push, back, restore | supported | supported | Home | captured (45957524569) | captured (45968953555) |
| NAV-002 | NavArgument | declared arguments | unsupported | unsupported | Limitations | not-applicable | not-applicable |
| GEO-001 | LatLng | distance and bearing maths | supported | supported | Geo | passed (46099102700) | captured (45968953555) |
| GEO-002 | LocationTracker | start, stop, updates | unsupported | unsupported | Limitations | not-applicable | not-applicable |
| UI-LIQUID-001 | LiquidGlassButton | filled, bordered, plain, disabled | unsupported | supported | LiquidGlass | not-applicable | not-run |
| UI-LIQUID-002 | LiquidGlassSwitch | on, off, disabled | unsupported | supported | LiquidGlass | not-applicable | not-run |
| UI-LIQUID-003 | LiquidGlassSlider | continuous and disabled | unsupported | supported | LiquidGlass | not-applicable | not-run |
| UI-LIQUID-004 | Liquid Glass fallback | non-iOS runtime | supported | unsupported | LiquidGlass | passed (46099102700) | not-applicable |
| PERM-SMS-001 | ReadSms, ReceiveSms, SendSms | legacy SMS routes | supported | supported | Permission | passed (46099102700) | passed (46108448068) |
| UI-ICON-004 | CupertinoIcon catalog | category filters | supported | supported | CupertinoIconsCatalog | passed (46099102700) | passed (46108448068) |
| UI-ALERT-005 | AdaptiveBasicAlertDialog | text field and critical severity | unsupported | supported | Dialog | not-applicable | passed (46108448068) |
| UI-ALERT-006 | AlertDialogIosStyle.ActionSheet | iPad popover | unsupported | supported | Dialog | not-applicable | failed (46099392157) |
| NAV-004 | HomeScreen | large-screen index layout | supported | supported | Home | captured (46107087160) | captured (46099392157) |
| UI-BAR-008 | AdaptiveScaffold | tablet tab and bar layout | supported | supported | Scaffold | captured (46107087160) | captured (46099392157) |
| UI-SHEET-003 | AdaptiveBottomSheet | tablet presentation | supported | supported | BottomSheet | captured (46107087160) | captured (46099392157) |
| UI-SHEET-002 | AdaptiveSheetState | detents, veto and dismissal | supported | supported | BottomSheet | passed (46099102700) | failed (46108448068) |
| UI-DATE-006 | AdaptiveDatePicker | picker and input display modes | supported | supported | DatePicker | failed (46099102700) | failed (46108448068) |
| UI-TIME-002 | AdaptiveTimePicker | 24-hour state | supported | supported | TimePicker | passed (46099102700) | passed (46108448068) |
| UI-BAR-005 | UIKitNavigationBarConfiguration | large titles and tint | unsupported | supported | TopBarDemo | not-applicable | not-run |
| UI-BAR-006 | UIKitTabBarConfiguration | selected and unselected tint | unsupported | supported | NavigationBar | not-applicable | not-run |
| UI-BAR-007 | UIKitUIBarButtonItem | system item, fixed and flexible space | unsupported | supported | Toolbar | not-applicable | not-run |
| WEB-006 | WebSettings | JavaScript off and on | supported | supported | WebView | failed (46099102700) | passed (46108448068) |
| IO-PICK-004 | FilePickerFileType.Custom/Extension | filter modes | supported | supported | FilePicker | not-run | not-run |
| IO-SAVE-002 | FileSaverLauncher | file and stream save | supported | supported | ProfilePicture | not-run | not-run |
| NAV-003 | rememberNavController | saveable state restoration | supported | supported | Home | passed (46099102700) | not-run |
| GEO-003 | ExtendedLocation types | altitude, speed, azimuth | supported | supported | Geo | not-run | not-run |
| EXCL-MAPS-001 | maps | excluded build-only module | unsupported | unsupported | Limitations | not-applicable | not-applicable |
| EXCL-MEDIA-001 | media | excluded module | unsupported | unsupported | Limitations | not-applicable | not-applicable |
| EXCL-NOTIF-001 | notification scheduler | excluded module | unsupported | unsupported | Limitations | not-applicable | not-applicable |
