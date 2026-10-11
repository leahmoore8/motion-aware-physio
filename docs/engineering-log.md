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