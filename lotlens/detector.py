"""Input validation and interpretable quality-drift detection."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "timestamp",
    "line_id",
    "batch_id",
    "shift",
    "units_inspected",
    "defect_count",
}
OPTIONAL_SIGNAL_COLUMNS = (
    "temperature_c",
    "vibration_mm_s",
    "pressure_bar",
)
CSV_TEMPLATE_COLUMNS = (
    "timestamp",
    "line_id",
    "batch_id",
    "shift",
    "units_inspected",
    "defect_count",
    *OPTIONAL_SIGNAL_COLUMNS,
    "operator_note",
)
REQUIRED_NUMERIC_COLUMNS = ("units_inspected", "defect_count")


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: list[str]
    data: pd.DataFrame | None = None


@dataclass(frozen=True)
class DetectionResult:
    status: str
    message: str
    baseline_rate_pct: float | None
    threshold_rate_pct: float | None
    current_rate_pct: float | None
    onset_time: str | None
    confirmed_time: str | None
    line_id: str | None
    batch_id: str | None
    baseline_points: int
    sustained_points: int
    evidence: list[dict[str, Any]]
    chart_data: pd.DataFrame

    def to_public_dict(self) -> dict[str, Any]:
        """Return only serializable, judge-visible calculated findings."""
        public = asdict(self)
        public.pop("chart_data", None)
        public["evidence"] = [dict(item) for item in self.evidence]
        return public


def validate_dataframe(data: pd.DataFrame) -> ValidationResult:
    """Normalize and validate the expected CSV shape.

    Inspection counts and production identifiers are required. Sensor context
    and operator notes may be omitted; blank sensor cells are preserved as NaN.
    """
    missing = sorted(REQUIRED_COLUMNS - set(data.columns))
    if missing:
        return ValidationResult(False, [f"Missing required columns: {', '.join(missing)}"])

    clean = data.copy()
    clean["timestamp"] = pd.to_datetime(clean["timestamp"], errors="coerce")
    bad_timestamps = int(clean["timestamp"].isna().sum())
    if bad_timestamps:
        return ValidationResult(False, [f"{bad_timestamps} row(s) have an invalid timestamp."])

    for column in REQUIRED_NUMERIC_COLUMNS:
        clean[column] = pd.to_numeric(clean[column], errors="coerce")
        if clean[column].isna().any():
            return ValidationResult(False, [f"Column `{column}` contains a missing or non-numeric value."])

    if not np.isfinite(clean[list(REQUIRED_NUMERIC_COLUMNS)].to_numpy(dtype=float)).all():
        return ValidationResult(False, ["Numeric readings must be finite values; infinity is not a valid measurement."])

    for column in OPTIONAL_SIGNAL_COLUMNS:
        if column not in clean:
            clean[column] = np.nan
            continue
        original = clean[column]
        numeric = pd.to_numeric(original, errors="coerce")
        has_text_value = original.notna() & original.astype(str).str.strip().ne("")
        if (has_text_value & numeric.isna()).any():
            return ValidationResult(False, [f"Column `{column}` contains a non-numeric value."])
        if not np.isfinite(numeric.dropna().to_numpy(dtype=float)).all():
            return ValidationResult(False, [f"Column `{column}` contains a non-finite value."])
        clean[column] = numeric

    if len(clean) < 12:
        return ValidationResult(False, ["At least 12 timestamped readings are needed to compare a baseline and monitored period."])

    if (clean["units_inspected"] <= 0).any():
        return ValidationResult(False, ["`units_inspected` must be greater than zero in every row."])

    if (clean["defect_count"] < 0).any():
        return ValidationResult(False, ["`defect_count` cannot be negative."])

    if (clean["defect_count"] > clean["units_inspected"]).any():
        return ValidationResult(False, ["`defect_count` cannot exceed `units_inspected`."])

    for column in ("units_inspected", "defect_count"):
        if not np.equal(clean[column], np.floor(clean[column])).all():
            return ValidationResult(False, [f"`{column}` must contain whole-number counts."])

    for column in ("line_id", "batch_id", "shift"):
        clean[column] = clean[column].fillna("").astype(str).str.strip()
        if (clean[column] == "").any():
            return ValidationResult(False, [f"`{column}` must be present in every row."])

    if clean["line_id"].nunique() != 1:
        return ValidationResult(False, ["This MVP analyzes one production line at a time. Filter the CSV to a single `line_id` before uploading."])

    if "operator_note" not in clean:
        clean["operator_note"] = ""
    clean["operator_note"] = clean["operator_note"].fillna("").astype(str)
    clean = clean.sort_values("timestamp").reset_index(drop=True)
    clean["defect_rate_pct"] = clean["defect_count"] / clean["units_inspected"] * 100
    return ValidationResult(True, [], clean)


def detect_quality_drift(
    data: pd.DataFrame,
    *,
    baseline_fraction: float = 0.60,
    min_change_pp: float = 2.0,
    sustained_points: int = 3,
) -> DetectionResult:
    """Detect a sustained increase in defect rate over an initial stable baseline.

    Threshold = baseline mean + max(3 population standard deviations,
    configured minimum change in percentage points). A qualifying alert needs
    `sustained_points` consecutive readings over that threshold.
    """
    validation = validate_dataframe(data)
    if not validation.valid or validation.data is None:
        raise ValueError(" ".join(validation.errors))

    clean = validation.data.copy()
    baseline_points = max(6, min(len(clean) - sustained_points, int(len(clean) * baseline_fraction)))
    baseline = clean.loc[: baseline_points - 1, "defect_rate_pct"]
    baseline_mean = float(baseline.mean())
    baseline_std = float(baseline.std(ddof=0))
    threshold = baseline_mean + max(3.0 * baseline_std, min_change_pp)
    clean["baseline_rate_pct"] = baseline_mean
    clean["threshold_rate_pct"] = threshold
    clean["above_threshold"] = clean["defect_rate_pct"] > threshold

    monitored = clean.iloc[baseline_points:]
    onset_position: int | None = None
    run = 0
    for index, above in zip(monitored.index.tolist(), monitored["above_threshold"].tolist()):
        run = run + 1 if above else 0
        if run >= sustained_points:
            onset_position = index - sustained_points + 1
            break

    latest = clean.iloc[-1]
    if onset_position is None:
        return DetectionResult(
            status="normal",
            message="No sustained increase above the configured defect-rate threshold was detected.",
            baseline_rate_pct=baseline_mean,
            threshold_rate_pct=threshold,
            current_rate_pct=float(latest["defect_rate_pct"]),
            onset_time=None,
            confirmed_time=None,
            line_id=str(latest["line_id"]),
            batch_id=None,
            baseline_points=baseline_points,
            sustained_points=sustained_points,
            evidence=[],
            chart_data=clean,
        )

    onset = clean.loc[onset_position]
    confirmed = clean.loc[onset_position + sustained_points - 1]
    first_evidence = clean.loc[onset_position : onset_position + sustained_points - 1]
    evidence = [
        {
            "timestamp": row["timestamp"].isoformat(),
            "batch_id": str(row["batch_id"]),
            "defect_count": int(row["defect_count"]),
            "units_inspected": int(row["units_inspected"]),
            "defect_rate_pct": round(float(row["defect_rate_pct"]), 2),
            "temperature_c": None if pd.isna(row["temperature_c"]) else round(float(row["temperature_c"]), 2),
            "vibration_mm_s": None if pd.isna(row["vibration_mm_s"]) else round(float(row["vibration_mm_s"]), 2),
            "pressure_bar": None if pd.isna(row["pressure_bar"]) else round(float(row["pressure_bar"]), 2),
            "operator_note": str(row["operator_note"]),
        }
        for _, row in first_evidence.iterrows()
    ]

    return DetectionResult(
        status="drift",
        message=f"Defect rate stayed above the configured threshold for {sustained_points} consecutive readings.",
        baseline_rate_pct=baseline_mean,
        threshold_rate_pct=threshold,
        current_rate_pct=float(latest["defect_rate_pct"]),
        onset_time=onset["timestamp"].isoformat(),
        confirmed_time=confirmed["timestamp"].isoformat(),
        line_id=str(onset["line_id"]),
        batch_id=str(onset["batch_id"]),
        baseline_points=baseline_points,
        sustained_points=sustained_points,
        evidence=evidence,
        chart_data=clean,
    )

