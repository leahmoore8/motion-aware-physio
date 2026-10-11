"""
Estimate heart rate from recorded PPG using frequency analysis.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import detrend


def estimate_hr(ppg, fs):
    # Remove the DC component and linear trend.
    signal = detrend(ppg)

    # Apply a Hann window to reduce spectral leakage.
    window = np.hanning(len(signal))
    spectrum = np.abs(np.fft.rfft(signal * window))

    # Compute FFT
    frequencies = np.fft.rfftfreq(len(signal), d=1 / fs)

    # Search within a plausible heart-rate range (40-180 BPM).
    valid = (frequencies >= 40 / 60) & (frequencies <= 180 / 60)

    peak_index = np.argmax(spectrum[valid])
    peak_frequency = frequencies[valid][peak_index]

    return peak_frequency * 60, frequencies, spectrum


def main(csv_path):
    df = pd.read_csv(csv_path)

    time_s = df["timestamp_ms"].to_numpy() / 1000
    ppg = df["ppg_ir"].to_numpy()

    fs = (len(time_s) - 1) / (time_s[-1] - time_s[0])

    hr, frequencies, spectrum = estimate_hr(ppg, fs)

    print(f"Sampling rate: {fs:.2f} Hz")
    print(f"Estimated heart rate: {hr:.1f} BPM")
    print("Expected synthetic heart rate: 72 BPM")

    plt.figure(figsize=(10, 5))
    plt.plot(frequencies * 60, spectrum, color="#D9468F")

    plt.xlim(40, 180)
    plt.xlabel("Frequency (BPM)")
    plt.ylabel("FFT magnitude")
    plt.title("PPG Frequency Spectrum")
    plt.axvline(72, color="gray", linestyle="--", label="Expected: 72 BPM")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    output_dir = Path(__file__).resolve().parents[2] / "docs" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_dir / "synthetic-ppg-spectrum.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate heart rate from PPG.")
    parser.add_argument("csv_path", type=Path)

    args = parser.parse_args()
    main(args.csv_path)