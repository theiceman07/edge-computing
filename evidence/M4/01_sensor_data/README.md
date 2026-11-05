# M4: Sensor data (3 pts)

**Checklist:** I wire/read the MPU6050 and show labelled normal and fault CSV runs (3 each)

**Status:** PARTIAL (fault runs synthetic, labelled)

**Notes:** Motor monitor not started on the Pi. Lives in motor-fault-monitor/.

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 01b7096)
- [docs/RESULTS_AND_LIMITATIONS.md](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/RESULTS_AND_LIMITATIONS.md): what is real and what is synthetic. Real MPU6050 recordings were made on the Pi (3 motor-running normal runs); raw files are git-ignored.
- [data/synthetic/calibration.json](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/data/synthetic/calibration.json) and the `data/synthetic/` CSVs: normal runs fitted to the real recordings, imbalance runs from an assumed fault model. **Synthetic, not real.**
- [data/synthetic_provided/](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/data/synthetic_provided/mpu6050_20261105_044432_normal_00.csv): supplied synthetic normal, imbalance and loose-mount runs (3 each). **Synthetic, not real.**
- [docs/MENTOR_SUMMARY.md](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/MENTOR_SUMMARY.md): mentor acceptance of labelled synthetic fault data (components unavailable).
