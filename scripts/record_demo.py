#!/usr/bin/env python3
"""Record a short screen capture of the dashboard in SIMULATION mode with an injected SIMULATED fault.

Drives headless Chromium over the DevTools protocol (needs `websockets`, already a streamlit dependency),
grabs frames, and assembles an MP4 with ffmpeg. A red 'SIMULATED DEMO - synthetic data' banner is
injected into every frame so the video cannot be mistaken for real-motor footage.

Prereq: a simulation-trained model active in data/models (see docs/MILESTONE_CHECKLIST.md) and the
dashboard running, e.g. `streamlit run app.py --server.port 8601 --server.headless true`.
Usage: python scripts/record_demo.py --url http://127.0.0.1:8601 --out docs/evidence/demo_simulated_dashboard.mp4
"""
import argparse
import asyncio
import base64
import json
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import websockets

BANNER = """(()=>{if(document.getElementById('demo-banner'))return;const d=document.createElement('div');
d.id='demo-banner';d.textContent='SIMULATED DEMO - synthetic data, not a real motor';
d.style.cssText='position:fixed;top:0;left:0;right:0;z-index:2147483647;background:#b00020;color:#fff;font:700 18px sans-serif;text-align:center;padding:6px';
document.body.appendChild(d);})()"""

CLICK_TEXT = """((t)=>{const els=[...document.querySelectorAll('button,label')];
const e=els.find(x=>x.innerText&&x.innerText.includes(t));if(!e)return 'missing';e.click();return 'ok';})(%s)"""

BODY_TEXT = "document.body.innerText"


class Cdp:
    def __init__(self, ws):
        self.ws, self.i = ws, 0

    async def call(self, method, **params):
        self.i += 1
        await self.ws.send(json.dumps({"id": self.i, "method": method, "params": params}))
        while True:
            msg = json.loads(await self.ws.recv())
            if msg.get("id") == self.i:
                return msg.get("result", {})

    async def js(self, expr):
        r = await self.call("Runtime.evaluate", expression=expr, returnByValue=True)
        return r.get("result", {}).get("value")


RECT = """((t)=>{const e=[...document.querySelectorAll('label')].find(x=>x.innerText&&x.innerText.includes(t));
if(!e)return null;const b=e.getBoundingClientRect();return [b.x+20,b.y+b.height/2];})(%s)"""


async def mouse_click(c, text: str) -> str:
    xy = await c.js(RECT % json.dumps(text))
    if not xy:
        return "missing"
    for ty in ("mousePressed", "mouseReleased"):
        await c.call("Input.dispatchMouseEvent", type=ty, x=xy[0], y=xy[1], button="left", clickCount=1)
    return "ok"


async def run(url: str, frames: Path, port: int, rate: int) -> list[str]:
    pages = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json"))
    ws_url = next(p["webSocketDebuggerUrl"] for p in pages if p["type"] == "page")
    log: list[str] = []
    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        c = Cdp(ws)
        await c.call("Page.enable")
        await c.call("Emulation.setDeviceMetricsOverride", width=1280, height=800, deviceScaleFactor=1, mobile=False)
        await c.call("Page.navigate", url=url)
        await asyncio.sleep(6)
        n = 0
        t_start = time.time()

        import re

        async def shot_for(seconds: float):
            nonlocal n
            end = time.time() + seconds
            last = 0.0
            while time.time() < end:
                await c.js(BANNER)
                if time.time() - last > 3:
                    last = time.time()
                    tt = await c.js(BODY_TEXT) or ""
                    m = re.search(r"Last window: (\w+)", tt)
                    r2 = re.search(r"Achieved rate\s*([\d.]+)", tt.replace("\n", " "))
                    log.append("  t=%4.0fs status: last_window=%s alert=%s rate=%s" % (
                        time.time() - t_start, m.group(1) if m else "-", "ALERT" in tt, r2.group(1) if r2 else "-"))
                r = await c.call("Page.captureScreenshot", format="jpeg", quality=70)
                (frames / f"f{n:05d}.jpg").write_bytes(base64.b64decode(r["data"]))
                n += 1
                await asyncio.sleep(0.9)

        await shot_for(2)
        ok = await c.js("""(()=>{const i=document.querySelector('input[aria-label^="Sample rate"]');if(!i)return 'missing';
        i.focus();i.select();document.execCommand('insertText',false,'%d');return i.value;})()""" % rate)
        await c.call("Input.dispatchKeyEvent", type="keyDown", key="Enter", code="Enter", windowsVirtualKeyCode=13, text="\r")
        await c.call("Input.dispatchKeyEvent", type="keyUp", key="Enter", code="Enter", windowsVirtualKeyCode=13)
        log.append(f"set requested sample rate to {rate} Hz (so 1 s windows fill under browser load): field={ok}")
        await shot_for(3)
        log.append(f"click Start: {await c.js(CLICK_TEXT % json.dumps('Start / new recording'))}")
        await shot_for(14)
        t = await c.js(BODY_TEXT)
        log.append("normal phase shows SIMULATION: %s | ALERT shown: %s" % ("SIMULATION" in t, "ALERT" in t))
        log.append(f"toggle fault ON: {await mouse_click(c, 'Inject SIMULATED fault')}")
        await shot_for(16)
        t = await c.js(BODY_TEXT)
        log.append("fault phase ALERT shown: %s | simulated-data note: %s" % ("ALERT" in t, "simulated" in t.lower()))
        log.append(f"toggle fault OFF: {await mouse_click(c, 'Inject SIMULATED fault')}")
        await shot_for(8)
        log.append(f"click Stop: {await c.js(CLICK_TEXT % json.dumps('Stop'))}")
        await shot_for(3)
        log.append(f"frames captured: {n}")
    return log


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--url", default="http://127.0.0.1:8601")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--port", type=int, default=9333)
    ap.add_argument("--rate", type=int, default=40, help="requested sample rate typed into the dashboard")
    a = ap.parse_args()
    tmp = Path(tempfile.mkdtemp(prefix="demo_frames_"))
    prof = Path(tempfile.mkdtemp(prefix="demo_chrome_"))
    chrome = subprocess.Popen(["chromium", "--headless=new", f"--remote-debugging-port={a.port}", f"--user-data-dir={prof}",
                               "--window-size=1280,800", "--no-first-run", "--disable-gpu", "about:blank"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(40):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{a.port}/json", timeout=1)
                break
            except Exception:
                time.sleep(0.5)
        log = asyncio.run(run(a.url, tmp, a.port, a.rate))
    finally:
        chrome.terminate()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2.5", "-i", str(tmp / "f%05d.jpg"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(a.out)], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.rmtree(prof, ignore_errors=True)
    print("\n".join(log))
    print(f"video: {a.out} ({a.out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
