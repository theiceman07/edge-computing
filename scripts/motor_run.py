"""Run the L298N-driven motor at a fixed, capped speed until Ctrl+C (or --seconds).

Wiring (BCM): IN1=GPIO17, IN2=GPIO27, ENA=GPIO22 (PWM). ENA jumper removed.
The duty cycle is hard-capped at MAX_DUTY because a 9 V supply through an L298N
(~2 V drop) gives ~7 V, above a 5 V motor's rating. Remove the cap only after
using a regulated supply that gives the motor <= 5 V.

Usage: python scripts/motor_run.py --duty 0.6 [--seconds 150]
Start this in its own terminal, then run collect_data.py in another.
"""
import argparse
import signal
import sys
import time

from gpiozero import OutputDevice, PWMOutputDevice

MAX_DUTY = 0.65


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--duty", type=float, default=0.6, help=f"0-{MAX_DUTY}")
    ap.add_argument("--seconds", type=float, default=0, help="0 = until Ctrl+C")
    ap.add_argument("--ramp", type=float, default=2.0, help="seconds to ramp up")
    args = ap.parse_args()
    duty = min(max(args.duty, 0.0), MAX_DUTY)
    if duty != args.duty:
        print(f"Duty clamped to {duty} (cap {MAX_DUTY}).")

    in1, in2, ena = OutputDevice(17), OutputDevice(27), PWMOutputDevice(22)
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        in1.on()
        in2.off()
        steps = 20
        for i in range(1, steps + 1):  # soft start
            ena.value = duty * i / steps
            time.sleep(args.ramp / steps)
        print(f"Motor running at duty {duty}. Ctrl+C to stop.")
        end = time.time() + args.seconds if args.seconds else None
        while end is None or time.time() < end:
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        ena.value = 0
        in1.off()
        in2.off()
        ena.close(); in1.close(); in2.close()
        print("Motor stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
