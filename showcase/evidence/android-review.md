> Post-review updates: the Cupertino icon font packaging defect was repaired
> in `sample/android/build.gradle.kts`, the APK now contains
> `assets/composeResources/.../font/sf_symbols.ttf`, and the catalog was
> recaptured. The Web View action loss was recovered with six separate captures.
> `record.py` later marked Android supported rows as `captured` (53) or `passed`
> (1); see `showcase/coverage.json` for the current statuses. This report is
> retained as the independent review snapshot taken before those updates.

# Android showcase evidence review

Read-only review of the Android showcase captures in
`/root/.t3/worktrees/nativeCmpKit/showcase` (branch
`feature/showcase-ui-verification`, base `a2c48c0b`). No Gradle task, workflow or
repository file was changed. Image inspection used a throwaway Pillow/fontTools
venv under `/tmp/opencode`.

**Bottom line:** all 34 PNGs are valid, full-resolution emulator screenshots, but
this is raw capture evidence only. Zero coverage rows have a recorded execution,
54/54 supported rows point at screenshot paths that do not exist, the WebView
scenario set is not part of `tour.json` and three of its six images are
byte-identical, and every Cupertino icon glyph renders as a missing-glyph box.
Nothing here should be recorded as `passed` or as Android acceptance, and it says
nothing about iOS.

---

## 1. Provenance

| Item | Observed |
| --- | --- |
| `screenshots/android/tour.json` | `session: bb97409ca8f33b40ae1a9e9a`, `device: api35-phone`, `ok: false` |
| Tour capture window | 07:49:59 to 08:05:34 UTC (status-bar clock advances 7:50 → 8:05) |
| WebView captures | 08:20:19 to 08:21:36 UTC, **not listed in `tour.json`** |
| Smoke run | 08:14–08:15 UTC, same session id (`smoke-android3b/smoke.json`) |
| `screenshots/runs.json` | `appSha: pending`, `runUrl: pending`, `job: pending`, runtime `pending` |
| Run id 45957524569 | Does not appear anywhere in the tree |
| Device model/density/API metrics | Not recorded in any capture manifest |

All images show the Android status bar (clock, Wi-Fi/cellular/battery), gesture
navigation bar and Material system styling; capture times advance monotonically
within one session. That is **consistent with a live API 35 emulator at
1080x2400**, not a host render. It is not cryptographic proof: the tree carries no
APK SHA, run/attempt/job, emulator model or density, so the APK-to-revision link
cannot be verified from these files alone.

---

## 2. PNG inventory

34/34 PNGs are 1080x2400, 8-bit RGBA, fully opaque, and decode without error.
Total 4.3 MiB. No blank frames (minimum 525 distinct colours and σ ≥ 17 per
channel), no truncated/corrupt files, no host-render artefacts, no browser chrome.

Duplicate/near-duplicate groups:

- `webview/cookie-roundtrip`, `webview/cookies-cleared` and
  `webview/javascript-title` are **byte-identical** (SHA-256 `7cdc5149…`, 60,146 B).
- `webview/second-page` differs from those three in only 349 pixels, all inside
  the top-left back-arrow box `(135,50)–(152,78)`.
- Effectively, four "different" WebView scenarios are the same visible
  "Kira Second Page" frame.

Full table is in Appendix A.

---

## 3. `tour.json`: captured, missing, and the WebView failure

`tour.json` records **28 captures**:

- Home index (`home/index`).
- 23 screen overviews: Button, Clickable, Switch, Slider, Progress, Date, Time,
  Alert Dialog, Bottom Sheet, Drop Down, Scaffold, Top Bar, Navigation Bar,
  Toolbar, Cupertino Icons, File Picker, Image Picker, File Saver, Camera Picker,
  Content Sharing, Permissions, Geo Maths, Known Limitations.
- Four state shots: alert `simple`, sheet `expanded`, dropdown `menu`, icon
  `search-chevron`.

Missing from `tour.json`:

- **Web View**: the screen is in `SCREENS`, but the step failed with
  `ClientError('The action response was lost. Inspect the live UI before deciding
  whether to retry.')` and produced no capture entry. The six `webview/*` PNGs
  were written ~15 minutes after the tour ended, with no matching record (their
  own session id is not recorded). **Inference:** a separate/manual pass against
  the same still-running app, not the checked-in `tour.py` sequence (which would
  also have emitted `after-back` and `after-forward`).
- `webview/after-back` and `webview/after-forward` are entirely absent, although
  `tour.py` captures them. The back/forward assertions have no image.
- **Component Showcase** (`Screen.Showcase`, the "All adaptive components in a
  single view" banner on Home) is reachable but is not in `SCREENS`. The README's
  "captures every indexed screen" is therefore not exact.
- No scrolled/lower-viewport capture for any tall screen; no dark-mode capture.

Because `ok` is `false`, this is formally a failed tour even though most screens
were captured.

---

## 4. Coverage mapping (no row marked passed)

Counts from `showcase/coverage.json`:

| Measure | Count |
| --- | --- |
| Total rows | 66 |
| Android supported | 54 |
| Android unsupported / not-applicable | 12 |
| Android execution `not-run` | 54 |
| Android execution `not-applicable` | 12 |
| Android `captured` / `passed` / `failed` | 0 / 0 / 0 |
| Rows whose recorded Android PNG path exists | 8 (all the shared `limitations/known-limitations` file) |
| Rows whose recorded Android PNG path is dead | 58 (including **54/54 supported**) |

`record.py` has not been run for this capture set. Consequently the manifest still
contains aspirational per-row paths such as
`screenshots/android/adaptivebutton/filled-enabled-and-disabled/api35-phone.png`,
which `tour.py` never produces (it writes per-screen directories).

If captures are re-mapped by `component`/`route` (what `record.py` would do):

- 42 of 54 supported rows are backed only by a default top-of-screen overview,
  with no asserted state: Button (4), Clickable (1), Switch (2), Slider (3),
  Progress (2), Date (4), Time (1), four bars, IO (8), Permissions (8),
  Share (3), Geo (1), and Home/NAV (1).
- 6 rows are backed by an image of the *wrong* or insufficient state:
  - `UI-ALERT-002` (single button) → two-button "simple" dialog.
  - `UI-MENU-002` (sections) → simple Copy/Share/Delete menu.
  - `UI-ICON-003` (size and content description) → search grid only; neither
    property is demonstrated.
  - `WEB-002` (back/forward) → second page only, no navigation proof.
  - `WEB-004` (JavaScript title) → identical second-page image, no JS result.
  - `WEB-005` (cookie round-trip) → identical second-page image, no cookie.
- 6 rows have some relevant state in frame, all with caveats:
  `UI-ALERT-001` (dialog open), `UI-SHEET-001` (sheet open, not expanded/dismissed),
  `UI-MENU-001` (menu open), `UI-ICON-001` (search works, glyphs broken),
  `WEB-001` (inline HTML is visible only in the unmapped `overview` image;
  `record.py` would attach the second page), `WEB-003` (error page + "errors 1").

Rows that are visibly contradicted or unrepresentable:

- `UI-SWITCH-001` expects "on, off and disabled"; the Adaptive Switch demo has
  three enabled switches. The only disabled switch is the Cupertino parity
  control (`UI-SWITCH-002`).
- `UI-CLICK-001` expects single/long/double/disabled; the screen has one "Tap me"
  button and no long/double/disabled example.
- `UI-DATE-002/003/004`: compact and range pickers are never opened; the range is
  "Any date" and "Weekdays only" is off, so bounds/selection are unproven.
- `UI-ALERT-002`, `UI-MENU-002`, `UI-BAR-004` (only expanded state), and the
  IO/SHARE/PERM rows are static or pre-action screens only.

Unsupported rows: 12. Eight point at the single `limitations/known-limitations`
image (the only path that exists), but that viewport shows only the FAB-internal
and no-determinate-progress cards. The NAV-002, PERM-STUB-001, GEO-002,
EXCL-MAPS/MEDIA/NOTIF claims are below the fold and not evidenced. The other four
unsupported paths (DATE-005, ALERT-003, ALERT-004, ICON-002) do not exist.

`record.py` risks for the lead:

1. `CAPTURE_ROWS` maps `("ui-adaptive-alert-dialog","simple")` to both
   `UI-ALERT-001` and `UI-ALERT-002`, and `("ui-adaptive-dropdown","menu")` to both
   menu rows; both would overstate evidence.
2. It maps `("webview","second-page")` to `WEB-001`+`WEB-002` and
   `javascript-title`/`cookie-roundtrip` to `WEB-004`/`WEB-005` even though those
   files are the same frame and the result text is clipped.
3. The tour's error screen is the display title `"Web View"`, while
   `SCREEN_ROWS` is keyed by directory `"webview"`. A recording run would **not**
   mark any WebView row failed; the failure would disappear.
4. WebView captures are absent from `tour.json`, so even a correct recording run
   would not attach them.
5. It assigns the screenshot path unconditionally, including to
   `not-applicable` rows, which would give unsupported rows an unrelated screen
   image.

---

## 5. Image review

### 5.1 Confirmed visual defect: all Cupertino icons are tofu

Both `ui-cupertino-icons/overview` (1,322 icons) and `search-chevron` (33 results)
render every glyph as a rectangle with an X — Android's missing-glyph box. Labels
and filtering work; the icons do not.

Checked against the bundled font: `sf_symbols.ttf` family is `CupertinoIcons`,
it contains all 1,233 unique codepoints used by the catalog (including
`leftChevron = 0xF3D2`), and has 1,274 cmap entries. So this is **not** a
missing-codepoint problem; the bundled family is not being applied at draw time
(inference: Compose resource/font fallback on Android). There is a desktop-only
semantics test and no Android device test for this component. This alone blocks
treating `UI-ICON-001`/`UI-ICON-003` as verified.

### 5.2 WebView evidence is not usable as captured

- The app-bar subtitle is
  `"$loading · errors N · back $canGoBack · $cookieStatus"` with `maxLines = 1`
  and ellipsis (source-confirmed). On 1080 px it renders as
  `Finished · errors 0 · back ...`; the cookie/JS result is **after** the ellipsis.
  That is why `javascript-title`, `cookie-roundtrip` and `cookies-cleared` are
  pixel-identical: the differing text is clipped, not because the actions failed.
- `invalid-destination` does show `Webpage not avail…` /
  `Finished · errors 1 · back t…` and the system `net::ERR_NAME_NOT_RESOLVED`
  page. That is the only WebView assertion with visible evidence.
- `second-page` proves a second HTML page loaded; it does not prove back/forward.
- The header title and status line truncate on both normal and error pages; the
  error/diagnostic content the component exposes is not readable.
- The WebView screen uses an iOS-style `ArrowBackIosNew` chevron while the shared
  scaffold uses a Material arrow; minor inconsistency.

### 5.3 Viewport clipping on tall screens

These are scrollable screens, so the clipping is a capture-completeness issue,
not a layout crash:

- **Date picker**: inline calendar is cut after 21 November 2026; the month row
  shows "November 2026" with no visible prev/next controls in frame; no selected
  date. A partially drawn blue arc sits at the bottom edge below the grid
  (purpose not identifiable from the still).
- **Time picker**: the 24-hour dial is cut roughly in half by the bottom edge.
- **Permissions**: only Multiple/Call/Camera/Gallery are visible; the remaining
  ~20 permission entries (notification, location, contacts, calendar, Bluetooth,
  Wi-Fi, storage, SMS) are below the fold.
- **Known Limitations**: the sixth card and a sliver of a seventh are cut; six of
  the eight unsupported-row claims are not in frame.
- Home's last visible card and the Share/FileSaver lower content are cut by the
  viewport in the same expected way.

### 5.4 Permissions semantics

`permissions/overview` shows `Gallery — Is permission granted: true` on a freshly
reset API 35 app, without any prompt, while Camera/Call are denied. Source:
`Permission.Gallery` maps only to `READ_EXTERNAL_STORAGE` with
`maxSdkVersion = 32`; on API 35 the mapping is filtered out and the registry
returns `Granted` for the empty permission list. So the checkbox is a vacuous
grant, not evidence of gallery access (source-based inference). This is worth
fixing or labeling; it currently misrepresents the permission state.

No Android system permission dialog, file picker, camera app, share sheet or
notification prompt appears in any capture.

### 5.5 Other concrete visual/layout observations

- **Bottom sheet "expanded"**: the sheet is only partially expanded (top edge
  ~41% down the screen, not full height), and its content is flush to the left edge — title, Close button,
  switch and list items have no horizontal padding. Source confirms the sample's
  `LazyColumn` has no padding; this is a sample layout issue, not necessarily a
  component bug, but it looks broken and the "expanded" label is inaccurate.
- **Alert dialog**: both Cancel and Ok are equally weighted filled blue pills.
  Material3 convention is text buttons with the confirm action distinguished; this
  is a design deviation, not a functional failure. "Ok" is also non-standard
  casing.
- **File saver**: large empty band (~150 dp) between the screen title and the
  description; export is disabled with an empty avatar. No save/reopen flow.
- **File picker**: the horizontally scrollable type chips are clipped mid-letter
  at the right edge ("D…"). This is a scroll affordance, but the still looks
  truncated.
- **Share**: only the form is shown; "Share File"/"Share Multiple Files" are
  disabled and no native sheet appears.
- **Camera**: "No photo captured"; no camera intent or permission prompt.
- **Image picker**: "No images selected"; no picker or Coil preview.
- **Switch**: AdaptiveSwitch has no disabled example (row mismatch above);
  the Cupertino disabled switch looks almost white on a very light track.
- **Progress**: the Cupertino eight-spoke spinner is extremely faint against the
  background; static capture cannot show animation anyway.
- **Home/Buttons copy**: "Clicked 1 times" (grammar), and the app brands itself
  "Kira" while the app id is `…nativecmpkit.sample`. The latter may be intended
  product naming; needs owner confirmation, not a defect claim.
- **Home count**: "24 component screens" excludes the Showcase banner and does
  not correspond to the 66 coverage rows (row granularity is per variant).

### 5.6 What is actually well covered visually

- Button variants, slider values (continuous 50%, volume 75%, custom 40/100,
  discrete 2/5, disabled 40%), time 12h/24h values, progress sizes, scaffold
  chrome, top bar, navigation bar, dropdown item/disabled state, alert dialog,
  bottom-sheet content, and the WebView error page all render coherently.
- The smoke counter transition is visible and correct.

---

## 6. Smoke flow

`/tmp/opencode/smoke-android3b` has exactly four 1080x2400 images:

1. `01-home.png` — Home at 8:14.
2. `02-buttons.png` — Adaptive Buttons, "Clicked 0 times", Disabled button present.
3. `03-buttons-after-tap.png` — "Clicked 1 times", Disabled button unchanged.
4. `04-home-after-back.png` — Home at 8:15, same layout as (1).

So the images confirm Home → Buttons → counter 0→1 → Back to Home. `smoke.json`
contains only the session, command list and screenshot names/bytes — no assertion
results, no recorded counter value, no back-result flag. The conclusion is visual
only; it is not a scripted assertion record. The counter change is real in the
pixels and is the strongest functional evidence in the whole Android set.

---

## 7. Recommended next captures (priority order)

**P0 — before any recording/acceptance**

1. Fix or diagnose the Android Cupertino icon font application, then re-capture
   the icon overview and `chevron` search. Add an Android device/host test that
   asserts a non-tofu glyph (pixel or font-family), not just semantics.
2. Re-capture WebView with a result surface that is visible on a phone: wrap the
   status line or add a dedicated result row/panel. Capture JS title, cookie set,
   cookie cleared, and invalid URL with the actual result visible; also capture
   `after-back` and `after-forward`, and a scrolled second page.
3. Only then run `record.py` with real run/attempt/job and an explicit
   `--passed-ids` list after review; fix its over-mapping and the
   `"Web View"`/`"webview"` error-key mismatch; regenerate `INDEX.md` (currently
   absent) and `COVERAGE.md`.

**P1 — fill the assertion gaps**

4. Action-state captures: single-button dialog, sectioned dropdown, compact date
   picker open/confirm/cancel, range start/end, date select + "Weekdays only" ON,
   sheet expanded + dismissed, toolbar collapsed vs expanded, switch toggled +
   disabled AdaptiveSwitch, clickable long/double/disabled, slider drag.
5. OS-level flows on the emulator: file picker single/multi/folder + selected
   file, saver save/reopen, image picker + Coil preview, camera capture/fallback,
   share sheet for text/URL/file(s), permission grant/deny/settings-return for
   camera, microphone, notification, location, contacts/calendar and Bluetooth.
6. Scroll-to-bottom captures for Permissions, Known Limitations, Date Picker and
   Time Picker; capture the Component Showcase screen.
7. Record emulator model/API/density, APK SHA, run/attempt/job and artifact names
   in the manifests so the run id is reproducible from the repo.

**P2 — polish**

8. Sheet content padding; file-type chip edge; file-saver vertical gap; "1 times"
   copy; "Ok" vs "OK"; alert action emphasis; WebView back-icon consistency.

---

## 8. What this review does not establish

- No iOS evidence was reviewed or claimed (only five iOS PNGs exist, uncaptured
  by this tour).
- No Android row is a pass: there is no run-bound execution entry, and several
  rows are contradicted by the image they point at.
- No library test, device test, consumer/ABI check, dependency/legal/security
  gate or release readiness is implied by 34 screenshots.
- The device/APK identity is inferred from system UI and session metadata, not
  cryptographically bound in this tree.

---

## Appendix A — Android PNG inventory

All are `1080x2400` RGBA, α = 255 throughout, and load cleanly.

| Path under `screenshots/android/` | Px | KiB | SHA-256[0:8] | Content / note |
| --- | --- | --- | --- | --- |
| `geo-math/overview/api35-phone.png` | 1080x2400 | 160 | `543cf1e7` | LatLng distance/bearing + "tracking unavailable" |
| `home/index/api35-phone.png` | 1080x2400 | 251 | `d87432e4` | Home index top; 24 screens |
| `io-camera-picker/overview/api35-phone.png` | 1080x2400 | 61 | `22c8e20d` | "No photo captured" |
| `io-file-picker/overview/api35-phone.png` | 1080x2400 | 96 | `0b14e012` | Config form; no picker |
| `io-file-saver/overview/api35-phone.png` | 1080x2400 | 75 | `17e4cdf3` | Empty avatar; export disabled |
| `io-image-picker/overview/api35-phone.png` | 1080x2400 | 61 | `229621da` | "No images selected" |
| `limitations/known-limitations/api35-phone.png` | 1080x2400 | 256 | `3ea22b97` | First 6 cards; clipped at bottom |
| `permissions/overview/api35-phone.png` | 1080x2400 | 180 | `19daca43` | 4 sections; Gallery granted true; clipped |
| `share/overview/api35-phone.png` | 1080x2400 | 126 | `98983ed5` | Form only; file share disabled |
| `ui-adaptive-alert-dialog/overview/api35-phone.png` | 1080x2400 | 95 | `ebaa9df7` | Two launcher buttons |
| `ui-adaptive-alert-dialog/simple/api35-phone.png` | 1080x2400 | 106 | `048235ea` | Two-button dialog open |
| `ui-adaptive-bottom-sheet/expanded/api35-phone.png` | 1080x2400 | 90 | `938a013c` | Partial sheet, flush-left content |
| `ui-adaptive-bottom-sheet/overview/api35-phone.png` | 1080x2400 | 49 | `16d9b7ff` | Launcher only |
| `ui-adaptive-button/overview/api35-phone.png` | 1080x2400 | 117 | `7e86063a` | Variants; "Clicked 0 times" |
| `ui-adaptive-clickable/overview/api35-phone.png` | 1080x2400 | 53 | `88505b8f` | Single "Tap me" |
| `ui-adaptive-date-picker/overview/api35-phone.png` | 1080x2400 | 160 | `075f3c67` | Config + calendar clipped after 21 Nov |
| `ui-adaptive-dropdown/menu/api35-phone.png` | 1080x2400 | 117 | `384db55d` | Simple menu; Delete black, Archive disabled |
| `ui-adaptive-dropdown/overview/api35-phone.png` | 1080x2400 | 103 | `f94b8279` | Two cards |
| `ui-adaptive-navigation-bar/overview/api35-phone.png` | 1080x2400 | 102 | `67970e6b` | Favorites tab |
| `ui-adaptive-progress/overview/api35-phone.png` | 1080x2400 | 95 | `170972b1` | 3 arcs + faint Cupertino spinner |
| `ui-adaptive-scaffold/overview/api35-phone.png` | 1080x2400 | 84 | `92ef2c55` | Scaffold + bottom nav |
| `ui-adaptive-slider/overview/api35-phone.png` | 1080x2400 | 101 | `1d65a41a` | 5 sliders with readouts |
| `ui-adaptive-switch/overview/api35-phone.png` | 1080x2400 | 118 | `9569774a` | 3 adaptive (none disabled) + 2 Cupertino |
| `ui-adaptive-time-picker/overview/api35-phone.png` | 1080x2400 | 129 | `641890e5` | 12h + partial 24h dial |
| `ui-adaptive-toolbar/overview/api35-phone.png` | 1080x2400 | 48 | `97cc1a6c` | Floating toolbar, expanded only |
| `ui-adaptive-top-bar/overview/api35-phone.png` | 1080x2400 | 177 | `5c3c3ce1` | Three info cards |
| `ui-cupertino-icons/overview/api35-phone.png` | 1080x2400 | 131 | `bb0ea081` | 1,322 tofu boxes |
| `ui-cupertino-icons/search-chevron/api35-phone.png` | 1080x2400 | 105 | `a735c6e6` | 33 tofu boxes |
| `webview/cookie-roundtrip/api35-phone.png` | 1080x2400 | 59 | `7cdc5149` | Second page; no cookie visible (duplicate) |
| `webview/cookies-cleared/api35-phone.png` | 1080x2400 | 59 | `7cdc5149` | Byte-identical to above |
| `webview/invalid-destination/api35-phone.png` | 1080x2400 | 106 | `915709dd` | ERR_NAME_NOT_RESOLVED; "errors 1" |
| `webview/javascript-title/api35-phone.png` | 1080x2400 | 59 | `7cdc5149` | Byte-identical; no JS result visible |
| `webview/overview/api35-phone.png` | 1080x2400 | 485 | `0ec887b3` | Inline HTML first page |
| `webview/second-page/api35-phone.png` | 1080x2400 | 59 | `24091fa7` | Second page; differs 349 px in back arrow |

## Appendix B — Row classification used above

- **42 overview-only supported rows:** four Button, one Clickable, two Switch,
  three Slider, two Progress, four Date, one Time, four Bars, eight IO,
  eight Permissions, three Share, one Geo, one NAV.
- **6 wrong/insufficient-state rows:** `UI-ALERT-002`, `UI-MENU-002`,
  `UI-ICON-003`, `WEB-002`, `WEB-004`, `WEB-005`.
- **6 in-frame-state rows with caveats:** `UI-ALERT-001`, `UI-SHEET-001`,
  `UI-MENU-001`, `UI-ICON-001`, `WEB-001`, `WEB-003`.
- 42 + 6 + 6 = 54 supported rows. None has a recorded execution.
