# Evidence index (one folder per checklist item, under evidence/)

**Team submission:** Malligaarjunan A V K, Manoj M, Poornaa Shree Praveenraj, Sanadhani S Iyer, Tejaswi K (team submission approved, as reported by the team).

**How to read this:** every row links to one folder. Its `README.md` says what was done, the status, and links every proof file, including proof that lives on the `motor-fault-monitor` branch (pinned to a commit, so it cannot change after submission). Vision items (M1, M2, M5 station) are on this branch; motor-monitor items (most of M3 actuator/Docker/latency, M4, M5 readiness) are on `motor-fault-monitor`. Generated or emulated data (not recorded from the real motor) is labelled as such everywhere.

Status: HAVE = evidence exists, PARTIAL = some evidence, IN PROGRESS = being worked on, TODO = not started.

| Milestone | Item | Pts | Status | Folder |
|---|---|---|---|---|
| M1 | Camera and repo | 2 | HAVE | [01_camera_and_repo](evidence/M1/01_camera_and_repo) |
| M1 | OpenCV pipeline | 4 | HAVE | [02_opencv_pipeline](evidence/M1/02_opencv_pipeline) |
| M1 | Baseline speed | 3 | HAVE | [03_baseline_speed](evidence/M1/03_baseline_speed) |
| M1 | Dataset v1 | 4 | HAVE | [04_dataset_v1](evidence/M1/04_dataset_v1) |
| M1 | Correct split | 2 | HAVE (split_counts.md: 111/31/16, 0 identical and 0 near-duplicate part photos across splits) | [05_correct_split](evidence/M1/05_correct_split) |
| M1 | Train and run detector | 5 | HAVE (enclosure trained, results and 10 wrong detections written up; numbers weak and no numeric target recorded, see RESULTS.md) | [06_train_and_run_detector](evidence/M1/06_train_and_run_detector) |
| M2 | Export to ONNX | 3 | HAVE | [01_export_onnx](evidence/M2/01_export_onnx) |
| M2 | Convert and run live | 4 | HAVE | [02_convert_and_run_live](evidence/M2/02_convert_and_run_live) |
| M2 | Accuracy check | 4 | HAVE | [03_accuracy_check](evidence/M2/03_accuracy_check) |
| M2 | Fair benchmark | 4 | HAVE | [04_fair_benchmark](evidence/M2/04_fair_benchmark) |
| M2 | CPU vs accelerator + stack | 2 | HAVE | [05_cpu_vs_accelerator](evidence/M2/05_cpu_vs_accelerator) |
| M2 | Own target and trade-off | 3 | HAVE | [06_own_target_tradeoff](evidence/M2/06_own_target_tradeoff) |
| M3 | Decision rule sheet | 3 | PARTIAL | [01_decision_rule_sheet](evidence/M3/01_decision_rule_sheet) |
| M3 | Two-stream pipeline | 4 | PARTIAL (two streams at once, FPS per stream; measured on own laptop with recorded rig frames, not on the Pi) | [02_two_stream_pipeline](evidence/M3/02_two_stream_pipeline) |
| M3 | Debounce | 4 | PARTIAL | [03_debounce](evidence/M3/03_debounce) |
| M3 | Actuator fires | 3 | PARTIAL | [04_actuator_fires](evidence/M3/04_actuator_fires) |
| M3 | Docker | 4 | PARTIAL | [05_docker](evidence/M3/05_docker) |
| M3 | End-to-end latency | 2 | PARTIAL | [06_end_to_end_latency](evidence/M3/06_end_to_end_latency) |
| M4 | Sensor data | 3 | PARTIAL (fault runs computer-generated, not recorded; labelled) | [01_sensor_data](evidence/M4/01_sensor_data) |
| M4 | Anomaly model | 4 | PARTIAL (alert shown only on a software-injected test fault, not a real motor fault) | [02_anomaly_model](evidence/M4/02_anomaly_model) |
| M4 | False alarms | 2 | HAVE (result is poor, reported as measured) | [03_false_alarms](evidence/M4/03_false_alarms) |
| M4 | Secure MQTT | 3 | HAVE | [04_secure_mqtt](evidence/M4/04_secure_mqtt) |
| M4 | Topics | 2 | HAVE (transport real, input windows generated, not recorded) | [05_topics](evidence/M4/05_topics) |
| M4 | PLC link | 2 | PARTIAL (software Modbus client, no physical PLC) | [06_plc_link](evidence/M4/06_plc_link) |
| M4 | Threat model | 1 | HAVE | [07_threat_model](evidence/M4/07_threat_model) |
| M4 | Reliability | 3 | HAVE | [08_reliability](evidence/M4/08_reliability) |
| M5 | Inspection rig | 2 | PARTIAL | [01_inspection_rig](evidence/M5/01_inspection_rig) |
| M5 | Pass/fail station | 4 | HAVE (23 trays, 12 good / 11 defective; see RESULTS.md for the caveats) | [02_passfail_station](evidence/M5/02_passfail_station) |
| M5 | Full chain on the device | 4 | HAVE (one limitation, see below) | [03_full_chain](evidence/M5/03_full_chain) |
| M5 | Live dashboard | 4 | PARTIAL (vision dashboard has no motor alert; motor alert is on the motor dashboard) | [04_live_dashboard](evidence/M5/04_live_dashboard) |
| M5 | Product readiness | 2 | PARTIAL (motor monitor done; vision service untested) | [05_product_readiness](evidence/M5/05_product_readiness) |
| M5 | Headline metric | 2 | HAVE | [06_headline_metric](evidence/M5/06_headline_metric) |
| M5 | Documents | 1 | PARTIAL | [07_documents](evidence/M5/07_documents) |
| M5 | Live demo and questions | 1 | PARTIAL (emulated demo only, no real motor fault) | [08_live_demo](evidence/M5/08_live_demo) |

Total points on the checklist: 100.

## Order of work (from the assessment sheet)
1. Finish **M3** first, because it gates M5 (decision rule sheet, debounce video, LED actuator video, Docker cold boot, latency.csv, two streams).
2. Do the **M1 and M2 Pi measurements** (baseline speed done; benchmark for the enclosure model, INT8 run live on the Pi, CPU vs accelerator table + stack diagram).
3. Collect **M4** sensor runs (in the `motor-fault-monitor` repo, `evidence/M4/`), then **M5** (20-part station test, 10-minute full chain, headline metric).
4. After each milestone: commit to branch `arjun` with the milestone in the message, update this file, and paste the permalinks into the sheet.

## Notes
- Raw output of `tools/pi_measure.sh` is in `evidence/pi_<timestamp>/`; copies are inside the item folders.
- The enclosure is the new IDRP part; nuts-and-bolts results are kept as the earlier baseline and are labelled as such.
- Videos (mp4) must be recorded with a phone or screen recorder; they are not created by the scripts.

## Status at 2026-11-05 (supersedes the 2026-11-02 section below)
- M1: camera/repo, OpenCV pipeline, baseline speed, dataset v1 (158 own labelled enclosure photos + data card), group-aware 70/20/10 split (0 leaks) and the enclosure detector write-up (RESULTS.md, 10 wrong detections, confusion matrices) all have evidence. The detector numbers are weak (test mAP50 0.416 on 16 images) and no numeric target was written down; this is reported as it is.
- M2: all six items have evidence (ONNX export, INT8 via onnxruntime run live, FP32 vs INT8 accuracy, 280-run benchmark, CPU vs accelerator table with no accelerator fitted, target committed before measuring). Note: INT8 was done with onnxruntime, not TFLite/TensorRT.
- M5: 10-minute camera -> detector -> dashboard run (`evidence/M5/03_full_chain`, 0 errors, no throttling), 23-tray PASS/FAIL test (`02_passfail_station`: 22 of 23 correct, false-pass 0 of 11) and headline metric, with cropped dashboard screenshots. LED output was disabled during these runs (GPIO pins are shared with the motor driver). A first invalid station attempt (20 clicks in 12 s, unchanged scene) was discarded.
- M3, M4, rest of M5: unchanged here. The motor-monitor evidence for M3/M4/M5 is on the `motor-fault-monitor` branch of this GitHub repo (`docs/MILESTONE_CHECKLIST.md`).
- Pushed to https://github.com/theiceman07/edge-computing (branch `edge-vision`).

## Status at end of 2026-11-02
- Committed on branch `arjun` but NOT yet pushed (no GitHub credentials on the Pi; run `git push origin arjun` and enter a token).
- Detector for the enclosure: not trained yet. Plan for 2026-11-03: Colab T4, `training/train_enclosure_colab.ipynb` + `training/enclosure_dataset.zip`, then export ONNX, benchmark on the Pi, wrong-detections write-up.
- Raw photos (`app/mydata_enc/`, `app/mydata_enc_hands/`) are local only, not in git; the labelled dataset is in `evidence/M1/04_dataset_v1/dataset/`.
