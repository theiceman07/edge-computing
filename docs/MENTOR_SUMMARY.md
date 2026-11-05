# Motor Health Monitor: summary for the mentor (2026-11-05)

Raspberry Pi 5 + MPU6050 vibration monitor: 1 s window features -> Isolation Forest -> debounced alert (3 windows) -> dashboard, MQTT (TLS+password), GPIO alert signal, Modbus tag.

## Real, measured on the Pi (evidence files in `docs/evidence/`)
- Secure MQTT self-test 6/6; bridge -> broker -> subscriber 120/120 messages.
- OTA install / invalid-artifact rejection / rollback; drift report.
- Docker image (dashboard healthy 3.6 s after start; 37 tests pass inside).
- Alert gateway: GPIO23 + Modbus tag followed the alert on 21/21 transitions; decision-to-output latency median 4.1 ms, p95 6.2 ms (replayed windows).
- systemd service: starts itself after reboot (14 s), restarts after `kill -9` (4.6 s).
- 37 unit tests pass.

## Not real, and labelled as such
- No real fault recordings exist: the rig lost access to components. The only real motor-running data is 3 normal runs with a loosely mounted sensor.
- `data/synthetic/` (parameters fitted to the real normal runs; imbalance is an assumed 2x amplitude model) and `data/synthetic_provided/` (supplied artificial set, not recorded) demonstrate the pipeline only. Every file/run id says synthetic; `docs/RESULTS_AND_LIMITATIONS.md` has the numbers.
- The demo video (`demo_simulated_dashboard.mp4`) is the dashboard in emulator (`SIMULATION`) mode with a software-injected test fault, with a "SIMULATED DEMO" banner on every frame.
- The MQTT topics, actuator and latency checks used windows replayed from recorded/generated data; no relay or PLC was attached.

## Agreed with the mentor (reported by the student, 2026-11-05)
Labelled computer-generated fault data is accepted in place of real fault recordings (components unavailable). It remains labelled as generated (not recorded); written confirmation to be attached.

## Honest result
No fault detection has been validated on the real motor. The model trained on real normal data flags every normal run from later sessions (false-alarm count in `docs/MILESTONE_CHECKLIST.md`), so it is not session-robust. Fix: rigid sensor mount, then >=3 normal and >=3 fault real runs, retrain, evaluate on separate runs.

## Where to look
`docs/MILESTONE_CHECKLIST.md` (every sheet criterion with status and evidence), `docs/RESULTS_AND_LIMITATIONS.md`, `docs/DATASHEET.md`, `docs/ARCHITECTURE.md`, `docs/DECISION_RULES.md`.
