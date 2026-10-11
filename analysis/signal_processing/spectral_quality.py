"""
Extract PPG and IMU spectral features for motion-aware quality assessment.
"""

import numpy as np
from scipy.signal import detrend


def dominant_frequency(signal, fs, min_hz=0.5, max_hz=3.5):
    signal = np.asarray(signal, dtype=float)

    if len(signal) < 2:
        return np.nan, np.array([]), np.array([])

    signal = detrend(signal)
    window = np.hanning(len(signal))

    spectrum = np.abs(np.fft.rfft(signal * window)) ** 2
    frequencies = np.fft.rfftfreq(len(signal), d=1 / fs)

    valid = (frequencies >= min_hz) & (frequencies <= max_hz)

    if not np.any(valid):
        return np.nan, frequencies, spectrum

    peak_index = np.argmax(spectrum[valid])
    peak_frequency = frequencies[valid][peak_index]

    return peak_frequency, frequencies, spectrum


def extract_spectral_features(ppg, ax, ay, az, fs):
    ppg_freq, frequencies, ppg_power = dominant_frequency(
        ppg, fs, min_hz=40 / 60, max_hz=180 / 60
    )

    # Combine spectral power from all three acceleration axes.
    motion_power = None

    for axis in (ax, ay, az):
        _, motion_frequencies, axis_power = dominant_frequency(
            axis, fs, min_hz=0.5, max_hz=3.5
        )

        if motion_power is None:
            motion_power = axis_power
        else:
            motion_power += axis_power

    valid_motion = (
        (motion_frequencies >= 0.5)
        & (motion_frequencies <= 3.5)
    )

    motion_freq = motion_frequencies[valid_motion][
        np.argmax(motion_power[valid_motion])
    ]

    # Fraction of PPG spectral power near the IMU motion frequency.
    motion_band = np.abs(frequencies - motion_freq) <= 0.2
    hr_band = (frequencies >= 40 / 60) & (frequencies <= 180 / 60)

    total_power = np.sum(ppg_power[hr_band])

    overlap = (
        np.sum(ppg_power[motion_band & hr_band]) / total_power
        if total_power > 0 else 0.0
    )

    return {
        "ppg_freq_hz": ppg_freq,
        "motion_freq_hz": motion_freq,
        "frequency_difference_hz": abs(ppg_freq - motion_freq),
        "spectral_overlap": overlap,
    }

MOTION_THRESHOLD = 0.06
OVERLAP_THRESHOLD = 0.35
FREQUENCY_TOLERANCE_HZ = 0.25


def assess_spectral_quality(features, motion_score):
    motion_present = motion_score > MOTION_THRESHOLD

    frequency_match = (
        features["frequency_difference_hz"] <= FREQUENCY_TOLERANCE_HZ
    )

    strong_overlap = (
        features["spectral_overlap"] >= OVERLAP_THRESHOLD
    )

    return motion_present and frequency_match and strong_overlap

import pandas as pd

from windowed_hr import analyze_windows


WINDOW_SECONDS = 5
STEP_SECONDS = 1


def analyze_spectral_quality(df, expected_hr=72):
    results = analyze_windows(df, expected_hr=expected_hr)

    time_s = df["timestamp_ms"].to_numpy() / 1000
    fs = (len(time_s) - 1) / (time_s[-1] - time_s[0])

    window_size = int(WINDOW_SECONDS * fs)
    step_size = int(STEP_SECONDS * fs)

    features = []

    for start in range(0, len(df) - window_size + 1, step_size):
        end = start + window_size
        window = df.iloc[start:end]

        spectral = extract_spectral_features(
            window["ppg_ir"].to_numpy(),
            window["ax"].to_numpy(),
            window["ay"].to_numpy(),
            window["az"].to_numpy(),
            fs
        )

        features.append(spectral)

    feature_df = pd.DataFrame(features)

    results = pd.concat(
        [results.reset_index(drop=True), feature_df],
        axis=1
    )

    results["spectral_flag"] = results.apply(
        lambda row: assess_spectral_quality(
            row,
            row["motion_score"]
        ),
        axis=1
    )

    return results