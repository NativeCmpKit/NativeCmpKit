# Showcase coverage

Base: `a2c48c0b9ebf3524192e680ecd4becc1f2880bb8` on `feature/showcase-ui-verification`.

The authoritative machine-readable manifest is [coverage.json](coverage.json).
Regenerate both files with `python3 showcase/generate_coverage.py`.

| ID | Component | Variant | Android | iOS | Route | Status |
| --- | --- | --- | --- | --- | --- | --- |
| UI-BUTTON-001 | AdaptiveButton | filled enabled and disabled | supported | supported | Button | not-run |
| UI-BUTTON-002 | AdaptiveButton | icon and label content | supported | supported | Button | not-run |
| UI-BUTTON-003 | AdaptiveIconButton | three enabled and one disabled | supported | supported | Button | not-run |
| UI-BUTTON-004 | CupertinoButton | filled, bordered, plain, disabled | supported | supported | Button | not-run |
| UI-CLICK-001 | Modifier.adaptiveClickable | single, long, double, disabled | supported | supported | AdaptiveClickable | not-run |
| UI-SWITCH-001 | AdaptiveSwitch | on, off and disabled | supported | supported | Switch | not-run |
| UI-SWITCH-002 | CupertinoSwitch | on, off, disabled, thumb content | supported | supported | Switch | not-run |
| UI-SLIDER-001 | AdaptiveSlider | continuous value readout | supported | supported | Slider | not-run |
| UI-SLIDER-002 | AdaptiveSlider | discrete steps | supported | supported | Slider | not-run |
| UI-SLIDER-003 | AdaptiveSlider | disabled and custom range | supported | supported | Slider | not-run |
| UI-PROGRESS-001 | AdaptiveCircularProgressIndicator | indeterminate sizes | supported | supported | ProgressBar | not-run |
| UI-PROGRESS-002 | CupertinoActivityIndicator | spinner | supported | supported | ProgressBar | not-run |
| UI-PROGRESS-003 | AdaptiveCircularProgressIndicator | determinate | unsupported | unsupported | ProgressBar | not-applicable |
| UI-FAB-001 | AdaptiveExpandableFAB | expanded/collapsed | unsupported | unsupported | Button | not-applicable |
| UI-DATE-001 | AdaptiveDatePicker | inline selection and readout | supported | supported | DatePicker | not-run |
| UI-DATE-002 | AdaptiveCompactDatePicker | open, confirm, cancel | supported | supported | DatePicker | not-run |
| UI-DATE-003 | AdaptiveDateRangePicker | start and end transition | supported | supported | DatePicker | not-run |
| UI-DATE-004 | DateBounds and SelectableDates | bounded weekdays only | supported | supported | DatePicker | not-run |
| UI-DATE-005 | UIKitDisplayMode | picker and wheels | unsupported | supported | DatePicker | not-applicable |
| UI-TIME-001 | AdaptiveTimePicker | 12-hour and 24-hour states | supported | supported | TimePicker | not-run |
| UI-ALERT-001 | AdaptiveAlertDialog | two-button confirm and cancel | supported | supported | Dialog | not-run |
| UI-ALERT-002 | AdaptiveAlertDialog | single button | supported | supported | Dialog | not-run |
| UI-ALERT-003 | AdaptiveBasicAlertDialog | text fields and critical severity | unsupported | supported | Dialog | not-applicable |
| UI-ALERT-004 | AlertDialogIosStyle.ActionSheet | iPhone sheet and iPad popover | unsupported | supported | Dialog | not-applicable |
| UI-SHEET-001 | AdaptiveBottomSheet | show, content, dismiss | supported | supported | BottomSheet | not-run |
| UI-MENU-001 | AdaptiveDropDown | simple destructive and disabled items | supported | supported | DropDown | not-run |
| UI-MENU-002 | AdaptiveDropDownSection | sections | supported | supported | DropDown | not-run |
| UI-BAR-001 | AdaptiveScaffold | top bar, bottom bar, content padding | supported | supported | ScaffoldDemo | not-run |
| UI-BAR-002 | AdaptiveTopBar | title, leading, trailing, menu | supported | supported | TopBarDemo | not-run |
| UI-BAR-003 | AdaptiveNavigationBar | items and selected index | supported | supported | NavigationBar | not-run |
| UI-BAR-004 | AdaptiveToolbar | collapsed and expanded | supported | supported | Toolbar | not-run |
| UI-ICON-001 | CupertinoIcon catalog | search and category | supported | supported | CupertinoIconsCatalog | not-run |
| UI-ICON-002 | SFSymbol and UIKitImage | system name, vector, bitmap | unsupported | supported | TopBarDemo | not-applicable |
| UI-ICON-003 | CupertinoIcon | size and content description | supported | supported | CupertinoIconsCatalog | not-run |
| IO-CTX-001 | LocalPlatformContext | host context smoke | supported | supported | FilePicker | not-run |
| IO-FILE-001 | KmpFile | read, stream, name and path | supported | supported | FilePicker | not-run |
| IO-PICK-001 | rememberFilePickerLauncher | single selection | supported | supported | FilePicker | not-run |
| IO-PICK-002 | rememberFilePickerLauncher | multiple with limit | supported | supported | FilePicker | not-run |
| IO-PICK-003 | FilePickerFileType.Folder | folder and cancel | supported | supported | FilePicker | not-run |
| IO-SAVE-001 | rememberFileSaverLauncher | bytes save and reopen | supported | supported | ProfilePicture | not-run |
| IO-COIL-001 | KmpFileFetcher and AsyncImage | preview success | supported | supported | ImagePicker | not-run |
| IO-CAMERA-001 | rememberCameraPickerLauncher | capture or fallback | supported | supported | CameraPickerScreen | not-run |
| PERM-SINGLE-001 | rememberPermissionState | camera grant and deny | supported | supported | Permission | not-run |
| PERM-BULK-001 | rememberMultiplePermissionsState | camera and microphone | supported | supported | Permission | not-run |
| PERM-STATE-001 | PermissionState | determined and settings return | supported | supported | Permission | not-run |
| PERM-NOTIF-001 | Notification and RemoteNotification | local and remote notification | supported | supported | Permission | not-run |
| PERM-LOC-001 | BackgroundLocation and location leaves | foreground and background location | supported | supported | Permission | not-run |
| PERM-PIM-001 | contacts and calendar leaves | read and write | supported | supported | Permission | not-run |
| PERM-BT-001 | Bluetooth and Wi-Fi leaves | scan/connect and nearby | supported | supported | Permission | not-run |
| PERM-CORE-001 | storage, call and SMS leaves | legacy routes | supported | supported | Permission | not-run |
| PERM-STUB-001 | desktop and web permission stubs | unavailable | unsupported | unsupported | Permission | not-applicable |
| SHARE-001 | ShareContent.Text | native share sheet | supported | supported | Share | not-run |
| SHARE-002 | ShareContent.Url | native share sheet | supported | supported | Share | not-run |
| SHARE-003 | ShareContent.File and Files | single and mixed files | supported | supported | Share | not-run |
| WEB-001 | WebViewState | deterministic HTML load | supported | supported | WebView | not-run |
| WEB-002 | WebViewNavigator | URL load, back and forward | supported | supported | WebView | not-run |
| WEB-003 | WebViewState.errorsForCurrentRequest | bad destination | supported | supported | WebView | not-run |
| WEB-004 | WebViewState.evaluateJavascript and settings | JavaScript on | supported | supported | WebView | not-run |
| WEB-005 | CookieManager | set, get, remove | supported | supported | WebView | not-run |
| NAV-001 | AdaptiveNavHost | push, back, restore | supported | supported | Home | not-run |
| NAV-002 | NavArgument | declared arguments | unsupported | unsupported | Home | not-applicable |
| GEO-001 | LatLng | distance and bearing maths | supported | supported | Home | not-run |
| GEO-002 | LocationTracker | start, stop, updates | unsupported | unsupported | Home | not-applicable |
| EXCL-MAPS-001 | maps | excluded build-only module | unsupported | unsupported | Home | not-applicable |
| EXCL-MEDIA-001 | media | excluded module | unsupported | unsupported | Home | not-applicable |
| EXCL-NOTIF-001 | notification scheduler | excluded module | unsupported | unsupported | Home | not-applicable |
