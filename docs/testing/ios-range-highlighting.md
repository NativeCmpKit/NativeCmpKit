# iOS range highlighting verification

The native range picker keeps the complete selection and highlights only eligible
days in the visible month and its neighbours. The visible window contains at
most 93 days, regardless of the selected range. The backend coalesces queued
refreshes and reads the current selection, viewport, bounds and rule after the
UIKit callback returns. Compose disposal and UIKit view release clear the
delegates and invalidate a pending refresh.

On iOS 16.2 and later the calendar observes the public visible-month callback.
The NativeCmpKit host also observes `layoutSubviews`, which preserves native
calendar presentation on iOS 16.0 and 16.1. The Material renderer serves older
iOS versions. Exercise actual month changes on 16.0 and 16.1 to verify that
layout observation delivers the required transitions on those versions.
[Apple callback availability](https://developer.apple.com/documentation/uikit/uicalendarviewdelegate/calendarview(_:didchangevisibledatecomponentsfrom:))

## Hosted receipt

`identity-apple-ui-date-range` ran at `fce9b13442d2a1bc336389008d6f820e8afbedac`
on an iPhone Air simulator. The owned `:nativecmpkit-ui:iosSimulatorArm64ApplicationTest`
task executed the six `NativeRangeHighlightTest` and three `SystemVersionTest`
methods named in the receipt. Gradle and the owned application both exited 0.
The application reported worker termination and its counts matched the fresh
JUnit reports. Nine tests passed with zero failures, errors or skips.
[Hosted job](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46158788951/job/141021223914) · [Exact command and reports](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46158788951/artifacts/15269314645)

The controlled cases verify the 89-day February through April 2026 window,
rule and bound changes, restoration after native deselection, complete endpoint
delivery, coalescing, and disposal of queued work. The original range-start
assertion failure is preserved under the historical revision. The remaining
checks require real presentation, scroll and performance measurements.
[Original hosted failure](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/42487150063/artifacts/13620796472) · [Issue #122](https://github.com/NativeCmpKit/NativeCmpKit/issues/122)

## Physical iPhone scenarios

Run the range picker on the oldest supported physical iPhone available and a
current iPhone. Include iOS 16.0 or 16.1 and iOS 16.2 or later. Record the exact
revision, picker host, device, OS, locale, calendar, time zone and year bounds.
Use an Instruments allocation and CPU trace for the matched original and
candidate builds. Retain the sample count, warm-up, median and tail time,
maximum and retained allocations, and frame interruptions.

| Exercise | Required observation |
| --- | --- |
| One day, one year and the full default range | Visible native work stays bounded. Record rule calls, created date components, native selection size and Instruments counters. |
| Move an endpoint inside and outside the visible window | The owner keeps the exact endpoints and the new visible window receives the correct highlights. Record allocations and refresh times. |
| Scroll through leap February and year boundaries in both directions | Eligible days stay highlighted and disabled gaps stay clear. Repeated scrolling does not accumulate selection resources. |
| Fling, jump months or years, then revisit a cached month | Highlights settle on the current window, including jumps past both neighbouring months. |
| Replace the rule with an interior gap, an all-denied rule and the original rule | Highlights and interactivity update without a tap or scroll. Record allocation and refresh times. |
| Change inclusive bounds inside and beyond the viewport | The full selection endpoints are retained, out-of-bounds days cannot be selected, and the viewport refreshes. |
| Tap the start, the same day, an earlier day, a later day and an interior day | The range state follows its tap policy and each native tap invokes the owner once. |
| Change selection during native selection or layout callbacks | No recursive writes, unexpected owner callback or repeated unchanged render. Record callback order. |
| Dispose or replace the state with a refresh queued | The old view receives no new write or owner callback and both delegates are released. |
| Retain a covered host, navigate away and back, then background and foreground | The inactive view does no continuing work and the current highlights appear when the picker returns. |
| Navigate by VoiceOver, the native header and programmatic month change | Each applicable route updates the displayed month and current highlights. |
| While scrolling, rapidly replace the rule, endpoints and bounds | The final values determine the highlights and no old owner is retained. |

Use the shared device procedure to retain the results. The hosted cases above
do not cover the affected older OS versions or the Instruments criteria.
[Physical-device procedure](nativecmpkit-physical-device-verification.md)
