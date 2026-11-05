# M3: Docker (4 pts)

**Checklist:** I build and start the container from a cold boot and trigger the actuator

**Status:** PARTIAL

**Notes:** Not started (Dockerfile/docker-compose exist, untested on the Pi).

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 802a158)
- [Dockerfile (motor monitor)](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/Dockerfile) and [docs/evidence/docker_coldstart_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/802a158fdc4f2f64943f398227d4d289ec826bef/docs/evidence/docker_coldstart_pi_2026-11-05.txt): image built on the Pi, cold start to healthy dashboard in 3.6 s, 37 tests pass inside. Actuator not driven from inside the container (no GPIO passthrough).
