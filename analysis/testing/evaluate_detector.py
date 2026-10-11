"""
Evaluate motion-aware HR reliability across synthetic test conditions.
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import the existing signal-processing pipeline.
analysis_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(analysis_dir / "signal_processing"))

from windowed_hr import analyze_windows
from motion_quality import assess_quality

from generate_synthetic import TEST_CASES


ERROR_TOLERANCE_BPM = 12


def evaluate_case(name, expected_hr):
    data_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "raw"
        / f"test_{name}.csv"
    )

    df = pd.read_csv(data_path)

    results = analyze_windows(df, expected_hr=expected_hr)
    results = assess_quality(results)

    incorrect = results["error_bpm"] > ERROR_TOLERANCE_BPM
    flagged = results["motion_flag"]

    tp = int((flagged & incorrect).sum())
    fp = int((flagged & ~incorrect).sum())
    fn = int((~flagged & incorrect).sum())
    tn = int((~flagged & ~incorrect).sum())

    accepted = results[~flagged]

    precision = tp / (tp + fp) if (tp + fp) else np.nan
    recall = tp / (tp + fn) if (tp + fn) else np.nan

    return {
        "test": name,
        "true_hr": expected_hr,
        "windows": len(results),
        "baseline_mae": results["error_bpm"].mean(),
        "accepted_mae": (
            accepted["error_bpm"].mean() if len(accepted) else np.nan
        ),
        "retention_pct": 100 * len(accepted) / len(results),
        "incorrect": int(incorrect.sum()),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "precision": precision,
        "recall": recall,
    }


def main():
    records = []

    for name, (hr, _, _) in TEST_CASES.items():
        records.append(evaluate_case(name, hr))

    summary = pd.DataFrame(records)

    print("\nSynthetic Evaluation Results")
    print(summary.round(2).to_string(index=False))

    output_dir = Path(__file__).resolve().parents[2] / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    summary.to_csv(output_dir / "synthetic_evaluation.csv", index=False)

    fig, ax = plt.subplots(figsize=(11, 5))

    x = np.arange(len(summary))
    width = 0.35

    ax.bar(
        x - width / 2,
        summary["baseline_mae"],
        width,
        color="#D9468F",
        label="Baseline FFT"
    )

    ax.bar(
        x + width / 2,
        summary["accepted_mae"],
        width,
        color="#2878B5",
        label="Accepted estimates"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(summary["test"], rotation=15)
    ax.set_ylabel("Mean Absolute HR Error (BPM)")
    ax.set_title("Synthetic HR Estimation: Baseline vs. Motion-Aware")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    figure_path = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "images"
        / "synthetic-evaluation.png"
    )

    plt.savefig(figure_path, dpi=150)
    print(f"\nSaved evaluation figure: {figure_path}")

    plt.show()


if __name__ == "__main__":
    main()