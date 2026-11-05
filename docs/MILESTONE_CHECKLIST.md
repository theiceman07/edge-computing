# Motor fault monitor vs the assessment sheet (M3 / M4 / M5), status 2026-11-05

Status key: DONE = evidence in repo, measured here; PARTIAL; NOT DONE. "Synthetic" data is not real evidence (see RESULTS_AND_LIMITATIONS.md).
Sheet criteria are shared with the edge-vision project; items that belong to the vision project are marked n/a.

## M3 Decide and Act
| Criterion | Status | Evidence / gap |
|---|---|---|
| Decision rule sheet | DONE | `docs/DECISION_RULES.md`. |
| Two-stream pipeline | n/a | Vision project. |
| Debounce | DONE (code) | 3 consecutive anomalous windows; counted in the false-alarm table below. |
| Actuator fires | PARTIAL | `scripts/alert_gateway.py` drives GPIO23 (active-high alert/stop signal) on a debounced alert; pin level read back for 21/21 transitions (`gateway_actuator_plc_latency_pi_2026-11-05.txt`). No relay/LED physically attached; replayed real windows, not a live fault. |
| Docker | DONE (dashboard) | `Dockerfile`; built on the Pi, cold start to healthy dashboard in 3.6 s, 37 tests pass inside (`docker_coldstart_pi_2026-11-05.txt`). Actuator/sensor not inside the container (no GPIO/I2C passthrough configured). |
| End-to-end latency (20+ events) | PARTIAL | Decision-to-output: median 4.1 ms, p95 6.2 ms, max 12.7 ms over 21 alert transitions (replay). Sensor-to-window time (1 s window) not included. |

## M4 Monitor and Connect
| Criterion | Status | Evidence / gap |
|---|---|---|
| Sensor data (MPU6050, labelled normal + fault CSVs, 3 each) | PARTIAL | Real normal CSVs exist. Real fault: 1 run with no vibration signal (tilt only). Synthetic fault runs exist but are not real. |
| Anomaly model (train on normal, show alert when fault injected) | PARTIAL | Pipeline works; alert on injected fault only demonstrated in simulation/synthetic. No real fault detection. |
| False alarms over 5 normal runs, explain threshold | DONE (result is poor) | Table below. Threshold: IsolationForest contamination=auto, debounce 3 windows. |
| Secure MQTT (refuses no-password, works with password + TLS) | DONE | `docs/evidence/mqtt_selftest_pi_2026-11-05.txt`, 6/6 PASS on this Pi. |
| Topics (publish detection and motor score, show on subscriber) | PARTIAL | `mqtt_bridge.py` publishes `factory/motor/score`; PC end-to-end evidence from 2026-10-23; not re-run on the Pi. |
| PLC link (tag changes on detection) | PARTIAL | Modbus TCP server (`src/motor_fault/gateway.py`, holding register 0 = alert) read back by a software client on every transition. No physical PLC tested. |
| Threat model | DONE | `docs/M4_threat_model.md` (mitigations applied: TLS, password file). |
| Reliability (drift report, OTA v1->v2 with rollback, auto-restart after crash) | PARTIAL | Drift report and OTA/rollback done on the Pi (evidence files). Auto-restart not done: the service file is fixed but not installed (needs sudo). |

### False alarms on real normal runs (model model_20261104T094656761800Z, debounce 3)
| Run (UTC) | Windows | Flagged | Alerts |
|---|---|---|---|
| 11-04 07:35 (held out, same session as training) | 120 | 5 (4%) | 0 |
| 11-04 10:07, 10:10, 10:13, 10:36, 10:42, 10:44, 10:47 | 111-125 each | 100% each | 1 each |
| 11-05 03:32, 03:33, 03:34 (motor spinning) | 51-58 each | 100% each | 1 each |

Only the same-session run passes. Every later session is flagged in full. The model does not generalise across sessions/sensor placement; it needs retraining on a rigidly mounted sensor with normal runs from several sessions.

## M5 Complete System + Dashboard
| Criterion | Status | Evidence / gap |
|---|---|---|
| Inspection rig, pass/fail station, headline metric | n/a / NOT DONE | Vision-project items. |
| Full chain on the device for 10 min | NOT DONE | Not run. |
| Live dashboard (live detections, 3 KPIs, motor alert) | PARTIAL | Starts, HTTP 200 (`dashboard_smoke_pi_2026-11-05.txt`); live view with real hardware not checked. |
| Product readiness (auto-start after power cycle, offline, logs) | NOT DONE | Service file ready, not installed. |
| Documents (README, architecture diagram) | PARTIAL | README, ARCHITECTURE.md (diagram), DATASHEET.md, DECISION_RULES.md written; no demo video. |
| Live demo (normal + injected fault) | NOT DONE | No real fault injection achieved. |

## What I could not do
- Install the service (no sudo): `ln -sfn "/home/juice/edge computing/motor-fault-monitor" /home/juice/motor-fault-monitor (already done on this Pi); sudo cp deploy/motor-monitor.service /etc/systemd/system/ && sudo systemctl enable --now motor-monitor`, then `sudo reboot`; for the crash test, `sudo systemctl kill -s KILL motor-monitor` and confirm it restarts.
- Anything needing a working imbalance fault on the rig.
