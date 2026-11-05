"""M3 two-stream pipeline: run two detector streams at once and report FPS per stream.

Each stream runs in its own thread with its own ONNX Runtime session and its own frame source.
Frame sources are recorded camera frames from app/mydata_enc (real photos taken on the rig),
read from disk and looped; there is no live camera in this run.

  stream A: app/enclosure.onnx (FP32)      on enclosure_good + empty frames
  stream B: app/enclosure_int8.onnx (INT8) on enclosure_defective frames

Usage: python two_stream.py [--seconds 60] [--threads 2] [--out .]
Writes fps_per_second.csv, summary.txt and two_stream_frame.png into --out.
"""
import argparse
import csv
import glob
import os
import platform
import threading
import time
from datetime import datetime, timezone

import cv2
import numpy as np
import onnxruntime as ort

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
APP = os.path.join(ROOT, "app")
NAMES = {0: "enclosure_good", 1: "enclosure_defective"}
IMGSZ = 480
CONF = 0.5


def letterbox(img, size=IMGSZ):
    h, w = img.shape[:2]
    r = min(size / h, size / w)
    nh, nw = int(round(h * r)), int(round(w * r))
    canvas = np.full((size, size, 3), 114, dtype=np.uint8)
    top, left = (size - nh) // 2, (size - nw) // 2
    canvas[top:top + nh, left:left + nw] = cv2.resize(img, (nw, nh))
    x = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    return x.transpose(2, 0, 1)[None], r, left, top


def postprocess(out, r, left, top):
    p = out[0][0].T  # (4725, 6): cx, cy, w, h, score_good, score_defective
    scores = p[:, 4:]
    cls = scores.argmax(1)
    conf = scores.max(1)
    keep = conf > CONF
    if not keep.any():
        return []
    b, c, s = p[keep, :4], cls[keep], conf[keep]
    boxes = np.stack([(b[:, 0] - b[:, 2] / 2 - left) / r, (b[:, 1] - b[:, 3] / 2 - top) / r, b[:, 2] / r, b[:, 3] / r], 1)
    idx = cv2.dnn.NMSBoxes(boxes.tolist(), s.tolist(), CONF, 0.45)
    return [(boxes[i], int(c[i]), float(s[i])) for i in np.array(idx).flatten()]


class Stream(threading.Thread):
    def __init__(self, name, model, frames, threads, stop):
        super().__init__(daemon=True)
        so = ort.SessionOptions()
        so.intra_op_num_threads = threads
        self.name_, self.model = name, os.path.basename(model)
        self.sess = ort.InferenceSession(model, so, providers=["CPUExecutionProvider"])
        self.inp = self.sess.get_inputs()[0].name
        self.frames, self.stop = frames, stop
        self.count, self.detections, self.class_counts = 0, 0, {v: 0 for v in NAMES.values()}
        self.last = None
        self.lock = threading.Lock()

    def run(self):
        i = 0
        while not self.stop.is_set():
            img = cv2.imread(self.frames[i % len(self.frames)])
            i += 1
            x, r, left, top = letterbox(img)
            dets = postprocess(self.sess.run(None, {self.inp: x}), r, left, top)
            with self.lock:
                self.count += 1
                self.detections += len(dets)
                for _, c, _ in dets:
                    self.class_counts[NAMES[c]] += 1
                self.last = (img, dets)


def run(streams, seconds, writer=None):
    stop = threading.Event()
    for s in streams:
        s.stop = stop
        s.start()
    prev = {s.name_: 0 for s in streams}
    t0 = time.perf_counter()
    for sec in range(1, seconds + 1):
        time.sleep(max(0.0, t0 + sec - time.perf_counter()))
        for s in streams:
            with s.lock:
                c = s.count
            if writer:
                writer.writerow([sec, s.name_, c, c - prev[s.name_]])
            prev[s.name_] = c
    elapsed = time.perf_counter() - t0
    stop.set()
    for s in streams:
        s.join()
    return elapsed


def draw(img, dets, title):
    img = img.copy()
    for (x, y, w, h), c, s in dets:
        col = (0, 200, 0) if c == 0 else (0, 0, 230)
        cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), col, 2)
        cv2.putText(img, f"{NAMES[c]} {s:.2f}", (int(x), max(12, int(y) - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 1)
    img = cv2.resize(img, (640, int(img.shape[0] * 640 / img.shape[1])))
    cv2.rectangle(img, (0, 0), (640, 26), (20, 20, 20), -1)
    cv2.putText(img, title, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=int, default=60)
    ap.add_argument("--threads", type=int, default=2, help="intra-op threads per ONNX session")
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    a = ap.parse_args()

    good = sorted(glob.glob(os.path.join(APP, "mydata_enc", "enclosure_good", "*.jpg")))
    empty = sorted(glob.glob(os.path.join(APP, "mydata_enc", "empty", "*.jpg")))
    bad = sorted(glob.glob(os.path.join(APP, "mydata_enc", "enclosure_defective", "*.jpg")))
    fp32, int8 = os.path.join(APP, "enclosure.onnx"), os.path.join(APP, "enclosure_int8.onnx")

    started = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # Baselines: each stream alone, same duration.
    single = {}
    for name, model, frames in [("A", fp32, good + empty), ("B", int8, bad)]:
        s = Stream(name, model, frames, a.threads, None)
        el = run([s], a.seconds)
        single[name] = s.count / el

    # Two streams at once.
    with open(os.path.join(a.out, "fps_per_second.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_s", "stream", "frames_total", "fps"])
        A = Stream("A", fp32, good + empty, a.threads, None)
        B = Stream("B", int8, bad, a.threads, None)
        elapsed = run([A, B], a.seconds, w)

    fa, fb = A.count / elapsed, B.count / elapsed
    panel = np.vstack([
        draw(*A.last, f"Stream A  {A.model}  {fa:.1f} FPS (both running)"),
        draw(*B.last, f"Stream B  {B.model}  {fb:.1f} FPS (both running)"),
    ])
    cv2.imwrite(os.path.join(a.out, "two_stream_frame.png"), panel)

    cpu = os.popen("sysctl -n machdep.cpu.brand_string 2>/dev/null").read().strip() or platform.processor()
    lines = [
        "M3 two-stream pipeline run",
        f"Started (UTC): {started}",
        f"Hardware: {platform.system()} {platform.release()} | {platform.machine()} | {cpu} | {os.cpu_count()} cores",
        "NOTE: run on the student's laptop, NOT the Raspberry Pi (Pi access ended).",
        f"Runtime: onnxruntime {ort.__version__} CPUExecutionProvider, {a.threads} intra-op threads per session, OpenCV {cv2.__version__}",
        "Input: recorded camera frames from app/mydata_enc (real rig photos), read from disk and looped; no live camera.",
        f"Duration: {a.seconds} s per run",
        "",
        "| Stream | Model | Frames source | Alone FPS | Both at once FPS | Frames (both) | Detections (both) |",
        "|---|---|---|---|---|---|---|",
        f"| A | enclosure.onnx (FP32) | enclosure_good + empty ({len(good) + len(empty)} files) | {single['A']:.1f} | {fa:.1f} | {A.count} | {A.detections} {A.class_counts} |",
        f"| B | enclosure_int8.onnx (INT8) | enclosure_defective ({len(bad)} files) | {single['B']:.1f} | {fb:.1f} | {B.count} | {B.detections} {B.class_counts} |",
        "",
        f"Combined throughput with both streams: {fa + fb:.1f} FPS",
        "Per-second FPS for the two-stream run: fps_per_second.csv. Last frame of each stream: two_stream_frame.png.",
    ]
    with open(os.path.join(a.out, "summary.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
