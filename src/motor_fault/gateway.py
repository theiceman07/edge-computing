"""Alert gateway: debounced alert -> GPIO signal (actuator) and Modbus TCP 'PLC tag' registers.

Standard library only. The Modbus server is a minimal read-only slave (function 3, read holding
registers) so a PLC / SCADA master or any Modbus client can poll the tags. No PLC hardware was
available; this is verified against a software Modbus client only.

Holding registers (unit id any):
  0 = alert active (0/1)      1 = last window anomalous (0/1)
  2 = score x1000 + 32768     3 = windows processed (mod 65536)
"""
from __future__ import annotations

import socketserver
import struct
import subprocess
import threading

ALERT_PIN_DEFAULT = 23  # BCM; drive an LED / relay / conveyor-stop input from here (active high)


class AlertOutput:
    """Drives one GPIO pin via `pinctrl` (no extra Python packages, no sudo on Raspberry Pi OS)."""

    def __init__(self, pin: int = ALERT_PIN_DEFAULT, enabled: bool = True) -> None:
        self.pin, self.enabled, self.state = pin, enabled, False
        self.set(False)

    def set(self, on: bool) -> None:
        self.state = bool(on)
        if self.enabled:
            subprocess.run(["pinctrl", "set", str(self.pin), "op", "dh" if on else "dl"], check=True)

    def release(self) -> None:
        self.set(False)
        if self.enabled:
            subprocess.run(["pinctrl", "set", str(self.pin), "ip"], check=False)


class TagTable:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._regs = [0, 0, 32768, 0]

    def update(self, alert: bool, anomalous: bool, score: float) -> None:
        with self._lock:
            self._regs[0] = int(alert)
            self._regs[1] = int(anomalous)
            self._regs[2] = max(0, min(65535, int(round(score * 1000)) + 32768))
            self._regs[3] = (self._regs[3] + 1) & 0xFFFF

    def read(self, addr: int, count: int) -> list[int] | None:
        with self._lock:
            if count < 1 or addr < 0 or addr + count > len(self._regs):
                return None
            return self._regs[addr:addr + count]


def _make_handler(tags: TagTable):
    class H(socketserver.BaseRequestHandler):
        def handle(self) -> None:
            while True:
                hdr = self._recv(7)
                if not hdr:
                    return
                tid, proto, length, unit = struct.unpack(">HHHB", hdr)
                pdu = self._recv(length - 1)
                if pdu is None or proto != 0:
                    return
                func = pdu[0]
                if func == 3 and len(pdu) == 5:
                    addr, count = struct.unpack(">HH", pdu[1:5])
                    vals = tags.read(addr, count)
                    if vals is None:
                        out = bytes([func | 0x80, 0x02])
                    else:
                        out = bytes([func, 2 * len(vals)]) + struct.pack(f">{len(vals)}H", *vals)
                else:
                    out = bytes([func | 0x80, 0x01])
                self.request.sendall(struct.pack(">HHHB", tid, 0, len(out) + 1, unit) + out)

        def _recv(self, n: int):
            buf = b""
            while len(buf) < n:
                chunk = self.request.recv(n - len(buf))
                if not chunk:
                    return None
                buf += chunk
            return buf
    return H


class ModbusServer:
    def __init__(self, tags: TagTable, host: str = "127.0.0.1", port: int = 1502) -> None:
        class S(socketserver.ThreadingTCPServer):
            allow_reuse_address = True
            daemon_threads = True
        self._srv = S((host, port), _make_handler(tags))
        self.port = self._srv.server_address[1]
        self._t = threading.Thread(target=self._srv.serve_forever, daemon=True)

    def start(self) -> None:
        self._t.start()

    def stop(self) -> None:
        self._srv.shutdown()
        self._srv.server_close()


def modbus_read(host: str, port: int, addr: int, count: int, timeout: float = 2.0) -> list[int]:
    """Tiny Modbus TCP client (function 3), used for tests and the demo."""
    import socket
    with socket.create_connection((host, port), timeout=timeout) as s:
        s.sendall(struct.pack(">HHHBBHH", 1, 0, 6, 1, 3, addr, count))
        hdr = s.recv(9)
        if hdr[7] & 0x80:
            raise RuntimeError(f"modbus exception {hdr[8]}")
        data = b""
        while len(data) < hdr[8]:
            data += s.recv(hdr[8] - len(data))
        return list(struct.unpack(f">{count}H", data))
