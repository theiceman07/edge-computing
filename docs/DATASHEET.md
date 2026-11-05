# Motor Health Monitor datasheet (prototype)
| Item | Value |
|---|---|
| Platform | Raspberry Pi 5, Python 3.11 venv |
| Sensor | MPU6050 (I2C 0x68), 50 Hz requested; achieved 43-50 Hz with motor running (rate dips under motor noise) |
| Motor drive | L298N, GPIO17/27 direction, GPIO22 PWM, duty capped at 0.65 in `motor_run.py` |
| Model | IsolationForest, 100 trees, 13 window features, 1 s windows |
| Dashboard | Streamlit, 127.0.0.1:8501 |
| Messaging | MQTT over TLS 8883 + password (self-test 6/6 on the Pi) |
| PLC link | Modbus TCP read-only holding registers 0-3, port 1502 (software client only) |
| Alert output | GPIO23 active high |
| Decision-to-output latency | median 4.1 ms, p95 6.2 ms (21 transitions, replay) |
| Container | Dockerfile (dashboard); healthy 3.6 s after start |
| Measured detection quality | **None validated.** Real normal runs from later sessions are flagged 100%; no real fault recordings; results on computer-generated data (55% false alarms, 45% detection) are not evidence |
| Intended use | Learning prototype. Not a safety system. |
