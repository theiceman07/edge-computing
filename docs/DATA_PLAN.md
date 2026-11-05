# Dataset plan (to be recorded on your own motor)

Real data can only come from your rig. Do not substitute downloaded datasets (e.g. CWRU is 12 kHz bearing data; this sensor samples at 50 Hz) or emulator-generated data as evidence.

## Runs to record
| Label | Runs | Duration | Condition |
|---|---|---|---|
| `normal` | 8 (3 train, 5 for false-alarm count) | 60 s | Motor at fixed speed, nothing attached, separate starts, ideally across 2 sessions |
| `imbalance` | 3 | 60 s | Small weight on shaft/fan, guard in place |
| `loose_mount` | 3 (optional) | 60 s | Sensor or motor mount screw loosened one turn |
| `blocked` | 3 (optional) | 30 s | Light brief load/obstruction, only if safe |

Let the motor settle 5 s before starting each run, and keep the sensor orientation, voltage and mounting the same.

## Commands
```bash
for i in 1 2 3 4 5 6 7 8; do python scripts/collect_data.py --mode hardware --sensor mpu6050 --label normal --duration 60; done
python scripts/collect_data.py --mode hardware --sensor mpu6050 --label imbalance --duration 60   # x3
python scripts/train_model.py --input data/raw/*_normal.csv --holdout-runs 1
python scripts/evaluate_model.py --input <held-out normal csv> <fault csvs>
```
Check the achieved rate printed after every run; discard runs where it is far below 50 Hz.

## Record-keeping
Note in a log for each run: date, motor voltage/duty, weight added and where, mount, room temperature. Commit CSVs with `git add -f` on your own branch.
