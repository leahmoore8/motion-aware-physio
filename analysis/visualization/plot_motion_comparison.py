"""
Compare synthetic PPG measurements with IMU motion activity.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_comparison(csv_path: Path):
    df = pd.read_csv(csv_path)

    time_s = (df["timestamp_ms"] - df["timestamp_ms"].iloc[0]) / 1000

    accel_mag = np.sqrt(
        df["ax"]**2 + df["ay"]**2 + df["az"]**2
    )

    # Remove the mean to focus on the changing PPG component.
    ppg_ac = df["ppg_ir"] - df["ppg_ir"].mean()

    fig, ax1 = plt.subplots(figsize=(12, 5))

    ax1.plot(
        time_s, ppg_ac,
        color="#D9468F",
        linewidth=1.5,
        label="IR PPG (mean removed)"
    )
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("PPG (counts)")
    ax1.grid(alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(
        time_s, accel_mag,
        color="#0821B2",
        linewidth=1.2,
        alpha=0.75,
        label="Acceleration magnitude"
    )
    ax2.set_ylabel("Acceleration (g)")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    plt.title("Synthetic PPG vs. Motion Activity")
    plt.tight_layout()

    output_dir = Path(__file__).resolve().parents[2] / "docs" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "synthetic-motion-comparison.png"
    plt.savefig(output_path, dpi=150)

    print(f"Saved figure to: {output_path}")

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare PPG and IMU motion signals."
    )

    parser.add_argument("csv_path", type=Path)

    args = parser.parse_args()

    plot_comparison(args.csv_path)