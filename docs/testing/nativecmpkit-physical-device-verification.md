# NativeCmpKit physical-device verification

Run this checklist on an authorized test Mac with physical Android, iPhone and
iPad devices. Hosted emulator and simulator jobs can proceed independently.
Record hardware results against the exact integration candidate before
authorizing packages, releases, Pages or deployments.

## Prepare the candidate

1. Create a clean checkout of the candidate commit. Record `git rev-parse HEAD`,
   the Gradle/JDK and Xcode versions, device model, OS build and form factor. Use
   the repository's JDK 17 and pinned tools. Prepare a synthetic photo, a small
   text file with known bytes, and a lab-controlled HTTPS site with a redirect,
   distinct page titles, a slow response, and cookies with distinct paths.
2. Use the repository's debug sample for the flows it exposes. For a row that
   needs an explicit anchor, a controlled URL, a minimum-OS build or callback
   counts the sample cannot display, use a local development-signed test host
   running the same library revision. Record the host source hash, package
   variant and the screen or test entry used for that row.

## Android

Connect the authorized phone over USB, enable USB debugging, and accept the
test Mac's debug prompt. Confirm the selected serial belongs to the physical
phone using `adb devices -l` and set `android_serial` to that serial in the
local shell. Keep it out of shared evidence.
[Android hardware setup](https://developer.android.com/studio/run/device/)

```sh
./gradlew :sample:android:assembleDebug --max-workers=2 --no-configuration-cache
set -- sample/android/build/outputs/apk/debug/*.apk
test "$#" -eq 1 && test -f "$1" || exit 1
adb -s "$android_serial" install -r "$1"
adb -s "$android_serial" shell am start -W \
  -n io.github.apdelrahman1911.nativecmpkit.sample/.MainActivity
```

Use a current supported Android device for the full matrix. The sample requires
API 24. For a library API 23 acceptance row, install a debug test host whose
merged manifest permits API 23 and whose dependencies include only the libraries
being checked. Record its merged manifest and use an actual API 23 phone.

| Flow | Steps and required observation |
| --- | --- |
| Camera and recreation | In **Camera Picker**, select **Open Camera**. Deny permission, grant through Settings, open the real camera, cancel, then capture a synthetic subject. Repeat with Android's **Don't keep activities** enabled. Check cancellation or unavailable feedback, a readable capture on success, one terminal callback per launch and recovery on the next launch. Restore the setting. |
| Permissions | In **Permissions**, request a supported permission from a clean state. Exercise denial, grant and revocation in Settings. Return to the app after each change and compare public status with the OS setting. Record the permission and which prompt the OS actually presented. |
| Picker, saver and share | In **File Picker**, pick the known file and then cancel a new request. Select a folder and test reopen after backgrounding or process restart using the documented persistence API. In **File Saver**, export the synthetic image, reopen it from the chosen provider and compare bytes with the expected export. In **Content Sharing**, share a selected file to a lab-controlled receiving app and confirm read access. Exercise cancellation separately. |
| WebView | Record the installed WebView provider and version with `adb shell dumpsys webviewupdate` on the selected device. In the WebView host open the controlled redirect, navigate back and forward, and restore the screen. Check final URL, title, visible page content and cookie scope. Stop the slow request and verify recovery with a fresh navigation. Record separately whether the test checked visible loading state or observed transport closure at the server. |

## iPhone and iPad

Pair each device with the test Mac in Xcode, enable Developer Mode, and select
an authorized development signing team. Open
`sample/ios/NativeCmpKit.xcodeproj`, choose the `NativeCmpKit` scheme and the
physical device as the destination, then choose **Product → Run** in Debug.
The project builds and embeds the device framework through
`:sample:common:embedAndSignAppleFrameworkForXcode`. Record the signed app
bundle identifier and the successful physical launch. Keep any local signing
changes and provisioning material outside the tracked source.
[Apple device setup and signing](https://developer.apple.com/documentation/Xcode/running-your-app-on-simulated-or-physical-devices)

| Flow | Steps and required observation |
| --- | --- |
| iPhone compact action sheet | Open **Show ActionSheet** in the alert sample in portrait. Confirm the native Cancel control is visible. Tap it once and require one Cancel callback, zero Confirm and outside-dismiss callbacks, and full dismissal. Reopen and verify the primary action and its corresponding callback independently. Use the dedicated callback-count host for exact counts. |
| iPad anchor, rotation and split view | Start full-screen in portrait. Exercise the default anchor, `AlertDialogIosPopoverAnchor.ViewRect` on an attached view, and `AlertDialogIosPopoverAnchor.BarButton` on the active navigation bar. Keep the sheet open through portrait → landscape → portrait. Repeat on an iPad in a second actual window width using Split View or its OS-supported split/windowing mode. Check the visible anchor follows its source, the same sheet remains owned where the platform supports it, and each dismiss/action produces one outcome. Repeat with an omitted or detached source and check the documented fallback. Record both orientation and width. |
| Camera, Photos and disclosure | In **Camera Picker**, deny access and verify the unavailable/error outcome. Grant the requested access, cancel one launch, capture a synthetic subject in portrait and landscape, and reopen the returned file. Exercise the named library picker or scoped photo access separately. Check results are readable, each launch completes once, and navigating away releases the owned UI. |
| Date-range picker | Exercise native month navigation, changed rules and bounds, disabled days, and disposal during a pending update on the supported iOS versions. Retain matched Instruments and callback evidence. Follow the [range-picker scenarios](ios-range-highlighting.md). |
| Files, sharing and WKWebView | Pick, reopen and export synthetic content through the real system provider. Share the exported file, cancel, and repeat after dismissing the first share sheet. In the WKWebView host, load the controlled HTTPS site, follow its redirect, check title/history/cookie scope, remount or restore, then stop a slow navigation and confirm recovery. Record the actual host, provider and network assertions. |

## Retain the result

For each row record the exact revision, host/app identity, device model, OS
build, actual commands or UI steps, total attempts, passes, failures, skips and
the failing assertion or observation. Retain sanitized screenshots, test
reports and logs as appropriate. Exclude device identifiers, account details,
personal captures and signing material. Rerun affected rows after a fix and
keep earlier failures associated with their original revisions. Clean up the
test app and data on the authorized devices. A missing device, OS or scenario
remains open in the release checklist.
