# M4: Reliability (3 pts)

**Checklist:** I show the drift report, OTA v1 to v2 with rollback, and auto-restart after a forced crash

**Status:** HAVE

**Notes:** Scripts written; not run on the Pi.

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 01b7096)
- [docs/evidence/drift_report_2026-11-05.md](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/evidence/drift_report_2026-11-05.md): drift report.
- [docs/evidence/ota_rollback_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/evidence/ota_rollback_pi_2026-11-05.txt): OTA v1 -> v2 install, invalid artifact rejected, rollback.
- [docs/evidence/systemd_autostart_crash_restart_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/evidence/systemd_autostart_crash_restart_pi_2026-11-05.txt): auto-restart after a forced crash (kill -9 -> healthy in 4.6 s).
