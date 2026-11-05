# M5: Live dashboard (4 pts)

**Checklist:** I show live detections, PASS/FAIL view, camera view, 3 KPIs and motor alert

**Status:** PARTIAL (vision dashboard has no motor alert; motor alert is on the motor dashboard)

**Notes:** Detections, PASS/FAIL, camera and KPIs work. Motor alert not integrated.

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Screenshots (2026-11-05, real camera on the Pi)
Live camera view with detection boxes and confidences, PASS/FAIL badge, object counts, headline and false-pass tiles, and FPS/latency are visible in `../03_full_chain/dashboard_during_10min_run_2026-11-05_1137.png` and the three screenshots in `../02_passfail_station/`. Note: this dashboard has no motor alert; the motor monitor has its own dashboard (see the `motor-fault-monitor` branch, emulated-demo video).

## Evidence on the `motor-fault-monitor` branch (pinned commit 802a158)
- [docs/evidence/demo_simulated_dashboard.mp4](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/docs/evidence/demo_simulated_dashboard.mp4): motor dashboard with alert (software-injected test fault, not a real motor fault).
- [docs/evidence/dashboard_smoke_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/docs/evidence/dashboard_smoke_pi_2026-11-05.txt): motor dashboard starts on the Pi, HTTP 200.
