# Engineering Log

## Project
Motion-Aware Physiological Sensing System

## Purpose
Document hardware development, firmware implementation,
experiments, debugging, engineering decisions, and results.

---

## 2026-10-11 — M0: ESP32-S3 Bring-Up

### Objective
Establish the embedded development environment and verify
successful firmware execution and USB serial communication.

### Hardware
- ESP32-S3-DevKitC-1-N16R8
- MacBook Air
- USB data cable

### Software
- VS Code
- PlatformIO
- Arduino framework

### Implementation
- Created PlatformIO firmware project
- Selected ESP32-S3-DevKitC-1 board configuration
- Enabled USB CDC serial communication
- Implemented serial initialization and periodic status messages
- Configured serial baud rate to 115200

### Results
- Firmware compiled successfully
- Firmware uploaded successfully
- ESP32-S3 detected over USB
- Serial Monitor displayed continuous status messages
- Verified execution of `setup()` and `loop()`

### Issues / Notes
- PlatformIO default board configuration identifies N8 variant
- Physical board is N16R8 (16 MB flash, 8 MB PSRAM)
- Memory configuration will need to be updated for future development

### Next Steps
- M1: MPU6050 sensor bring-up
- Establish I2C communication
- Acquire accelerometer and gyroscope measurements

## 2026-10-11 — Synthetic Data Acquisition

### Objective
Develop and validate the serial acquisition pipeline before
integrating the physical PPG and IMU sensors.

### Implementation
- Generated synthetic PPG and IMU measurements on ESP32-S3
- Configured nominal sampling rate of 50 Hz
- Implemented comma-separated serial data transmission
- Developed Python acquisition script using pyserial
- Added CSV logging and basic input validation

### Data Format
timestamp_ms,ppg_ir,ppg_red,ax,ay,az,gx,gy,gz

### Test Results
- Recording duration: 31.64s
- Samples recorded: 1583
- Measured average sample rate: 50.00 Hz
- CSV successfully generated: [Yes]

### Notes
Synthetic data was used to validate the acquisition pipeline.
No physical sensor measurements were collected.

### Next Steps
- Implement waveform visualization
- Integrate physical MPU6050 and MAX30102 sensors
- Evaluate sensor sampling and synchronization

## 2026-10-11 — M5: Synthetic Signal Visualization

### Objective
Visualize synchronized synthetic PPG and IMU measurements and
examine the relationship between movement and PPG distortion.

### Implementation
- Developed offline visualization scripts using pandas, NumPy, and Matplotlib
- Plotted IR and red PPG signals, three-axis acceleration, and acceleration magnitude
- Compared mean-removed IR PPG with acceleration magnitude

### Results
- Observed periodic PPG oscillations during stationary intervals
- Simulated movement introduced additional oscillations into the PPG waveform
- PPG distortion coincided with increased acceleration activity
- Successfully generated and saved both visualization figures

### Next Steps
- Estimate heart rate from synthetic PPG measurements
- Compare heart-rate estimates during stationary and moving intervals
- Develop a motion-aware signal quality metric

## 2026-10-11 — Synthetic HR Estimation and Motion-Aware Reliability

### Objective
Evaluate whether IMU motion measurements can identify unreliable
PPG-derived heart-rate estimates.

### Implementation
- Implemented FFT-based heart-rate estimation from IR PPG
- Applied 5-second sliding windows with 1-second steps
- Calculated acceleration magnitude and its standard deviation
- Implemented a preliminary motion threshold of 0.06 g
- Classified HR estimates as accepted or flagged

### Results
- Synthetic ground-truth HR: 72 BPM
- Simulated motion artifact frequency: 2 Hz (120 cycles/min)
- Total windows: 27
- Correct baseline estimates: 15
- Incorrect baseline estimates: 12
- Baseline mean absolute error: 21.33 BPM
- Accepted windows: 15 (55.6%)
- Flagged windows: 12 (44.4%)
- Mean HR error of accepted windows: 0.00 BPM
- Mean HR error of flagged windows: 48.00 BPM
- Incorrect estimates detected: 12/12
- Correct estimates retained: 15/15

### Limitations
- Evaluation used one deterministic synthetic recording
- Motion threshold was selected using the same recording
- Overlapping windows are not statistically independent
- Motion-aware detection flags estimates but does not correct them
- Real sensor performance remains untested

### Next Steps
- Test the detector on additional synthetic conditions
- Evaluate false positives and false negatives across recordings
- Investigate motion artifact reduction
- Validate with physical PPG and IMU sensors

## 2026-10-11 — Multi-Condition Synthetic Evaluation

### Objective
Evaluate whether the initial IMU-based motion detector generalizes
across different heart rates, motion frequencies, and PPG artifact amplitudes.

### Implementation
- Generated five 60-second synthetic PPG/IMU recordings at 50 Hz
- Varied simulated HR, motion frequency, and artifact amplitude
- Evaluated 5-second FFT windows with 1-second steps
- Kept the IMU motion threshold fixed at 0.06 g
- Defined incorrect HR estimates as errors greater than 12 BPM

### Results
| Test | Baseline MAE | Accepted MAE | False Positives |
|---|---:|---:|---:|
| Baseline | 24.00 BPM | 0.00 BPM | 0 |
| Low motion artifact | 0.00 BPM | 0.00 BPM | 28 |
| Higher HR | 12.00 BPM | 0.00 BPM | 0 |
| Motion near HR | 6.00 BPM | 6.00 BPM | 28 |
| Faster motion | 36.86 BPM | 0.00 BPM | 0 |

- Detector retained 50% of HR estimates in every test
- All estimates classified as incorrect were successfully flagged
- Detector unnecessarily rejected accurate estimates in two conditions
- Results demonstrate limitations of using IMU motion intensity alone

### Limitations
- Synthetic signals use simplified sinusoidal PPG and motion models
- Five test conditions share the same repeating motion schedule
- Motion intensity and PPG artifact amplitude are not always correlated
- Overlapping FFT windows are not independent observations
- Incorrect HR threshold (>12 BPM) may miss smaller but meaningful errors
- Results do not establish performance on real physiological recordings

### Next Steps
- Develop combined PPG and IMU frequency-domain features
- Investigate motion-related spectral overlap
- Reduce false positives without increasing false negatives
- Evaluate across additional synthetic conditions

## 2026-10-11 — Combined PPG + IMU Quality Assessment

### Objective
Determine whether combining PPG spectral features with IMU measurements
reduces unnecessary rejection of accurate heart-rate estimates.

### Implementation
- Extracted dominant PPG frequency using FFT
- Estimated dominant motion frequency from combined accelerometer-axis spectra
- Calculated PPG spectral energy near the estimated motion frequency
- Implemented combined motion and spectral-overlap detector
- Compared against the original motion-only detector across five synthetic datasets

### Results
| Metric | Motion-only | Combined |
|---|---:|---:|
| Incorrect estimates detected | 84/84 | 84/84 |
| False positives | 56 | 28 |
| False negatives | 0 | 0 |
| Precision | 60% | 75% |
| Recall | 100% | 100% |
| Overall retention | 50% | 60% |

- Eliminated all 28 false positives in the low-artifact test
- Preserved detection of incorrect HR estimates in the baseline,
  high-HR, and fast-motion tests
- Motion-near-HR condition still produced 28 false positives

### Limitations
- Results are from five synthetic development datasets
- Thresholds have not been independently validated
- Overlapping windows are not statistically independent
- Five-second FFT resolution limits separation of nearby frequencies
- Frequency agreement does not prove motion contamination
- Current evaluation measures HR accuracy rather than waveform quality

### Next Steps
- Evaluate unchanged detector thresholds on held-out synthetic recordings
- Investigate HR continuity and additional signal-quality features
- Test irregular motion and varying heart rates
- Validate with physical sensors