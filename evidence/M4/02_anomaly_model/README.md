# M4: Anomaly model (4 pts)

**Checklist:** I train on normal data only and show the live alert when I inject the fault

**Status:** PARTIAL (alert shown only on a software-injected test fault, not a real motor fault)

**Notes:** Needs real data.

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 802a158)
- [src/motor_fault/train.py](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/src/motor_fault/train.py): Isolation Forest trained on normal data only.
- [docs/RESULTS_AND_LIMITATIONS.md](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/docs/RESULTS_AND_LIMITATIONS.md): results on real and generated (non-recorded) data, including the honest negative result.
- [docs/evidence/demo_simulated_dashboard.mp4](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/docs/evidence/demo_simulated_dashboard.mp4): dashboard alert when an artificial test fault is injected in software (a demo banner is on every frame).
