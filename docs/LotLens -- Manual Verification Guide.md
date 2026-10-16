# LotLens — Manual Verification Guide

This document records the user's completed manual reviews of the local and deployed LotLens builds on 14 October 2026. The steps and expected results below are retained so the same checks can be repeated after material changes. Do not include the AMD API key, screenshots of secrets, or real factory data in any report.

**Verification owner:** User  
**Date performed:** 14 October 2026  
**Build/revision:** Local working tree; no Git revision was recorded. The project root was not a Git repository at the time of review.  
**Local review status:** Passed — all listed local manual checks completed; the AMD brief passed its focused content review.
**Hosted review status:** Passed — the user reports that the deployed project worked as expected, including AMD-generated brief output. This is a user-reported result; Codex did not independently access or rerun the hosted app.

**Implementation update (17 October 2026):** The app now defaults to the bundled factory-derived synthetic LINE-04 fixture, uses the supplied LotLens lockup and favicon, and packages its runtime assets and fixture for GitHub and Docker checkouts. These latest UI and packaging changes have not been manually reviewed yet.

## 1. Run LotLens locally

Open PowerShell and run:

```powershell
Set-Location "E:\Hackathons\LabLabAI\AMD Developers ACT III"
python --version
```

Python should be version 3.11 or newer. For the first run, create and prepare the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

For later runs, skip the `venv` creation and package installation; activate the existing environment:

```powershell
Set-Location "E:\Hackathons\LabLabAI\AMD Developers ACT III"
.\.venv\Scripts\Activate.ps1
```

Start the app:

```powershell
streamlit run app.py
```

Open the local address Streamlit prints, normally `http://localhost:8501`. Keep the PowerShell window open while using the app. Stop it with **Ctrl+C** in that window.

If PowerShell blocks activation, allow it only for the current PowerShell process, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

The project `.env` is loaded on app startup. If you added or changed its settings while the app was already open, select **Reload AMD settings from .env** in the sidebar. Never paste the API key into chat or include it in a screenshot.

## 2. Record each result

For each verification ID, mark **Pass**, **Fail**, or **Blocked** and add a brief observation. **Blocked** means you could not perform the step, such as a network or account issue. A failure message is useful evidence; do not retry by changing or sharing the API key.

### MV-01 — App starts and sample data is ready

**Do this:** Start LotLens as described above. Leave **Data source** set to **Sample scenario** and leave the scenario at **Seeded drift**. Do not run analysis yet.

**Expected:** The page identifies the data as synthetic. It shows 48 readings, line `LINE-04`, two batches, and the time window. The page says the dataset is ready and offers **Run analysis**. No result is shown until you run it.

**Result:** Pass  
**Notes:** Ran as expected.

### MV-02 — Stable scenario produces no alert

**Do this:** Select **Stable process**, click **Run analysis**, and wait for the result.

**Expected:** Status says **No qualifying drift** (or equivalent). There is no affected batch, onset, or confirmation time. The trend remains visible, and the page explains that no qualifying sustained increase was found under the configured rule.

**Result:** Pass  
**Notes:** Ran as expected; stable scenario produced no alert.

### MV-03 — Seeded scenario detects the intended drift

**Do this:** Select **Seeded drift** and click **Run analysis**.

**Expected:** Status says **Drift detected**. The affected line is `LINE-04`, the affected batch is `LOT-8042-B`, the onset is about **Oct 14, 11:20**, and confirmation is about **Oct 14, 11:40**. The chart marks the baseline, threshold, and change point. The finding should confirm three sustained threshold crossings. Times are shown in the fixture's timestamp values.

**Result:** Pass  
**Observed line / batch / onset / confirmation:** `LINE-04` / `LOT-8042-B` / Oct 14, 11:20 / Oct 14, 11:40.  
**Observed metrics:** Baseline 1.21%; threshold 3.21%; latest 7.00%; first 28 readings used for baseline.  
**Notes:** Ran as expected; onset matched the seeded change and confirmation followed 20 minutes later.

### MV-04 — Sensor context remains descriptive

**Do this:** With the seeded result visible, expand **Inspect machine signal context**. Select Temperature, Vibration, and Pressure one at a time.

**Expected:** Each selection updates the sensor trend and labels the signal and units. The caption explains that these signals are contextual and are not the detector's alert rule or operating limits.

**Result:** Pass  
**Notes:** Ran as expected.

### MV-05 — Evidence, sources, and handoff are inspectable

**Do this:** Review **Alert evidence** and **Procedure references**, expand **Inspect input readings**, and download **shift handoff**. Open the downloaded text file.

**Expected:** The alert evidence contains the three supporting readings and their rates. Procedure excerpts have source IDs and are labeled synthetic. The handoff includes status, lot, onset/confirmation, baseline/threshold, supporting readings, procedure excerpts, data provenance, and the human-review limitation. It must not describe a confirmed cause or an action taken.

**Result:** Pass  
**Notes:** Ran as expected. The shift handoff was downloaded in the hackathon folder; procedure references were present.

### MV-06 — AMD brief works with the configured key

**Do this:** Keep **Seeded drift** selected and the analysis result visible. If AMD is still shown as awaiting configuration, select **Reload AMD settings from .env**. Confirm the sidebar says AMD inference is ready, then click **Generate investigation brief** once and wait for the response.

**Expected:** A generated summary, possible checks (if supported by the procedures), uncertainty, and endpoint-reported model attribution appear. The calculated alert facts remain separate from the model-written text. For each suggested check, its source ID matches one of the visible procedure references. No key or authorization header appears in the UI.

**Review carefully:** Flag any invented measurement, unsupported cause, unsupported recommendation, incorrect source ID, or missing uncertainty. AMD may return a model attribution that includes a version suffix; record it exactly as displayed.

**Initial call:** Pass for connectivity and brief rendering. The initial brief made an unsupported “within typical ranges” claim, which prompted a narrower request context and stricter model instructions.  
**Retest:** Pass. The brief identified the alert without restating measurements, cited OPS-04 §2.6 and QSP-17 §4.2/§4.3 for its possible checks, stated that no root cause was established, and did not claim sensor readings were normal or within a range.  
**Displayed model:** `self-dploy/DeepSeek-V4-Flash`  
**Tokens:** 892  
**Review notes:** The summary and possible checks preserve human decision authority. No unsupported sensor-range claim was present in the retest.

If the request fails, record the exact user-facing error text and mark this step **Fail** or **Blocked** as appropriate. The deterministic alert, evidence, and handoff should remain available. Do not include secrets, request headers, or private account details in the report.

### MV-07 — Valid CSV upload works

**Do this:** Return to **Sample scenario**, choose **Stable process**, and download its sample CSV. Then choose **Upload CSV** and upload that downloaded file. Run the analysis.

**Expected:** The page labels the input as uploaded data with unverified origin, shows its reading count and time window, and produces the same no-drift result as MV-02. The input readings remain inspectable.

**Result:** Pass  
**Notes:** Ran as expected.

### MV-08 — Invalid CSVs are explained as input issues

Make each malformed file from a copy of the downloaded sample CSV; keep all files synthetic.

1. **Missing field:** Remove the required `shift` column and upload. Expected: a missing required column message; no quality finding. (Earlier manual runs tested `operator_note` as required; it is now optional.)
2. **Too few readings:** Keep only 11 data rows and upload. Expected: an insufficient-evidence message explaining that at least 12 readings are needed.
3. **Multiple production lines:** Change `line_id` on one data row so the file has two line IDs. Expected: a message that this MVP analyzes one production line at a time.
4. **Malformed or incomplete CSV (optional):** Upload a plain-text file saved with a `.csv` extension. Expected: either a parsing/input-format error or a missing-required-columns message, never a production alert.

After each case, return to **Sample scenario** and confirm the valid built-in flow is still usable.

**Result:** Pass  
**Notes by case (1–4) at the time of the original review:** All ran as expected. Case 1 reported missing `operator_note` under the older schema; case 2 reported insufficient evidence (at least 12 readings); case 3 reported the one-line restriction; case 4 reported missing required columns, which is an acceptable input-validation response. The current build makes notes optional; the required-field case now uses `shift`.

### MV-09 — Analysis changes when the selected dataset changes

**Do this:** Run analysis on **Seeded drift**, then switch to **Stable process**.

**Expected:** The old drift result and generated brief disappear for the changed scenario until **Run analysis** is selected again. After running, the stable result shows no qualifying drift. This confirms that an earlier result is not shown as if it belongs to the newly selected data.

**Result:** Pass  
**Notes:** Ran as expected.

## 3. User review for the Reinvent Commerce extension

The Commerce panel was added after the Track 1 review recorded above. The user reviewed MV-COM-01 and MV-COM-02 in the local app on 14 October 2026. The user then exercised the uploaded-data Commerce workflow for MV-COM-03 with the synthetic CSV fixtures on 14 October 2026. No real factory data was used.

### MV-COM-01 — Seeded quality drift maps to stock

**Do this:** Select **Sample scenario → Seeded drift** and run the analysis.

**Expected:** The Commerce panel maps `LOT-8042-B` to `ACT-HSG-04`. It reports 180 affected on-hand units, 65 already reserved, 230 available units in the unaffected lot, 120 unallocated open-order units, a total reallocation need of 185 units, 0 uncovered units, and 45 clean units left after the proposed allocation. The recommendation is clearly for human review and says no inventory or order is changed.

**Result:** Pass — user reviewed screenshot on 14 October 2026. The panel showed the expected batch/SKU mapping and inventory figures: 180 affected, 65 reserved, 230 unaffected available, 120 unallocated orders, 185 total need, 0 uncovered, and 45 clean units remaining. The recommendation requires human approval and states that inventory and orders are not changed.

### MV-COM-02 — Stable scenario has no implicated lot

**Do this:** Select **Sample scenario → Stable process** and run the analysis.

**Expected:** The Industry panel reports no qualifying drift, and the Commerce panel says no lot is currently implicated. It must not recommend holding either sample lot.

**Result:** Pass — user reviewed screenshot on 14 October 2026. LotLens reported no qualifying sustained drift and no lot currently implicated; it did not recommend holding either sample lot.

### MV-COM-03 — Uploaded alert requires matching commerce snapshots

**Do this:** Upload production readings that produce an alert, then provide an inventory snapshot and open-orders CSV using the schemas in the [Commerce data dictionary](../data/COMMERCE_DATA_DICTIONARY.md). Include one case where the alert batch is mapped and another where it is missing from inventory.

**Expected:** A mapped batch shows the corresponding SKU impact. An unmapped batch requests a lot-to-SKU mapping. If either Commerce file is absent or invalid, LotLens explains that Commerce context is unavailable while retaining the Industry result.

**Result:** Pass — user screenshots on 14 October 2026 showed all three uploaded-data cases: the mapped alert displayed SKU-level inventory impact; the unmapped alert requested a lot-to-SKU mapping; and an invalid inventory schema produced a clear warning while the Industry chart and alert evidence remained visible. The missing-file prompt is present in the app, but a missing-file screenshot was not provided; the invalid-file case satisfies the guide's absent-or-invalid fallback check.

**Build/revision at time of user screenshots:** Local working tree based on `509445f`, with Commerce changes not yet committed; those changes were committed as `22ae0d5`. Do not include API keys, screenshots of secrets, or real factory data.

### Codex focused verification — 14 October 2026

**Build/revision checked:** `22ae0d5` (`Add and document Reinvent Commerce workflow`); application code was unchanged during this check. The uncommitted changes at the time were documentation only.

**Result:** Pass — 20 focused assertions passed locally. The checks accepted the synthetic production CSV, detected the sustained drift on `LOT-8042-B` with three evidence readings, produced no alert for the stable sample, accepted mapped Commerce inputs, confirmed the expected allocation figures (180 affected, 65 reserved, 230 clean available, 120 unallocated orders, 185 need, 0 uncovered, 45 remaining), returned `unmapped` for a valid inventory snapshot without the alerted batch, and rejected an inventory CSV with missing required fields. A Streamlit `AppTest` startup smoke run also completed without uncaught exceptions (8 main-area and 14 sidebar elements rendered).

**Limit:** These checks used synthetic sample data and synthetic fixtures, including a factory-derived synthetic copy. They do not validate the detector against independent factory history, establish statistical suitability for a production line, or verify AMD endpoint behavior. A pilot on an approved, sanitized factory export with known reference outcomes remains unperformed.

## 4. Repeat the local review after a material change

The local results above apply to the local build. If a later code change needs review, record a new date and build/revision, then append the new outcomes rather than replacing this record. Use this format:

```text
MV-01 Pass — page showed 48 readings and LINE-04.
MV-02 Pass — no qualifying drift.
MV-03 Fail — batch was ..., onset ..., confirmation ...
MV-04 Pass
MV-05 Pass
MV-06 Blocked — [exact user-facing error; no secrets]
MV-07 Pass
MV-08 Pass — cases 1–3; skipped 4
MV-09 Pass
```

Include the exact visible error text or a brief description for failures. Do not send the API key, `.env` contents, screenshots containing credentials, or real factory data. The current local-review outcomes are already recorded above and in the phase checklist. A future review report should identify which build it covers.

## 5. Hosted deployment review record

**Review date:** 14 October 2026

**Reviewer:** User

**Deployment:** [https://lotlens.streamlit.app/](https://lotlens.streamlit.app/)

**Result:** Pass — the user reports that the deployed project was reviewed and everything worked as expected. The hosted app generated the investigation brief below. This record reflects the user's report and is not an independent Codex verification.

**Reported AMD brief details:**

- Drift status on `LINE-04`, batch `LOT-8042-B`.
- Onset at `2026-10-14T11:20:00`; confirmation at `11:40:00`.
- Endpoint-reported model: `self-dploy/DeepSeek-V4-Flash`; usage: 850 tokens.
- Possible checks cited `OPS-04 §2.6`, `QSP-17 §4.2`, and `QSP-17 §4.3`.
- The brief stated the cause was unresolved, no sensor readings or maintenance records were included in the alert, and the excerpts supplied no numeric limits for threshold assessment. It left decisions to human review.

The user reported that the deployed project worked as expected. No hosted failure or follow-up issue was reported. Repeat the relevant checks after a material application, model, prompt, or deployment change.

## 6. Upload template and optional sensor context

**Review date:** 15 October 2026

**Build/revision:** local working tree after `aeeb6bb`; upload-guidance changes were not yet committed during this check.

**Result:** Pass — 18 focused checks passed. `LINE-04_Production_Quality_Log.csv` was accepted by the uploader and analyzed. The upload screen rendered the CSV template download and field guide. A copy with all optional sensor and note columns removed also uploaded and analyzed successfully; the app explicitly showed that no machine sensor readings were supplied while retaining the defect-rate analysis. Partial/blank sensor context was accepted, while a non-numeric supplied sensor value was rejected as an input issue. Streamlit app startup, upload-mode rendering, and analysis completed without uncaught exceptions.

**Provenance clarification (15 October 2026):** The user confirms that `lotlens_synthetic_manufacturing_data.csv` was derived from real factory data. A byte comparison found `LINE-04_Production_Quality_Log.csv` identical to that synthetic copy. These checks therefore used a factory-derived synthetic fixture, not raw factory records or an independent holdout. They verify CSV upload and analysis behavior on that fixture only; they do not validate detector accuracy against factory history or establish suitability for production use. The canonical LINE-04 fixture is now included in Git as the default app dataset; its byte-identical duplicate remains local and Git-ignored.
