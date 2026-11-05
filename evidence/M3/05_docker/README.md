# M3: Docker (4 pts)

**Checklist:** I build and start the container from a cold boot and trigger the actuator

**Status:** PARTIAL

**Notes:** Not started (Dockerfile/docker-compose exist, untested on the Pi).

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 01b7096)
- [Dockerfile (motor monitor)](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/Dockerfile) and [docs/evidence/docker_coldstart_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/evidence/docker_coldstart_pi_2026-11-05.txt): image built on the Pi, cold start to healthy dashboard in 3.6 s, 37 tests pass inside. Actuator not driven from inside the container (no GPIO passthrough).
