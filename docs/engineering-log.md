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