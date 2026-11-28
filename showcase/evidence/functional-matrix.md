# Functional verdict matrix

Generated from `showcase/coverage.json`; regenerate with
`python3 showcase/automation/functional_matrix.py`.

| Flow | Coverage rows | Android | iOS |
| --- | --- | --- | --- |
| `buttons` | UI-BUTTON-001 | passed | passed |
| `clickable` | UI-CLICK-001 | passed | failed |
| `switch` | UI-SWITCH-001 | passed | passed |
| `slider` | UI-SLIDER-001 | passed | failed |
| `date-bounds` | UI-DATE-004 | failed, passed | failed |
| `alert-cancel` | UI-ALERT-001 | passed | passed |
| `alert-confirm` | UI-ALERT-001 | passed | passed |
| `alert-text-field` | UI-ALERT-003, UI-ALERT-005 | — | passed |
| `action-sheet` | UI-ALERT-004 | — | passed |
| `sheet` | UI-SHEET-001 | passed | passed |
| `dropdown` | UI-MENU-001 | passed | passed |
| `scaffold-tab` | UI-BAR-001 | passed | passed |
| `topbar` | UI-BAR-002 | passed | passed |
| `navbar` | UI-BAR-003 | passed | passed |
| `toolbar` | UI-BAR-004 | passed | passed |
| `permissions-bulk-deny` | PERM-BULK-001 | passed | passed |
| `webview` | WEB-001, WEB-002, WEB-003, WEB-004, WEB-005 | passed | — |
| `geo-math` | GEO-001 | passed | — |
| `liquidglass` | UI-LIQUID-004 | passed | — |
| `permissions-sms-rows` | PERM-SMS-001 | passed | passed |
| `icons-category` | UI-ICON-004 | passed | passed |
| `sheet-veto` | UI-SHEET-002 | passed | failed |
| `date-display` | UI-DATE-006 | failed | failed |
| `time-24h` | UI-TIME-002 | passed | passed |
| `webview-js` | WEB-006 | failed | failed |
| `nav-restore` | NAV-003 | passed | — |

## Row verdicts without a flow record

These rows carry a passed/failed execution status without a matching
machine-readable flow entry: either a manual assertion in an earlier session
or a result file from before the driver wrote after every flow.

| Row | Platform | Status | Run |
| --- | --- | --- | --- |
| UI-ALERT-006 | ios | failed | 46099392157 |
