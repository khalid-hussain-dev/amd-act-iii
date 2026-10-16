# Real-Data Pilot and Verification Guide

This guide explains how a data owner and quality lead can prepare an approved, sanitized dataset and manually review LotLens's current CSV workflow. The upload screen also contains a blank CSV template and field guide. The document is a procedure for review; it does not certify the detector for production control or replace the organization's data-protection review.

## Current verification status (15 October 2026)

- **Synthetic workflow checks: passed.** The uploaded-reading validator and drift detector, stable/no-alert behavior, mapped and unmapped Commerce cases, malformed inventory handling, Streamlit startup, CSV template, and sensor-free uploads were checked locally against synthetic scenarios and fixtures.
- **`LINE-04_Production_Quality_Log.csv`:** The user confirms that the byte-identical `lotlens_synthetic_manufacturing_data.csv` copy was derived from real factory data. The canonical LINE-04 file is bundled in the public repository because it backs the default scenario; the duplicate source-named copy remains local and Git-ignored. Treat the bundled file as a **factory-derived synthetic fixture**, not a raw factory export or independent factory dataset. Its transformation and relationship to actual operating conditions are not documented here.
- **Real-data pilot: limited and not production-validating.** The upload path and detector have been exercised on the factory-derived synthetic fixture, but its transformation, data-owner approval, and relationship to actual operating conditions are not documented here. This does not establish detector accuracy on independent factory history or validate the alert rule for production use.
- **Next concrete step:** Document the data owner's approval, transformation/sanitization method, and intended permitted uses. For an independent pilot, use an approved representative export with known normal/incident periods and record the human reference assessment. Matching inventory and open-orders CSVs are only needed if Commerce impact is also being reviewed.

The exact local verification outcomes are recorded in the [manual verification guide](LotLens%20--%20Manual%20Verification%20Guide.md). No production or operational conclusion should be inferred from the synthetic checks.

## What the current build supports

- LotLens opens with the bundled factory-derived synthetic LINE-04 fixture. Users can select the reproducible seeded-drift or stable synthetic scenario, or upload a production-readings CSV through **Upload CSV**. The current interface analyzes one production line per file.
- Optional Commerce context is supplied as two more CSVs: an inventory snapshot and aggregated unallocated open orders.
- The uploads and analysis state are held in the active Streamlit session. The app has no durable dataset store or live connection to MES, SCADA, QMS, ERP, or order systems.
- The detector is deterministic. It sorts readings by timestamp, uses the first 60% as the baseline, sets the alert threshold to `baseline mean + max(3 × population standard deviation, 2 percentage points)`, and alerts after three consecutive monitored readings above that threshold. This is the current demo rule, not a validated plant control limit.
- Packaged procedure excerpts are synthetic. The current app does not accept or retrieve a plant's actual SOP library.

## Data approval and handling

Before preparing files:

- Get approval from the data owner and the quality/process owner for the chosen time window, fields, and intended review.
- Use an approved private/local deployment for confidential material. The public demo is for synthetic or non-sensitive data only.
- Remove or replace employee names, customer information, device serials, facility details, and other identifying or restricted fields. Keep `operator_note` blank or redact it unless its content is approved for this use.
- Use pseudonymous line, batch, and SKU identifiers where practical. These identifiers and timestamps can still be sensitive.
- Generating an AMD brief sends the alert status, line and batch IDs, onset and confirmation timestamps, and retrieved procedure excerpts to the configured AMD endpoint. The adapter does not send raw sensor readings or inspection counts to the model. Only generate the brief if that metadata and the supplied excerpts are approved for that endpoint.
- Confirm the applicable hosting and endpoint data-handling terms with the organization. The app's lack of durable storage does not establish the host's or model provider's retention policy.

For the first pilot, use a narrow, read-only export and keep an approved copy in the organization's controlled environment. Do not connect a production system or let LotLens make an operational change.

## Prepare the production-readings CSV

Required columns:

```text
timestamp,line_id,batch_id,shift,units_inspected,defect_count
```

Optional context columns are `temperature_c`, `vibration_mm_s`, `pressure_bar`, and `operator_note`. They may be omitted or blank. The sensors are displayed as descriptive context; the alert rule uses inspection counts. The in-app **Download CSV template** includes both required and optional column headers.

| Column | Preparation guidance |
| --- | --- |
| `timestamp` | Use one consistent, parseable format and timezone for the entire file. Record the timezone and sampling cadence for the review. |
| `line_id` | Include exactly one line per file. Split multi-line exports before upload. |
| `batch_id` | Use the lot identifier associated with each reading. Keep the same pseudonymous ID in the inventory snapshot when assessing Commerce impact. |
| `shift` | Use a non-empty shift label for every row. |
| `temperature_c` (optional) | Numeric Celsius values. Convert from another unit before upload and record the conversion. |
| `vibration_mm_s` (optional) | Numeric mm/s values. Convert from another unit before upload and record the conversion. |
| `pressure_bar` (optional) | Numeric bar values. Convert from another unit before upload and record the conversion. |
| `units_inspected` | Positive whole-number count for each sample. |
| `defect_count` | Whole-number count from zero through `units_inspected`. Ensure the organization's definition of a defect matches the export. |
| `operator_note` (optional) | Optional text. Redact names, contact details, free-text customer data, and unapproved incident details. |

LotLens currently requires at least 12 valid rows, finite required numeric values, non-empty line/batch/shift fields, and one `line_id`. Supplied sensor values must be finite numbers, but sensor columns are optional. Do not combine different units, definitions of defect, timezones, or sampling processes in one file. Columns with different names or units must be mapped/converted before upload; the current MVP does not provide a source-column mapping wizard.

### Select a review window that fits the current detector

1. Select a time range whose early 60% is known to be a stable interval. The detector does not let the user choose a separate baseline window today.
2. Include later data that the quality owner can label as normal, drift, or a known incident. Do not choose the window after seeing LotLens's answer.
3. Preserve the source timestamps, row order context, and lot transitions. Record any removed rows, unit conversions, or resampling.
4. Have a quality/process owner confirm the target incident or confirm that the selected period has no known incident.

If the file cannot provide a credible stable first 60%, stop and do not interpret the resulting alert as a valid quality finding. The baseline and threshold are generic demo settings and must be calibrated and independently validated before operational use.

## Prepare Commerce snapshots (optional)

Inventory CSV header:

```text
sku,product_name,batch_id,on_hand_units,reserved_units
```

Open-orders CSV header:

```text
sku,unallocated_open_order_units
```

Include one inventory row per SKU/batch and one aggregated open-orders row per SKU. Counts must be non-negative whole numbers; `reserved_units` cannot exceed `on_hand_units`. The `batch_id` in the inventory file must exactly match a batch in the readings to map the alert. The `sku` must match between inventory and orders. Count only orders not already allocated to a lot in `unallocated_open_order_units` to avoid double-counting.

LotLens reports the rule-based snapshot calculation:

```text
clean available = sum(on_hand_units - reserved_units) across unaffected lots for the SKU
reallocation need = reserved units in the alerted lot + unallocated open-order units
reallocation capacity = min(clean available, reallocation need)
uncovered units = max(0, reallocation need - clean available)
```

This is a point-in-time review prompt. It is not a demand forecast, fulfillment promise, automated stock hold, order change, or replenishment action.

## Manual verification procedure

Do this with synthetic or approved, sanitized data in an authorized environment. Record the app version or commit and the data's non-sensitive source description. Do not attach the raw dataset to a public issue or submission.

### 1. Confirm the input was accepted

- Select **Upload CSV** and provide the prepared readings file.
- Confirm LotLens labels it **Uploaded dataset — origin not verified** and reports the expected reading count, line, batches, and time window.
- Compare those summary details with the approved export. If any differ, stop and fix the input before analysis.

### 2. Review Industry analysis against an independent reference

- Select **Run analysis**.
- Confirm the plotted readings, baseline, threshold, detected onset/confirmation, line, and affected batch are consistent with the chosen window and the fixed detector rule.
- Compare the finding with the quality owner's known incident record or documented review. Record any missed event, false alert, unexpected batch assignment, or baseline contamination.
- Treat the alert as an investigation lead only. Do not use it to release, hold, or alter product without the responsible human process.

### 3. Review optional Commerce impact

- Upload both matching Commerce snapshots.
- Check that the alert batch maps to the expected SKU and that affected on-hand/reserved counts agree with the source snapshot.
- Recalculate the unaffected available stock, reallocation need, uncovered units, and remaining clean units by hand for the selected SKU.
- Confirm the recommendation is a human-review prompt and no stock or order changed.
- For a separate negative case, use an inventory snapshot without the alerted batch and confirm LotLens requests a lot-to-SKU mapping. If either Commerce file is missing or invalid, confirm the Industry finding remains visible and the app explains what Commerce context is unavailable.

### 4. Review AMD brief handling (only if approved)

- Before selecting **Generate investigation brief**, confirm the endpoint is authorized to receive the pseudonymous line/batch IDs, alert times, and procedure excerpts.
- Confirm the displayed measured evidence remains rendered by the detector, separate from the model-written summary and checks.
- Check that any suggested checks cite visible sources and that uncertainty is stated. The current sources are synthetic, so do not present them as the plant's approved procedures.
- Confirm no raw temperature, vibration, pressure, defect counts, free-text notes, or credentials appear in the generated brief or a screenshot.

### 5. Record the review

Record the following in the manual verification log:

- Date, app commit/build, reviewer roles, and approved environment.
- A redacted description of the source, time range, timezone, sampling cadence, units, defect definition, and preprocessing.
- Whether the known incident/no-incident expectation was met, plus any false positives, missed events, or mapping discrepancies.
- For Commerce, the redacted SKU/lot mapping result and independently recalculated stock figures.
- Whether the AMD brief was generated; if so, note that its alert identifiers/timestamps and procedure excerpts were sent to the configured AMD endpoint. Never record the API key.

Screenshots should show the result and relevant context while hiding raw records, personal or proprietary identifiers, credentials, and browser/profile details.

## Stop conditions and limits

Stop the review and return to the data owner if the schema or units are ambiguous, the baseline contains a known incident, timestamps cannot be reconciled, lot-to-SKU mapping is uncertain, sensitive content remains, or the alert conflicts with the quality owner's reference without an understood reason.

A successful upload only demonstrates that the file path works. It does not validate the statistical rule, establish causation, prove a production-quality benefit, or make LotLens production-ready. Before an operational pilot, the team would need domain-reviewed baseline/threshold configuration, approved SOP retrieval, authenticated access, deployment and retention review, auditability, and a separately validated change-management process.
