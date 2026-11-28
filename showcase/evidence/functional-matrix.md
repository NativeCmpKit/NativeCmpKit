# Functional verdict matrix

Generated from `showcase/coverage.json`; regenerate with
`python3 showcase/automation/functional_matrix.py`.

| Flow | Coverage rows | Android | iOS |
| --- | --- | --- | --- |
| `buttons` | UI-BUTTON-001 | — | passed |
| `clickable` | UI-CLICK-001 | — | failed |
| `switch` | UI-SWITCH-001 | — | passed |
| `slider` | UI-SLIDER-001 | — | failed |
| `date-bounds` | UI-DATE-004 | failed | failed |
| `alert-cancel` | UI-ALERT-001 | — | passed |
| `alert-confirm` | UI-ALERT-001 | — | passed |
| `alert-text-field` | UI-ALERT-003, UI-ALERT-005 | — | passed |
| `action-sheet` | UI-ALERT-004 | — | passed |
| `sheet` | UI-SHEET-001 | — | passed |
| `dropdown` | UI-MENU-001 | passed | passed |
| `scaffold-tab` | UI-BAR-001 | passed | passed |
| `topbar` | UI-BAR-002 | — | passed |
| `navbar` | UI-BAR-003 | — | passed |
| `toolbar` | UI-BAR-004 | — | passed |
| `permissions-bulk-deny` | PERM-BULK-001 | — | passed |
| `permissions-sms-rows` | PERM-SMS-001 | passed | passed |
| `icons-category` | UI-ICON-004 | — | passed |
| `sheet-veto` | UI-SHEET-002 | — | failed |
| `date-display` | UI-DATE-006 | — | failed |
| `time-24h` | UI-TIME-002 | — | passed |
| `webview-js` | WEB-006 | — | failed |

## Row verdicts without a flow record

These rows carry a passed/failed execution status without a matching
machine-readable flow entry: either a manual assertion in an earlier session
or a result file from before the driver wrote after every flow.

| Row | Platform | Status | Run |
| --- | --- | --- | --- |
| UI-BUTTON-001 | android | passed | 45957524569 |
