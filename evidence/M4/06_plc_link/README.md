# M4: PLC link (2 pts)

**Checklist:** I show the PLC tag change when an object is detected

**Status:** PARTIAL (software Modbus client, no physical PLC)

**Notes:** Not started.

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 802a158)
- [src/motor_fault/gateway.py](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/src/motor_fault/gateway.py): Modbus TCP server, holding register 0 = alert tag.
- [docs/evidence/gateway_actuator_plc_latency_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/docs/evidence/gateway_actuator_plc_latency_pi_2026-11-05.txt): tag read back by a Modbus client on every alert transition (21/21).
