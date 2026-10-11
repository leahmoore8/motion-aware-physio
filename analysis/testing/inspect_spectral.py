"""
Inspect combined PPG and IMU spectral features on synthetic data.
"""

from pathlib import Path
import sys

import pandas as pd

analysis_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(analysis_dir / "signal_processing"))

from spectral_quality import analyze_spectral_quality


data_path = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "raw"
    / "test_baseline.csv"
)

df = pd.read_csv(data_path)
results = analyze_spectral_quality(df, expected_hr=72)

columns = [
    "time_s",
    "hr_bpm",
    "motion_score",
    "ppg_freq_hz",
    "motion_freq_hz",
    "frequency_difference_hz",
    "spectral_overlap",
    "spectral_flag",
]

print(results[columns].round(3).to_string(index=False))