"""
Generate synthetic PPG and IMU recordings for algorithm testing.
"""

from pathlib import Path

import numpy as np
import pandas as pd


FS = 50
DURATION_S = 60
SEED = 42

TEST_CASES = {
    "baseline": (72, 2.0, 2500),
    "low_motion": (72, 2.0, 1000),
    "high_hr": (96, 2.0, 2500),
    "motion_near_hr": (90, 1.6, 2500),
    "fast_motion": (72, 2.5, 2500),
}


def generate_recording(hr_bpm, motion_hz, artifact_amplitude, seed=SEED):
    rng = np.random.default_rng(seed)

    t = np.arange(0, DURATION_S, 1 / FS)

    hr_hz = hr_bpm / 60

    # Alternate between 5 seconds stationary and 5 seconds moving.
    moving = (t % 10) >= 5

    pulse = np.sin(2 * np.pi * hr_hz * t)
    motion = moving * np.sin(2 * np.pi * motion_hz * t)

    ppg_ir = (
        82000
        + 1500 * pulse
        + artifact_amplitude * motion
        + rng.normal(0, 100, len(t))
    )

    ppg_red = (
        78000
        + 1100 * np.sin(2 * np.pi * hr_hz * t + 0.1)
        + 0.72 * artifact_amplitude * motion
        + rng.normal(0, 100, len(t))
    )

    ax = 0.02 + 0.4 * motion + rng.normal(0, 0.005, len(t))
    ay = 0.01 + 0.2 * motion + rng.normal(0, 0.005, len(t))
    az = 1.0 + 0.1 * motion + rng.normal(0, 0.005, len(t))

    gx = moving * 15 * np.cos(2 * np.pi * motion_hz * t)
    gy = moving * 8 * np.cos(2 * np.pi * motion_hz * t)
    gz = np.zeros_like(t)

    return pd.DataFrame({
        "timestamp_ms": np.round(t * 1000).astype(int),
        "ppg_ir": np.round(ppg_ir).astype(int),
        "ppg_red": np.round(ppg_red).astype(int),
        "ax": ax,
        "ay": ay,
        "az": az,
        "gx": gx,
        "gy": gy,
        "gz": gz,
    })


def main():
    output_dir = Path(__file__).resolve().parents[2] / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, (hr, motion_hz, amplitude) in TEST_CASES.items():
        df = generate_recording(hr, motion_hz, amplitude)

        output_path = output_dir / f"test_{name}.csv"
        df.to_csv(output_path, index=False)

        print(f"{name}: {len(df)} samples -> {output_path.name}")


if __name__ == "__main__":
    main()