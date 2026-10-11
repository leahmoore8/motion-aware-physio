# Motion-Aware Physiological Sensing System
## Development Roadmap

**Hardware:** ESP32-S3-DevKitC-1-N16R8, MAX30102 PPG, MPU6050 IMU

**Software:** C/C++ (Arduino/PlatformIO), Python, Git/GitHub

**Objective:** Develop an embedded sensing platform that acquires
synchronized physiological and motion measurements, investigates
motion-induced artifacts in PPG signals, and implements motion-aware
signal-quality assessment.

---

## M0 — Development Environment & ESP32 Bring-Up

**Goal:** Establish the embedded development environment and verify
successful firmware execution.

- [x] Create GitHub repository
- [x] Clone repository locally
- [x] Initialize project directory structure
- [x] Configure `.gitignore`
- [x] Install VS Code + PlatformIO
- [x] Create PlatformIO firmware project
- [x] Configure ESP32-S3 board and Arduino framework
- [x] Compile initial firmware
- [x] Upload firmware to ESP32-S3
- [x] Verify USB serial communication at 115200 baud
- [x] Document M0 in engineering log
- [x] Commit and push M0

**Deliverable:** ESP32-S3 successfully executes firmware and
transmits periodic status messages over USB serial.

---

## M1 — MPU6050 IMU Bring-Up

**Goal:** Establish I2C communication and acquire motion measurements.

- [ ] Solder MPU6050 header pins
- [ ] Document MPU6050 wiring and ESP32 GPIO assignments
- [ ] Connect MPU6050 to ESP32-S3
- [ ] Implement I2C bus scanner
- [ ] Detect MPU6050 at expected address (typically `0x68`)
- [ ] Initialize MPU6050 accelerometer and gyroscope
- [ ] Read raw accelerometer and gyroscope measurements
- [ ] Convert raw measurements to physical units (g, deg/s)
- [ ] Verify measurements under stationary conditions
- [ ] Verify measurements while rotating/moving sensor
- [ ] Document M1 results and issues
- [ ] Commit and push M1

**Deliverable:** ESP32-S3 continuously acquires and displays
3-axis acceleration and 3-axis angular velocity.

---

## M2 — MAX30102 PPG Bring-Up

**Goal:** Acquire raw optical physiological measurements.

- [ ] Solder MAX30102 header pins
- [ ] Verify breakout power requirements and pinout
- [ ] Document MAX30102 wiring
- [ ] Connect MAX30102 to ESP32-S3
- [ ] Detect MAX30102 over I2C (typically `0x57`)
- [ ] Configure red and infrared LED measurements
- [ ] Read raw PPG samples
- [ ] Verify optical response with and without finger contact
- [ ] Record a stationary PPG waveform
- [ ] Identify a visible pulsatile component
- [ ] Document M2 results and issues
- [ ] Commit and push M2

**Deliverable:** ESP32-S3 successfully acquires raw red/IR PPG
measurements from the MAX30102.

---

## M3 — Multi-Sensor Integration

**Goal:** Acquire synchronized PPG and IMU data.

- [ ] Connect both sensors to shared I2C bus
- [ ] Verify both I2C addresses are detected
- [ ] Initialize both sensors in firmware
- [ ] Select and document sampling rates
- [ ] Implement timestamped sensor acquisition
- [ ] Implement nonblocking acquisition where practical
- [ ] Define serial data format
- [ ] Stream PPG and IMU measurements over USB
- [ ] Check for missing samples and timing irregularities
- [ ] Document M3 results
- [ ] Commit and push M3

**Target data fields:**

`timestamp_ms,ppg_ir,ppg_red,ax,ay,az,gx,gy,gz`

**Note:** Define how measurements from different sensor rates
are aligned before treating each row as synchronized.

**Deliverable:** ESP32-S3 streams timestamped physiological and
motion measurements in a consistent format.

---

## M4 — Python Data Acquisition & Logging

**Goal:** Receive and store sensor data on Mac.

- [x] Create Python virtual environment
- [x] Add dependencies to `analysis/requirements.txt`
- [x] Implement serial communication using `pyserial`
- [x] Parse ESP32 data stream
- [x] Validate incoming measurements
- [x] Save timestamped measurements to CSV
- [ ] Handle serial disconnects and malformed packets
- [ ] Verify recorded data integrity
- [ ] Document acquisition workflow
- [x] Commit and push M4

**Deliverable:** Python application records experimental sensor
data into CSV files for offline analysis.

---

## M5 — Real-Time Visualization

**Goal:** Visualize physiological and motion measurements.

### Offline Visualization (Synthetic Data)
- [x] Implement offline PPG visualization from recorded CSV
- [x] Implement accelerometer magnitude calculation
- [x] Plot acceleration magnitude over time
- [x] Align PPG and IMU plots on common time axis
- [x] Compare synthetic PPG distortion with IMU acceleration
- [x] Save figures of working plots

### Real-Time Visualization
- [ ] Implement real-time PPG plotting
- [ ] Implement rolling visualization window
- [ ] Add gyroscope visualization if useful
- [ ] Verify visualization during physical movement

### Documentation
- [x] Document M5 offline visualization results
- [ ] Commit and push offline visualization

**Deliverable:** Live visualization of physiological waveforms
and corresponding motion measurements.

---

## M6 — Experimental Data Collection

**Goal:** Investigate the relationship between movement and
PPG signal quality.

- [ ] Define experimental protocol
- [ ] Record stationary baseline
- [ ] Record controlled hand/wrist movements
- [ ] Record walking measurements
- [ ] Record higher-motion conditions if feasible
- [ ] Keep sensor placement consistent
- [ ] Label recordings by movement condition
- [ ] Record sampling rates and experiment durations
- [ ] Evaluate data completeness and sensor saturation
- [ ] Create representative plots for each condition
- [ ] Document observations
- [ ] Commit and push M6

**Deliverable:** Labeled experimental dataset demonstrating
PPG behavior under different motion conditions.

---

## M7 — Digital Signal Processing

**Goal:** Extract useful physiological features and investigate motion artifacts.

### Frequency Analysis & Heart-Rate Estimation
- [x] Inspect PPG signal frequency content using FFT
- [x] Implement baseline FFT-based heart-rate estimation
- [x] Implement sliding-window HR estimation (5 s windows, 1 s steps)
- [x] Compare HR estimates across synthetic stationary and moving intervals
- [ ] Estimate baseline noise and signal variability
- [ ] Implement PPG filtering
- [ ] Detect candidate pulse peaks
- [ ] Compare FFT-based and peak-based HR estimation

### Motion & Signal Processing
- [x] Extract initial IMU motion feature (acceleration magnitude variability)
- [x] Identify motion-related frequency components in synthetic PPG
- [x] Quantify HR estimation error during simulated movement
- [ ] Compare pulse detection across movement conditions
- [ ] Investigate frequency-domain motion artifact reduction
- [ ] Compare raw and processed waveforms
- [ ] Validate DSP pipeline with physical sensor data

### Documentation
- [x] Document initial synthetic FFT and HR estimation results
- [ ] Document filtering, peak detection, and final DSP results
- [ ] Commit and push completed M7

**Deliverable:** Signal-processing pipeline with physiological and motion-derived features.

---

## M8 — Motion-Aware Signal Quality Assessment

**Goal:** Develop an algorithm that evaluates PPG reliability using physiological and motion measurements.

### Initial Motion-Aware Algorithm
- [x] Develop initial IMU motion feature (standard deviation of acceleration magnitude)
- [x] Implement threshold-based motion reliability flagging
- [x] Visualize accepted and flagged HR estimates over time
- [x] Compare flagged estimates against known synthetic HR ground truth
- [x] Calculate initial accepted and flagged HR estimation errors
- [x] Evaluate false positives and false negatives on initial synthetic recording

### Algorithm Development & Evaluation
- [ ] Define broader signal-quality criteria
- [ ] Design baseline PPG-only quality assessment
- [ ] Develop additional motion-related features
- [ ] Define GOOD / MODERATE / POOR quality categories
- [ ] Establish an evaluation protocol with labeled examples
- [ ] Generate synthetic datasets with varying HR, motion frequency, and artifact amplitude
- [ ] Evaluate performance across multiple synthetic conditions using a fixed threshold
- [ ] Compare PPG-only and motion-aware approaches
- [ ] Investigate threshold selection and generalization
- [ ] Validate algorithm using physical sensor recordings

### Documentation
- [x] Document initial algorithm results and limitations
- [ ] Document multi-condition evaluation and final algorithm performance
- [ ] Commit and push completed M8

**Deliverable:** Motion-aware algorithm that identifies potentially unreliable physiological measurements.

---

## M9 — Final Validation & Documentation

**Goal:** Produce a reproducible, portfolio-ready engineering project.

- [ ] Verify complete end-to-end system
- [ ] Conduct repeatable validation experiments
- [ ] Summarize quantitative results
- [ ] Create system architecture diagram
- [ ] Document hardware wiring and component selection
- [ ] Add prototype photos
- [ ] Add representative waveform and analysis plots
- [ ] Update README with setup and usage instructions
- [ ] Document known limitations
- [ ] Record short system demonstration
- [ ] Commit and push final documentation

**Deliverable:** Reproducible embedded sensing system with
documented hardware, firmware, analysis, experiments, and results.

---

## Optional Extensions

These are not required for V1.

- [ ] Implement on-device PPG filtering
- [ ] Implement real-time signal-quality assessment on ESP32
- [ ] Benchmark execution time and memory usage
- [ ] Explore lightweight embedded ML
- [ ] Design a custom PCB
- [ ] Explore FPGA-based DSP implementation
- [ ] Add wireless data transmission
- [ ] Investigate adaptive motion-artifact cancellation