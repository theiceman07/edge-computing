# Decision rule sheet (motor fault monitor)
| Item | Value |
|---|---|
| Input | 1 s window of MPU6050 acceleration (g, includes gravity) at 50 Hz; window needs >= 80% of expected samples (`min_window_fill`) |
| Features | RMS, std, peak, peak-to-peak per axis + magnitude RMS (13) |
| Per-window decision | IsolationForest trained on normal windows only; prediction -1 = anomalous window |
| Threshold | `contamination=auto` (model's own offset); not tuned on fault data |
| Debounce | alert after **3** consecutive anomalous windows; clears on the first normal window (`debounce_windows` in config.yaml) |
| Action | alert active -> GPIO23 high (stop/alert signal) and Modbus register 0 = 1 |
| Safe state | if the sensor cannot be read, collection exits with code 2 and never falls back to the emulator; GPIO23 is released to low/input when the gateway stops |
| Known limitation | model is not robust across sessions/sensor placement (see MILESTONE_CHECKLIST false-alarm table); not a safety system |
