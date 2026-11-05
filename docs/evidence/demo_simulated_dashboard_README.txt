demo_simulated_dashboard.mp4 (2026-11-05, ~17 s, recorded on the Pi with scripts/record_demo.py)

WHAT IT IS: the Streamlit dashboard in emulator (SIMULATION) mode, using the "Inject SIMULATED fault" toggle. A red banner
"SIMULATED DEMO - synthetic data, not a real motor" is overlaid on every frame. It shows the pipeline (window features ->
model -> debounced alert) reacting to an artificial, software-injected fault: vibration jumps in the chart, last window = ANOMALY, then ALERT.
WHAT IT IS NOT: real motor footage or evidence of fault detection on the real rig.

Recording conditions: the requested sample rate was set to 40 Hz in the UI because the browser + dashboard on one Pi
only achieved ~33 Hz; the alert took ~10 s after the toggle. The model used is the emulator-trained model
(data/models_sim), installed temporarily with ota_model.py and rolled back afterwards.
Re-create: scripts/record_demo.py (needs a sim model active in data/models and the dashboard on port 8601).
