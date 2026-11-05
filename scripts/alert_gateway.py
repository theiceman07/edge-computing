#!/usr/bin/env python3
"""Replay recorded windows through model + debounced alert; drive GPIO alert pin and Modbus tags.

Usage: python scripts/alert_gateway.py --replay data/raw/<a>.csv [more.csv ...] [--pin 23] [--port 1502]
Each CSV is scored window by window, in order, as if live. Prints one line per alert transition
with the decision->output latency (time from the alert decision to the GPIO pin read back AND the
Modbus tag read back). This measures the software decision-to-output path only (not sensor->window).
"""
import _bootstrap  # noqa: F401
import argparse
import statistics
import subprocess
import sys
import time
from pathlib import Path

from motor_fault.alerts import AlertPolicy
from motor_fault.config import MODEL_DIR, load_config
from motor_fault.features import FEATURE_NAMES
from motor_fault.gateway import AlertOutput, ModbusServer, TagTable, modbus_read
from motor_fault.inference import AnomalyDetector, find_latest_model, load_model
from motor_fault.train import load_features


def pin_is_high(pin: int) -> bool:
    return " hi " in subprocess.run(["pinctrl", "get", str(pin)], capture_output=True, text=True).stdout


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--replay", nargs="+", type=Path, required=True)
    ap.add_argument("--model", type=Path, default=None)
    ap.add_argument("--pin", type=int, default=23)
    ap.add_argument("--port", type=int, default=1502)
    ap.add_argument("--no-gpio", action="store_true")
    a = ap.parse_args()
    model = load_model(a.model or find_latest_model(MODEL_DIR))
    cfg = load_config(window_seconds=model.window_seconds, sample_rate_hz=model.sample_rate_hz)
    det, pol = AnomalyDetector(model), AlertPolicy(cfg.debounce_windows)
    tags, out = TagTable(), AlertOutput(a.pin, enabled=not a.no_gpio)
    srv = ModbusServer(tags, port=a.port)
    srv.start()
    lat, prev = [], False
    try:
        for f in a.replay:
            df = load_features([f], cfg.window_seconds, cfg.sample_rate_hz, cfg.min_window_fill)
            for r in df[FEATURE_NAMES].to_dict("records"):
                res = det.evaluate(r)
                active, _ = pol.update(res.prediction)
                t0 = time.perf_counter()
                out.set(active)
                tags.update(active, res.prediction == -1, res.score)
                if active != prev:
                    ok_pin = (not out.enabled) or pin_is_high(a.pin) == active
                    ok_tag = modbus_read("127.0.0.1", srv.port, 0, 1)[0] == int(active)
                    dt = (time.perf_counter() - t0) * 1000
                    lat.append(dt)
                    print(f"alert {'RAISED ' if active else 'CLEARED'} pin_ok={ok_pin} tag_ok={ok_tag} latency={dt:.1f} ms [{f.name[-30:]}]")
                    prev = active
    finally:
        out.release()
        srv.stop()
    if lat:
        s = sorted(lat)
        print(f"transitions={len(lat)} median={statistics.median(s):.1f} ms p95={s[int(0.95 * (len(s) - 1))]:.1f} ms max={s[-1]:.1f} ms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
