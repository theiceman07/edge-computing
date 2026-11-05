# Architecture
```mermaid
flowchart LR
  S[MPU6050 over I2C] --> A[Acquisition 50 Hz]
  A --> F[Window features 1 s]
  F --> M[IsolationForest]
  M --> P[Debounce: 3 consecutive anomalous windows]
  P --> D[Streamlit dashboard + alerts]
  P --> G[Alert gateway]
  G --> O[GPIO23 alert / stop signal]
  G --> T[Modbus TCP tags, port 1502]
  M --> Q[MQTT publisher, TLS 8883]
  Q --> B[(Mosquitto broker)]
  B --> X[Subscriber]
  U[ota_model.py install / rollback] -. newest model .-> M
```
Status: every box has run on the Pi except live sensor-to-gateway wiring (the gateway was tested by replaying recorded windows) and a physical PLC/relay (none attached). See `docs/MILESTONE_CHECKLIST.md`.
