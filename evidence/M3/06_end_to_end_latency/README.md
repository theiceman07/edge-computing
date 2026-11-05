# M3: End-to-end latency (2 pts)

**Checklist:** I measure frame-to-actuator latency over 20+ events

**Status:** PARTIAL

**Notes:** PARTIAL measurement only. Per-frame camera-to-actuator-COMMAND latency over a 120 s live run (1469 frames): median 97.0 ms, p95 118.7 ms, max 360.2 ms (INT8 model, Pi 5, USB camera 640x480). The actuator was a software stub (no LED driven), and the camera saw no enclosure, so there were 0 real events. The required 20+ physical events (part placed -> LED lights, ideally with a timestamped photo or scope) are NOT done.

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 802a158)
- [docs/evidence/gateway_actuator_plc_latency_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/docs/evidence/gateway_actuator_plc_latency_pi_2026-11-05.txt): decision-to-output latency over 21 alert transitions, median 4.1 ms, p95 6.2 ms, max 12.7 ms (replayed windows; 1 s sensor window not included).
