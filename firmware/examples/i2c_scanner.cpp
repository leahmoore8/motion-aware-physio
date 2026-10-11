#include <Arduino.h>
#include <Wire.h>

#define SDA_PIN 8
#define SCL_PIN 9

void setup() {
    Serial.begin(115200);
    delay(2000);

    Serial.println("Motion-Aware Physiological Sensing");
    Serial.println("M1: I2C Scanner");

    Wire.begin(SDA_PIN, SCL_PIN);
    Wire.setClock(100000);
}

void loop() {
    Serial.println("\nScanning I2C bus...");

    int deviceCount = 0;

    for (uint8_t address = 1; address < 127; address++) {
        Wire.beginTransmission(address);

        uint8_t error = Wire.endTransmission();

        if (error == 0) {
            Serial.print("Device found at 0x");

            if (address < 16) {
                Serial.print("0");
            }

            Serial.println(address, HEX);
            deviceCount++;
        }
    }

    if (deviceCount == 0) {
        Serial.println("No I2C devices detected.");
    } else {
        Serial.print("Total devices: ");
        Serial.println(deviceCount);
    }

    delay(3000);
}