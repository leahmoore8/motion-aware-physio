#include <Arduino.h>

void setup() {
    Serial.begin(115200);
    delay(2000);

    Serial.println("================================");
    Serial.println("Motion-Aware Physiological Sensing");
    Serial.println("ESP32-S3 initialized!");
    Serial.println("================================");
}

void loop() {
    Serial.println("ESP32-S3 running...");
    delay(1000);
}