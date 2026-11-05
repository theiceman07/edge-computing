# M4: Topics (2 pts)

**Checklist:** I publish detection and motor score and show them on a subscriber

**Status:** HAVE (transport real, input windows generated, not recorded)

**Notes:** Delivered on a PC with generated (non-recorded) data. Repeat on the Pi.

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 802a158)
- [docs/evidence/mqtt_topics_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/docs/evidence/mqtt_topics_pi_2026-11-05.txt): bridge -> TLS broker -> subscriber on the Pi, 120/120 messages on `factory/motor/score`.
- [scripts/mqtt_bridge.py](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/scripts/mqtt_bridge.py): publisher.
