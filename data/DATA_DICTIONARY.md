# LotLens Synthetic Dataset — Data Dictionary

This document describes the reproducible samples created by `lotlens/sample_data.py`. Every row is synthetic and intended only for the LotLens demo. The values are not factory measurements, operating limits, or validated process-control guidance.

## Dataset profile

- **Rows:** 48 readings.
- **Time spacing:** 10 minutes, beginning at 06:00 on 14 October 2026. Timestamps have no timezone attached.
- **Production line:** `LINE-04` for every row.
- **Shift:** `Morning` for every row.
- **Seeded drift scenario:** Rows 1–32 use lot `LOT-8042-A`; rows 33–48 use lot `LOT-8042-B`. The sample generator raises defect counts and changes temperature, vibration, and pressure at row 33.
- **Stable scenario:** All 48 readings use lot `LOT-8042-A`; the periodic synthetic readings continue without the seeded change.
- **Inspection size:** 100 units per reading.
- **Reproducibility:** Values use deterministic index-based patterns; no random seed or external source data is used.

## Fields

| Column | Type | Unit / format | Synthetic behavior | Validation / interpretation |
|---|---|---|---|---|
| `timestamp` | datetime | ISO-compatible timestamp; no timezone | 10-minute increments | Must parse. LotLens sorts readings by this field. |
| `line_id` | string | Identifier | Always `LINE-04` | Required and non-empty. |
| `batch_id` | string | Lot identifier | `LOT-8042-A` before the change; `LOT-8042-B` from row 33 | Required and non-empty. |
| `shift` | string | Shift label | Always `Morning` | Required and non-empty. |
| `temperature_c` | number | °C | Cycles through 72.00–72.75 in the stable interval; adds 4.50 °C in the drift interval | Must be numeric. These are illustrative values, not approved operating limits. |
| `vibration_mm_s` | number | mm/s | Cycles through 2.05–2.29 in the stable interval; adds 0.72 mm/s in the drift interval | Must be numeric. These are illustrative values, not approved operating limits. |
| `pressure_bar` | number | bar | Alternates between 6.20 and 6.23 in the stable interval; subtracts 0.38 bar in the drift interval | Must be numeric. These are illustrative values, not approved operating limits. |
| `units_inspected` | integer-like number | units | Always 100 | Must be a whole number greater than zero. |
| `defect_count` | integer-like number | units | Stable interval cycles through counts of 1 and 2; drift interval cycles through counts of 5, 6, and 7 | Must be a whole number, non-negative, and no greater than `units_inspected`. |
| `operator_note` | string | Free text | Blank except two synthetic notes in the drift interval | Optional; the validator converts missing values to an empty string. The notes do not establish a cause. |

## Derived measure

LotLens calculates each row's inspection defect rate from counts:

```text
defect_rate_pct = defect_count / units_inspected * 100
```

The sample detector uses the first 60% of timestamp-sorted readings as its baseline. It sets the threshold to the baseline mean plus the larger of three population standard deviations or 2 percentage points. An alert requires three consecutive monitored readings above that threshold. These settings are demo logic, not validated industrial quality-control limits.

## CSV use

Keep the column names and units unchanged when preparing a compatible CSV. Do not combine readings from different units, sampling intervals, or timezones without documenting the conversion. Use synthetic or non-sensitive data for the hackathon demo.
