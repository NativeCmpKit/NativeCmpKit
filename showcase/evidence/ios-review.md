> Post-review updates: the Alert Dialog overview/simple states and the
> WebView JavaScript/cookie/clear/invalid states were captured separately with
> the same live session. The iOS Time Picker remains uncaptured and is the single
> supported iOS coverage row still `not-run`. The shared worktree's
> `coverage.json` was later updated by the lead's `record.py`; this report is the
> independent subagent snapshot taken before that record step.

# iOS showcase tour — 2026-11-27

Worktree: `/root/.t3/worktrees/nativeCmpKit/showcase`
Revision: `e4ec7441` (working tree had pre-existing edits to `README.md`,
`showcase/automation/{smoke,tour}.py`, `showcase/COVERAGE.md`,
`showcase/coverage.json`, `showcase/evidence/build-failures.md`; none were
changed by this run).
Session: `dc8ed10bbd25ac3ef8eaa30a`, target `ios`, `iphone-simulator`, 402×874.

## Command (run exactly once)

```sh
python3 showcase/automation/tour.py \
  --client-dir /tmp/opencode/ui-test-actions \
  --connection /tmp/opencode/session-ios3/connection.json \
  --token-file /tmp/opencode/showcase-token \
  --platform ios \
  --output-root screenshots \
  --continue-on-error
```

- Start `2026-11-27T09:26:04Z`, last capture `10:01:32Z`, stop shortly after
  `10:02Z` → **~36 minutes** (not the expected 15–20).
- Process exit status **0**, but only because `--continue-on-error` converts
  failures to status 0. The run itself is **not clean**: `tour.json` has
  `"ok": false`.
- Log: `/tmp/opencode/research/tour.log`.

## Result: 25 captures, 3 errors

`screenshots/ios/tour.json` → `captures: 25`, `errors: 3`, `ok: false`.
25 PNG files exist and every one is fresh: the five PNGs left by the earlier
partial run (08:44–08:46) all changed SHA-256 and were rewritten 09:26–10:01.
No stale image was retained in place of a failure (the failed screens never had
an older file).

### Errors (verbatim from tour.json)

| screen | error |
|---|---|
| Adaptive Time Picker | `ClientError('HTTP 408 (condition_timeout)')` |
| Adaptive Alert Dialog | `RuntimeError("Could not find the Home entry for 'Adaptive Alert Dialog'")` |
| Web View | `RuntimeError("No visible element for 'Load second HTML page'")` |

### Missing artifacts because of those errors

- `ui-adaptive-time-picker/overview` — no file.
- `ui-adaptive-alert-dialog/overview` and `ui-adaptive-alert-dialog/simple` — no files.
- `webview/second-page`, `after-back`, `after-forward`, `javascript-title`,
  `cookie-roundtrip`, `cookies-cleared`, `invalid-destination` — no files
  (only `webview/overview` exists).
- `ui-cupertino-icons/search-chevron` — not produced; the code only shots it when
  `find_search()` finds the in-screen search field, and it returned nothing.
  This one is silent (no error entry).

## Smoke-critical screens

| screen | captured? | notes |
|---|---|---|
| Adaptive Buttons | **yes** | overview, 09:26:56 |
| Adaptive Switch | **yes** | overview, 09:28:01 |
| Adaptive Slider | **yes** | overview, 09:28:30 |
| Adaptive Date Picker | **yes** | overview, 09:30:04 |
| Adaptive Alert Dialog | **NO** | automation never reached the Home card; no dialog state captured |
| Adaptive Bottom Sheet | **yes** | overview + expanded |
| Adaptive Dropdown | **yes** | overview + menu |
| Permissions | **yes** | overview only; no OS permission dialog was triggered |
| WebView | **partially** | overview only; all 7 interaction scenarios missing |
| Known Limitations | **yes** | known-limitations |

Coverage rows were **not** marked passed and `showcase/coverage.json` was **not**
edited by this run. (It did change on disk at 09:37:50 during the tour — another
process/session in this shared worktree, not this run. Same for
`showcase/COVERAGE.md`.)

## Captures

| # | component / scenario | bytes | mtime (UTC) |
|---|---|---|---|
| 1 | `home/index` | 138669 | 09:26:18 |
| 2 | `ui-adaptive-button/overview` | 102085 | 09:26:56 |
| 3 | `ui-adaptive-clickable/overview` | 37574 | 09:27:27 |
| 4 | `ui-adaptive-switch/overview` | 76913 | 09:28:01 |
| 5 | `ui-adaptive-slider/overview` | 67391 | 09:28:30 |
| 6 | `ui-adaptive-progress/overview` | 59345 | 09:29:07 |
| 7 | `ui-adaptive-date-picker/overview` | 115302 | 09:30:04 |
| 8 | `ui-adaptive-bottom-sheet/overview` | 38774 | 09:38:01 |
| 9 | `ui-adaptive-bottom-sheet/expanded` | 76295 | 09:38:11 |
| 10 | `ui-adaptive-dropdown/overview` | 72173 | 09:38:50 |
| 11 | `ui-adaptive-dropdown/menu` | 79815 | 09:39:08 |
| 12 | `ui-adaptive-scaffold/overview` | 55014 | 09:40:42 |
| 13 | `ui-adaptive-top-bar/overview` | 126319 | 09:43:15 |
| 14 | `ui-adaptive-navigation-bar/overview` | 64512 | 09:45:34 |
| 15 | `ui-adaptive-toolbar/overview` | 55130 | 09:47:10 |
| 16 | `ui-cupertino-icons/overview` | 130880 | 09:47:55 |
| 17 | `io-file-picker/overview` | 72125 | 09:48:59 |
| 18 | `io-image-picker/overview` | 45060 | 09:50:14 |
| 19 | `io-file-saver/overview` | 56619 | 09:51:19 |
| 20 | `io-camera-picker/overview` | 46325 | 09:52:23 |
| 21 | `share/overview` | 81248 | 09:53:50 |
| 22 | `webview/overview` | 197410 | 09:55:22 |
| 23 | `permissions/overview` | 155554 | 09:57:23 |
| 24 | `geo-math/overview` | 130964 | 09:59:33 |
| 25 | `limitations/known-limitations` | 198048 | 10:01:32 |

Note the 8-minute gap between #7 (09:30) and #8 (09:38): that is the Time Picker
timeout plus the failed Alert Dialog search (the 408 plus 40 scroll attempts).

## Visual inspection (representative images)

**Home (1).** Renders correctly: "Kira" wordmark, "Compose Adaptive Look & Feel"
with blue accents, search field, "24 component screens", "Reset state", and
"UI Components" cards. Icons (sparkles, dialog, bottom-sheet, progress, switch,
slider) all draw. No truncation or overlap. "Adaptive Alert Dialog" is visibly
the second card here — so its absence is an automation-path failure, not proof
the screen is missing.

**Adaptive Buttons (2).** All six groups render: Filled/Disabled, Filled Glass,
Icon Buttons (heart/share/plus + greyed disabled), Buttons with Icons
(Create New, Share), Cupertino Filled/Bordered/Plain. Disabled variants are
deliberately low-contrast, not missing. No clipping.

**Adaptive Switch (4).** Wi-Fi/Notifications/Dark Mode rows plus
"Cupertino Switch (parity control)". Native-looking green iOS switch, blue
parity switch, grey disabled. Layout clean.

**Adaptive Slider (5).** Five rows (Brightness 50%, Volume 75%, Custom range
40/100, Discrete 2/5, Disabled). Labels and values align; thumb/track render.
The screen claims "Liquid Glass on iOS 26+", but in the still the track is a flat
grey line with a plain white thumb — no glass material is visually evident.

**Adaptive Date Picker (7).** Range chips, Weekdays-only toggle, compact picker
field ("Nov 27, 2026"), range row, and an inline November 2026 calendar all
render. The calendar is cut by the bottom edge at day 14; the screen is
scrollable, so this is viewport, not truncation.

**Alert Dialog.** No image; cannot assess. Only the Home card is visible (see
Home above).

**Adaptive Bottom Sheet, expanded (9).** Native sheet presentation is visible
(grabber, rounded top). **Visible layout defect:** the sheet content is drawn
offset up and left — the title is horizontally clipped ("ottom Sheet") and
vertically cut by the sheet's top edge, and the grabber overlaps the title. The
"Close" pill, "Allow swipe to hide" toggle and "Show Alert Dialog" button are
crammed together with almost no vertical rhythm. Could be a mid-transition
frame, but the sheet's own bounds look settled.

**Adaptive Dropdown, menu (11).** Real iOS UIMenu with Copy / Share / red Delete
/ disabled Archive over the content. The top-right and in-card icon buttons are
`ellipsis`-style dots (at 1× they look like a face; a 4× crop confirms three
dots in a circle). No defect.

**Permissions (23).** Renders Multiple/Call/Camera/Gallery sections with granted
and denied states. Content is centre-aligned and the Gallery section is cut at
the bottom edge (scrollable). Statuses shown are Android-flavoured
(`Denied(shouldShowRationale=false)`) on iOS — worth a wording review, but no
rendering fault. No OS permission sheet appears, as expected: the tour never taps
"Request permission".

**WebView, overview (22).** WKWebView loads the local HTML, with headings,
bullets and the link visible. The in-screen title bar truncates to
"Kira WebView D…" / "Finished · errors 0 · ba…" (ellipsis by design) and shows a
warning-triangle button. The icon-only control row (Back, Forward, Reload, Stop,
Globe, Code) is drawn along the bottom.

**Known Limitations (25).** All card text renders fully: Expandable FAB, no
determinate circular progress, buttons without size/selected state, iOS 26
switch/slider parameter replacement, time format, menu anchor, etc. Bottom card
is cut by the viewport edge (scrollable).

**Cupertino Icons (16).** 1,332 icons render as real glyphs — **no tofu / no
missing-glyph boxes**. Grid labels are ellipsised (`bookmark_s…`,
`check_mark_…`, `battery_char…`), which is the intended single-line grid
behaviour, not a font failure. The in-screen search interaction was not captured.

**Top Bar (13) / Navigation Bar (14).** Native `UINavigationBar` with large
title and trailing items (heart, ellipsis-circle, share) and native `UITabBar`
with Home/Favorite/Profile. Both look like iOS 26 system chrome: floating
capsule bar buttons, translucent tab bar. This is the only place where a
Liquid-Glass-like material is clearly visible.

**File Picker (17), Share (21), Camera Picker (20).** All render. File-type chips
run past the right edge (PDF clipped, next chip a sliver) — a horizontal strip
that needs scrolling. Share URL text wraps after
`https://github.com/Apdelrahman1911/`. No overlap.

## Root cause of the WebView failure (verified, read-only probe)

After the tour, a single non-capturing AX probe opened Web View and dumped the
tree. The control icon buttons exist as `AXButton` but expose the **icon's own
name**, not the Compose `contentDescription` the script searches for:

- expected `Navigate Back` → exposed as `Back`
- expected `Navigate Forward` → `Forward`
- expected `Reload` → `refresh`
- expected `Stop Loading` → `Close`
- expected `Load URL` → `Globe`
- expected `Load second HTML page` → `embed code`

Text-labelled controls do surface correctly (`Evaluate JavaScript title`,
`Set and read cookie`, `Load invalid URL`), which matches the one success and the
later failures in the script. So the WebView screen was reachable; only the
selector vocabulary is wrong on iOS. **No screenshots were taken during this
probe and no source was edited.**

The Time Picker 408 and the Alert Dialog miss happen consecutively; the Alert
Dialog card is visible in the 09:26 Home capture, so the second failure is best
explained by state left behind after the Time Picker condition timeout. That is
a hypothesis, not verified — the tour was not re-run.

## Caveats

- This is **one** iOS simulator run. It does not establish Android/desktop/web
  behaviour, native/device evidence, consumer/API-ABI checks, or release
  readiness.
- Screens are captures of the first viewport. Nothing was scrolled inside a
  component screen, so "content continues below the fold" is expected and not
  evidence of truncation.
- The iOS session's tunnel degraded late in the run (large `tree.snapshot`
  requests began returning "action response was lost"; limit 200 kept working).
  This did not affect any recorded capture — they all predate the degradation.
- Shared worktree: `showcase/coverage.json` and `showcase/COVERAGE.md` were
  rewritten at 09:37:50 by another process while this tour ran. I did not touch
  them, and they must not be read as output of this run.
