# Android functional UI run — 2026-11-27

- Workflow run: [45993784178](https://github.com/NativeCmpKit/NativeCmpKit/actions/runs/45993784178)
- Job: `140487958128` (`android`), conclusion `success` (session ended normally)
- Revision: `e751b57f06fc7ee4a76bbc5f2c30fbcbb874fdb3`
- Device: Pixel 6 AVD, API 35, 1080×2400 @ 420 dpi (`api35-phone`)
- APK: `:sample:android:assembleDebug` from the same revision
- Driver: `showcase/automation/functional.py` over the pinned `ui-test-actions`
  client `0c818c5d72e8c30c59bd1287c330a40392bf8e89`

## Full-suite result

Command (inside the live session):

```sh
python3 -u showcase/automation/functional.py \
  --client-dir ui-test-actions \
  --connection connection.json --token-file showcase-token \
  --platform android --device api35-phone
```

Summary at 12:44 UTC: **17 passed, 6 failed, 5 blocked** (28 flows attempted).

### Passed (observable state asserted)

`buttons`, `clickable` (single and long press), `switch`, `slider`,
`alert-cancel`, `alert-confirm`, `time-24h`, `permissions-bulk-deny`
(two OS dialogs denied, final state `All permissions granted: false`),
`sheet`, `topbar`, `toolbar`, `navbar`, `icons-category`, `geo-math`,
`limitations`, `liquidglass` (Android fallback state), `webview`
(second page, JS title, cookie `kira=1`, cleared, one error).

Each flow restarted the app, opened its screen through the Home index,
acted on the real control, and asserted the resulting text/state. Before/after
PNGs are under `screenshots/android/functional/<flow>/`.

### Failed in that pass, and diagnosis

| Flow | Error | Diagnosis |
| --- | --- | --- |
| `dropdown` | missing `Duplicate` | Flow clicked the top-bar menu; the duplicate `More options` label resolved to the simple menu (which has Copy/Share/Delete). Later passed after retargeting. |
| `alert-text-field` | no `Show Text Field Dialog` | The whole section is inside `if (currentPlatform.isIOS)`. Not an Android feature. |
| `action-sheet` | no `Show ActionSheet` | Same iOS-only section. |
| `date-bounds` | `HTTP 408` | Transport timeout mid-flow; not retested before the session closed. |
| `scaffold-tab` | no `Profile` | The sample tabs are Home/Favorites/Settings. Later passed after retargeting. |
| `permissions-sms-rows` | missing `SendSms` | Row below the fold. Later passed with scroll-aware assertion. |

### Follow-up runs on the same session

- `scaffold-tab`, `permissions-sms-rows`: **passed** (12:52 UTC).
- `dropdown`: **passed** (12:55 UTC) against the simple menu (`Copy` → `Copied!`).
- `date-bounds`: `HTTP 530` — the tunnel closed as the 60-minute session ended;
  no verdict, must be re-run.

## Counts that must not be promoted

- This is one Android phone configuration. It says nothing about iPad, Android
  tablet, iPhone, desktop, JS/Wasm or native pickers.
- `permission-camera`, `file-picker`, `file-saver`, `share`, `camera` were
  **blocked**, not passed: the OS dialogs were not driven.
- Android double-click is not drivable: two `input tap` processes exceed
  Compose's ~300 ms double-tap window, so the flow asserts single and long press
  only. iOS drives `--count 2`.
- Screenshots alone are not part of this verdict; the assertions are.

## Follow-up needed

1. Re-run the full suite on the next Android session (merges by flow id, so only
   the missing flows are replaced) and record with `record_functional.py`.
2. iOS phone session for the iOS-only `alert-text-field` and `action-sheet`
   flows, plus `date-bounds`, `dropdown` (UIMenu) and `topbar` Add.
3. Android tablet (1600×2560) and iPad sessions.
