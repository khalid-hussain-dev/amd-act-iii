# LotLens — Manual Verification Guide

This document records the user's completed manual review of the local LotLens build on 14 October 2026. The steps and expected results below are retained so the same checks can be repeated after material changes or deployment. Do not include the AMD API key, screenshots of secrets, or real factory data in any report.

**Verification owner:** User  
**Date performed:** 14 October 2026  
**Build/revision:** Local working tree; no Git revision was recorded. The project root was not a Git repository at the time of review.  
**Overall status:** Passed — all listed manual checks completed; the AMD brief passed its focused content review.

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

1. **Missing field:** Remove the `operator_note` column and upload. Expected: a missing required column message; no quality finding.
2. **Too few readings:** Keep only 11 data rows and upload. Expected: an insufficient-evidence message explaining that at least 12 readings are needed.
3. **Multiple production lines:** Change `line_id` on one data row so the file has two line IDs. Expected: a message that this MVP analyzes one production line at a time.
4. **Malformed or incomplete CSV (optional):** Upload a plain-text file saved with a `.csv` extension. Expected: either a parsing/input-format error or a missing-required-columns message, never a production alert.

After each case, return to **Sample scenario** and confirm the valid built-in flow is still usable.

**Result:** Pass  
**Notes by case (1–4):** All ran as expected. Case 1 reported missing `operator_note`; case 2 reported insufficient evidence (at least 12 readings); case 3 reported the one-line restriction; case 4 reported missing required columns, which is an acceptable input-validation response.

### MV-09 — Analysis changes when the selected dataset changes

**Do this:** Run analysis on **Seeded drift**, then switch to **Stable process**.

**Expected:** The old drift result and generated brief disappear for the changed scenario until **Run analysis** is selected again. After running, the stable result shows no qualifying drift. This confirms that an earlier result is not shown as if it belongs to the newly selected data.

**Result:** Pass  
**Notes:** Ran as expected.

## 3. Repeat the review after a material change

The results above apply to the local build reviewed on the date shown. If a later code change or deployment needs review, record a new date and build/revision, then append the new outcomes rather than replacing this record. Use this format:

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
