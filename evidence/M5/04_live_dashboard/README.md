# M5: Live dashboard (4 pts)

**Checklist:** I show live detections, PASS/FAIL view, camera view, 3 KPIs and motor alert

**Status:** PARTIAL (vision dashboard has no motor alert; motor alert is on the motor dashboard)

**Notes:** Detections, PASS/FAIL, camera and KPIs work. Motor alert not integrated.

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Screenshots (2026-11-05, real camera on the Pi)
Live camera view with detection boxes and confidences, PASS/FAIL badge, object counts, headline and false-pass tiles, and FPS/latency are visible in `../03_full_chain/dashboard_during_10min_run_2026-11-05_1137.png` and the three screenshots in `../02_passfail_station/`. Note: this dashboard has no motor alert; the motor monitor has its own dashboard (see the `motor-fault-monitor` branch, simulated-demo video).

## Evidence on the `motor-fault-monitor` branch (pinned commit 01b7096)
- [docs/evidence/demo_simulated_dashboard.mp4](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/evidence/demo_simulated_dashboard.mp4): motor dashboard with alert (SIMULATED fault).
- [docs/evidence/dashboard_smoke_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/evidence/dashboard_smoke_pi_2026-11-05.txt): motor dashboard starts on the Pi, HTTP 200.
