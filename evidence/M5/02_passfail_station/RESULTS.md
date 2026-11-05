# 20+ tray PASS/FAIL station test: results (2026-11-05, Raspberry Pi 5, Logitech Brio 100)

Kit: `--expect bolt=2,nut=2`. Model: `app/best.onnx` (nuts-and-bolts YOLO11n @320, test mAP50 0.972 from the Colab run). Station confirm 5 frames, station conf 0.5.
Procedure: `docs/STATION.md`. Each tray: parts laid out, verdict stable, then the true class was clicked (Tray is GOOD / DEFECTIVE). Raw log: `station_log.csv` (23 rows).

## Result as logged (23 trays: 12 good, 11 defective)
| | decided PASS | decided FAIL |
|---|---|---|
| truth GOOD | 11 | 1 |
| truth DEFECTIVE | 0 | 11 |

**Headline: 22 of 23 correct (96%). False-pass rate: 0 of 11 defective trays passed (0%). False-fail rate: 1 of 12 good trays failed.**

## Sensitivity: row 20 may be a double click
Rows 19 and 20 were logged 0.8 s apart with identical counts (2 bolts + 2 nuts), which is too fast for two separate trays. Without row 20: 21 of 22 correct (95%), false-pass 0 of 11. The conclusion does not change.

## Defective trays by what the detector saw (all caught)
| What the detector counted | defective trays | decided FAIL |
|---|---|---|
| other (crowded / wrong mix, detector counts 3 bolts 1 nuts) | 2 | 2 |
| missing bolt | 2 | 2 |
| extra nut | 2 | 2 |
| missing nut | 1 | 1 |
| extra bolt | 1 | 1 |
| other (crowded / wrong mix, detector counts 5 bolts 5 nuts) | 1 | 1 |
| other (crowded / wrong mix, detector counts 4 bolts 5 nuts) | 1 | 1 |
| other (crowded / wrong mix, detector counts 4 bolts 4 nuts) | 1 | 1 |

## The one error
Tray 5 was a good tray (2 bolts + 2 nuts) but the detector counted 3 bolts, so the station said FAIL (a false fail, "extra 1 bolt"). A false fail only costs a re-check; the dangerous error (false pass) did not occur in this test.

## Limitations (honest)
- Small sample (23 trays); the 12 good / 11 defective split differs from the sheet's 10 / 10. Trays 21-23 were crowded trays (4-5 bolts and 4-5 nuts), which are easy to flag; the harder cases are single missing/extra parts (trays 2-18).
- A first attempt was discarded and not used: 20 clicks in 12 s with an unchanged scene (5 bolts + 5 nuts every row) was not a valid test.
- Truth was decided by the operator before looking at the verdict, per the procedure; this is a self-run test, not an independent one.
- Model and parts are the nuts-and-bolts kit, not the printed enclosure; the detector ran at about 7-8 FPS with the LED/GPIO output disabled (pins shared with the motor driver).
