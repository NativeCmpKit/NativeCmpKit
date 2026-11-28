# `ui-test-actions` — limitations, root causes and improvement backlog

Independent consumer report from the NativeCmpKit Showcase project.

- **Library**: `ui-test-actions/ui-test-actions`
- **Revision tested**: `0c818c5d72e8c30c59bd1287c330a40392bf8e89`
  (single pinned revision used by every session below)
- **Targets exercised**: Android emulator (API 35, x86_64, Pixel 6 AVD) and iOS
  Simulator (iPhone 17 Pro, iPad Pro 13-inch (M4), iOS 26.5), via
  Cloudflare Quick Tunnel, driven by the Python client (`ui_sdk.LiveUI`,
  `agent.py`) and by direct HTTP actions.
- **Author role**: consumer, not maintainer. Source references below are to the
  pinned checkout; line numbers are from that revision.

Evidence runs (all NativeCmpKit/NativeCmpKit):

| Run | Platform | Device | Purpose |
| --- | --- | --- | --- |
| [46099102700](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46099102700) | Android | Pixel 6, API 35, 1080×2400 | full functional suite + retests |
| [46114711444](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46114711444) | Android | Pixel 6, API 35, 1080×2400 | tour recapture |
| [46107087160](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46107087160) | Android | 1600×2560 @ 320 dpi | tablet tour + functional |
| [46014167086](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46014167086) | iOS | iPhone 17 Pro, iOS 26.5 | functional + partial tour |
| [46108448068](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46108448068) | iOS | iPhone 17 Pro, iOS 26.5 | six-flow retest |
| [46114716852](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46114716852) | iOS | iPhone 17 Pro, iOS 26.5 | tour including Time Picker |
| [46099392157](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46099392157) | iOS | iPad Pro 13-inch (M4), iOS 26.5 | tablet tour + functional |

Everything below was observed on those runs unless explicitly marked
**inferred** or **not confirmed**.

---

## 0. Executive summary

`ui-test-actions` is a capable "one app, tap and read text" harness. It was
sufficient to assert 25 Android rows and 19 iOS rows end-to-end, including
permission dialogs, menus, sheets, web content, rotation on Android and native
UIKit bars. It is **not yet sufficient for exhaustive component-library
verification** because four gaps dominate:

1. **Semantics fidelity is low.** The iOS tree maps only
   role/name/text/editable/password (`ios_axe.py:36-70`), and the Android page
   source parser maps only role/name/text/visible/enabled
   (`webdriver_driver.py:60-99`). `checked`, `checkable`, `selected`,
   `scrollable`, `focused` are accepted by the selector contract
   (`contract.py:43-47`) but never populated on either platform. Switch, chip,
   tab and slider state therefore cannot be selected reliably; the driver has to
   click by coordinates and then re-read text.
2. **No iOS rotation.** `AxeSimulator.capabilities()` (`ios_axe.py:82`) exposes
   no `device.rotate`/`device.orientation`; the iOS tour capability dump
   confirms it. Android rotation works.
3. **Interaction primitives are thin.** No scroll-into-view, no element-scoped
   scroll, no reliable multi-tap on iOS (`--count` led to
   `action_outcome_unknown`), no press-drag composition, and gestures on the
   iOS AXe path are `tap`/`draw` only.
4. **Session/tunnel failure semantics are coarse.** `HTTP 400 invalid_arguments`
   is returned immediately after `app.restart` even for a valid selector; a lost
   response is reported as `action_outcome_unknown` with no way to query the
   outcome; the 38 s request timeout and fixed session deadline surface as
   `HTTP 408`/`HTTP 530` with no reconnection.

None of these is a reason to abandon the harness. They are concrete,
locally-fixable driver gaps.

---

## 1. How the harness is built (what the limits follow from)

Relevant pinned source:

| Concern | File / function |
| --- | --- |
| Command schemas and selector fields | `contract.py:43-116` |
| Selector matching | `automation.py:194-205` |
| Element actionability and bounds clipping | `automation.py:236-252` |
| Condition waits and `408` | `automation.py:254-267` |
| HTTP client, 38 s timeout, retries | `agent.py:63-118` |
| Unknown-outcome error | `agent.py:168-176` |
| Android driver (Appium/UIAutomator2) | `webdriver_driver.py:60-260` |
| iOS driver (AXe) | `ios_axe.py:36-185` |
| Device/session capabilities | `mobile_driver.py:289-313`, `ios_axe.py:82` |
| Session lifetime | `session.py:516,585`, `lifecycle.py:57-90` |

Two different worlds sit behind one contract:

- **Android** uses an Appium/UIAutomator2 endpoint. The tree is page-source XML;
  touch is a W3C pointer sequence with an explicit click/drag implementation
  (`webdriver_driver.py:225-260`).
- **iOS** uses the AXe binary for observation (`axe describe-ui`) and input
  (`axe tap`, `axe draw`, `axe key`). Text insertion is clipboard + ⌘A/⌘V
  (`ios_axe.py:143-160`).

This asymmetry explains most platform-specific findings below.

---

## 2. Limitation catalogue

Each entry follows the requested ten-point structure. "Confirmed" means directly
observed or read from the pinned source; "inferred" is labelled.

---

### L1 — Native system dialogs are outside the tested surface

**1. Goal.** Drive file picker, photo picker, share sheet and camera UI to a
deterministic selection so IO rows can be functionally verified.

**2. What exists today.** Touch, text and selectors are scoped to the launched
application. Android observes an Appium session for the app under test; iOS asks
AXe for the app's accessibility tree (`ios_axe.py:88-100`). Permission prompts
*were* reachable on both platforms (bulk deny passed on Android and iOS), so the
harness can act on at least some system-owned alerts.

**3. What failed / was missing.** The project never obtained a deterministic
selection path for:
`DocumentsUI` (Android file picker), `PHPickerViewController`/`UIImagePickerController`
(iOS photo picker), `UIActivityViewController` (share), or the emulator camera.
The flows were reported **blocked**, not failed:
`file-picker`, `file-saver`, `share`, `camera`, `permission-camera`.
No command exists to enumerate windows/alert owners or to target a system
package/bundle.

**4. Technical reason.** **Inferred, not confirmed.** System pickers are separate
processes/windows. The Android Appium session is created for the app package, and
AXe describes the app's accessibility hierarchy. Without a documented way to
switch context or target another bundle, a selector cannot name a file row.
Permission alerts work because they are presented in-process or surfaced through
the app's alert window.

**5. Layer.** `ui-test-actions` (missing window/context targeting) plus test
design (no deterministic fixture selection implemented).

**6. Workaround.** Seed fixtures into `Download`/photo library (done), then use
coordinates and blind back-navigation. Rejected as evidence because it is not
deterministic and cannot prove the filter reached the picker.

**7. Permanent fix.** Add `ui.windows` (list owners/titles/bounds),
`ui.target` (switch observation/input to a package/bundle or SpringBoard), and
`alert.accept/deny` helpers. On Android, allow Appium sessions with
`autoGrantPermissions=false` and no `appPackage` restriction, or a second
UIAutomator2 session for `com.google.android.documentsui`. On iOS, add an AXe
`--app`/SpringBoard mode or an XCUITest springboard session.

**8. Verification.** A fixture-based flow must: open the picker, assert a row
with the seeded file name, select it, and assert the app readout. Run on API 35
and iOS 26.5, 20 repetitions, zero coordinate fallbacks.

**9. Evidence.** Blocked entries in
`showcase/evidence/functional-spec.md`; no screenshots because the dialogs were
never entered.

**10. Version.** `0c818c5d72e8c30c59bd1287c330a40392bf8e89`.

---

### L2 — iOS rotation is not exposed (confirmed)

**1. Goal.** Verify `NAV-003` state restoration by rotating landscape → portrait
and asserting the same screen/state remains.

**2. What exists today.** The contract defines `device.rotate` and
`device.orientation` (`contract.py:113-115`). Android advertises
`device.orientation` (`mobile_driver.py:290-295`) and it worked: `nav-restore`
passed on Android phone and tablet. iOS with the AXe bridge advertises neither;
the capability dump in `screenshots/ios/tour.json` lists no rotation command.

**3. What failed.** `NAV-003` on iOS is `not-run`; the flow is explicitly
Android-only. Attempting rotation would be rejected by capability negotiation.

**4. Technical reason.** **Confirmed at the capability level:**
`AxeSimulator.capabilities()` returns
`mobile.capabilities() | {tree.snapshot, pointer.click, pointer.drag,
pointer.scroll, keyboard.press, text.insert}` (`ios_axe.py:82-86`).
`device.rotate` is only added by `mobile_driver.capabilities()` when
`target == "ios" and self.legacy is not None` (`mobile_driver.py:300-302`);
the AXe path constructs without legacy, so it disappears. Whether AXe itself can
rotate is not documented here.

**5. Layer.** `ui-test-actions`.

**6. Workaround.** None in-harness. We did not shell into the runner from the
client; the connection artifact exposes HTTP only.

**7. Permanent fix.** Implement rotation with `xcrun simctl` / Simulator UI
automation (e.g. `simctl ui` appearance APIs or AppleScript menu rotation) and
advertise `device.rotate`/`device.orientation` on the AXe path with wait-for-
settled semantics.

**8. Verification.** Rotate twice, assert the same screen text and a changed
viewport orientation, repeat 10× on iPhone and iPad.

**9. Evidence.** `screenshots/ios/tour.json` capability list;
`showcase/coverage.json` `NAV-003` iOS `not-run`.

**10. Version.** same revision.

---

### L3 — Accessibility semantics are incomplete (confirmed; largest gap)

**1. Goal.** Select and assert switches, sliders, chips, tabs and progress by
semantic state rather than by position.

**2. What exists today.** Selector supports `role`, `name`, `text`,
`text_contains`, `resource_id`, `enabled`, `visible` and
`properties.{focused,selected,checked,editable,checkable,clickable,scrollable,password}`
(`contract.py:43-47`). Matching reads those properties (`automation.py:194-205`).

**3. What failed.**
- iOS switches appear as `AXCheckBox` with names `On`/`Off` and **no**
  `checkable`/`checked` properties. Selector by `properties.checked` never
  matched; the driver had to match role `AXCheckBox` and click coordinates.
- iOS sliders appear as an unnamed `AXGroup` with no role, label or value.
  The element could not be selected; we fell back to dragging the geometric
  track found by a snapshot scan (`functional.py:drag_slider`).
- iOS Material chips/date-range chips expose no `selected` flag; the flow had to
  read a text readout instead.
- Android page source also carries no `checkable`/`checked`/`selected` mapping
  (`webdriver_driver.py:60-99`).

**4. Technical reason.** **Confirmed in source.** The iOS mapper
(`ios_axe.py:36-70`) emits only
`properties={password, editable}`. The Android mapper emits no `properties` key
at all. The contract therefore promises more than the drivers deliver.

**5. Layer.** `ui-test-actions` mapping, plus upstream accessibility:
`CupertinoSlider` does expose Compose `setProgress` semantics
(`CupertinoSlider.kt:668-700`), so the library is not entirely at fault, but
Compose→UIKit accessibility bridging is partial.

**6. Workaround.** Role/`AXCheckBox` matching, snapshot scans for `View` nodes
with `checkable`, coordinate drags on a sibling track. All position-dependent;
none survives layout changes (phone vs tablet).

**7. Permanent fix.** Populate the full semantics set from AXe traits/attributes
and UIAutomator attributes: `checked`, `checkable`, `selected`, `scrollable`,
`focused`, `value` (numeric/text), `adjustable`. Normalise roles
(`AXCheckBox→switch`, `AXSlider/Adjustable→slider`, `AXButton→button`).
Add `name_contains`/`value_contains` selectors. Add an `element.adjust`
command (`direction`, `value`) that uses `setProgress`/`adjust_to_value`.

**8. Verification.** On the Showcase Screen: select Wi-Fi switch by
`properties={checked:false}`; toggle and assert `checked:true`; adjust slider by
`element.adjust value=0.8`; assert `value` ≥ 0.75. Same on Android and iOS,
phone and tablet.

**9. Evidence.** `screenshots/functional/...` for iOS slider/sheet-veto failures;
source lines above; `screenshots/ios/tour.json` capability/tree snapshots.

**10. Version.** same revision.

---

### L4 — Off-screen content cannot be scrolled into view or asserted

**1. Goal.** Reach controls below the fold, e.g. “Allow swipe to hide” inside a
bottom sheet, the display-mode switch on a long date screen.

**2. What exists today.** `pointer.scroll` scrolls at a coordinate
(`contract.py:70`, `automation.py:168-170`); there is no element-scoped scroll
and no scroll-into-view.

**3. What failed.**
- `sheet-veto` on iPhone and iPad: `no node for 'Allow swipe to hide'`.
- `date-display` on phone widths: the switch toggles the picker, the layout
  collapses, the readout leaves the viewport, and `missing visible text
  'Inline display: Input'` follows. At 1600×2560 the same flow passes.
- `element.assert state=absent` refuses to conclude on a truncated tree
  (`observation_incomplete`, 422) — correct, but there is no way to grow the
  observed region.

**4. Technical reason.** **Confirmed for iOS:** the tree marks nodes
`visible=false` when their frame has no intersection with the viewport
(`ios_axe.py:52-64`), and Compose prunes offscreen semantics. Android page
source only lists attached views. Scrolling at a fixed screen centre may land on
an inner scrollable (calendar) instead of the outer container — observed on the
date screen.

**5. Layer.** `ui-test-actions` (missing element-scoped scroll) plus Compose
lazy/offscreen semantics.

**6. Workaround.** Scroll in fixed increments and re-snapshot; choose a scroll
point that is not inside an inner scroller. Unreliable; failed on the sheet.

**7. Permanent fix.** Add `element.scroll_into_view(id|selector)` and
`element.scroll(id, direction, distance)` implemented as a drag inside the
element's bounds (Android) or AXe draw inside the element frame (iOS). Retry
until the node's frame intersects the viewport. Also expose the full tree with
`visible:false` instead of pruning where the platform allows.

**8. Verification.** Sheet switch and date display switch become selectable and
assertable at 402×874; flow passes on 10/10 runs without coordinate guesses.

**9. Evidence.** `screenshots/ios/functional/sheet-veto/...-failed-after.png`;
`date-display` screenshots on phone vs tablet; error strings above.

**10. Version.** same revision.

---

### L5 — Search results are not observable on iOS after typing (confirmed observation, cause unconfirmed)

**1. Goal.** Navigate the 25-entry Home index by typing into “Search components”.

**2. What exists today.** `text.insert` uses clipboard paste
(`ios_axe.py:143-149`); the tree is re-read with `tree.snapshot`.

**3. What failed.** On iPhone and iPad, after tapping the field and inserting
`Adaptive Clickable`, the AX tree still contained only the `AXTextArea` search
field — no result rows. On Android the same approach works. The tour therefore
uses scroll navigation on iOS (`open_screen(..., use_search=False)`).

**4. Technical reason.** **Not confirmed.** Hypotheses: Compose iOS marks the
results as a sibling accessibility container hidden while the keyboard/search
focus is active; or AXe's `describe-ui` follows the focused element. We have not
inspected the native accessibility hierarchy outside AXe.

**5. Layer.** Could be AXe/`ui-test-actions`, Compose iOS accessibility, or the
Showcase search semantics. Undetermined.

**6. Workaround.** Scroll the index (works, but slower and flaky near list ends).

**7. Permanent fix.** Add `--all-windows`/`--include-hidden` observation and a
`keyboard.dismiss` command; investigate the focused-element traversal in AXe.
Also expose `AXUIElementCopyAttributeValue` children of the window rather than
the focused subtree.

**8. Verification.** iOS flow types a filter and asserts a result row by text in
one snapshot; 10/10 runs.

**9. Evidence.** Probe transcript in the session log (search field only),
`tour.py` iOS branch, Home screenshots.

**10. Version.** same revision.

---

### L6 — Attribute split between `name` and `text` is platform-specific

**1. Goal.** Find a control by its visible label.

**2. What exists today.** Selector has separate `name` and `text`;
`text_contains` searches both (`automation.py:196-198`).

**3. What failed.** Compose iOS exposes some labels as `AXValue` (→ `text`) and
others as `AXLabel` (→ `name`). Exact `text` selectors missed “Tap me” and
“LiquidGlassButton”; Android exposed the same strings as `text`. This forced a
`find_any(text|name)` helper.

**4. Technical reason.** **Confirmed mapping:** `ios_axe.py:54-56` sets
`name=AXLabel/title`, `text=AXValue`; Android sets
`text=value/text`, `name=label/content-desc/name`
(`webdriver_driver.py:69-78`).

**5. Layer.** `ui-test-actions` normalisation.

**6. Workaround.** Try `text` then `name`; mostly works.

**7. Permanent fix.** Add `label_contains` that searches both, or a unified
`label` field; keep `text`/`name` for power users. Document the mapping.

**8. Verification.** One selector finds the same Compose control on both
platforms.

**9. Evidence.** `functional.py` `find_any`; failures “no node for 'Tap me'” and
“missing 'LiquidGlassButton'”.

**10. Version.** same revision.

---

### L7 — No element-scoped text/state assertions; only tree selectors

**1. Goal.** Assert that a specific row (switch, slider) switched, not just that
some text exists.

**2. What exists today.** `element.assert`/`element.wait` with selectors and
`properties`.

**3. What failed.** Because properties are missing (L3), assertions degrade to
“text X is visible”, which can match a header or another row. `text_value` in
the driver scrapes a node and parses strings.

**4. Technical reason.** Same as L3; plus no `value` field in either tree.

**5. Layer.** `ui-test-actions`.

**6. Workaround.** Read the readout text; add sample readouts (`Wi-Fi: on`,
`Range: From today`).

**7. Permanent fix.** Include `value` (AXValue, Android `text`/`value`
separately) and expose `element.assert` on a node id plus expected value.

**8. Verification.** Assert slider value 0.8 directly, not its label text.

**9. Evidence.** `functional.py` `text_value`, `assert_text`.

**10. Version.** same revision.

---

### L8 — `app.restart` is not synchronized with app readiness (confirmed symptom)

**1. Goal.** Restart the app between flows for isolation.

**2. What exists today.** `app.restart` is a command; the next action is
independent.

**3. What failed.** Immediately after `app.restart`, the first `element.wait`
intermittently returned `HTTP 400 (invalid_arguments)` — with a valid selector
(`text_contains`), on both platforms. Retrying 1.5 s later succeeds; a
`wait_home` loop was needed. This happened on iOS several times and on Android
after long suites.

**4. Technical reason.** **Not confirmed.** The 400 is the generic validation
error (`contract.py:127-153`), yet the payload is valid. Possible causes: the
action is routed before the driver session is attached, or the driver returns an
unstructured error that is mapped to `invalid_arguments`. Needs server-side
tracing; the client cannot see the rejected field.

**5. Layer.** `ui-test-actions` (error mapping/readiness), possibly the platform
driver during launch.

**6. Workaround.** `wait_home()` polling loop with retries; 1.5 s backoff.

**7. Permanent fix.** Make `app.restart` wait for “first stable tree + app
process foreground” and return only then; add `app.wait_ready(timeout_ms)`.
Never map driver-session-missing to `invalid_arguments` — use
`not_ready`/`session_starting` with a retry hint.

**8. Verification.** 100 consecutive `restart → element.wait` cycles with zero
400s and p99 under 2 s after return.

**9. Evidence.** Session logs and `tour.py` retry code; `wait_home` helper;
`showcase/evidence/functional-ios-2026-11-27.md`.

**10. Version.** same revision.

---

### L9 — Multi-tap (`count`) is unreliable on both platforms

**1. Goal.** Verify double-tap (`Modifier.adaptiveClickable.onDoubleClick`).

**2. What exists today.** `pointer.click count=1..3`.

**3. What failed.**
- Android: `count=2` runs two separate `input tap` invocations
  (`mobile_driver.py:393-409`); process startup exceeds Compose's ~300 ms
  double-tap window. Result: two single clicks (`Clicks: 2`, `Double: 0`).
- iOS: AXe `tap --count 2` produced
  `ClientError('The action response was lost...')` twice; the flow was removed.

**4. Technical reason.** Confirmed for Android (separate processes); unconfirmed
for iOS (AXe hangs or the HTTP reply is lost during multi-tap).

**5. Layer.** `ui-test-actions` / AXe.

**6. Workaround.** Do not drive double-tap; document as untested.

**7. Permanent fix.** Android: emit a single `input tap` sequence with explicit
`down/up` timing inside the double-tap window (e.g. `input touchscreen tap` pair
via `sendevent`, or `adb shell input tap x y; input tap x y` in one shell is
still too slow — use `motionevent`). iOS: implement native double-tap via AXe
or `simctl` HID events; add a `pointer.double_tap` command.

**8. Verification.** Showcase `Double` counter increments on both platforms,
10/10 runs.

**9. Evidence.** `screenshots/android/functional/clickable/...failed-after.png`
(Clicks: 2, Double: 0); iOS error text.

**10. Version.** same revision.

---

### L10 — Drag implementation cannot drive some controls (slider)

**1. Goal.** Move `AdaptiveSlider` from 50 % to a higher value.

**2. What exists today.** `pointer.drag` implemented as W3C pointer
down/move/up (Android) or `axe draw` (iOS). iOS also exposes `pointer.gesture`
only through the Appium path (`webdriver_driver.py:165-170`), not AXe.

**3. What failed.** iOS: dragging the track group centre to the right edge left
the value unchanged (`slider did not move`). Android: same flow passed.

**4. Technical reason.** **Not confirmed.** AXe `draw` may synthesize a swipe too
fast or without intermediate move events; Compose sliders may require a press
pause. Alternatively the drag started on the thumb but ended outside the touch
slop.

**5. Layer.** `ui-test-actions` iOS input; possibly Compose gesture handling.

**6. Workaround.** None reliable. Slider is `failed` on iOS; `UI-SLIDER-001`
remains failed.

**7. Permanent fix.** Implement drag as a track of points with configurable
duration and intermediate steps, and add `element.drag(id, dx, dy)`; verify
against UISlider and Compose slider.

**8. Verification.** Slider value changes and is asserted by `value`.

**9. Evidence.** `screenshots/ios/functional/slider/...-failed-after.png`.

**10. Version.** same revision.

---

### L11 — Overlay/window ownership is invisible

**1. Goal.** Detect and interact with popovers, sheets, alerts and system
windows; distinguish app content from overlay.

**2. What exists today.** A single flat tree per snapshot, no window list, no
z-order, no modal flag.

**3. What failed.** iPad ActionSheet popover: the screenshot shows a centred
popover with Ok/Remove and **no Cancel**; the tree offered no Cancel and the
flow failed. Whether Cancel is hidden by UIKit popover convention or missing
from the tree could not be distinguished from the snapshot. Sheet content
(“Allow swipe to hide”) also could not be located.

**4. Technical reason.** **Inferred.** AXe returns the app hierarchy; UIKit
renders popovers/sheets in presentation containers that may not surface all
actions as children, and there is no window metadata to tell “not present” from
“not exposed”.

**5. Layer.** `ui-test-actions` observation, plus UIKit behaviour/Showcase
expectation.

**6. Workaround.** Screenshot inspection; assert by text when present.

**7. Permanent fix.** Add `ui.windows` with role/owner/bounds, `alert.present`,
and `tree.snapshot(window=…)`; expose `modal: true` and `z_index`.

**8. Verification.** iPad popover: assert exactly one window, assert Cancel
absence is reported as `modal_cancel: absent`, and dismiss via outside tap.

**9. Evidence.** `screenshots/ios/alertdialogiosstyle-actionsheet/ipad-popover/ipad-simulator.png`.

**10. Version.** same revision.

---

### L12 — Session and tunnel lifetime is fixed and failure modes are opaque

**1. Goal.** Run 60–90 minute suites over a Cloudflare Quick Tunnel and keep
evidence consistent.

**2. What exists today.** Session duration 1–180 min (`session.py:516,585`);
hold deadline `duration*60+45` (`lifecycle.py:57-90`); HTTP client timeout 38 s
with 2 retries (`agent.py:63-118`).

**3. What failed.**
- At session end, actions surfaced `HTTP 408 (condition_timeout)` and then
  `HTTP 530` (tunnel origin gone). One run lost its final flow results.
- A lost action reply (clickable, iOS) raised
  `action_outcome_unknown` with no way to ask whether the tap happened.
- No reconnect after the tunnel disappears; a new connection artifact is needed.

**4. Technical reason.** Confirmed mechanics: fixed deadline; quick tunnel is
runner-owned and stops with the job; `fetch()` treats a 5xx without a structured
error as retryable but a lost response as uncertain.

**5. Layer.** `ui-test-actions` lifecycle/tunnel design.

**6. Workaround.** Persist results after every flow (implemented in our driver);
end sessions early; avoid depending on late-session actions.

**7. Permanent fix.** Heartbeat/`session.extend(minutes)`; unique session URL
reuse; `/v1/health`; idempotency ledger so a client can query the outcome of a
request id; graceful 410 with `seconds_remaining` before expiry; reconnection
tokens.

**8. Verification.** Kill the tunnel mid-action, reconnect, query the request id,
and receive the true outcome; session extends by 30 min.

**9. Evidence.** `date-bounds` 408/530 at 12:52/12:57; iOS clickable
`action_outcome_unknown`; lifecycle source above.

**10. Version.** same revision.

---

### L13 — Screenshots are not bound to a UI state

**1. Goal.** Guarantee that a screenshot matches the assertion that just passed.

**2. What exists today.** `/v1/screenshot` captures the framebuffer directly; no
snapshot id, no stability wait. `visual.wait` samples regions but is not used by
screenshots.

**3. What failed.** Captures taken immediately after taps were occasionally
mid-animation or showed the post-layout jump (date display mode), making visual
evidence weaker than the assertion. No correctness failure, but evidence quality
suffered.

**4. Technical reason.** Confirmed: screenshot path does not reference a tree
snapshot.

**5. Layer.** `ui-test-actions`.

**6. Workaround.** Take screenshots after text assertions (our driver does).

**7. Permanent fix.** `screenshot(wait_stable_ms, bind_snapshot=true)` returning
`{png, snapshot_id}`; sample two frames until identical or timeout.

**8. Verification.** Screenshot after a click is pixel-stable and its
snapshot_id matches the assertion snapshot.

**9. Evidence.** Date display screenshots; spinner progress captures.

**10. Version.** same revision.

---

### L14 — Device model and window class are not first-class

**1. Goal.** Run identical suites on phone and tablet and keep evidence separate.

**2. What exists today.** The simulator UDID/device is supplied by the workflow;
viewport is discovered from the framebuffer/Appium. Android tablet size is set
with `adb wm size` outside the harness.

**3. What failed.** Nothing failed, but the harness has no notion of device
class or logical size; artifact names, screenshot names and coverage keys had to
be managed by our wrapper.

**4. Technical reason.** Design choice: harness is device-agnostic.

**5. Layer.** `ui-test-actions` (feature gap), our workflow (workaround).

**6. Workaround.** `--device` naming, `record.py --tablet`, separate comparison
sheets.

**7. Permanent fix.** Expose `device.info {model, os, window_class, viewport,
dpi, orientation}` and include it in every artifact/response.

**8. Verification.** Same suite reports device class and stores evidence under
that class without external naming conventions.

**9. Evidence.** `showcase/evidence/session-runbook.md`; artifact names
`ui-session-android-tablet-…`.

**10. Version.** same revision.

---

### L15 — Error taxonomy is too coarse for automation

**1. Goal.** Distinguish “not found”, “not visible”, “not actionable”, “tree
truncated”, “driver not ready”, “reply lost”, “session expired”.

**2. What exists today.** Codes exist (`condition_timeout`, `invalid_arguments`,
`assertion_failed`, `observation_incomplete`, `action_outcome_unknown`,
`session_ended`) but mapping is inconsistent: a driver readiness problem becomes
`invalid_arguments`; a missing element becomes `condition_timeout` (408) rather
than 404/422.

**3. What failed.** Every `element.wait` miss logs `HTTP 408`, indistinguishable
from a tunnel timeout; retry logic in the driver therefore treats genuine
“not found” as transient.

**4. Technical reason.** `wait_for` raises 408 on deadline (`automation.py:254-267`);
`invalid_arguments` is the catch-all 400.

**5. Layer.** `ui-test-actions`.

**6. Workaround.** Message-text matching in the driver.

**7. Permanent fix.** Use `element_not_found` (404/422) for wait misses, reserve
408 for transport; add structured `details {selector, snapshot_id, last_match}`;
include the rejected field in `invalid_arguments`.

**8. Verification.** Unit tests over the error table; client can branch without
parsing prose.

**9. Evidence.** Driver logs; error payloads in session output.

**10. Version.** same revision.

---

### L16 — Text input depends on clipboard and focus

**1. Goal.** Type into search fields and alert text fields.

**2. What exists today.** iOS: `clipboard.set` + ⌘A/⌘V; Android: IME/clipboard
or `input text`.

**3. What failed.** Search typing triggered L5; text field flow passed. In
principle paste can race with focus, and `replace` relies on ⌘A.

**4. Technical reason.** Confirmed implementation; race unconfirmed.

**5. Layer.** `ui-test-actions`.

**6. Workaround.** None needed for the passing flows.

**7. Permanent fix.** Implement `text.insert` via native keyboard events per
character or XCUITest `typeText`, with focus verification.

**8. Verification.** Insert into a field immediately after tap, 20 runs, no lost
characters.

**9. Evidence.** `ios_axe.py:143-149`; search probe.

**10. Version.** same revision.

---

### L17 — No process-death / saveable-state control

**1. Goal.** Verify navigation state restoration and `rememberSaveable`.

**2. What exists today.** `app.restart` is a cold restart; no background/
foreground, no “kill and restore saved instance state”.

**3. What failed.** We could only verify rotation-based recreation on Android
(`nav-restore`). True process-death restoration is untested on both platforms.

**4. Technical reason.** No lifecycle commands beyond launch/close/restart.

**5. Layer.** `ui-test-actions`.

**6. Workaround.** Rotation on Android only.

**7. Permanent fix.** `app.background`, `app.foreground`, `app.kill
(preserve_state=true)` using `am kill`/`simctl terminate` with state restoration
and an assertion hook.

**8. Verification.** Navigate, kill preserving state, relaunch, assert route and
state.

**9. Evidence.** `showcase/coverage.json` `NAV-003` iPhone `not-run`.

**10. Version.** same revision.

---

### L18 — Batch and tracing are uneven across drivers

**1. Goal.** Speed up long suites and debug failures.

**2. What exists today.** `/v2/batch` exists; the Python client supports it.
AXe supports `trace.start/stop`, `visual.*`; the Appium driver adds gestures but
not all commands.

**3. What failed.** We did not use batch because a lost reply makes a multi-step
batch ambiguous and there is no per-step result replay. Traces exist on iOS but
not on the Android Appium path in our sessions.

**4. Technical reason.** Partial driver matrices (`ios_axe.py:82`,
`webdriver_driver.py:122`).

**5. Layer.** `ui-test-actions`.

**6. Workaround.** Single actions; screenshots after assertions.

**7. Permanent fix.** Batch with per-step request ids and idempotent replay;
uniform trace support; export a machine-readable action log with snapshots.

**8. Verification.** A 50-step batch produces 50 queries and survives a dropped
connection.

**9. Evidence.** Capability dumps per platform.

**10. Version.** same revision.

---

## 3. Prioritized improvement backlog

### P0 — Essential for functional component testing

| ID | Problem | Proposal | Platforms | Acceptance criteria |
| --- | --- | --- | --- | --- |
| P0-1 | Switch/chip/tab/slider state not selectable | Populate `checked`, `checkable`, `selected`, `value`, `adjustable`; normalise roles; add `name_contains`; add `element.adjust` | Android, iOS | Wi-Fi switch selectable by `checked:false`, toggle asserts `checked:true`; slider adjusted by value on both |
| P0-2 | No iOS rotation | Implement rotation via simctl/Simulator automation; advertise `device.rotate/orientation`; wait for viewport change | iOS | `NAV-003` passes on iPhone and iPad, 10/10 |
| P0-3 | Native pickers/share/camera untargetable | `ui.windows`, `ui.target(package|bundle)`, `alert.accept/deny`; document system-UI sessions | Android, iOS | Seeded `kira-fixture.txt/.png` selected through the real picker and asserted in-app |
| P0-4 | Off-screen controls unreachable | `element.scroll_into_view`, `element.scroll(id, direction)`; do not prune offscreen nodes where possible | Android, iOS | Sheet veto and date display flows pass at 402×874 |
| P0-5 | `app.restart` race returns 400 | Block until foreground + stable tree; add `app.wait_ready`; new error code `not_ready` | Android, iOS | 100 restarts with immediate `element.wait`, zero 400s |
| P0-6 | Lost action outcome unqueryable | Idempotency ledger + `GET /v2/action/{request_id}`; dedupe tap window | Both | After a forced dropped reply, query returns the true outcome |

### P1 — Reliability and platform parity

| ID | Problem | Proposal | Acceptance |
| --- | --- | --- | --- |
| P1-1 | Double tap unreliable | Single-shell precise tap pair (Android), native double-tap (iOS) | Showcase `Double` counter increments 10/10 both |
| P1-2 | Drag cannot move slider | Multi-point drag with duration + `element.drag` | Slider value changes and is asserted |
| P1-3 | Screenshot/state mismatch | Stable screenshot bound to `snapshot_id` | Pixel-stable screenshots, snapshot matches assertion |
| P1-4 | 408 used for not-found | New `element_not_found` code; reserve 408 for transport | Client branches without string matching |
| P1-5 | Fixed session expiry, no reconnect | Heartbeat, `session.extend`, health endpoint, reconnection token | Kill tunnel, resume and finish the flow |
| P1-6 | iOS search results invisible | Investigate AXe focused traversal; add all-window observation | Filter + select result in one snapshot |
| P1-7 | Text/name split | Unified `label` selector + mapping docs | Same selector finds Compose labels on both |
| P1-8 | Window/overlay blind | `ui.windows`, modal flag, dismissal helper | iPad popover reported correctly and dismissed |

### P2 — Developer experience, performance, evidence

| ID | Problem | Proposal | Acceptance |
| --- | --- | --- | --- |
| P2-1 | No device metadata | `device.info` in every response/artifact | Evidence keyed by model/class automatically |
| P2-2 | Batch ambiguity | Per-step ids + replay; traces on Android | 50-step batch survives a drop |
| P2-3 | Coarse errors | Structured `details` with selector and last snapshot | One-line diagnosis from error JSON |
| P2-4 | Slow suites | Persistent app state option, batch, parallel device sessions | 30-flow suite under 20 min |
| P2-5 | Docs gap | Document per-driver capability matrix and Compose mapping | Capability table generated from code |
| P2-6 | Evidence provenance | Include UI-test revision, device, OS in every artifact | Reproducible evidence bundle |

---

## 4. Reproduction recipes

1. **iOS rotation gap**
   ```sh
   python3 -c "import sys; sys.path.insert(0,'ui-test-actions'); from ui_sdk import LiveUI; ui=LiveUI.open(connection,token); print(sorted(ui.capabilities()['commands']))"
   ```
   No `device.rotate` / `device.orientation`.

2. **Restart race**
   ```python
   ui.action("app.restart", {"id": app})
   ui.action("element.wait", {"selector": {"text_contains": "component screens"},
                              "state": "present", "timeout_ms": 5000})
   ```
   Intermittently `HTTP 400 (invalid_arguments)`; retry after 1.5 s succeeds.

3. **Switch semantics**
   ```python
   ui.action("element.wait", {"selector": {"properties": {"checked": False}}, ...})
   ```
   Never matches on iOS (AXCheckBox has no `checked`), and does not match on
   Android (no properties parsed).

4. **Double tap**
   ```python
   ui.action("pointer.click", {"x": x, "y": y, "count": 2})
   ```
   Android: two clicks, no double; iOS: `action_outcome_unknown`.

5. **Overlay**
   Open the iPad ActionSheet; `tree.snapshot` has no Cancel; screenshot shows
   Ok/Remove.

---

## 5. What worked well

For balance: the following were reliable across many runs and should not be
regressed.

- `element.wait`/`assert` on text and role, snapshot ids, and truncated-tree
  protection for absence.
- Android permission dialogs (multiple, sequential) – bulk deny passed.
- App launch/restart/terminate, app metrics, clipboard, Unicode text.
- Cloudflare tunnel through a 60–90 minute session; screenshots (PNG), traces
  and recording endpoints.
- Deterministic coordinate clicks and drags on ordinary Compose controls.
- Session artifact publication with a one-time token digest.

---

*Report prepared from the pinned checkout `0c818c5d72e8c30c59bd1287c330a40392bf8e89`
and the evidence runs listed at the top. All error strings are quoted verbatim
from driver output; unconfirmed causes are marked as such.*
