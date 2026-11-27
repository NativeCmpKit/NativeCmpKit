#!/usr/bin/env python3
"""Generate the NativeCmpKit showcase coverage manifest and readable index.

The JSON file is authoritative. Rows start as not-run and are updated from
reviewed hosted sessions. Regenerate after editing the row table below:

    python3 showcase/generate_coverage.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_SHA = "a2c48c0b9ebf3524192e680ecd4becc1f2880bb8"
BRANCH = "feature/showcase-ui-verification"
ANDROID_APP = "io.github.apdelrahman1911.nativecmpkit.sample"
IOS_BUNDLE = "io.github.apdelrahman1911.nativecmpkit.sample"

SUPPORT_ALL = ("supported", "supported", "supported", "supported")
SUPPORT_MOBILE = ("supported", "supported", "unsupported", "unsupported")
SUPPORT_IOS = ("unsupported", "supported", "unsupported", "unsupported")
SUPPORT_ANDROID = ("supported", "unsupported", "unsupported", "unsupported")
SUPPORT_NONE = ("unsupported", "unsupported", "unsupported", "unsupported")


def slug(value: str) -> str:
    out = []
    for ch in value.lower():
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def support(values: tuple[str, str, str, str]) -> dict[str, str]:
    return dict(zip(("android", "ios", "desktop", "web"), values))


def row(
    row_id: str,
    module: str,
    component: str,
    variant: str,
    values,
    route: str,
    steps: list[str],
    expected: list[str],
    *,
    window: str = "phone",
    setup: list[str] | None = None,
    limitations: list[str] | None = None,
    screenshot: str | None = None,
) -> dict:
    values = SUPPORT_ALL if values == "all" else values
    values = SUPPORT_MOBILE if values == "mobile" else values
    values = SUPPORT_IOS if values == "ios" else values
    values = SUPPORT_ANDROID if values == "android" else values
    values = SUPPORT_NONE if values == "none" else values
    support_map = support(values)
    component_slug = slug(component)
    scenario_slug = slug(variant)
    shots = screenshot or {
        "android": f"screenshots/android/{component_slug}/{scenario_slug}/api35-phone.png",
        "ios": f"screenshots/ios/{component_slug}/{scenario_slug}/iphone-simulator.png",
    }
    execution = {
        platform: {
            "status": "not-run" if state == "supported" else "not-applicable",
            "run": None,
            "attempt": None,
            "job": None,
        }
        for platform, state in support_map.items()
    }
    return {
        "id": row_id,
        "module": module,
        "component": component,
        "variant": variant,
        "support": support_map,
        "windowClass": window,
        "route": route,
        "setup": setup or [],
        "steps": steps,
        "expected": expected,
        "flowId": f"android-phone-{slug(component)}-{scenario_slug}",
        "screenshot": shots,
        "execution": execution,
        "defect": None,
        "limitations": limitations or [],
    }


ROWS = [
    # UI controls
    row("UI-BUTTON-001", "kira-ui", "AdaptiveButton", "filled enabled and disabled",
        "all", "Button",
        ["Open the Button screen", "Tap the enabled filled button", "Read the click counter"],
        ["Counter increments from 0 to 1", "The disabled button stays visible and unchanged"]),
    row("UI-BUTTON-002", "kira-ui", "AdaptiveButton", "icon and label content",
        "all", "Button",
        ["Open the Button screen", "Inspect the icon-label row"],
        ["The label is visible", "The leading icon has a non-empty content description where supplied"]),
    row("UI-BUTTON-003", "kira-ui", "AdaptiveIconButton", "three enabled and one disabled",
        "all", "Button",
        ["Open the Button screen", "Inspect the icon-button row"],
        ["Four icon buttons render", "The disabled button cannot be activated"]),
    row("UI-BUTTON-004", "kira-ui", "CupertinoButton", "filled, bordered, plain, disabled",
        "all", "Button",
        ["Open the Button screen", "Inspect the Cupertino section", "Tap the filled variant"],
        ["All color factories render distinct containers",
         "Disabled variant uses the disabled alpha and does not count as a tap"],
        limitations=["The public API has no size parameter and no selected state."]),
    row("UI-CLICK-001", "kira-ui", "Modifier.adaptiveClickable", "single, long, double, disabled",
        "all", "AdaptiveClickable",
        ["Open the Adaptive Clickable screen", "Tap, long-press, and double-tap the card",
         "Read the event log"],
        ["Each gesture is counted once", "The disabled card stays inert",
         "The Material platform shows indication while iOS uses press scale"]),
    row("UI-SWITCH-001", "kira-ui", "AdaptiveSwitch", "on, off and disabled",
        "all", "Switch",
        ["Open the Switch screen", "Toggle the first switch", "Inspect the disabled switch"],
        ["The readout follows the checked state", "The disabled switch does not change"]),
    row("UI-SWITCH-002", "kira-ui", "CupertinoSwitch", "on, off, disabled, thumb content",
        "all", "Switch",
        ["Open the Switch screen", "Inspect the Cupertino section"],
        ["The 51x31 track and thumb render on every target",
         "The disabled switch cannot be toggled"],
        limitations=["On iOS 26 AdaptiveSwitch drops thumbContent and custom colors; CupertinoSwitch is the parity control."]),
    row("UI-SLIDER-001", "kira-ui", "AdaptiveSlider", "continuous value readout",
        "all", "Slider",
        ["Open the Slider screen", "Drag the brightness slider", "Read the percentage"],
        ["The percentage follows the thumb", "The value stays within 0..100"]),
    row("UI-SLIDER-002", "kira-ui", "AdaptiveSlider", "discrete steps",
        "all", "Slider",
        ["Open the Slider screen", "Move the stepped slider to several positions"],
        ["Values snap to the stepped positions", "Tick marks are visible on iOS below 26"],
        limitations=["iOS 26 LiquidGlassSlider silently drops the steps parameter."]),
    row("UI-SLIDER-003", "kira-ui", "AdaptiveSlider", "disabled and custom range",
        "all", "Slider",
        ["Open the Slider screen", "Inspect the disabled slider", "Drag the 0..100 slider"],
        ["The disabled slider does not move", "The custom range readout reaches 100"]),
    row("UI-PROGRESS-001", "kira-ui", "AdaptiveCircularProgressIndicator", "indeterminate sizes",
        "all", "ProgressBar",
        ["Open the Progress Bar screen", "Inspect the three sizes"],
        ["All three indeterminate indicators render and animate",
         "No determinate progress control is advertised"]),
    row("UI-PROGRESS-002", "kira-ui", "CupertinoActivityIndicator", "spinner",
        "all", "ProgressBar",
        ["Open the Progress Bar screen", "Inspect the Cupertino spinner"],
        ["The eight-spoke spinner is visible", "Progress semantics are present"]),
    row("UI-PROGRESS-003", "kira-ui", "AdaptiveCircularProgressIndicator", "determinate",
        "none", "ProgressBar",
        ["Attempt to construct a determinate indicator from public API"],
        ["No determinate parameter or overload exists"],
        screenshot={"android": "screenshots/android/ui-progress/unsupported-determinate/api35-phone.png",
                    "ios": "screenshots/ios/ui-progress/unsupported-determinate/iphone-simulator.png"},
        limitations=["Determinate circular progress is not part of the public API."]),
    row("UI-FAB-001", "kira-ui", "AdaptiveExpandableFAB", "expanded/collapsed",
        "none", "Button",
        ["Attempt to call AdaptiveExpandableFAB from the showcase module"],
        ["Compilation is impossible because the declaration is internal"],
        screenshot={"android": "screenshots/android/ui-fab/unsupported-internal/api35-phone.png",
                    "ios": "screenshots/ios/ui-fab/unsupported-internal/iphone-simulator.png"},
        limitations=["AdaptiveExpandableFAB and UIKitExpandableFABItem are internal in this revision."]),

    # Date and time
    row("UI-DATE-001", "kira-ui", "AdaptiveDatePicker", "inline selection and readout",
        "all", "DatePicker",
        ["Open the Date Picker screen", "Select a different day", "Read the selected date"],
        ["The readout changes", "The native iOS calendar or Material picker is used"]),
    row("UI-DATE-002", "kira-ui", "AdaptiveCompactDatePicker", "open, confirm, cancel",
        "all", "DatePicker",
        ["Open the Date Picker screen", "Open the compact picker", "Cancel once",
         "Open again and confirm a date"],
        ["Cancel leaves the previous selection", "Confirm updates the readout"]),
    row("UI-DATE-003", "kira-ui", "AdaptiveDateRangePicker", "start and end transition",
        "all", "DatePicker",
        ["Open the Date Picker screen", "Tap a start day", "Tap a later end day",
         "Tap inside the completed range"],
        ["The range start/end readout appears", "A tap inside a completed range starts a new range",
         "The iOS < 16.2 fallback is labelled as Material"]),
    row("UI-DATE-004", "kira-ui", "DateBounds and SelectableDates", "bounded weekdays only",
        "all", "DatePicker",
        ["Open the Date Picker screen", "Enable Weekdays only", "Attempt a weekend",
         "Choose Next 30 days"],
        ["Weekend selection is rejected or snapped to a selectable day",
         "Dates outside the bound are unavailable"]),
    row("UI-DATE-005", "kira-ui", "UIKitDisplayMode", "picker and wheels",
        "ios", "DatePicker",
        ["Open the Date Picker screen on iOS", "Inspect the wheels picker"],
        ["The wheels presentation differs from the inline calendar",
         "The mode is fixed at state creation"]),
    row("UI-TIME-001", "kira-ui", "AdaptiveTimePicker", "12-hour and 24-hour states",
        "all", "TimePicker",
        ["Open the Time Picker screen", "Inspect both states"],
        ["Both time readouts render", "The iOS format follows the device locale even when is24Hour differs"]),

    # Presentation
    row("UI-ALERT-001", "kira-ui", "AdaptiveAlertDialog", "two-button confirm and cancel",
        "all", "Dialog",
        ["Open the Alert Dialog screen", "Show the simple dialog", "Tap Cancel",
         "Show again and tap Ok"],
        ["Cancel closes without a confirmation", "Ok closes and records the confirmation"]),
    row("UI-ALERT-002", "kira-ui", "AdaptiveAlertDialog", "single button",
        "all", "Dialog",
        ["Open the Alert Dialog screen", "Show the single-button dialog", "Tap Got it"],
        ["Only one action is visible", "The dialog dismisses"]),
    row("UI-ALERT-003", "kira-ui", "AdaptiveBasicAlertDialog", "text fields and critical severity",
        "ios", "Dialog",
        ["Open the Alert Dialog screen on iOS", "Show the text-field dialog",
         "Type a name", "Show the complex dialog"],
        ["The confirm action enables after typing", "Secure/number-pad fields are configured",
         "Critical severity is applied on supported UIKit hosts"]),
    row("UI-ALERT-004", "kira-ui", "AlertDialogIosStyle.ActionSheet", "iPhone sheet and iPad popover",
        "ios", "Dialog",
        ["Open the Alert Dialog screen", "Show the ActionSheet"],
        ["iPhone presents a bottom action sheet",
         "iPad presents a centred popover because no public anchor API exists"],
        limitations=["The iPad anchor is the presenting view, not a caller-selected source view or bar item."]),
    row("UI-SHEET-001", "kira-ui", "AdaptiveBottomSheet", "show, content, dismiss",
        "all", "BottomSheet",
        ["Open the Bottom Sheet screen", "Open the sheet", "Interact with its content",
         "Swipe down"],
        ["The sheet presents with a drag handle", "Dismissal reports back",
         "The iOS inset/shape parameters are ignored"]),

    # Menus and bars
    row("UI-MENU-001", "kira-ui", "AdaptiveDropDown", "simple destructive and disabled items",
        "all", "DropDown",
        ["Open the Drop Down screen", "Open the simple menu", "Tap an enabled item",
         "Reopen and inspect the disabled item"],
        ["The selected action readout changes", "The destructive item is styled as destructive",
         "The disabled item does not fire"]),
    row("UI-MENU-002", "kira-ui", "AdaptiveDropDownSection", "sections",
        "all", "DropDown",
        ["Open the Drop Down screen", "Open the sectioned menu"],
        ["iOS shows inline submenus", "Material shows the caller-built section divider"]),
    row("UI-BAR-001", "kira-ui", "AdaptiveScaffold", "top bar, bottom bar, content padding",
        "all", "ScaffoldDemo",
        ["Open the Scaffold screen", "Inspect the content padding", "Switch tabs"],
        ["Content is not obscured by the bars", "The tab selection changes"]),
    row("UI-BAR-002", "kira-ui", "AdaptiveTopBar", "title, leading, trailing, menu",
        "all", "TopBarDemo",
        ["Open the Top Bar screen", "Inspect the title and items", "Open the trailing menu"],
        ["The title is visible", "Bar items render natively on iOS",
         "The menu action fires"]),
    row("UI-BAR-003", "kira-ui", "AdaptiveNavigationBar", "items and selected index",
        "all", "NavigationBar",
        ["Open the Navigation Bar screen", "Select a different tab"],
        ["The selected tab changes", "No selection is possible with an invalid index"]),
    row("UI-BAR-004", "kira-ui", "AdaptiveToolbar", "collapsed and expanded",
        "all", "Toolbar",
        ["Open the Toolbar screen", "Switch expanded state", "Tap an item"],
        ["The Material toolbar expands", "iOS requires non-empty iosItems and shows a native toolbar"]),

    # Symbols and images
    row("UI-ICON-001", "kira-cupertino-icons", "CupertinoIcon catalog", "search and category",
        "all", "CupertinoIconsCatalog",
        ["Open the Cupertino Icons screen", "Search for 'chevron'", "Select a category",
         "Inspect a representative grid"],
        ["The grid filters to matching names", "The count updates",
         "Representative glyphs render without tofu"]),
    row("UI-ICON-002", "kira-ui", "SFSymbol and UIKitImage", "system name and vector",
        "ios", "TopBarDemo",
        ["Open the Top Bar screen on iOS", "Inspect the SF Symbol and vector bar items"],
        ["System-name and rasterized vector images render",
         "The icon font fallback is not presented as an SF Symbol",
         "The UIKitImage.Bitmap variant is not exercised by this screen"]),
    row("UI-ICON-003", "kira-cupertino-icons", "CupertinoIcon", "size and content description",
        "all", "CupertinoIconsCatalog",
        ["Open the Cupertino Icons screen", "Inspect 16/24/48dp samples"],
        ["Glyphs scale without clipping", "Decorative icons expose no duplicate label"]),

    # IO
    row("IO-CTX-001", "kira-core", "LocalPlatformContext", "host context smoke",
        "all", "FilePicker",
        ["Open the File Picker screen", "Read the context type readout"],
        ["Android reports Context", "Other targets report the opaque sentinel"]),
    row("IO-FILE-001", "kira-io", "KmpFile", "read, stream, name and path",
        "all", "FilePicker",
        ["Open the File Picker screen", "Pick a small text file", "Read bytes and stream",
         "Inspect name and path"],
        ["Bytes are non-empty", "Stream matches bytes", "Path is platform-shaped, not always a filesystem path"]),
    row("IO-PICK-001", "kira-file-picker", "rememberFilePickerLauncher", "single selection",
        "all", "FilePicker",
        ["Open the File Picker screen", "Tap single select", "Choose a seeded file"],
        ["Exactly one result is shown", "The file is readable"]),
    row("IO-PICK-002", "kira-file-picker", "rememberFilePickerLauncher", "multiple with limit",
        "all", "FilePicker",
        ["Open the File Picker screen", "Enable multiple", "Select more than the limit"],
        ["Results are truncated to maxItems", "Cancelling yields an empty list"]),
    row("IO-PICK-003", "kira-file-picker", "FilePickerFileType.Folder", "folder and cancel",
        "all", "FilePicker",
        ["Open the File Picker screen", "Pick a folder", "Cancel a file pick"],
        ["A folder result is shown where supported", "Web folder selection returns empty",
         "Cancel leaves the previous result unchanged"]),
    row("IO-SAVE-001", "kira-file-picker", "rememberFileSaverLauncher", "bytes save and reopen",
        "all", "ProfilePicture",
        ["Open the File Saver screen", "Save generated bytes", "Reopen the saved file"],
        ["Android/iOS/desktop return a readable KmpFile", "Cancel returns null",
         "Web triggers a download and does not invoke onResult"]),
    row("IO-COIL-001", "kira-file-picker-coil", "KmpFileFetcher and AsyncImage", "preview success",
        "all", "ImagePicker",
        ["Open the Image Picker screen", "Pick a seeded image"],
        ["The preview renders", "The fetcher streams rather than copying the whole file"]),
    row("IO-CAMERA-001", "kira-camera-picker", "rememberCameraPickerLauncher", "capture or fallback",
        "mobile", "CameraPickerScreen",
        ["Open the Camera Picker screen", "Grant camera permission", "Tap capture"],
        ["A captured image returns on a camera-capable device",
         "The iOS simulator falls back to the photo library",
         "Desktop/web do nothing and never call back"]),

    # Permissions
    row("PERM-SINGLE-001", "kira-permissions", "rememberPermissionState", "camera grant and deny",
        "mobile", "Permission",
        ["Reset app permissions", "Open Permissions", "Request Camera", "Grant or deny the OS prompt"],
        ["The row status reflects the OS result", "A deny updates the rationale state"]),
    row("PERM-BULK-001", "kira-permissions", "rememberMultiplePermissionsState", "camera and microphone",
        "mobile", "Permission",
        ["Open Permissions", "Tap Request permissions", "Answer the prompts"],
        ["allPermissionsGranted follows the results", "revokedPermissions lists denied entries"]),
    row("PERM-STATE-001", "kira-permissions", "PermissionState", "determined and settings return",
        "mobile", "Permission",
        ["Grant a permission", "Move the app to the background and return", "Open app settings"],
        ["Granted is retained", "The settings return refreshes status"]),
    row("PERM-NOTIF-001", "kira-permissions", "Notification and RemoteNotification",
        "local and remote notification",
        "mobile", "Permission",
        ["Open Permissions", "Request Notification", "Inspect RemoteNotification"],
        ["Android below API 33 reports no represented runtime permission",
         "RemoteNotification has no Android mapping and reports Granted"]),
    row("PERM-LOC-001", "kira-permissions", "BackgroundLocation and location leaves",
        "foreground and background location",
        "mobile", "Permission",
        ["Open Permissions", "Request FineLocation", "Request BackgroundLocation"],
        ["Foreground and background requests are separate", "iOS Always requires a prior WhenInUse grant"]),
    row("PERM-PIM-001", "kira-permissions", "contacts and calendar leaves",
        "read and write",
        "mobile", "Permission",
        ["Open Permissions", "Request contacts", "Request calendar"],
        ["Read/write rows update independently", "The iOS calendar helper is events-only"]),
    row("PERM-BT-001", "kira-permissions", "Bluetooth and Wi-Fi leaves", "scan/connect and nearby",
        "mobile", "Permission",
        ["Open Permissions", "Request Bluetooth", "Request Wi-Fi nearby devices"],
        ["Each leaf reports its own status", "The iOS Wi-Fi probe is a local-network probe, not a Wi-Fi permission"]),
    row("PERM-CORE-001", "kira-permissions", "storage, call and SMS leaves", "legacy routes",
        "mobile", "Permission",
        ["Open Permissions", "Inspect storage/call/SMS rows"],
        ["SDK-window gaps are labelled not-represented", "iOS SMS read/receive are NotGranted"]),
    row("PERM-STUB-001", "kira-permissions", "desktop and web permission stubs", "unavailable",
        "none", "Permission",
        ["Run the showcase on desktop or web", "Request any permission"],
        ["Status stays Denied(false)", "No callback fires", "The UI labels the platform as unavailable"]),

    # Share and WebView
    row("SHARE-001", "kira-share", "ShareContent.Text", "native share sheet",
        "mobile", "Share",
        ["Open Share", "Tap Share Text", "Dismiss the share sheet"],
        ["The native share sheet opens", "iOS reports Dismissed on cancel",
         "Android reports Success when the chooser opens, not delivery"]),
    row("SHARE-002", "kira-share", "ShareContent.Url", "native share sheet",
        "mobile", "Share",
        ["Open Share", "Tap Share URL", "Dismiss the sheet"],
        ["The URL is accepted by the share sheet", "The result readout updates"]),
    row("SHARE-003", "kira-share", "ShareContent.File and Files", "single and mixed files",
        "mobile", "Share",
        ["Open Share", "Pick one file", "Share File", "Pick multiple files and share"],
        ["The file payload reaches the share sheet", "No real external recipient is used"]),
    row("WEB-001", "kira-webview", "WebViewState", "deterministic HTML load",
        "all", "WebView",
        ["Open Web View", "Tap Load HTML", "Read title and loading state"],
        ["The known title appears", "Loading reaches Finished",
         "isLoading is initially true on every platform"]),
    row("WEB-002", "kira-webview", "WebViewNavigator", "URL load, back and forward",
        "all", "WebView",
        ["Open Web View", "Load the owned second page", "Go back", "Go forward"],
        ["canGoBack/canGoForward follow the history",
         "Desktop/web HTML base-URL and header parameters are ignored"]),
    row("WEB-003", "kira-webview", "WebViewState.errorsForCurrentRequest", "bad destination",
        "all", "WebView",
        ["Open Web View", "Load an invalid destination", "Read the error list"],
        ["Android/iOS append native errors", "Desktop/web add a synthetic error"]),
    row("WEB-004", "kira-webview", "WebViewState.evaluateJavascript and settings", "JavaScript on",
        "all", "WebView",
        ["Open Web View", "Enable JavaScript", "Evaluate document.title"],
        ["The callback returns the known title", "JavaScript is off by default"]),
    row("WEB-005", "kira-webview", "CookieManager", "set, get, remove",
        "all", "WebView",
        ["Open Web View", "Set a synthetic cookie", "Read it back", "Remove all cookies"],
        ["The cookie round-trips", "Desktop generic handlers refuse removeAllCookies",
         "Web only sees host-page cookies"]),

    # Navigation and geo
    row("NAV-001", "kira-navigation", "AdaptiveNavHost", "push, back, restore",
        "all", "Home",
        ["Open a component screen", "Tap Back", "Open it again"],
        ["The route stack returns to Home", "Per-destination saveable state is dropped after pop"]),
    row("NAV-002", "kira-navigation", "NavArgument", "declared arguments",
        "none", "Home",
        ["Attempt to pass a value argument through navigate()"],
        ["Arguments are declarations only; no value is delivered",
         "Nested graphs and deep links are absent"],
        screenshot={"android": "screenshots/android/nav/unsupported-arguments/api35-phone.png",
                    "ios": "screenshots/ios/nav/unsupported-arguments/iphone-simulator.png"},
        limitations=["AdaptiveNavHostController.navigate(route, arguments) ignores arguments."]),
    row("GEO-001", "kira-geo", "LatLng", "distance and bearing maths",
        "all", "Geo",
        ["Open the geo maths section", "Read the distance and angle for fixed coordinates"],
        ["0,0 to 0,1 is about 111.19 km", "Cardinal bearings round to 0/90/180/270"]),
    row("GEO-002", "kira-geo", "LocationTracker", "start, stop, updates",
        "none", "Home",
        ["Start the tracker", "Wait for an update", "Stop the tracker"],
        ["The public states are never populated on any platform",
         "Android additionally needs an Android-only bind call"],
        screenshot={"android": "screenshots/android/geo/unsupported-tracker/api35-phone.png",
                    "ios": "screenshots/ios/geo/unsupported-tracker/iphone-simulator.png"},
        limitations=["iOS/desktop/web are no-op stubs; Android LocationTracker does not update its public States."]),

    # Excluded modules
    row("EXCL-MAPS-001", "kira-maps", "maps", "excluded build-only module",
        "none", "Home",
        ["Inspect the module"],
        ["Only a build file exists; no app screen is advertised"]),
    row("EXCL-MEDIA-001", "kira-media", "media", "excluded module",
        "none", "Home",
        ["Inspect the module"],
        ["Not included in settings.gradle.kts; no app screen is advertised"]),
    row("EXCL-NOTIF-001", "kira-notifications", "notification scheduler", "excluded module",
        "none", "Home",
        ["Inspect the module"],
        ["Not included in settings.gradle.kts; the notification PERMISSION remains in scope"]),
]


def render(document: dict) -> None:
    lines = [
        "# Showcase coverage",
        "",
        f"Base: `{document['base']['sha']}` on `{document['base']['branch']}`.",
        "",
        "The authoritative machine-readable manifest is [coverage.json](coverage.json).",
        "Regenerate both files with `python3 showcase/generate_coverage.py`.",
        "",
        "| ID | Component | Variant | Android | iOS | Route | Android run | iOS run |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in document["rows"]:
        a = item["execution"]["android"]
        i = item["execution"]["ios"]
        lines.append(
            "| {id} | {component} | {variant} | {a} | {i} | {route} | {ar} | {ir} |".format(
                id=item["id"], component=item["component"], variant=item["variant"],
                a=item["support"]["android"], i=item["support"]["ios"], route=item["route"],
                ar=a["status"] + (f" ({a['run']})" if a.get("run") else ""),
                ir=i["status"] + (f" ({i['run']})" if i.get("run") else ""),
            )
        )
    (ROOT / "showcase" / "COVERAGE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    for item in ROWS:
        if all(value == "unsupported" for value in item["support"].values()):
            item["route"] = "Limitations"
            item["screenshot"] = {
                "android": "screenshots/android/limitations/known-limitations/api35-phone.png",
                "ios": "screenshots/ios/limitations/known-limitations/iphone-simulator.png",
            }
    document = {
        "schemaVersion": 1,
        "generatedBy": "showcase/generate_coverage.py",
        "base": {"repository": "NativeCmpKit/NativeCmpKit", "sha": BASE_SHA, "branch": BRANCH},
        "app": {
            "androidApplicationId": ANDROID_APP,
            "iosBundleId": IOS_BUNDLE,
            "entryPoint": "sample/common/src/commonMain/kotlin/io.github.apdelrahman1911.kira.sample/App.kt",
        },
        "platformRuntimes": {
            "android": "GitHub-hosted ubuntu-24.04, KVM API 35 x86_64 Google APIs emulator",
            "ios": "GitHub-hosted macos-26, explicitly selected iPhone simulator UDID",
            "desktop": "not part of the mobile capture matrix",
            "web": "not part of the mobile capture matrix",
        },
        "rows": ROWS,
    }
    out = ROOT / "showcase" / "coverage.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")

    render(document)
    print(f"wrote {len(ROWS)} rows")


if __name__ == "__main__":
    main()
