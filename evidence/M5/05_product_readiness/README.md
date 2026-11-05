# M5: Product readiness (2 pts)

**Checklist:** I show auto-start after power-cycle, offline run and logs

**Status:** PARTIAL (motor monitor done; vision service untested)

**Notes:** Not started (deploy/vision.service untested).

## Evidence files in this folder
(none yet)

Rules: only numbers measured by me on my own hardware; commit on branch `arjun` with the milestone in the message.

## Evidence on the `motor-fault-monitor` branch (pinned commit 01b7096)
- [docs/evidence/reboot_autostart_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/evidence/reboot_autostart_pi_2026-11-05.txt): after a real reboot the service started itself 14 s after boot.
- [docs/evidence/systemd_autostart_crash_restart_pi_2026-11-05.txt](https://github.com/theiceman07/edge-computing/blob/01b70968780b7693451ec20e38bdc1d70ff71af4/docs/evidence/systemd_autostart_crash_restart_pi_2026-11-05.txt): restart after a forced crash; logs via `journalctl -u motor-monitor`. Runs offline (127.0.0.1).
