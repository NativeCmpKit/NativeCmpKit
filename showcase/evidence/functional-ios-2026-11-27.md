# iOS functional UI run — 2026-11-27

- Workflow run: [46014167086](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/46014167086)
- iOS job: `140556939197`
- Revision: `94a93ef8e9d8d02c33454b48ebff5db72711384b`
- Device: `iPhone 17 Pro`, iOS 26.5 simulator, 402×874 pt, portrait
- Driver: `showcase/automation/functional.py` over ui-test-actions
  `0c818c5d72e8c30c59bd1287c330a40392bf8e89`
- Session: `bba824c324aecaeeedc7c493` (Cloudflare Quick Tunnel)

The session ran the tour first (stopped after three captures when the search-index
navigation turned out not to expose result rows on iOS) and then two functional
passes. The second pass used scroll-based Home navigation and is the recorded one.

## Recorded result

`16 passed, 6 failed, 0 blocked` — 22 flows executed. `screenshots/ios/functional-iphone-simulator.json`.

Passed: `buttons`, `switch`, `dropdown` (top-bar UIMenu → Duplicate), `alert-cancel`,
`alert-text-field` (name field, Cancel), `alert-confirm`, `scaffold-tab`,
`action-sheet` (native popover dismissal), `permissions-sms-rows`, `time-24h`,
`permissions-bulk-deny` (two OS prompts denied), `sheet`, `topbar` (Share and Add
system item), `toolbar`, `navbar`, `icons-category`.

Pending retest in that run:

| Flow | Observed |
| --- | --- |
| `clickable` | action response lost mid-flow (`ClientError`); single/long press not asserted this pass |
| `slider` | iOS exposes the UISlider as an unnamed `AXGroup`; label lookup was exact, not substring |
| `date-bounds` | `HTTP 408` condition timeout; no verdict |
| `sheet-veto` | the in-sheet switch row was below the visible sheet fold |
| `date-display` | toggle fired but the readout did not change; needs row-targeted switch click |
| `webview-js` | JavaScript-off evaluation did not produce `JS: null` |

A third pass at 16:15 was cut off by the 30-minute driver timeout after
`icons-category`; `geo-math`, `limitations`, `liquidglass` and `webview` were not
re-run in this session.

## Platform findings from this session

- The Home search field is visible but **not** exposed as a filter on iOS: after
  typing, the AX tree still contains only the `AXTextArea`, so the tour uses
  scroll navigation on iOS (`open_screen(..., use_search=False)`).
- iOS switches are `AXCheckBox` with names `On`/`Off`, not `AXSwitch`.
- iOS sliders have no role; the track is an `AXGroup` sharing the label's left
  edge. The driver now drives that group.
- The iOS alert screen's text-field and action-sheet sections **are** reachable
  and passed; Android correctly skips them as not-applicable.
- `AXe` rejects `keyboard.press BACK` (HTTP 400), so `ensure_home` no longer sends
  the Android key on iOS.
- Immediately after `app.restart` the first action can return
  `HTTP 400 invalid_arguments`; retrying after ~2 s succeeds.

## Not covered by this run

- iPad popover (`UI-ALERT-006`), large-screen layout.
- iOS Time Picker capture and the 24-hour picker visual state (functional readout passed).
- WebView second page, cookie and error states were last captured in run
  `45968953555`; they were not re-captured in this session.
- Desktop/web targets are out of scope for this device matrix.
