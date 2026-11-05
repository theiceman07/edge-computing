# M5: Pass/fail station (4 pts)

**Checklist:** I test 20 parts (10 good, 10 defective) and show the confusion matrix and false-pass rate

**Status:** HAVE (23 trays, 12 good / 11 defective; see RESULTS.md for the caveats)

**Evidence:** `station_log.csv` (raw clicks), `RESULTS.md` (confusion matrix, false-pass rate, per-defect table, limitations), `STATION_procedure.md`.
**Result:** 22 of 23 correct, false-pass 0 of 11, false-fail 1 of 12.

## Screenshots (cropped to the dashboard; taken on the Pi, 2026-11-05, Chromium at 127.0.0.1:5000)
- `dashboard_tray1_PASS_2026-11-05_1155.png` (11:55): first tray logged. Kit of 2 bolts + 2 nuts detected, badge PASS ("kit complete"), headline 1 / 1, trays tested 1.
- `dashboard_2_trays_extra_bolt_FAIL_2026-11-05_1157.png` (11:57): 2 trays logged (2 / 2 correct). Current tray shows 3 bolts + 2 nuts, badge FAIL ("extra 1 bolt"), as it should for an extra-bolt tray.
- `dashboard_20_trays_19of20_2026-11-05_1201.png` (12:01): counters after 20 trays: 19 / 20 correct, false-pass 0% (0 of 8 defective), false fails 1 of 12. Three more defective trays were added afterwards; the final result is in `RESULTS.md` (22 of 23, false-pass 0 of 11).
