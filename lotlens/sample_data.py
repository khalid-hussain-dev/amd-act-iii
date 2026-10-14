"""Repeatable synthetic manufacturing data for the LotLens demo."""

from __future__ import annotations

import pandas as pd


def build_sample_dataset(*, scenario: str = "drift") -> pd.DataFrame:
    """Return repeatable synthetic readings for the drift or stable scenario."""
    if scenario not in {"drift", "stable"}:
        raise ValueError("scenario must be 'drift' or 'stable'")

    timestamps = pd.date_range("2026-10-14 06:00", periods=48, freq="10min")
    records: list[dict[str, object]] = []

    for index, timestamp in enumerate(timestamps):
        affected = scenario == "drift" and index >= 32
        # Deterministic variation keeps the sample stable across app refreshes.
        defect_count = (1 if index % 5 else 2) if not affected else (5 + index % 3)
        temperature = 72.0 + (index % 4) * 0.25 + (4.5 if affected else 0.0)
        vibration = 2.05 + (index % 3) * 0.12 + (0.72 if affected else 0.0)
        pressure = 6.2 - (0.38 if affected else 0.0) + (index % 2) * 0.03

        records.append(
            {
                "timestamp": timestamp,
                "line_id": "LINE-04",
                "batch_id": "LOT-8042-B" if affected else "LOT-8042-A",
                "shift": "Morning",
                "temperature_c": round(temperature, 2),
                "vibration_mm_s": round(vibration, 2),
                "pressure_bar": round(pressure, 2),
                "units_inspected": 100,
                "defect_count": defect_count,
                "operator_note": (
                    "Slight finish variation observed at station 4"
                    if affected and index in (35, 40)
                    else ""
                ),
            }
        )

    return pd.DataFrame.from_records(records)

