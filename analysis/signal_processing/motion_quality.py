"""
Assess PPG heart-rate reliability using IMU motion intensity.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from windowed_hr import analyze_windows


MOTION_THRESHOLD = 0.06
EXPECTED_HR = 72


def assess_quality(results):
    results = results.copy()

    results["motion_flag"] = results["motion_score"] > MOTION_THRESHOLD
    results["hr_reliable"] = ~results["motion_flag"]

    return results


def main(csv_path):
    df = pd.read_csv(csv_path)

    results = analyze_windows(df)
    results = assess_quality(results)

    reliable = results[results["hr_reliable"]]
    flagged = results[~results["hr_reliable"]]

    print(f"Total windows: {len(results)}")
    print(f"Reliable windows: {len(reliable)}")
    print(f"Flagged windows: {len(flagged)}")

    if not reliable.empty:
        print(f"Mean HR error (accepted): {reliable['error_bpm'].mean():.2f} BPM")

    if not flagged.empty:
        print(f"Mean HR error (flagged): {flagged['error_bpm'].mean():.2f} BPM")

    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

    # Heart-rate estimates, separated by reliability classification.
    axes[0].scatter(
        reliable["time_s"],
        reliable["hr_bpm"],
        color="#D9468F",
        label="Accepted",
        s=55
    )

    axes[0].scatter(
        flagged["time_s"],
        flagged["hr_bpm"],
        color="#D97706",
        marker="x",
        label="Flagged",
        s=65
    )

    axes[0].axhline(
        EXPECTED_HR,
        linestyle="--",
        color="gray",
        label="Expected: 72 BPM"
    )

    axes[0].set_ylabel("Heart Rate (BPM)")
    axes[0].set_title("Motion-Aware Heart-Rate Reliability")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # IMU motion intensity and detection threshold.
    axes[1].plot(
        results["time_s"],
        results["motion_score"],
        color="#2878B5",
        marker="o"
    )

    axes[1].axhline(
        MOTION_THRESHOLD,
        color="#D97706",
        linestyle="--",
        label=f"Threshold: {MOTION_THRESHOLD} g"
    )

    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Motion Score (g)")
    axes[1].set_title("IMU-Based Motion Detection")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.tight_layout()

    output_dir = Path(__file__).resolve().parents[2] / "docs" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "synthetic-motion-quality.png"
    plt.savefig(output_path, dpi=150)

    print(f"Saved figure to: {output_path}")

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Assess motion-related PPG signal reliability."
    )
    parser.add_argument("csv_path", type=Path)

    args = parser.parse_args()
    main(args.csv_path)