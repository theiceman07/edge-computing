# M3: Two-stream pipeline (4 pts)

**Checklist:** I run two streams at once and show FPS per stream

**Status:** PARTIAL (two streams measured at once on my own laptop with recorded rig frames; not on the Pi)

**Notes:** Pi access had ended, so this was run on my laptop (Apple M5, macOS, onnxruntime CPU). The frames are real photos recorded on the rig (`app/mydata_enc`), read from disk and looped; no live camera was attached during this run. Numbers are not Pi numbers.

## What runs
`two_stream.py` starts two threads at the same time, each with its own ONNX Runtime session (2 threads each) and its own frame source:

- **Stream A:** `app/enclosure.onnx` (FP32) on `enclosure_good` + `empty` frames (107 files)
- **Stream B:** `app/enclosure_int8.onnx` (INT8) on `enclosure_defective` frames (77 files)

Each stream is first run alone for 60 s (baseline), then both run together for 60 s, logging frames per second for each stream.

## Result (2026-11-05, 60 s per run)
| Stream | Alone FPS | Both at once FPS |
|---|---|---|
| A (FP32) | 38.7 | 28.3 |
| B (INT8) | 45.4 | 35.0 |

Combined throughput with both streams: 63.4 FPS. Each stream slows by about a quarter when they share the CPU.

## Evidence files in this folder
- `summary.txt`: hardware, runtime, settings and the table above (written by the script).
- `fps_per_second.csv`: FPS for each stream, every second of the two-stream run (60 rows per stream).
- `two_stream_frame.png`: last frame of each stream with detections and the live FPS overlay.
- `two_stream.py`: the script. Re-run with `python two_stream.py --seconds 60` (needs onnxruntime, opencv-python, numpy).

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.
