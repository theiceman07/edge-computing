# M4: Secure MQTT (3 pts)

**Checklist:** I show the broker refuses no-password and works with password + TLS

**Status:** HAVE

**Notes:** Passed on a PC (docs/evidence in motor-fault-monitor). Repeat on the Pi.

## Evidence files in this folder
- PC_only_not_the_Pi.txt

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 802a158)
- [docs/evidence/mqtt_selftest_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/docs/evidence/mqtt_selftest_pi_2026-11-05.txt): on the Pi, 6/6 PASS: anonymous, wrong password, plain TCP and untrusted certificate refused; password + TLS works.
- [deploy/mosquitto/mosquitto.conf](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/deploy/mosquitto/mosquitto.conf): broker config (port 8883, allow_anonymous false, password file).
