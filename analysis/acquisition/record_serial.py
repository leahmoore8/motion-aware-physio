"""
Serial data acquisition for the motion-aware sensing system.

Reads timestamped PPG and IMU measurements from the ESP32
and saves a recording to CSV.
"""

import argparse
import csv
import time
from datetime import datetime
from pathlib import Path

import serial


COLUMNS = [
    "timestamp_ms",
    "ppg_ir",
    "ppg_red",
    "ax",
    "ay",
    "az",
    "gx",
    "gy",
    "gz",
]

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def record(port: str, duration: int, baud_rate: int = 115200):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = DATA_DIR / f"synthetic_{timestamp}.csv"

    sample_count = 0
    start_time = None

    with serial.Serial(port, baud_rate, timeout=1) as esp32:
        # Opening the port may reset the board.
        time.sleep(2)
        esp32.reset_input_buffer()

        print(f"Connected to {port}")
        print(f"Recording for {duration} seconds...")

        with output_path.open("w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(COLUMNS)

            while True:
                if start_time is not None:
                    if time.monotonic() - start_time >= duration:
                        break

                line = esp32.readline().decode("utf-8", errors="replace").strip()

                if not line or line.startswith("timestamp_ms"):
                    continue

                values = line.split(",")

                if len(values) != len(COLUMNS):
                    continue

                try:
                    int(values[0])
                    int(values[1])
                    int(values[2])

                    for value in values[3:]:
                        float(value)

                except ValueError:
                    continue

                if start_time is None:
                    start_time = time.monotonic()

                writer.writerow(values)
                sample_count += 1

    print(f"Recorded {sample_count} samples")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Record ESP32 sensor measurements to CSV."
    )

    parser.add_argument("--port", required=True, help="ESP32 serial port")
    parser.add_argument("--duration", type=int, default=30)

    args = parser.parse_args()

    record(args.port, args.duration)