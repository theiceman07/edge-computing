#!/usr/bin/env python3
"""Fit a vibration model to REAL normal recordings, then generate SYNTHETIC runs from it.

Output is marked sensor_mode="synthetic_calibrated". It is NOT real data:
  * normal runs   -> parameters (gravity vector, spectral peaks, noise, run-to-run scale)
                     fitted from the real motor-running recordings passed with --real-normal
  * imbalance runs-> an ASSUMED fault model (peak amplitudes x --imbalance-gain); there is no
                     usable real imbalance recording to fit it to, so this part is an assumption.
The fitted values are written to calibration.json together with the source files.

Usage: python scripts/calibrate_synthetic.py --real-normal data/raw/a.csv data/raw/b.csv ...
"""
import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

MODE = "synthetic_calibrated"
AXES = ("ax_g", "ay_g", "az_g")
FS = 50.0
N_PEAKS = 3
SKIP = 50  # drop first second (motor ramp / settle)


def fit_run(path: Path) -> dict:
    d = pd.read_csv(path).iloc[SKIP:]
    x = d[list(AXES)].to_numpy(float)
    mean = x.mean(0)
    xc = x - mean
    n = len(xc)
    win = np.hanning(n)
    spec = np.abs(np.fft.rfft(xc * win[:, None], axis=0)) * 2 / win.sum()
    freqs = np.fft.rfftfreq(n, 1 / FS)
    peaks = []
    for a in range(3):
        s = spec[:, a].copy()
        s[freqs < 0.5] = 0  # ignore slow drift
        idx = []
        for _ in range(N_PEAKS):
            i = int(np.argmax(s))
            idx.append(i)
            s[max(0, i - 3):i + 4] = 0
        recon_var = sum((spec[i, a] ** 2) / 2 for i in idx)
        resid_std = float(np.sqrt(max(xc[:, a].var() - recon_var, 1e-8)))
        peaks.append({"freq_hz": [float(freqs[i]) for i in idx],
                      "amp_g": [float(spec[i, a]) for i in idx], "resid_std_g": resid_std})
    return {"file": path.name, "mean_g": mean.tolist(), "std_g": xc.std(0).tolist(), "peaks": peaks}


def pool(fits: list[dict]) -> dict:
    tot = np.array([np.linalg.norm(f["std_g"]) for f in fits])
    ref = float(tot.mean())
    params = {"mean_g": np.mean([f["mean_g"] for f in fits], axis=0).tolist(), "axes": []}
    for a in range(3):
        params["axes"].append({
            "freq_hz": np.median([f["peaks"][a]["freq_hz"] for f in fits], axis=0).tolist(),
            "amp_g": np.mean([f["peaks"][a]["amp_g"] for f in fits], axis=0).tolist(),
            "resid_std_g": float(np.mean([f["peaks"][a]["resid_std_g"] for f in fits])),
        })
    params["scale_range"] = [float(tot.min() / ref), float(tot.max() / ref)]
    params["mean_spread_g"] = np.std([f["mean_g"] for f in fits], axis=0).tolist()
    return params


def synth_run(params: dict, label: str, gain: float, rng: np.random.Generator, seconds: float,
              start: datetime, idx: int) -> pd.DataFrame:
    t = np.arange(int(seconds * FS)) / FS
    lo, hi = params["scale_range"]
    s = rng.uniform(lo, hi)
    cols = []
    for a in range(3):
        ax = params["axes"][a]
        y = params["mean_g"][a] + rng.normal(0, 0.5 * params["mean_spread_g"][a] + 1e-4)
        for f, amp in zip(ax["freq_hz"], ax["amp_g"]):
            y = y + gain * s * amp * np.sin(2 * np.pi * f * t + rng.uniform(0, 2 * np.pi))
        y = y + rng.normal(0, s * ax["resid_std_g"], len(t))
        cols.append(y)
    run_id = f"{MODE}_{start:%Y%m%dT%H%M%S}_{idx:02d}_{label}"
    ts = [(start + timedelta(seconds=float(v))).isoformat() for v in t]
    return pd.DataFrame({"timestamp_utc": ts, "elapsed_seconds": np.round(t, 4),
                         "ax_g": cols[0], "ay_g": cols[1], "az_g": cols[2],
                         "sensor_mode": MODE, "run_id": run_id, "label": label})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--real-normal", nargs="+", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=Path("data/synthetic"))
    ap.add_argument("--n-normal", type=int, default=8)
    ap.add_argument("--n-imbalance", type=int, default=4)
    ap.add_argument("--imbalance-gain", type=float, default=2.0,
                    help="ASSUMED multiplier on fitted vibration peak amplitudes")
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    fits = [fit_run(p) for p in a.real_normal]
    params = pool(fits)
    a.out.mkdir(parents=True, exist_ok=True)
    cal = {"generated_utc": datetime.now(timezone.utc).isoformat(), "sensor_mode": MODE,
           "NOT_REAL_DATA": True, "seed": a.seed,
           "normal_source": "fitted from REAL recordings listed in per_run_fits",
           "imbalance_source": f"ASSUMED: fitted peak amplitudes x {a.imbalance_gain}; not fitted from real data",
           "imbalance_gain": a.imbalance_gain, "pooled_params": params, "per_run_fits": fits}
    (a.out / "calibration.json").write_text(json.dumps(cal, indent=2))
    rng = np.random.default_rng(a.seed)
    start = datetime(2026, 11, 5, 12, 0, 0, tzinfo=timezone.utc)
    n = 0
    for label, count, gain in (("normal", a.n_normal, 1.0), ("imbalance", a.n_imbalance, a.imbalance_gain)):
        for i in range(count):
            df = synth_run(params, label, gain, rng, a.seconds, start + timedelta(minutes=n), i)
            df.to_csv(a.out / f"{df['run_id'].iloc[0]}.csv", index=False, float_format="%.6f")
            n += 1
    print(json.dumps({"pooled_params": params}, indent=2))
    print(f"Wrote {n} synthetic runs and calibration.json to {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
