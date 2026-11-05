# M3: Actuator fires (3 pts)

**Checklist:** I make the relay, LED or conveyor-stop signal work live

**Status:** PARTIAL

**Notes:** LEDs wired on GPIO 17/27/22, wiring test lights all three. Live detection-to-LED demo still to record.

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 01b7096)
- [docs/evidence/gateway_actuator_plc_latency_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/evidence/gateway_actuator_plc_latency_pi_2026-11-05.txt): GPIO23 alert/stop signal followed the debounced alert on 21/21 transitions (pin level read back on the Pi). No relay or LED physically attached; replayed windows.
