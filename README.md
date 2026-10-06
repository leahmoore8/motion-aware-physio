# Motion-Aware Physiological Sensing System

An embedded sensing platform for investigating the effects of
physical movement on wearable physiological measurements.

The system simultaneously acquires photoplethysmography (PPG)
and inertial measurement unit (IMU) data using an ESP32-based
embedded platform. Synchronized physiological and motion signals
are analyzed to characterize motion-induced artifacts and develop
real-time signal-quality assessment methods.

## System Architecture

MAX30102 PPG ─┐
              ├── ESP32-S3 ──> Data Acquisition ──> Signal Processing
MPU6050 IMU ──┘

## Initial Goals

1. Acquire synchronized PPG and IMU measurements.
2. Develop a reliable embedded data-acquisition pipeline.
3. Visualize and log sensor data in real time.
4. Characterize PPG behavior under different motion conditions.
5. Develop a real-time signal-quality assessment algorithm.

## Future Extensions

- Embedded DSP
- Motion-artifact detection
- Sensor fusion
- Edge ML
- BLE data transmission
- Custom PCB
- FPGA/RTL implementation of DSP components
