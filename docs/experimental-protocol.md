# Experimental Protocol

## Objective

Investigate the effects of physical movement on PPG signal
quality using synchronized optical and inertial measurements.

## Hardware

- ESP32-S3-DevKitC-1-N16R8
- MAX30102 PPG sensor
- MPU6050 IMU

## Test Conditions

### 1. Stationary Baseline
- Sensor held stationary
- 60-second recording
- Evaluate baseline PPG waveform quality

### 2. Controlled Hand Movement
- Repeated lateral and vertical movements
- 60-second recording
- Compare PPG distortion with acceleration

### 3. Walking
- Normal walking pace
- 60-second recording
- Examine periodic motion artifacts

### 4. Higher-Motion Activity
- Faster arm movements
- 60-second recording
- Evaluate signal degradation under increased motion

## Measurements

- Raw infrared PPG
- Raw red PPG
- Three-axis acceleration
- Three-axis angular velocity
- Sample timestamps

## Evaluation

- Signal continuity
- PPG waveform quality
- Motion magnitude
- Pulse detection consistency
- Relationship between motion and signal distortion

## Notes

Sensor placement and contact pressure should be kept as
consistent as possible across experimental conditions.