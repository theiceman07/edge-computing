# M4 Threat model
| Level | Threat | Mitigation (mark the two you applied and tested) |
|---|---|---|
| Sensor/device | Loose or failed MPU6050 gives stale data | Stale-timeout -> `SENSOR ERROR` (`stale_timeout_s` in config.yaml); no silent fallback to simulation |
| Network | Anonymous or eavesdropped MQTT | Broker with `allow_anonymous false`, password file, TLS on 8883 (`deploy/mosquitto`); test: `test_mqtt.sh` |
| Software | Dashboard exposed on LAN without auth | Bind to 127.0.0.1 / firewall rule; document port |
| Model | Bad update breaks detection | Keep previous model file; rollback after OTA v1 -> v2 |

Applied and demonstrated on the Pi (2026-11-05):
1) Network: MQTT broker with TLS on 8883, `allow_anonymous false` and a password file. Evidence: `docs/evidence/mqtt_selftest_pi_2026-11-05.txt` (anonymous, wrong password, plain TCP and untrusted certificate refused; password + TLS works).
2) Model: keep the previous model and roll back after a bad OTA update. Evidence: `docs/evidence/ota_rollback_pi_2026-11-05.txt` (v1 -> v2 install, invalid artifact rejected, rollback to v1).

Earlier PC run of the network test (2026-10-23): `docs/evidence/mqtt_selftest_pc_2026-10-23.txt`.
