# Hardware: parts list and wiring

Matches the code in this repo: MPU6050 over I2C at 0x68, Raspberry Pi 5, 50 Hz sampling. Verify against your own breakout's documentation before powering anything.

## Parts list
| # | Part | Notes |
|---|---|---|
| 1 | Raspberry Pi 5 + 27 W USB-C PSU, microSD (or SSD) | Already have |
| 2 | MPU6050 breakout (GY-521) | Main sensor. Supported target in the code |
| 3 | Small DC motor, 6-12 V (e.g. 775 or 555 brushed) | Needs a shaft you can attach an off-centre weight to |
| 4 | Separate motor supply, 12 V 2-3 A | Never power the motor from the Pi |
| 5 | Logic-level N-MOSFET (IRLZ44N) or ready-made MOSFET PWM module | Switches the motor; 3.3 V gate drive |
| 6 | Flyback diode (1N5819 or 1N4007) across the motor | Protects the MOSFET |
| 7 | 100 ohm gate resistor + 10 kohm gate pulldown | Only if you build the MOSFET stage yourself |
| 8 | Dupont jumper wires, breadboard or perfboard | Keep sensor wires short and away from the shaft |
| 9 | Rigid mount for the sensor (screw or hot glue on the motor housing, or a 3D-printed bracket) | Rigid contact matters more than anything else for data quality |
| 10 | Fault-injection items: M3 bolt + nuts or modelling clay to stick on the shaft/fan (imbalance); loose screw on the mount (loose mount) | Add small amounts only |
| 11 | Heavy base (wood block or clamp) | Keeps table vibration out of the data |
| 12 | Optional: IR/Hall tachometer, ADXL345 breakout, INA219 current sensor | Not needed for v1. ADXL345 is untested here |
| 13 | Optional: guard (clear shield or box), safety glasses | Needed for imbalance runs |

## Wiring: sensor
```
 Pi 5 header                      MPU6050 (GY-521)
 pin 1  3V3  ------------------>  VCC
 pin 3  GPIO2 (SDA) ------------>  SDA
 pin 5  GPIO3 (SCL) ------------>  SCL
 pin 6  GND  ------------------>  GND
                                   AD0 -> GND (address 0x68)
                                   INT, XDA, XCL unconnected
```

## Wiring: motor
```
 12 V supply (+) ----------------+---------------> Motor (+)
                                 |                    |
                              [1N5819]  (stripe/cathode toward +12 V)
                                 |                    |
 12 V supply (-) --+------------ +---- Motor (-) ---> MOSFET Drain
                   |                                  MOSFET Source ---+--> 12 V (-)
                   |                                                   |
                   +---------------------------------------------------+--> Pi GND (pin 9)
 Pi GPIO18 (pin 12) --[100 ohm]--> MOSFET Gate ---[10 k]--> Source/GND
```
Rules: common ground between the Pi and the 12 V supply; diode across the motor terminals; the motor's current never passes through a Pi pin. Run the motor at a fixed duty cycle (or fully on) for all runs; the model compares like with like only.

## Layout
```
 [12V PSU] -> [MOSFET] -> [Motor] ===shaft+test weight
                              |
                      [MPU6050 glued/screwed to housing]
                              | I2C (short wires)
                        [Raspberry Pi 5] -> Streamlit dashboard / MQTT
```

## First checks
1. `sudo raspi-config nonint do_i2c 0 && sudo reboot` (this machine currently has no `/dev/i2c-1`).
2. `i2cdetect -y 1` should show 0x68.
3. `python scripts/check_i2c.py --sensor mpu6050`.
4. Spin the motor with the sensor mounted and confirm the readings change.

## Limits to be aware of
At 50 Hz sampling the Nyquist limit is 25 Hz, so only shaft speeds below about 25 Hz (1500 rpm) are properly resolved, and bearing faults are not visible. For a faster motor either lower its speed or raise `sample_rate_hz` (the MPU6050 can go to 1 kHz, but a Python I2C loop will need measuring).
