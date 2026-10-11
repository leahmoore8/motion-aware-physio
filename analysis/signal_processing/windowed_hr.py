"""
Compare FFT-based heart-rate estimates across stationary and moving windows.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from estimate_hr import estimate_hr


WINDOW_SECONDS = 5
STEP_SECONDS = 1
EXPECTED_HR = 72


def analyze_windows(df):
    time_s = df["timestamp_ms"].to_numpy() / 1000
    ppg = df["ppg_ir"].to_numpy()

    ax = df["ax"].to_numpy()
    ay = df["ay"].to_numpy()
    az = df["az"].to_numpy()

    fs = (len(time_s) - 1) / (time_s[-1] - time_s[0])

    window_size = int(WINDOW_SECONDS * fs)
    step_size = int(STEP_SECONDS * fs)

    results = []

    for start in range(0, len(ppg) - window_size + 1, step_size):
        end = start + window_size

        window_ppg = ppg[start:end]

        hr, _, _ = estimate_hr(window_ppg, fs)

        accel_mag = np.sqrt(
            ax[start:end] ** 2
            + ay[start:end] ** 2
            + az[start:end] ** 2
        )

        motion_score = np.std(accel_mag)

        center_time = (time_s[start] + time_s[end - 1]) / 2

        results.append({
            "time_s": center_time - time_s[0],
            "hr_bpm": hr,
            "motion_score": motion_score,
            "error_bpm": abs(hr - EXPECTED_HR),
        })

    return pd.DataFrame(results)


def main(csv_path):
    df = pd.read_csv(csv_path)
    results = analyze_windows(df)

    print(results.round(2).to_string(index=False))

    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

    axes[0].plot(
        results["time_s"],
        results["hr_bpm"],
        marker="o",
        color="#D9468F",
        label="Estimated HR"
    )
    axes[0].axhline(
        EXPECTED_HR,
        linestyle="--",
        color="gray",
        label="Expected: 72 BPM"
    )
    axes[0].set_ylabel("Heart Rate (BPM)")
    axes[0].set_title("Windowed Heart-Rate Estimation")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].plot(
        results["time_s"],
        results["motion_score"],
        marker="o",
        color="#2878B5"
    )
    axes[1].set_ylabel("Motion Score (g)")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_title("IMU Motion Intensity")
    axes[1].grid(alpha=0.3)

    plt.tight_layout()

    output_dir = Path(__file__).resolve().parents[2] / "docs" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "synthetic-windowed-hr.png"
    plt.savefig(output_path, dpi=150)

    print(f"\nSaved figure to: {output_path}")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare HR estimates across time windows."
    )
    parser.add_argument("csv_path", type=Path)

    args = parser.parse_args()
    main(args.csv_path)