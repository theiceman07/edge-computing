# M5: Full chain on the device (4 pts)

**Checklist:** I run camera to dashboard together for 10 minutes and fix what breaks

**Status:** HAVE (one limitation, see below)

## What was run (2026-11-05, Raspberry Pi 5, Logitech Brio 100 USB camera)
`app/server.py --model best.onnx --imgsz 320 --expect bolt=2,nut=2 --map50 0.972` (camera -> ONNX detector -> station logic -> dashboard at http://127.0.0.1:5000), polled every 10 s from `/api/stats` for 591 s (60 samples). Raw samples: `full_chain_10min_samples.csv`.

## Results (measured)
| Item | Value |
|---|---|
| Duration | 591 s, 60 samples, 0 poll errors, detector `running` in every sample |
| Frames processed | 29 -> 4524 |
| Detection FPS | min 6.0, median 7.8, max 9.2 |
| Video FPS | median 7.9 (dashboard label says "locked 15"; the Pi did not reach it under this load) |
| Detector latency | median 44.9 ms, max 182.7 ms |
| Stats `error` field | empty in all samples |
| Temperature | 45.0 -> 52.1 C, `get_throttled` 0x0 throughout (no throttling) |
| Server log | 0 tracebacks |

## What broke / limitations (honest)
- Nothing crashed. The scene was adjusted by hand during the first ~3 minutes (camera framing and parts moved), so object counts changed early in the run; that is setup, not a fault.
- Frame rate is about 7-8 FPS, below the 15 FPS the dashboard is capped at.
- The LED/GPIO output was **disabled for this run** (a stub `gpiozero` that raises ImportError, so `Leds` falls back to no-op) because GPIO 17/27/22 are shared with the L298N motor driver of the motor-fault-monitor rig and driving them could spin the motor. The chain tested here is camera -> detector -> dashboard; the LED actuator was not part of this run.
- Model is the nuts-and-bolts detector (`best.onnx`, test mAP50 0.972 from the Colab run), not the enclosure model.

## Screenshot
`dashboard_during_10min_run_2026-11-05_1137.png` (11:37, about 6 minutes into the run): live dashboard with the camera view and detection boxes (5 bolts, 5 nuts), badge FAIL against the 2 bolt + 2 nut kit, about 7 FPS detection, no errors. Cropped to the dashboard only.
