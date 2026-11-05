# M3: Decision rule sheet (3 pts)

**Checklist:** I write the input, threshold, action and safe state if the camera fails

**Status:** PARTIAL

**Notes:** Sheet filled with the real values (conf 0.40, LED debounce N=2, station confirm 5). Camera-unplug test and latency figures are still blank on purpose.

## Evidence files in this folder
- M3_decision_rule_sheet.md

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 01b7096)
- [docs/DECISION_RULES.md](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/DECISION_RULES.md): motor-monitor decision rules (input, threshold, debounce 3 windows, action, safe state on sensor failure).
