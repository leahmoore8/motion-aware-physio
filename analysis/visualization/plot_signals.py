"""
Plot recorded PPG and IMU measurements.

Loads a sensor CSV recording and visualizes the PPG signals,
acceleration magnitude, and their relationship to motion.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_signals(csv_path: Path):
    df = pd.read_csv(csv_path)

    required_columns = [
        "timestamp_ms", "ppg_ir", "ppg_red",
        "ax", "ay", "az"
    ]

    if not all(col in df.columns for col in required_columns):
        raise ValueError("CSV is missing required sensor columns.")

    # Convert timestamps to seconds relative to the first sample.
    time_s = (df["timestamp_ms"] - df["timestamp_ms"].iloc[0]) / 1000

    # Compute acceleration magnitude from the three IMU axes.
    accel_mag = np.sqrt(
        df["ax"]**2 + df["ay"]**2 + df["az"]**2
    )

    fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)

    # PPG signals
    axes[0].plot(time_s, df["ppg_ir"], label="IR", linewidth=1)
    axes[0].plot(time_s, df["ppg_red"], label="Red", linewidth=1)
    axes[0].set_ylabel("PPG (raw counts)")
    axes[0].set_title("Synthetic PPG Signals")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # IMU acceleration
    axes[1].plot(time_s, df["ax"], label="X", linewidth=1)
    axes[1].plot(time_s, df["ay"], label="Y", linewidth=1)
    axes[1].plot(time_s, df["az"], label="Z", linewidth=1)
    axes[1].set_ylabel("Acceleration (g)")
    axes[1].set_title("IMU Acceleration")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    # Acceleration magnitude
    axes[2].plot(time_s, accel_mag, linewidth=1)
    axes[2].axhline(1.0, linestyle="--", alpha=0.5, label="1 g reference")
    axes[2].set_ylabel("Magnitude (g)")
    axes[2].set_xlabel("Time (s)")
    axes[2].set_title("Acceleration Magnitude")
    axes[2].legend()
    axes[2].grid(alpha=0.3)

    fig.suptitle(f"Motion-Aware Physiological Sensing — {csv_path.name}")
    plt.tight_layout()

    output_dir = Path(__file__).resolve().parents[2] / "docs" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "synthetic-signal-visualization.png"
    plt.savefig(output_path, dpi=150)

    print(f"Saved figure to: {output_path}")

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visualize recorded PPG and IMU signals."
    )

    parser.add_argument("csv_path", type=Path, help="Path to sensor CSV")

    args = parser.parse_args()

    plot_signals(args.csv_path)