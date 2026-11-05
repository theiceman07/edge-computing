# M3: Debounce (4 pts)

**Checklist:** I show one bad frame does not trigger and N frames in a row do

**Status:** PARTIAL

**Notes:** Unit tests pass (tests/test_leds_debounce.py). Record the live demo with the LEDs.

## Evidence files in this folder
- test_leds_debounce.py

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit f3547da)
- [docs/DECISION_RULES.md](https://github.com/theiceman07/edge-computing/blob/f3547da8c01ce330a1d1792aac484b70331cccd4/docs/DECISION_RULES.md): motor alert only after 3 consecutive anomalous windows.
- [docs/MILESTONE_CHECKLIST.md](https://github.com/theiceman07/edge-computing/blob/f3547da8c01ce330a1d1792aac484b70331cccd4/docs/MILESTONE_CHECKLIST.md): false-alarm table showing debounced alert counts per run.
