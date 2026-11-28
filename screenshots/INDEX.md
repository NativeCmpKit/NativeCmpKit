# Showcase device screenshots

App revision: `e4ec7441`
Base handoff: `a2c48c0b9ebf3524192e680ecd4becc1f2880bb8`

Every image is a PNG captured from the live GitHub-hosted Android emulator or
iOS Simulator through ui-test-actions. Host renders and mockups are not used.

## android

- Run: https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/45957524569
- Job/attempt: `140367856551` / `1`
- Device: Pixel 6 API 35 Google APIs x86_64, 1080x2400 @ 420 dpi
- Runtime: Android 15 (API 35)
- ui-test-actions: `0c818c5d72e8c30c59bd1287c330a40392bf8e89`

| Capture | Component / scenario | Expected observation | Image |
| --- | --- | --- | --- |
| `functional/action-sheet` | functional | See coverage.json | ![functional action-sheet](android/functional/action-sheet/api35-phone-before.png) |
| `functional/action-sheet` | functional | See coverage.json | ![functional action-sheet](android/functional/action-sheet/api35-phone-failed-after.png) |
| `functional/alert-cancel` | functional | See coverage.json | ![functional alert-cancel](android/functional/alert-cancel/api35-phone-after.png) |
| `functional/alert-cancel` | functional | See coverage.json | ![functional alert-cancel](android/functional/alert-cancel/api35-phone-before.png) |
| `functional/alert-cancel` | functional | See coverage.json | ![functional alert-cancel](android/functional/alert-cancel/api35-tablet-after.png) |
| `functional/alert-cancel` | functional | See coverage.json | ![functional alert-cancel](android/functional/alert-cancel/api35-tablet-before.png) |
| `functional/alert-confirm` | functional | Cancel closes without a confirmation / Ok closes and records the confirmation | ![functional alert-confirm](android/functional/alert-confirm/api35-phone-after.png) |
| `functional/alert-confirm` | functional | See coverage.json | ![functional alert-confirm](android/functional/alert-confirm/api35-phone-before.png) |
| `functional/alert-confirm` | functional | See coverage.json | ![functional alert-confirm](android/functional/alert-confirm/api35-tablet-after.png) |
| `functional/alert-confirm` | functional | See coverage.json | ![functional alert-confirm](android/functional/alert-confirm/api35-tablet-before.png) |
| `functional/alert-text-field` | functional | See coverage.json | ![functional alert-text-field](android/functional/alert-text-field/api35-phone-before.png) |
| `functional/alert-text-field` | functional | See coverage.json | ![functional alert-text-field](android/functional/alert-text-field/api35-phone-failed-after.png) |
| `functional/buttons` | functional | Counter increments from 0 to 1 / The disabled button stays visible and unchanged | ![functional buttons](android/functional/buttons/api35-phone-after.png) |
| `functional/buttons` | functional | See coverage.json | ![functional buttons](android/functional/buttons/api35-phone-before.png) |
| `functional/buttons` | functional | See coverage.json | ![functional buttons](android/functional/buttons/api35-tablet-after.png) |
| `functional/buttons` | functional | See coverage.json | ![functional buttons](android/functional/buttons/api35-tablet-before.png) |
| `functional/clickable` | functional | Each gesture is counted once / The disabled card stays inert / The Material platform shows indication while iOS uses press scale | ![functional clickable](android/functional/clickable/api35-phone-after.png) |
| `functional/clickable` | functional | See coverage.json | ![functional clickable](android/functional/clickable/api35-phone-before.png) |
| `functional/clickable` | functional | See coverage.json | ![functional clickable](android/functional/clickable/api35-tablet-after.png) |
| `functional/clickable` | functional | See coverage.json | ![functional clickable](android/functional/clickable/api35-tablet-before.png) |
| `functional/date-bounds` | functional | Weekend selection is rejected or snapped to a selectable day / Dates outside the bound are unavailable | ![functional date-bounds](android/functional/date-bounds/api35-phone-after.png) |
| `functional/date-bounds` | functional | See coverage.json | ![functional date-bounds](android/functional/date-bounds/api35-phone-before.png) |
| `functional/date-bounds` | functional | See coverage.json | ![functional date-bounds](android/functional/date-bounds/api35-phone-failed-after.png) |
| `functional/date-bounds` | functional | See coverage.json | ![functional date-bounds](android/functional/date-bounds/api35-tablet-after.png) |
| `functional/date-bounds` | functional | See coverage.json | ![functional date-bounds](android/functional/date-bounds/api35-tablet-before.png) |
| `functional/date-display` | functional | See coverage.json | ![functional date-display](android/functional/date-display/api35-phone-before.png) |
| `functional/date-display` | functional | The mode changes on Material / The iOS wheels state is fixed at creation | ![functional date-display](android/functional/date-display/api35-phone-failed-after.png) |
| `functional/date-display` | functional | See coverage.json | ![functional date-display](android/functional/date-display/api35-tablet-after.png) |
| `functional/date-display` | functional | See coverage.json | ![functional date-display](android/functional/date-display/api35-tablet-before.png) |
| `functional/dropdown` | functional | The selected action readout changes / The destructive item is styled as destructive / The disabled item does not fire | ![functional dropdown](android/functional/dropdown/api35-phone-after.png) |
| `functional/dropdown` | functional | See coverage.json | ![functional dropdown](android/functional/dropdown/api35-phone-before.png) |
| `functional/dropdown` | functional | See coverage.json | ![functional dropdown](android/functional/dropdown/api35-tablet-after.png) |
| `functional/dropdown` | functional | See coverage.json | ![functional dropdown](android/functional/dropdown/api35-tablet-before.png) |
| `functional/geo-math` | functional | 0,0 to 0,1 is about 111.19 km / Cardinal bearings round to 0/90/180/270 | ![functional geo-math](android/functional/geo-math/api35-phone-after.png) |
| `functional/geo-math` | functional | See coverage.json | ![functional geo-math](android/functional/geo-math/api35-phone-before.png) |
| `functional/geo-math` | functional | See coverage.json | ![functional geo-math](android/functional/geo-math/api35-tablet-after.png) |
| `functional/geo-math` | functional | See coverage.json | ![functional geo-math](android/functional/geo-math/api35-tablet-before.png) |
| `functional/icons-category` | functional | The count changes from the All value / Representative glyphs remain rendered | ![functional icons-category](android/functional/icons-category/api35-phone-after.png) |
| `functional/icons-category` | functional | See coverage.json | ![functional icons-category](android/functional/icons-category/api35-phone-before.png) |
| `functional/icons-category` | functional | See coverage.json | ![functional icons-category](android/functional/icons-category/api35-tablet-after.png) |
| `functional/icons-category` | functional | See coverage.json | ![functional icons-category](android/functional/icons-category/api35-tablet-before.png) |
| `functional/limitations` | functional | See coverage.json | ![functional limitations](android/functional/limitations/api35-phone-after.png) |
| `functional/limitations` | functional | See coverage.json | ![functional limitations](android/functional/limitations/api35-phone-before.png) |
| `functional/limitations` | functional | See coverage.json | ![functional limitations](android/functional/limitations/api35-tablet-after.png) |
| `functional/limitations` | functional | See coverage.json | ![functional limitations](android/functional/limitations/api35-tablet-before.png) |
| `functional/liquidglass` | functional | The screen states that Liquid Glass is iOS 26 only / Adaptive controls are named as the fallback | ![functional liquidglass](android/functional/liquidglass/api35-phone-after.png) |
| `functional/liquidglass` | functional | See coverage.json | ![functional liquidglass](android/functional/liquidglass/api35-phone-before.png) |
| `functional/liquidglass` | functional | See coverage.json | ![functional liquidglass](android/functional/liquidglass/api35-tablet-after.png) |
| `functional/liquidglass` | functional | See coverage.json | ![functional liquidglass](android/functional/liquidglass/api35-tablet-before.png) |
| `functional/nav-restore` | functional | The route stack is restored / Popped destination state is dropped | ![functional nav-restore](android/functional/nav-restore/api35-phone-after.png) |
| `functional/nav-restore` | functional | See coverage.json | ![functional nav-restore](android/functional/nav-restore/api35-phone-before.png) |
| `functional/nav-restore` | functional | See coverage.json | ![functional nav-restore](android/functional/nav-restore/api35-tablet-after.png) |
| `functional/nav-restore` | functional | See coverage.json | ![functional nav-restore](android/functional/nav-restore/api35-tablet-before.png) |
| `functional/navbar` | functional | The selected tab changes / No selection is possible with an invalid index | ![functional navbar](android/functional/navbar/api35-phone-after.png) |
| `functional/navbar` | functional | See coverage.json | ![functional navbar](android/functional/navbar/api35-phone-before.png) |
| `functional/navbar` | functional | See coverage.json | ![functional navbar](android/functional/navbar/api35-tablet-after.png) |
| `functional/navbar` | functional | See coverage.json | ![functional navbar](android/functional/navbar/api35-tablet-before.png) |
| `functional/permissions-bulk-deny` | functional | allPermissionsGranted follows the results / revokedPermissions lists denied entries | ![functional permissions-bulk-deny](android/functional/permissions-bulk-deny/api35-phone-after.png) |
| `functional/permissions-bulk-deny` | functional | See coverage.json | ![functional permissions-bulk-deny](android/functional/permissions-bulk-deny/api35-phone-before.png) |
| `functional/permissions-bulk-deny` | functional | See coverage.json | ![functional permissions-bulk-deny](android/functional/permissions-bulk-deny/api35-tablet-after.png) |
| `functional/permissions-bulk-deny` | functional | See coverage.json | ![functional permissions-bulk-deny](android/functional/permissions-bulk-deny/api35-tablet-before.png) |
| `functional/permissions-sms-rows` | functional | The rows render independently / Android reports its own status / iOS reports NotGranted for read/receive | ![functional permissions-sms-rows](android/functional/permissions-sms-rows/api35-phone-after.png) |
| `functional/permissions-sms-rows` | functional | See coverage.json | ![functional permissions-sms-rows](android/functional/permissions-sms-rows/api35-phone-before.png) |
| `functional/permissions-sms-rows` | functional | See coverage.json | ![functional permissions-sms-rows](android/functional/permissions-sms-rows/api35-tablet-after.png) |
| `functional/permissions-sms-rows` | functional | See coverage.json | ![functional permissions-sms-rows](android/functional/permissions-sms-rows/api35-tablet-before.png) |
| `functional/scaffold-tab` | functional | Content is not obscured by the bars / The tab selection changes | ![functional scaffold-tab](android/functional/scaffold-tab/api35-phone-after.png) |
| `functional/scaffold-tab` | functional | See coverage.json | ![functional scaffold-tab](android/functional/scaffold-tab/api35-phone-before.png) |
| `functional/scaffold-tab` | functional | See coverage.json | ![functional scaffold-tab](android/functional/scaffold-tab/api35-tablet-after.png) |
| `functional/scaffold-tab` | functional | See coverage.json | ![functional scaffold-tab](android/functional/scaffold-tab/api35-tablet-before.png) |
| `functional/sheet` | functional | The sheet presents with a drag handle / Dismissal reports back / The iOS inset/shape parameters are ignored | ![functional sheet](android/functional/sheet/api35-phone-after.png) |
| `functional/sheet` | functional | See coverage.json | ![functional sheet](android/functional/sheet/api35-phone-before.png) |
| `functional/sheet` | functional | See coverage.json | ![functional sheet](android/functional/sheet/api35-tablet-after.png) |
| `functional/sheet` | functional | See coverage.json | ![functional sheet](android/functional/sheet/api35-tablet-before.png) |
| `functional/sheet-veto` | functional | The vetoed dismissal keeps the sheet / The close button dismisses it | ![functional sheet-veto](android/functional/sheet-veto/api35-phone-after.png) |
| `functional/sheet-veto` | functional | See coverage.json | ![functional sheet-veto](android/functional/sheet-veto/api35-phone-before.png) |
| `functional/sheet-veto` | functional | See coverage.json | ![functional sheet-veto](android/functional/sheet-veto/api35-tablet-after.png) |
| `functional/sheet-veto` | functional | See coverage.json | ![functional sheet-veto](android/functional/sheet-veto/api35-tablet-before.png) |
| `functional/slider` | functional | The percentage follows the thumb / The value stays within 0..100 | ![functional slider](android/functional/slider/api35-phone-after.png) |
| `functional/slider` | functional | See coverage.json | ![functional slider](android/functional/slider/api35-phone-before.png) |
| `functional/slider` | functional | See coverage.json | ![functional slider](android/functional/slider/api35-tablet-after.png) |
| `functional/slider` | functional | See coverage.json | ![functional slider](android/functional/slider/api35-tablet-before.png) |
| `functional/switch` | functional | The readout follows the checked state / The disabled switch does not change | ![functional switch](android/functional/switch/api35-phone-after.png) |
| `functional/switch` | functional | See coverage.json | ![functional switch](android/functional/switch/api35-phone-before.png) |
| `functional/switch` | functional | See coverage.json | ![functional switch](android/functional/switch/api35-tablet-after.png) |
| `functional/switch` | functional | See coverage.json | ![functional switch](android/functional/switch/api35-tablet-before.png) |
| `functional/time-24h` | functional | The 24-hour readout renders / iOS follows the device locale | ![functional time-24h](android/functional/time-24h/api35-phone-after.png) |
| `functional/time-24h` | functional | See coverage.json | ![functional time-24h](android/functional/time-24h/api35-phone-before.png) |
| `functional/time-24h` | functional | See coverage.json | ![functional time-24h](android/functional/time-24h/api35-tablet-after.png) |
| `functional/time-24h` | functional | See coverage.json | ![functional time-24h](android/functional/time-24h/api35-tablet-before.png) |
| `functional/toolbar` | functional | The Material toolbar expands / iOS requires non-empty iosItems and shows a native toolbar | ![functional toolbar](android/functional/toolbar/api35-phone-after.png) |
| `functional/toolbar` | functional | See coverage.json | ![functional toolbar](android/functional/toolbar/api35-phone-before.png) |
| `functional/toolbar` | functional | See coverage.json | ![functional toolbar](android/functional/toolbar/api35-tablet-after.png) |
| `functional/toolbar` | functional | See coverage.json | ![functional toolbar](android/functional/toolbar/api35-tablet-before.png) |
| `functional/topbar` | functional | The title is visible / Bar items render natively on iOS / The menu action fires | ![functional topbar](android/functional/topbar/api35-phone-after.png) |
| `functional/topbar` | functional | See coverage.json | ![functional topbar](android/functional/topbar/api35-phone-before.png) |
| `functional/topbar` | functional | See coverage.json | ![functional topbar](android/functional/topbar/api35-tablet-after.png) |
| `functional/topbar` | functional | See coverage.json | ![functional topbar](android/functional/topbar/api35-tablet-before.png) |
| `functional/webview` | functional | The known title appears / Loading reaches Finished / isLoading is initially true on every platform | ![functional webview](android/functional/webview/api35-phone-after.png) |
| `functional/webview` | functional | See coverage.json | ![functional webview](android/functional/webview/api35-phone-before.png) |
| `functional/webview` | functional | See coverage.json | ![functional webview](android/functional/webview/api35-phone-failed-after.png) |
| `functional/webview` | functional | See coverage.json | ![functional webview](android/functional/webview/api35-tablet-after.png) |
| `functional/webview` | functional | See coverage.json | ![functional webview](android/functional/webview/api35-tablet-before.png) |
| `functional/webview-js` | functional | See coverage.json | ![functional webview-js](android/functional/webview-js/api35-phone-before.png) |
| `functional/webview-js` | functional | JavaScript is off by default / Enabling it allows the evaluation | ![functional webview-js](android/functional/webview-js/api35-phone-failed-after.png) |
| `functional/webview-js` | functional | See coverage.json | ![functional webview-js](android/functional/webview-js/api35-tablet-before.png) |
| `functional/webview-js` | functional | See coverage.json | ![functional webview-js](android/functional/webview-js/api35-tablet-failed-after.png) |
| `geo-math/overview` | geo-math | Deterministic LatLng distance/bearing plus the tracker-unavailable state. | ![geo-math overview](android/geo-math/overview/api35-phone.png) |
| `geo-math/overview` | geo-math | Deterministic LatLng distance/bearing plus the tracker-unavailable state. | ![geo-math overview](android/geo-math/overview/api35-tablet.png) |
| `home/index` | home | Searchable component index, stable routes and per-screen reset. | ![home index](android/home/index/api35-phone.png) |
| `home/index` | home | Searchable component index, stable routes and per-screen reset. | ![home index](android/home/index/api35-tablet.png) |
| `io-camera-picker/overview` | io-camera-picker | Camera launch and the platform-specific unavailable fallback. | ![io-camera-picker overview](android/io-camera-picker/overview/api35-phone.png) |
| `io-camera-picker/overview` | io-camera-picker | Camera launch and the platform-specific unavailable fallback. | ![io-camera-picker overview](android/io-camera-picker/overview/api35-tablet.png) |
| `io-file-picker/overview` | io-file-picker | Platform file selection, filters, metadata and streaming readout. | ![io-file-picker overview](android/io-file-picker/overview/api35-phone.png) |
| `io-file-picker/overview` | io-file-picker | Platform file selection, filters, metadata and streaming readout. | ![io-file-picker overview](android/io-file-picker/overview/api35-tablet.png) |
| `io-file-saver/overview` | io-file-saver | Save/export entry point and result state. | ![io-file-saver overview](android/io-file-saver/overview/api35-phone.png) |
| `io-file-saver/overview` | io-file-saver | Save/export entry point and result state. | ![io-file-saver overview](android/io-file-saver/overview/api35-tablet.png) |
| `io-image-picker/overview` | io-image-picker | Picked image preview through the KmpFile Coil pipeline. | ![io-image-picker overview](android/io-image-picker/overview/api35-phone.png) |
| `io-image-picker/overview` | io-image-picker | Picked image preview through the KmpFile Coil pipeline. | ![io-image-picker overview](android/io-image-picker/overview/api35-tablet.png) |
| `limitations/known-limitations` | limitations | Source-confirmed unsupported and internal APIs; not working parity. | ![limitations known-limitations](android/limitations/known-limitations/api35-phone.png) |
| `limitations/known-limitations` | limitations | Source-confirmed unsupported and internal APIs; not working parity. | ![limitations known-limitations](android/limitations/known-limitations/api35-tablet.png) |
| `permissions/overview` | permissions | Public permission status and request rows; OS dialogs are separate. | ![permissions overview](android/permissions/overview/api35-phone.png) |
| `permissions/overview` | permissions | Public permission status and request rows; OS dialogs are separate. | ![permissions overview](android/permissions/overview/api35-tablet.png) |
| `share/overview` | share | Native share payloads and terminal result state. | ![share overview](android/share/overview/api35-phone.png) |
| `share/overview` | share | Native share payloads and terminal result state. | ![share overview](android/share/overview/api35-tablet.png) |
| `ui-adaptive-alert-dialog/overview` | ui-adaptive-alert-dialog | The confirm action enables after typing / Secure/number-pad fields are configured / Critical severity is applied on supported UIKit hosts | ![ui-adaptive-alert-dialog overview](android/ui-adaptive-alert-dialog/overview/api35-phone.png) |
| `ui-adaptive-alert-dialog/overview` | ui-adaptive-alert-dialog | See coverage.json | ![ui-adaptive-alert-dialog overview](android/ui-adaptive-alert-dialog/overview/api35-tablet.png) |
| `ui-adaptive-alert-dialog/simple` | ui-adaptive-alert-dialog | Only one action is visible / The dialog dismisses | ![ui-adaptive-alert-dialog simple](android/ui-adaptive-alert-dialog/simple/api35-phone.png) |
| `ui-adaptive-alert-dialog/simple` | ui-adaptive-alert-dialog | See coverage.json | ![ui-adaptive-alert-dialog simple](android/ui-adaptive-alert-dialog/simple/api35-tablet.png) |
| `ui-adaptive-bottom-sheet/expanded` | ui-adaptive-bottom-sheet | See coverage.json | ![ui-adaptive-bottom-sheet expanded](android/ui-adaptive-bottom-sheet/expanded/api35-phone.png) |
| `ui-adaptive-bottom-sheet/expanded` | ui-adaptive-bottom-sheet | See coverage.json | ![ui-adaptive-bottom-sheet expanded](android/ui-adaptive-bottom-sheet/expanded/api35-tablet.png) |
| `ui-adaptive-bottom-sheet/overview` | ui-adaptive-bottom-sheet | See coverage.json | ![ui-adaptive-bottom-sheet overview](android/ui-adaptive-bottom-sheet/overview/api35-phone.png) |
| `ui-adaptive-bottom-sheet/overview` | ui-adaptive-bottom-sheet | The sheet uses the wide presentation / Close dismisses it | ![ui-adaptive-bottom-sheet overview](android/ui-adaptive-bottom-sheet/overview/api35-tablet.png) |
| `ui-adaptive-button/overview` | ui-adaptive-button | The label is visible / The leading icon has a non-empty content description where supplied | ![ui-adaptive-button overview](android/ui-adaptive-button/overview/api35-phone.png) |
| `ui-adaptive-button/overview` | ui-adaptive-button | See coverage.json | ![ui-adaptive-button overview](android/ui-adaptive-button/overview/api35-tablet.png) |
| `ui-adaptive-clickable/overview` | ui-adaptive-clickable | See coverage.json | ![ui-adaptive-clickable overview](android/ui-adaptive-clickable/overview/api35-phone.png) |
| `ui-adaptive-clickable/overview` | ui-adaptive-clickable | See coverage.json | ![ui-adaptive-clickable overview](android/ui-adaptive-clickable/overview/api35-tablet.png) |
| `ui-adaptive-date-picker/overview` | ui-adaptive-date-picker | The readout changes / The native iOS calendar or Material picker is used | ![ui-adaptive-date-picker overview](android/ui-adaptive-date-picker/overview/api35-phone.png) |
| `ui-adaptive-date-picker/overview` | ui-adaptive-date-picker | See coverage.json | ![ui-adaptive-date-picker overview](android/ui-adaptive-date-picker/overview/api35-tablet.png) |
| `ui-adaptive-dropdown/menu` | ui-adaptive-dropdown | iOS shows inline submenus / Material shows the caller-built section divider | ![ui-adaptive-dropdown menu](android/ui-adaptive-dropdown/menu/api35-phone.png) |
| `ui-adaptive-dropdown/overview` | ui-adaptive-dropdown | See coverage.json | ![ui-adaptive-dropdown overview](android/ui-adaptive-dropdown/overview/api35-phone.png) |
| `ui-adaptive-dropdown/overview` | ui-adaptive-dropdown | See coverage.json | ![ui-adaptive-dropdown overview](android/ui-adaptive-dropdown/overview/api35-tablet.png) |
| `ui-adaptive-navigation-bar/overview` | ui-adaptive-navigation-bar | See coverage.json | ![ui-adaptive-navigation-bar overview](android/ui-adaptive-navigation-bar/overview/api35-phone.png) |
| `ui-adaptive-navigation-bar/overview` | ui-adaptive-navigation-bar | See coverage.json | ![ui-adaptive-navigation-bar overview](android/ui-adaptive-navigation-bar/overview/api35-tablet.png) |
| `ui-adaptive-progress/overview` | ui-adaptive-progress | All three indeterminate indicators render and animate / No determinate progress control is advertised | ![ui-adaptive-progress overview](android/ui-adaptive-progress/overview/api35-phone.png) |
| `ui-adaptive-progress/overview` | ui-adaptive-progress | See coverage.json | ![ui-adaptive-progress overview](android/ui-adaptive-progress/overview/api35-tablet.png) |
| `ui-adaptive-scaffold/overview` | ui-adaptive-scaffold | See coverage.json | ![ui-adaptive-scaffold overview](android/ui-adaptive-scaffold/overview/api35-phone.png) |
| `ui-adaptive-scaffold/overview` | ui-adaptive-scaffold | Bars span the window / Tab content updates without clipping | ![ui-adaptive-scaffold overview](android/ui-adaptive-scaffold/overview/api35-tablet.png) |
| `ui-adaptive-slider/overview` | ui-adaptive-slider | Values snap to the stepped positions / Tick marks are visible on iOS below 26 | ![ui-adaptive-slider overview](android/ui-adaptive-slider/overview/api35-phone.png) |
| `ui-adaptive-slider/overview` | ui-adaptive-slider | See coverage.json | ![ui-adaptive-slider overview](android/ui-adaptive-slider/overview/api35-tablet.png) |
| `ui-adaptive-switch/overview` | ui-adaptive-switch | The 51x31 track and thumb render on every target / The disabled switch cannot be toggled | ![ui-adaptive-switch overview](android/ui-adaptive-switch/overview/api35-phone.png) |
| `ui-adaptive-switch/overview` | ui-adaptive-switch | See coverage.json | ![ui-adaptive-switch overview](android/ui-adaptive-switch/overview/api35-tablet.png) |
| `ui-adaptive-time-picker/overview` | ui-adaptive-time-picker | Both time readouts render / The iOS format follows the device locale even when is24Hour differs | ![ui-adaptive-time-picker overview](android/ui-adaptive-time-picker/overview/api35-phone.png) |
| `ui-adaptive-time-picker/overview` | ui-adaptive-time-picker | See coverage.json | ![ui-adaptive-time-picker overview](android/ui-adaptive-time-picker/overview/api35-tablet.png) |
| `ui-adaptive-toolbar/overview` | ui-adaptive-toolbar | See coverage.json | ![ui-adaptive-toolbar overview](android/ui-adaptive-toolbar/overview/api35-phone.png) |
| `ui-adaptive-toolbar/overview` | ui-adaptive-toolbar | See coverage.json | ![ui-adaptive-toolbar overview](android/ui-adaptive-toolbar/overview/api35-tablet.png) |
| `ui-adaptive-top-bar/overview` | ui-adaptive-top-bar | System-name and rasterized vector images render / The icon font fallback is not presented as an SF Symbol / The UIKitImage.Bitmap variant is not exercised by this screen | ![ui-adaptive-top-bar overview](android/ui-adaptive-top-bar/overview/api35-phone.png) |
| `ui-adaptive-top-bar/overview` | ui-adaptive-top-bar | See coverage.json | ![ui-adaptive-top-bar overview](android/ui-adaptive-top-bar/overview/api35-tablet.png) |
| `ui-cupertino-icons/category-arrows` | ui-cupertino-icons | See coverage.json | ![ui-cupertino-icons category-arrows](android/ui-cupertino-icons/category-arrows/api35-tablet.png) |
| `ui-cupertino-icons/category-communication` | ui-cupertino-icons | See coverage.json | ![ui-cupertino-icons category-communication](android/ui-cupertino-icons/category-communication/api35-tablet.png) |
| `ui-cupertino-icons/overview` | ui-cupertino-icons | See coverage.json | ![ui-cupertino-icons overview](android/ui-cupertino-icons/overview/api35-phone.png) |
| `ui-cupertino-icons/overview` | ui-cupertino-icons | See coverage.json | ![ui-cupertino-icons overview](android/ui-cupertino-icons/overview/api35-tablet.png) |
| `ui-cupertino-icons/search-chevron` | ui-cupertino-icons | The grid filters to matching names / The count updates / Representative glyphs render without tofu | ![ui-cupertino-icons search-chevron](android/ui-cupertino-icons/search-chevron/api35-phone.png) |
| `ui-liquid-glass/overview` | ui-liquid-glass | See coverage.json | ![ui-liquid-glass overview](android/ui-liquid-glass/overview/api35-tablet.png) |
| `webview/after-back` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview after-back](android/webview/after-back/api35-tablet.png) |
| `webview/after-forward` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview after-forward](android/webview/after-forward/api35-tablet.png) |
| `webview/cookie-roundtrip` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview cookie-roundtrip](android/webview/cookie-roundtrip/api35-phone.png) |
| `webview/cookie-roundtrip` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview cookie-roundtrip](android/webview/cookie-roundtrip/api35-tablet.png) |
| `webview/cookies-cleared` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview cookies-cleared](android/webview/cookies-cleared/api35-phone.png) |
| `webview/cookies-cleared` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview cookies-cleared](android/webview/cookies-cleared/api35-tablet.png) |
| `webview/invalid-destination` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview invalid-destination](android/webview/invalid-destination/api35-phone.png) |
| `webview/invalid-destination` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview invalid-destination](android/webview/invalid-destination/api35-tablet.png) |
| `webview/javascript-title` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview javascript-title](android/webview/javascript-title/api35-phone.png) |
| `webview/javascript-title` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview javascript-title](android/webview/javascript-title/api35-tablet.png) |
| `webview/overview` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview overview](android/webview/overview/api35-phone.png) |
| `webview/overview` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview overview](android/webview/overview/api35-tablet.png) |
| `webview/second-page` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview second-page](android/webview/second-page/api35-phone.png) |
| `webview/second-page` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview second-page](android/webview/second-page/api35-tablet.png) |

## ios

- Run: https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/45968953555
- Job/attempt: `140404371284` / `1`
- Device: iPhone simulator via AXe, 402x874
- Runtime: iOS 26.5 simulator (Xcode 26.6)
- ui-test-actions: `0c818c5d72e8c30c59bd1287c330a40392bf8e89`

| Capture | Component / scenario | Expected observation | Image |
| --- | --- | --- | --- |
| `alertdialogiosstyle-actionsheet/ipad-popover` | alertdialogiosstyle-actionsheet | The action sheet is a centred popover / Cancel is reachable | ![alertdialogiosstyle-actionsheet ipad-popover](ios/alertdialogiosstyle-actionsheet/ipad-popover/ipad-simulator.png) |
| `functional/action-sheet` | functional | See coverage.json | ![functional action-sheet](ios/functional/action-sheet/ipad-simulator-before.png) |
| `functional/action-sheet` | functional | See coverage.json | ![functional action-sheet](ios/functional/action-sheet/ipad-simulator-failed-after.png) |
| `functional/action-sheet` | functional | iPhone presents a bottom action sheet / iPad presents a centred popover because no public anchor API exists | ![functional action-sheet](ios/functional/action-sheet/iphone-simulator-after.png) |
| `functional/action-sheet` | functional | See coverage.json | ![functional action-sheet](ios/functional/action-sheet/iphone-simulator-before.png) |
| `functional/alert-cancel` | functional | See coverage.json | ![functional alert-cancel](ios/functional/alert-cancel/ipad-simulator-after.png) |
| `functional/alert-cancel` | functional | See coverage.json | ![functional alert-cancel](ios/functional/alert-cancel/ipad-simulator-before.png) |
| `functional/alert-cancel` | functional | See coverage.json | ![functional alert-cancel](ios/functional/alert-cancel/iphone-simulator-after.png) |
| `functional/alert-cancel` | functional | See coverage.json | ![functional alert-cancel](ios/functional/alert-cancel/iphone-simulator-before.png) |
| `functional/alert-confirm` | functional | See coverage.json | ![functional alert-confirm](ios/functional/alert-confirm/ipad-simulator-after.png) |
| `functional/alert-confirm` | functional | See coverage.json | ![functional alert-confirm](ios/functional/alert-confirm/ipad-simulator-before.png) |
| `functional/alert-confirm` | functional | Cancel closes without a confirmation / Ok closes and records the confirmation | ![functional alert-confirm](ios/functional/alert-confirm/iphone-simulator-after.png) |
| `functional/alert-confirm` | functional | See coverage.json | ![functional alert-confirm](ios/functional/alert-confirm/iphone-simulator-before.png) |
| `functional/alert-text-field` | functional | See coverage.json | ![functional alert-text-field](ios/functional/alert-text-field/ipad-simulator-after.png) |
| `functional/alert-text-field` | functional | See coverage.json | ![functional alert-text-field](ios/functional/alert-text-field/ipad-simulator-before.png) |
| `functional/alert-text-field` | functional | The confirm action enables after typing / Secure/number-pad fields are configured / Critical severity is applied on supported UIKit hosts | ![functional alert-text-field](ios/functional/alert-text-field/iphone-simulator-after.png) |
| `functional/alert-text-field` | functional | See coverage.json | ![functional alert-text-field](ios/functional/alert-text-field/iphone-simulator-before.png) |
| `functional/buttons` | functional | See coverage.json | ![functional buttons](ios/functional/buttons/ipad-simulator-after.png) |
| `functional/buttons` | functional | See coverage.json | ![functional buttons](ios/functional/buttons/ipad-simulator-before.png) |
| `functional/buttons` | functional | Counter increments from 0 to 1 / The disabled button stays visible and unchanged | ![functional buttons](ios/functional/buttons/iphone-simulator-after.png) |
| `functional/buttons` | functional | See coverage.json | ![functional buttons](ios/functional/buttons/iphone-simulator-before.png) |
| `functional/clickable` | functional | See coverage.json | ![functional clickable](ios/functional/clickable/ipad-simulator-before.png) |
| `functional/clickable` | functional | See coverage.json | ![functional clickable](ios/functional/clickable/ipad-simulator-failed-after.png) |
| `functional/clickable` | functional | Each gesture is counted once / The disabled card stays inert / The Material platform shows indication while iOS uses press scale | ![functional clickable](ios/functional/clickable/iphone-simulator-after.png) |
| `functional/clickable` | functional | See coverage.json | ![functional clickable](ios/functional/clickable/iphone-simulator-before.png) |
| `functional/clickable` | functional | See coverage.json | ![functional clickable](ios/functional/clickable/iphone-simulator-failed-after.png) |
| `functional/date-bounds` | functional | See coverage.json | ![functional date-bounds](ios/functional/date-bounds/ipad-simulator-after.png) |
| `functional/date-bounds` | functional | See coverage.json | ![functional date-bounds](ios/functional/date-bounds/ipad-simulator-before.png) |
| `functional/date-bounds` | functional | Weekend selection is rejected or snapped to a selectable day / Dates outside the bound are unavailable | ![functional date-bounds](ios/functional/date-bounds/iphone-simulator-after.png) |
| `functional/date-bounds` | functional | See coverage.json | ![functional date-bounds](ios/functional/date-bounds/iphone-simulator-before.png) |
| `functional/date-bounds` | functional | See coverage.json | ![functional date-bounds](ios/functional/date-bounds/iphone-simulator-failed-after.png) |
| `functional/date-display` | functional | See coverage.json | ![functional date-display](ios/functional/date-display/ipad-simulator-before.png) |
| `functional/date-display` | functional | See coverage.json | ![functional date-display](ios/functional/date-display/ipad-simulator-failed-after.png) |
| `functional/date-display` | functional | See coverage.json | ![functional date-display](ios/functional/date-display/iphone-simulator-before.png) |
| `functional/date-display` | functional | The mode changes on Material / The iOS wheels state is fixed at creation | ![functional date-display](ios/functional/date-display/iphone-simulator-failed-after.png) |
| `functional/dropdown` | functional | See coverage.json | ![functional dropdown](ios/functional/dropdown/ipad-simulator-after.png) |
| `functional/dropdown` | functional | See coverage.json | ![functional dropdown](ios/functional/dropdown/ipad-simulator-before.png) |
| `functional/dropdown` | functional | The selected action readout changes / The destructive item is styled as destructive / The disabled item does not fire | ![functional dropdown](ios/functional/dropdown/iphone-simulator-after.png) |
| `functional/dropdown` | functional | See coverage.json | ![functional dropdown](ios/functional/dropdown/iphone-simulator-before.png) |
| `functional/geo-math` | functional | See coverage.json | ![functional geo-math](ios/functional/geo-math/ipad-simulator-after.png) |
| `functional/geo-math` | functional | See coverage.json | ![functional geo-math](ios/functional/geo-math/ipad-simulator-before.png) |
| `functional/geo-math` | functional | See coverage.json | ![functional geo-math](ios/functional/geo-math/iphone-simulator-after.png) |
| `functional/geo-math` | functional | See coverage.json | ![functional geo-math](ios/functional/geo-math/iphone-simulator-before.png) |
| `functional/icons-category` | functional | See coverage.json | ![functional icons-category](ios/functional/icons-category/ipad-simulator-after.png) |
| `functional/icons-category` | functional | See coverage.json | ![functional icons-category](ios/functional/icons-category/ipad-simulator-before.png) |
| `functional/icons-category` | functional | The count changes from the All value / Representative glyphs remain rendered | ![functional icons-category](ios/functional/icons-category/iphone-simulator-after.png) |
| `functional/icons-category` | functional | See coverage.json | ![functional icons-category](ios/functional/icons-category/iphone-simulator-before.png) |
| `functional/limitations` | functional | See coverage.json | ![functional limitations](ios/functional/limitations/ipad-simulator-after.png) |
| `functional/limitations` | functional | See coverage.json | ![functional limitations](ios/functional/limitations/ipad-simulator-before.png) |
| `functional/limitations` | functional | See coverage.json | ![functional limitations](ios/functional/limitations/iphone-simulator-after.png) |
| `functional/limitations` | functional | See coverage.json | ![functional limitations](ios/functional/limitations/iphone-simulator-before.png) |
| `functional/liquidglass` | functional | See coverage.json | ![functional liquidglass](ios/functional/liquidglass/ipad-simulator-before.png) |
| `functional/liquidglass` | functional | See coverage.json | ![functional liquidglass](ios/functional/liquidglass/ipad-simulator-failed-after.png) |
| `functional/liquidglass` | functional | See coverage.json | ![functional liquidglass](ios/functional/liquidglass/iphone-simulator-before.png) |
| `functional/liquidglass` | functional | See coverage.json | ![functional liquidglass](ios/functional/liquidglass/iphone-simulator-failed-after.png) |
| `functional/navbar` | functional | See coverage.json | ![functional navbar](ios/functional/navbar/ipad-simulator-after.png) |
| `functional/navbar` | functional | See coverage.json | ![functional navbar](ios/functional/navbar/ipad-simulator-before.png) |
| `functional/navbar` | functional | The selected tab changes / No selection is possible with an invalid index | ![functional navbar](ios/functional/navbar/iphone-simulator-after.png) |
| `functional/navbar` | functional | See coverage.json | ![functional navbar](ios/functional/navbar/iphone-simulator-before.png) |
| `functional/permissions-bulk-deny` | functional | See coverage.json | ![functional permissions-bulk-deny](ios/functional/permissions-bulk-deny/ipad-simulator-after.png) |
| `functional/permissions-bulk-deny` | functional | See coverage.json | ![functional permissions-bulk-deny](ios/functional/permissions-bulk-deny/ipad-simulator-before.png) |
| `functional/permissions-bulk-deny` | functional | allPermissionsGranted follows the results / revokedPermissions lists denied entries | ![functional permissions-bulk-deny](ios/functional/permissions-bulk-deny/iphone-simulator-after.png) |
| `functional/permissions-bulk-deny` | functional | See coverage.json | ![functional permissions-bulk-deny](ios/functional/permissions-bulk-deny/iphone-simulator-before.png) |
| `functional/permissions-sms-rows` | functional | See coverage.json | ![functional permissions-sms-rows](ios/functional/permissions-sms-rows/ipad-simulator-after.png) |
| `functional/permissions-sms-rows` | functional | See coverage.json | ![functional permissions-sms-rows](ios/functional/permissions-sms-rows/ipad-simulator-before.png) |
| `functional/permissions-sms-rows` | functional | The rows render independently / Android reports its own status / iOS reports NotGranted for read/receive | ![functional permissions-sms-rows](ios/functional/permissions-sms-rows/iphone-simulator-after.png) |
| `functional/permissions-sms-rows` | functional | See coverage.json | ![functional permissions-sms-rows](ios/functional/permissions-sms-rows/iphone-simulator-before.png) |
| `functional/scaffold-tab` | functional | See coverage.json | ![functional scaffold-tab](ios/functional/scaffold-tab/ipad-simulator-after.png) |
| `functional/scaffold-tab` | functional | See coverage.json | ![functional scaffold-tab](ios/functional/scaffold-tab/ipad-simulator-before.png) |
| `functional/scaffold-tab` | functional | Content is not obscured by the bars / The tab selection changes | ![functional scaffold-tab](ios/functional/scaffold-tab/iphone-simulator-after.png) |
| `functional/scaffold-tab` | functional | See coverage.json | ![functional scaffold-tab](ios/functional/scaffold-tab/iphone-simulator-before.png) |
| `functional/sheet` | functional | See coverage.json | ![functional sheet](ios/functional/sheet/ipad-simulator-after.png) |
| `functional/sheet` | functional | See coverage.json | ![functional sheet](ios/functional/sheet/ipad-simulator-before.png) |
| `functional/sheet` | functional | The sheet presents with a drag handle / Dismissal reports back / The iOS inset/shape parameters are ignored | ![functional sheet](ios/functional/sheet/iphone-simulator-after.png) |
| `functional/sheet` | functional | See coverage.json | ![functional sheet](ios/functional/sheet/iphone-simulator-before.png) |
| `functional/sheet-veto` | functional | See coverage.json | ![functional sheet-veto](ios/functional/sheet-veto/ipad-simulator-before.png) |
| `functional/sheet-veto` | functional | See coverage.json | ![functional sheet-veto](ios/functional/sheet-veto/ipad-simulator-failed-after.png) |
| `functional/sheet-veto` | functional | See coverage.json | ![functional sheet-veto](ios/functional/sheet-veto/iphone-simulator-before.png) |
| `functional/sheet-veto` | functional | The vetoed dismissal keeps the sheet / The close button dismisses it | ![functional sheet-veto](ios/functional/sheet-veto/iphone-simulator-failed-after.png) |
| `functional/slider` | functional | See coverage.json | ![functional slider](ios/functional/slider/ipad-simulator-before.png) |
| `functional/slider` | functional | See coverage.json | ![functional slider](ios/functional/slider/ipad-simulator-failed-after.png) |
| `functional/slider` | functional | See coverage.json | ![functional slider](ios/functional/slider/iphone-simulator-before.png) |
| `functional/slider` | functional | The percentage follows the thumb / The value stays within 0..100 | ![functional slider](ios/functional/slider/iphone-simulator-failed-after.png) |
| `functional/switch` | functional | See coverage.json | ![functional switch](ios/functional/switch/ipad-simulator-after.png) |
| `functional/switch` | functional | See coverage.json | ![functional switch](ios/functional/switch/ipad-simulator-before.png) |
| `functional/switch` | functional | The readout follows the checked state / The disabled switch does not change | ![functional switch](ios/functional/switch/iphone-simulator-after.png) |
| `functional/switch` | functional | See coverage.json | ![functional switch](ios/functional/switch/iphone-simulator-before.png) |
| `functional/time-24h` | functional | See coverage.json | ![functional time-24h](ios/functional/time-24h/ipad-simulator-after.png) |
| `functional/time-24h` | functional | See coverage.json | ![functional time-24h](ios/functional/time-24h/ipad-simulator-before.png) |
| `functional/time-24h` | functional | The 24-hour readout renders / iOS follows the device locale | ![functional time-24h](ios/functional/time-24h/iphone-simulator-after.png) |
| `functional/time-24h` | functional | See coverage.json | ![functional time-24h](ios/functional/time-24h/iphone-simulator-before.png) |
| `functional/toolbar` | functional | See coverage.json | ![functional toolbar](ios/functional/toolbar/ipad-simulator-after.png) |
| `functional/toolbar` | functional | See coverage.json | ![functional toolbar](ios/functional/toolbar/ipad-simulator-before.png) |
| `functional/toolbar` | functional | The Material toolbar expands / iOS requires non-empty iosItems and shows a native toolbar | ![functional toolbar](ios/functional/toolbar/iphone-simulator-after.png) |
| `functional/toolbar` | functional | See coverage.json | ![functional toolbar](ios/functional/toolbar/iphone-simulator-before.png) |
| `functional/topbar` | functional | See coverage.json | ![functional topbar](ios/functional/topbar/ipad-simulator-failed-after.png) |
| `functional/topbar` | functional | The title is visible / Bar items render natively on iOS / The menu action fires | ![functional topbar](ios/functional/topbar/iphone-simulator-after.png) |
| `functional/topbar` | functional | See coverage.json | ![functional topbar](ios/functional/topbar/iphone-simulator-before.png) |
| `functional/webview` | functional | See coverage.json | ![functional webview](ios/functional/webview/ipad-simulator-before.png) |
| `functional/webview` | functional | See coverage.json | ![functional webview](ios/functional/webview/ipad-simulator-failed-after.png) |
| `functional/webview-js` | functional | See coverage.json | ![functional webview-js](ios/functional/webview-js/ipad-simulator-after.png) |
| `functional/webview-js` | functional | See coverage.json | ![functional webview-js](ios/functional/webview-js/ipad-simulator-before.png) |
| `functional/webview-js` | functional | JavaScript is off by default / Enabling it allows the evaluation | ![functional webview-js](ios/functional/webview-js/iphone-simulator-after.png) |
| `functional/webview-js` | functional | See coverage.json | ![functional webview-js](ios/functional/webview-js/iphone-simulator-before.png) |
| `functional/webview-js` | functional | See coverage.json | ![functional webview-js](ios/functional/webview-js/iphone-simulator-failed-after.png) |
| `geo-math/overview` | geo-math | Deterministic LatLng distance/bearing plus the tracker-unavailable state. | ![geo-math overview](ios/geo-math/overview/ipad-simulator.png) |
| `geo-math/overview` | geo-math | Deterministic LatLng distance/bearing plus the tracker-unavailable state. | ![geo-math overview](ios/geo-math/overview/iphone-simulator.png) |
| `home/index` | home | Searchable component index, stable routes and per-screen reset. | ![home index](ios/home/index/ipad-simulator.png) |
| `home/index` | home | Searchable component index, stable routes and per-screen reset. | ![home index](ios/home/index/iphone-simulator.png) |
| `io-camera-picker/overview` | io-camera-picker | Camera launch and the platform-specific unavailable fallback. | ![io-camera-picker overview](ios/io-camera-picker/overview/ipad-simulator.png) |
| `io-camera-picker/overview` | io-camera-picker | Camera launch and the platform-specific unavailable fallback. | ![io-camera-picker overview](ios/io-camera-picker/overview/iphone-simulator.png) |
| `io-file-picker/overview` | io-file-picker | Platform file selection, filters, metadata and streaming readout. | ![io-file-picker overview](ios/io-file-picker/overview/ipad-simulator.png) |
| `io-file-picker/overview` | io-file-picker | Platform file selection, filters, metadata and streaming readout. | ![io-file-picker overview](ios/io-file-picker/overview/iphone-simulator.png) |
| `io-file-saver/overview` | io-file-saver | Save/export entry point and result state. | ![io-file-saver overview](ios/io-file-saver/overview/ipad-simulator.png) |
| `io-file-saver/overview` | io-file-saver | Save/export entry point and result state. | ![io-file-saver overview](ios/io-file-saver/overview/iphone-simulator.png) |
| `io-image-picker/overview` | io-image-picker | Picked image preview through the KmpFile Coil pipeline. | ![io-image-picker overview](ios/io-image-picker/overview/ipad-simulator.png) |
| `io-image-picker/overview` | io-image-picker | Picked image preview through the KmpFile Coil pipeline. | ![io-image-picker overview](ios/io-image-picker/overview/iphone-simulator.png) |
| `limitations/known-limitations` | limitations | Source-confirmed unsupported and internal APIs; not working parity. | ![limitations known-limitations](ios/limitations/known-limitations/ipad-simulator.png) |
| `limitations/known-limitations` | limitations | Source-confirmed unsupported and internal APIs; not working parity. | ![limitations known-limitations](ios/limitations/known-limitations/iphone-simulator.png) |
| `permissions/overview` | permissions | Public permission status and request rows; OS dialogs are separate. | ![permissions overview](ios/permissions/overview/ipad-simulator.png) |
| `permissions/overview` | permissions | Public permission status and request rows; OS dialogs are separate. | ![permissions overview](ios/permissions/overview/iphone-simulator.png) |
| `share/overview` | share | Native share payloads and terminal result state. | ![share overview](ios/share/overview/ipad-simulator.png) |
| `share/overview` | share | Native share payloads and terminal result state. | ![share overview](ios/share/overview/iphone-simulator.png) |
| `ui-adaptive-alert-dialog/overview` | ui-adaptive-alert-dialog | See coverage.json | ![ui-adaptive-alert-dialog overview](ios/ui-adaptive-alert-dialog/overview/ipad-simulator.png) |
| `ui-adaptive-alert-dialog/overview` | ui-adaptive-alert-dialog | See coverage.json | ![ui-adaptive-alert-dialog overview](ios/ui-adaptive-alert-dialog/overview/iphone-simulator.png) |
| `ui-adaptive-alert-dialog/simple` | ui-adaptive-alert-dialog | See coverage.json | ![ui-adaptive-alert-dialog simple](ios/ui-adaptive-alert-dialog/simple/ipad-simulator.png) |
| `ui-adaptive-alert-dialog/simple` | ui-adaptive-alert-dialog | Only one action is visible / The dialog dismisses | ![ui-adaptive-alert-dialog simple](ios/ui-adaptive-alert-dialog/simple/iphone-simulator.png) |
| `ui-adaptive-bottom-sheet/expanded` | ui-adaptive-bottom-sheet | See coverage.json | ![ui-adaptive-bottom-sheet expanded](ios/ui-adaptive-bottom-sheet/expanded/ipad-simulator.png) |
| `ui-adaptive-bottom-sheet/expanded` | ui-adaptive-bottom-sheet | See coverage.json | ![ui-adaptive-bottom-sheet expanded](ios/ui-adaptive-bottom-sheet/expanded/iphone-simulator.png) |
| `ui-adaptive-bottom-sheet/overview` | ui-adaptive-bottom-sheet | The sheet uses the wide presentation / Close dismisses it | ![ui-adaptive-bottom-sheet overview](ios/ui-adaptive-bottom-sheet/overview/ipad-simulator.png) |
| `ui-adaptive-bottom-sheet/overview` | ui-adaptive-bottom-sheet | See coverage.json | ![ui-adaptive-bottom-sheet overview](ios/ui-adaptive-bottom-sheet/overview/iphone-simulator.png) |
| `ui-adaptive-button/overview` | ui-adaptive-button | See coverage.json | ![ui-adaptive-button overview](ios/ui-adaptive-button/overview/ipad-simulator.png) |
| `ui-adaptive-button/overview` | ui-adaptive-button | The label is visible / The leading icon has a non-empty content description where supplied | ![ui-adaptive-button overview](ios/ui-adaptive-button/overview/iphone-simulator.png) |
| `ui-adaptive-clickable/overview` | ui-adaptive-clickable | See coverage.json | ![ui-adaptive-clickable overview](ios/ui-adaptive-clickable/overview/ipad-simulator.png) |
| `ui-adaptive-clickable/overview` | ui-adaptive-clickable | See coverage.json | ![ui-adaptive-clickable overview](ios/ui-adaptive-clickable/overview/iphone-simulator.png) |
| `ui-adaptive-date-picker/overview` | ui-adaptive-date-picker | See coverage.json | ![ui-adaptive-date-picker overview](ios/ui-adaptive-date-picker/overview/ipad-simulator.png) |
| `ui-adaptive-date-picker/overview` | ui-adaptive-date-picker | The readout changes / The native iOS calendar or Material picker is used | ![ui-adaptive-date-picker overview](ios/ui-adaptive-date-picker/overview/iphone-simulator.png) |
| `ui-adaptive-dropdown/menu` | ui-adaptive-dropdown | See coverage.json | ![ui-adaptive-dropdown menu](ios/ui-adaptive-dropdown/menu/ipad-simulator.png) |
| `ui-adaptive-dropdown/menu` | ui-adaptive-dropdown | iOS shows inline submenus / Material shows the caller-built section divider | ![ui-adaptive-dropdown menu](ios/ui-adaptive-dropdown/menu/iphone-simulator.png) |
| `ui-adaptive-dropdown/overview` | ui-adaptive-dropdown | See coverage.json | ![ui-adaptive-dropdown overview](ios/ui-adaptive-dropdown/overview/ipad-simulator.png) |
| `ui-adaptive-dropdown/overview` | ui-adaptive-dropdown | See coverage.json | ![ui-adaptive-dropdown overview](ios/ui-adaptive-dropdown/overview/iphone-simulator.png) |
| `ui-adaptive-navigation-bar/overview` | ui-adaptive-navigation-bar | See coverage.json | ![ui-adaptive-navigation-bar overview](ios/ui-adaptive-navigation-bar/overview/ipad-simulator.png) |
| `ui-adaptive-navigation-bar/overview` | ui-adaptive-navigation-bar | See coverage.json | ![ui-adaptive-navigation-bar overview](ios/ui-adaptive-navigation-bar/overview/iphone-simulator.png) |
| `ui-adaptive-progress/overview` | ui-adaptive-progress | See coverage.json | ![ui-adaptive-progress overview](ios/ui-adaptive-progress/overview/ipad-simulator.png) |
| `ui-adaptive-progress/overview` | ui-adaptive-progress | All three indeterminate indicators render and animate / No determinate progress control is advertised | ![ui-adaptive-progress overview](ios/ui-adaptive-progress/overview/iphone-simulator.png) |
| `ui-adaptive-scaffold/overview` | ui-adaptive-scaffold | Bars span the window / Tab content updates without clipping | ![ui-adaptive-scaffold overview](ios/ui-adaptive-scaffold/overview/ipad-simulator.png) |
| `ui-adaptive-scaffold/overview` | ui-adaptive-scaffold | See coverage.json | ![ui-adaptive-scaffold overview](ios/ui-adaptive-scaffold/overview/iphone-simulator.png) |
| `ui-adaptive-slider/overview` | ui-adaptive-slider | See coverage.json | ![ui-adaptive-slider overview](ios/ui-adaptive-slider/overview/ipad-simulator.png) |
| `ui-adaptive-slider/overview` | ui-adaptive-slider | Values snap to the stepped positions / Tick marks are visible on iOS below 26 | ![ui-adaptive-slider overview](ios/ui-adaptive-slider/overview/iphone-simulator.png) |
| `ui-adaptive-switch/overview` | ui-adaptive-switch | See coverage.json | ![ui-adaptive-switch overview](ios/ui-adaptive-switch/overview/ipad-simulator.png) |
| `ui-adaptive-switch/overview` | ui-adaptive-switch | The 51x31 track and thumb render on every target / The disabled switch cannot be toggled | ![ui-adaptive-switch overview](ios/ui-adaptive-switch/overview/iphone-simulator.png) |
| `ui-adaptive-time-picker/overview` | ui-adaptive-time-picker | See coverage.json | ![ui-adaptive-time-picker overview](ios/ui-adaptive-time-picker/overview/ipad-simulator.png) |
| `ui-adaptive-time-picker/overview` | ui-adaptive-time-picker | See coverage.json | ![ui-adaptive-time-picker overview](ios/ui-adaptive-time-picker/overview/iphone-simulator.png) |
| `ui-adaptive-toolbar/overview` | ui-adaptive-toolbar | See coverage.json | ![ui-adaptive-toolbar overview](ios/ui-adaptive-toolbar/overview/ipad-simulator.png) |
| `ui-adaptive-toolbar/overview` | ui-adaptive-toolbar | See coverage.json | ![ui-adaptive-toolbar overview](ios/ui-adaptive-toolbar/overview/iphone-simulator.png) |
| `ui-adaptive-top-bar/overview` | ui-adaptive-top-bar | See coverage.json | ![ui-adaptive-top-bar overview](ios/ui-adaptive-top-bar/overview/ipad-simulator.png) |
| `ui-adaptive-top-bar/overview` | ui-adaptive-top-bar | System-name and rasterized vector images render / The icon font fallback is not presented as an SF Symbol / The UIKitImage.Bitmap variant is not exercised by this screen | ![ui-adaptive-top-bar overview](ios/ui-adaptive-top-bar/overview/iphone-simulator.png) |
| `ui-cupertino-icons/category-arrows` | ui-cupertino-icons | See coverage.json | ![ui-cupertino-icons category-arrows](ios/ui-cupertino-icons/category-arrows/ipad-simulator.png) |
| `ui-cupertino-icons/category-arrows` | ui-cupertino-icons | See coverage.json | ![ui-cupertino-icons category-arrows](ios/ui-cupertino-icons/category-arrows/iphone-simulator.png) |
| `ui-cupertino-icons/category-communication` | ui-cupertino-icons | See coverage.json | ![ui-cupertino-icons category-communication](ios/ui-cupertino-icons/category-communication/ipad-simulator.png) |
| `ui-cupertino-icons/category-communication` | ui-cupertino-icons | See coverage.json | ![ui-cupertino-icons category-communication](ios/ui-cupertino-icons/category-communication/iphone-simulator.png) |
| `ui-cupertino-icons/overview` | ui-cupertino-icons | See coverage.json | ![ui-cupertino-icons overview](ios/ui-cupertino-icons/overview/ipad-simulator.png) |
| `ui-cupertino-icons/overview` | ui-cupertino-icons | The grid filters to matching names / The count updates / Representative glyphs render without tofu | ![ui-cupertino-icons overview](ios/ui-cupertino-icons/overview/iphone-simulator.png) |
| `ui-liquid-glass/overview` | ui-liquid-glass | See coverage.json | ![ui-liquid-glass overview](ios/ui-liquid-glass/overview/ipad-simulator.png) |
| `webview/after-back` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview after-back](ios/webview/after-back/ipad-simulator.png) |
| `webview/after-back` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview after-back](ios/webview/after-back/iphone-simulator.png) |
| `webview/cookie-roundtrip` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview cookie-roundtrip](ios/webview/cookie-roundtrip/iphone-simulator.png) |
| `webview/cookies-cleared` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview cookies-cleared](ios/webview/cookies-cleared/iphone-simulator.png) |
| `webview/invalid-destination` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview invalid-destination](ios/webview/invalid-destination/iphone-simulator.png) |
| `webview/javascript-title` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview javascript-title](ios/webview/javascript-title/iphone-simulator.png) |
| `webview/overview` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview overview](ios/webview/overview/ipad-simulator.png) |
| `webview/overview` | webview | Deterministic HTML, navigation/errors, JavaScript and cookie state. | ![webview overview](ios/webview/overview/iphone-simulator.png) |

## Side-by-side Android / iOS

- [geo-math/overview.png](compare/geo-math/overview.png)
- [home/index.png](compare/home/index.png)
- [io-camera-picker/overview.png](compare/io-camera-picker/overview.png)
- [io-file-picker/overview.png](compare/io-file-picker/overview.png)
- [io-file-saver/overview.png](compare/io-file-saver/overview.png)
- [io-image-picker/overview.png](compare/io-image-picker/overview.png)
- [limitations/known-limitations.png](compare/limitations/known-limitations.png)
- [permissions/overview.png](compare/permissions/overview.png)
- [share/overview.png](compare/share/overview.png)
- [ui-adaptive-alert-dialog/overview.png](compare/ui-adaptive-alert-dialog/overview.png)
- [ui-adaptive-alert-dialog/simple.png](compare/ui-adaptive-alert-dialog/simple.png)
- [ui-adaptive-bottom-sheet/expanded.png](compare/ui-adaptive-bottom-sheet/expanded.png)
- [ui-adaptive-bottom-sheet/overview.png](compare/ui-adaptive-bottom-sheet/overview.png)
- [ui-adaptive-button/overview.png](compare/ui-adaptive-button/overview.png)
- [ui-adaptive-clickable/overview.png](compare/ui-adaptive-clickable/overview.png)
- [ui-adaptive-date-picker/overview.png](compare/ui-adaptive-date-picker/overview.png)
- [ui-adaptive-dropdown/menu.png](compare/ui-adaptive-dropdown/menu.png)
- [ui-adaptive-dropdown/overview.png](compare/ui-adaptive-dropdown/overview.png)
- [ui-adaptive-navigation-bar/overview.png](compare/ui-adaptive-navigation-bar/overview.png)
- [ui-adaptive-progress/overview.png](compare/ui-adaptive-progress/overview.png)
- [ui-adaptive-scaffold/overview.png](compare/ui-adaptive-scaffold/overview.png)
- [ui-adaptive-slider/overview.png](compare/ui-adaptive-slider/overview.png)
- [ui-adaptive-switch/overview.png](compare/ui-adaptive-switch/overview.png)
- [ui-adaptive-toolbar/overview.png](compare/ui-adaptive-toolbar/overview.png)
- [ui-adaptive-top-bar/overview.png](compare/ui-adaptive-top-bar/overview.png)
- [ui-cupertino-icons/overview.png](compare/ui-cupertino-icons/overview.png)
- [webview/cookie-roundtrip.png](compare/webview/cookie-roundtrip.png)
- [webview/cookies-cleared.png](compare/webview/cookies-cleared.png)
- [webview/invalid-destination.png](compare/webview/invalid-destination.png)
- [webview/javascript-title.png](compare/webview/javascript-title.png)
- [webview/overview.png](compare/webview/overview.png)

## Side-by-side tablet windows

- [geo-math/overview/tablet.png](compare-tablet/geo-math/overview/tablet.png)
- [home/index/tablet.png](compare-tablet/home/index/tablet.png)
- [io-camera-picker/overview/tablet.png](compare-tablet/io-camera-picker/overview/tablet.png)
- [io-file-picker/overview/tablet.png](compare-tablet/io-file-picker/overview/tablet.png)
- [io-file-saver/overview/tablet.png](compare-tablet/io-file-saver/overview/tablet.png)
- [io-image-picker/overview/tablet.png](compare-tablet/io-image-picker/overview/tablet.png)
- [limitations/known-limitations/tablet.png](compare-tablet/limitations/known-limitations/tablet.png)
- [permissions/overview/tablet.png](compare-tablet/permissions/overview/tablet.png)
- [share/overview/tablet.png](compare-tablet/share/overview/tablet.png)
- [ui-adaptive-alert-dialog/overview/tablet.png](compare-tablet/ui-adaptive-alert-dialog/overview/tablet.png)
- [ui-adaptive-alert-dialog/simple/tablet.png](compare-tablet/ui-adaptive-alert-dialog/simple/tablet.png)
- [ui-adaptive-bottom-sheet/expanded/tablet.png](compare-tablet/ui-adaptive-bottom-sheet/expanded/tablet.png)
- [ui-adaptive-bottom-sheet/overview/tablet.png](compare-tablet/ui-adaptive-bottom-sheet/overview/tablet.png)
- [ui-adaptive-button/overview/tablet.png](compare-tablet/ui-adaptive-button/overview/tablet.png)
- [ui-adaptive-clickable/overview/tablet.png](compare-tablet/ui-adaptive-clickable/overview/tablet.png)
- [ui-adaptive-date-picker/overview/tablet.png](compare-tablet/ui-adaptive-date-picker/overview/tablet.png)
- [ui-adaptive-dropdown/overview/tablet.png](compare-tablet/ui-adaptive-dropdown/overview/tablet.png)
- [ui-adaptive-navigation-bar/overview/tablet.png](compare-tablet/ui-adaptive-navigation-bar/overview/tablet.png)
- [ui-adaptive-progress/overview/tablet.png](compare-tablet/ui-adaptive-progress/overview/tablet.png)
- [ui-adaptive-scaffold/overview/tablet.png](compare-tablet/ui-adaptive-scaffold/overview/tablet.png)
- [ui-adaptive-slider/overview/tablet.png](compare-tablet/ui-adaptive-slider/overview/tablet.png)
- [ui-adaptive-switch/overview/tablet.png](compare-tablet/ui-adaptive-switch/overview/tablet.png)
- [ui-adaptive-time-picker/overview/tablet.png](compare-tablet/ui-adaptive-time-picker/overview/tablet.png)
- [ui-adaptive-toolbar/overview/tablet.png](compare-tablet/ui-adaptive-toolbar/overview/tablet.png)
- [ui-adaptive-top-bar/overview/tablet.png](compare-tablet/ui-adaptive-top-bar/overview/tablet.png)
- [ui-cupertino-icons/category-arrows/tablet.png](compare-tablet/ui-cupertino-icons/category-arrows/tablet.png)
- [ui-cupertino-icons/category-communication/tablet.png](compare-tablet/ui-cupertino-icons/category-communication/tablet.png)
- [ui-cupertino-icons/overview/tablet.png](compare-tablet/ui-cupertino-icons/overview/tablet.png)
- [ui-liquid-glass/overview/tablet.png](compare-tablet/ui-liquid-glass/overview/tablet.png)
- [webview/after-back/tablet.png](compare-tablet/webview/after-back/tablet.png)
- [webview/overview/tablet.png](compare-tablet/webview/overview/tablet.png)

## Functional flows

- `android/functional-api35-phone.json` — device `api35-phone`: **23 passed**, 2 failed, 5 blocked, 32 flows. Runs: [45993784178](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/45993784178), [46099102700](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46099102700).
- `android/functional-api35-tablet.json` — device `api35-tablet`: **24 passed**, 1 failed, 5 blocked, 32 flows. Runs: [45993784178](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/45993784178), [46099102700](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46099102700).
- `ios/functional-ipad-simulator.json` — device `ipad-simulator`: **18 passed**, 8 failed, 5 blocked, 32 flows. Runs: [46014167086](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46014167086), [46108448068](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46108448068).
- `ios/functional-iphone-simulator.json` — device `iphone-simulator`: **19 passed**, 3 failed, 0 blocked, 22 flows (partial result file; see showcase/evidence/). Runs: [46014167086](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46014167086), [46108448068](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46108448068).

## Status

The per-row execution state is maintained in
[showcase/coverage.json](../showcase/coverage.json) and summarized in
[showcase/COVERAGE.md](../showcase/COVERAGE.md). A capture proves the screen
rendered on that device; interaction assertions are recorded separately and
must name the run/attempt/job that produced them.

Unsupported rows point at the Known Limitations screen and are marked
`not-applicable`; they are not evidence of working functionality.
