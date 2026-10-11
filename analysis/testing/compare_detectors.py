"""
Compare motion-only and combined PPG/IMU quality detectors.
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

analysis_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(analysis_dir / "signal_processing"))

from spectral_quality import analyze_spectral_quality
from generate_synthetic import TEST_CASES


ERROR_TOLERANCE_BPM = 12
MOTION_THRESHOLD = 0.06


def evaluate_flags(results, flags):
    incorrect = results["error_bpm"] > ERROR_TOLERANCE_BPM
    accepted = results[~flags]

    tp = int((flags & incorrect).sum())
    fp = int((flags & ~incorrect).sum())
    fn = int((~flags & incorrect).sum())
    tn = int((~flags & ~incorrect).sum())

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "retention_pct": 100 * len(accepted) / len(results),
        "accepted_mae": (
            accepted["error_bpm"].mean() if len(accepted) else np.nan
        ),
    }


def main():
    repo_root = Path(__file__).resolve().parents[2]
    records = []

    for name, (hr, _, _) in TEST_CASES.items():
        data_path = repo_root / "data" / "raw" / f"test_{name}.csv"
        df = pd.read_csv(data_path)

        results = analyze_spectral_quality(df, expected_hr=hr)

        motion_flags = results["motion_score"] > MOTION_THRESHOLD
        spectral_flags = results["spectral_flag"]

        for detector, flags in [
            ("Motion-only", motion_flags),
            ("Combined", spectral_flags),
        ]:
            metrics = evaluate_flags(results, flags)

            records.append({
                "test": name,
                "detector": detector,
                **metrics,
            })

    summary = pd.DataFrame(records)

    print("\nDetector Comparison")
    print(summary.round(2).to_string(index=False))

    output_dir = repo_root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_dir / "detector_comparison.csv", index=False)

    # Compare false positives between detectors.
    pivot = summary.pivot(
        index="test",
        columns="detector",
        values="fp"
    )

    x = np.arange(len(pivot))
    width = 0.35

    fig, ax = plt.subplots(figsize=(11, 5))

    ax.bar(
        x - width / 2,
        pivot["Motion-only"],
        width,
        color="#D9468F",
        label="Motion-only"
    )

    ax.bar(
        x + width / 2,
        pivot["Combined"],
        width,
        color="#2878B5",
        label="Combined PPG + IMU"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(pivot.index, rotation=15)
    ax.set_ylabel("False Positives")
    ax.set_title("Motion-Only vs. Combined Signal-Quality Detection")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    figure_path = repo_root / "docs" / "images" / "detector-comparison.png"
    plt.savefig(figure_path, dpi=150)

    print(f"\nSaved figure: {figure_path}")
    plt.show()


if __name__ == "__main__":
    main()