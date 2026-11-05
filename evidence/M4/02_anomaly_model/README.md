# M4: Anomaly model (4 pts)

**Checklist:** I train on normal data only and show the live alert when I inject the fault

**Status:** PARTIAL (alert shown on synthetic/simulated fault only)

**Notes:** Needs real data.

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 01b7096)
- [src/motor_fault/train.py](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/src/motor_fault/train.py): Isolation Forest trained on normal data only.
- [docs/RESULTS_AND_LIMITATIONS.md](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/RESULTS_AND_LIMITATIONS.md): results on real and synthetic data, including the honest negative result.
- [docs/evidence/demo_simulated_dashboard.mp4](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/evidence/demo_simulated_dashboard.mp4): dashboard alert when a SIMULATED fault is injected (banner on every frame).
