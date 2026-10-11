/**
 * Motion-Aware Physiological Sensing
 * Synthetic sensor stream for testing serial acquisition.
 *
 * Output: timestamp_ms, ppg_ir, ppg_red, ax, ay, az, gx, gy, gz
 * Sample rate: 50 Hz
 */

#include <Arduino.h>
#include <math.h>

constexpr uint32_t SAMPLE_INTERVAL_MS = 20;
constexpr float HEART_RATE_HZ = 1.2f;

uint32_t nextSampleTime = 0;

void setup() {
    Serial.begin(115200);
    delay(2000);

    Serial.println("timestamp_ms,ppg_ir,ppg_red,ax,ay,az,gx,gy,gz");
    nextSampleTime = millis();
}

void loop() {
    uint32_t now = millis();

    if ((int32_t)(now - nextSampleTime) < 0) {
        return;
    }

    nextSampleTime += SAMPLE_INTERVAL_MS;

    float t = now / 1000.0f;
    float phase = 2.0f * PI * HEART_RATE_HZ * t;

    // Simulate movement during the second half of each 10-second cycle
    bool moving = fmodf(t, 10.0f) >= 5.0f;

    float motion = moving ? sinf(2.0f * PI * 2.0f * t) : 0.0f;

    // Synthetic optical measurements with movement-related distortion
    int32_t ppgIr = 82000 + 1500 * sinf(phase) + 2500 * motion;
    int32_t ppgRed = 78000 + 1100 * sinf(phase + 0.1f) + 1800 * motion;

    // Acceleration in g; angular velocity in degrees/second
    float ax = 0.02f + 0.4f * motion;
    float ay = 0.01f + 0.2f * motion;
    float az = 1.0f + 0.1f * motion;

    float gx = moving ? 15.0f * cosf(2.0f * PI * 2.0f * t) : 0.0f;
    float gy = moving ? 8.0f * cosf(2.0f * PI * 2.0f * t) : 0.0f;
    float gz = 0.0f;

    Serial.printf(
        "%lu,%ld,%ld,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f\n",
        (unsigned long)now,
        (long)ppgIr,
        (long)ppgRed,
        ax, ay, az,
        gx, gy, gz
    );
}