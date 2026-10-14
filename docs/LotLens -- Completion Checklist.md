# LotLens — Phase Completion Checklist

This checklist tracks implementation against the phases in [LotLens — Project Brief and Build Plan](LotLens%20--%20Project%20Brief%20and%20Build%20Plan.md). It is updated whenever project implementation changes.

## Status meanings

- `[x]` Implemented in the project files. This does not mean the behavior has been run or verified.
- `[ ]` Not implemented yet, or awaiting an input or decision.
- **Manual verification:** Results are recorded separately from implementation. The user completed the listed checks against the local build and reports that the deployed app worked as expected on 14 October 2026; Codex did not rerun either review. Repeat relevant checks after material changes.

## Track 1 engineering exit — Intelligent Industry

**Status: Complete for the current MVP**, based on the implemented source and the user's recorded local/hosted manual reviews. No verification tests were run by Codex for this update.

- The production-quality alert, synthetic stable/drift scenarios, evidence, procedure-grounded AMD brief, review UI, and handoff are implemented.
- The public repository and deployed app are recorded as live; hosted success is user-reported.
- Remaining Track 1 checklist entries are team coordination, final-demo evidence, and visual assets that have not yet been supplied. They do not block the current engineering scope and remain deferred with submission preparation.

## Phase 0 — Lock the product contract

- [x] Primary user: factory quality lead or process engineer.
- [x] Primary track: Intelligent Industry.
- [x] MVP scenario: one production line, a stable period, one seeded quality drift, and an affected lot.
- [x] Detector rule and AI boundaries are described in the project brief and README.
- [x] Define demo acceptance targets from the synthetic fixture: no alert in the stable scenario; in the seeded-drift scenario, onset at the known change point and confirmation within three consecutive post-change readings (20 minutes at the fixture's 10-minute cadence).
- [x] Record the selected AMD model name and corrected endpoint in the local `.env` configuration.
- [x] Add the AMD API key to local `.env` (secret value is not recorded in project documentation).
- [ ] PARALLAX assigns team owners and an integration checkpoint for workstreams.

## Phase 1 — Build the demo data and detector

- [x] Generate a reproducible synthetic dataset with a stable interval and seeded drift.
- [x] Provide separate reproducible seeded-drift and stable-process scenarios for alert and normal-state demonstrations.
- [x] Add a data dictionary with units, synthetic ranges, and generation notes (`data/DATA_DICTIONARY.md`).
- [x] Validate required columns, timestamps, numeric readings, missing values, and count ranges.
- [x] Restrict each analysis to one production line so unrelated lines are not mixed into one baseline.
- [x] Reject non-finite measurements and fractional inspected/defect counts.
- [x] Calculate defect rate from inspected and defective unit counts.
- [x] Implement the baseline threshold and sustained-crossing rule.
- [x] Return structured alert details and supporting rows.
- [x] User manually confirmed the stable scenario had no alert and seeded drift began at Oct 14, 11:20 and confirmed at 11:40 (20-minute delay; 1.21% baseline, 3.21% threshold).
- [x] User completed manual checks MV-01–MV-05 and MV-07–MV-09 against the local build; outcomes are recorded in the [Manual Verification Guide](LotLens%20--%20Manual%20Verification%20Guide.md).

## Phase 2 — Add procedure evidence and AMD inference

- [x] Add clearly labeled synthetic procedure excerpts.
- [x] Retrieve procedure sections transparently from the alert context.
- [x] Implement an AMD Token Factory chat adapter and document its current API format.
- [x] Keep model configuration in environment variables; `.env` is excluded by `.gitignore`.
- [x] Load newly populated local `.env` settings on app rerun without overriding non-empty host environment secrets; provide a reload control.
- [x] Send structured detector findings and retrieved procedure excerpts to the adapter.
- [x] Require a correctly typed response with summary, possible checks, and uncertainty; discard checks with unsupported source IDs or missing text.
- [x] Treat uploaded notes and procedure excerpts as untrusted prompt data; constrain the response size and cited check output.
- [x] Keep raw measurements out of the AMD brief context and prohibit unsupported claims about sensor ranges or trends, based on the first manual output review.
- [x] Capture and display the endpoint-reported model and available token usage with the generated brief and handoff, without exposing credentials.
- [x] Render observed evidence directly from detector output so the model cannot invent or paraphrase measured facts.
- [x] Render the evidence and model interpretation in a single styled panel with escaped model text and source-ID badges.
- [x] Bound the AMD brief response size and show truthful progress while waiting for the model.
- [x] Keep inference failures separate from the calculated alert in the UI.
- [x] User entered the selected AMD model name and corrected endpoint in local `.env`.
- [x] User added the AMD API key to local `.env`; the secret remains uncommitted and is not recorded here.
- [x] User completed the AMD call and focused content review (MV-06); the retest and reported model attribution are recorded in the [Manual Verification Guide](LotLens%20--%20Manual%20Verification%20Guide.md).
- [ ] Capture AMD service/model evidence for the final demo and submission.

## Phase 3 — Build the investigation UI

- [x] Create a Streamlit app with sample-data and CSV-upload paths.
- [x] Add an in-app sample CSV download and identify uploaded dataset changes by file content.
- [x] Allow the user to switch between the two synthetic scenarios and download the selected one.
- [x] Add explicit dataset-ready, insufficient-evidence, invalid-data, analysis-progress, and AMD-configuration states.
- [x] Distinguish a CSV parsing failure from the no-file-selected state and explain that it is an input issue.
- [x] Show reading count, production line, batch count, and time window before the user runs analysis.
- [x] Make data-origin messaging distinguish synthetic scenarios from user-uploaded CSVs.
- [x] Show the specific missing AMD settings at the inference entry point.
- [x] Add initial Mineral Precision theme tokens and apply them to the interface.
- [x] Show alert status, lot, onset, baseline, current defect rate, and trend chart.
- [x] Add a selectable sensor-context trend for temperature, vibration, and pressure with a descriptive baseline; keep it distinct from alert logic.
- [x] Show supporting readings, procedure excerpts, synthetic-data labels, and human-review language.
- [x] Add an investigation-brief action and downloadable handoff with detector evidence, procedure excerpts, data provenance, and clearly separated AI interpretation when available.
- [x] Keep the logo as a plain-text `LotLens` placeholder.
- [x] Implement separate normal-result and drift-result states, including the selected scenario in the provenance label.
- [x] Map timeout, authorization, rate-limit, provider, and malformed-response failures to safe messages while preserving the deterministic result.
- [x] Show distinct AMD-ready and credentials-pending states, explain that local analysis remains available, and show the exact missing settings with the reload action.
- [ ] Integrate user-approved visual assets when supplied; replace the placeholder only when the finished logo is supplied.
- [x] User manually reviewed the local visual interactions and reported the listed UI and CSV checks passed; see the [Manual Verification Guide](LotLens%20--%20Manual%20Verification%20Guide.md).

## Phase 4 — Integrate and record local manual review

- [x] Wire sample and upload inputs through the detector, procedure retrieval, AMD brief action, and inference fallback.
- [x] Populate chart, facts, evidence, and handoff from the same selected analysis result; invalidate saved results when the selected sample or uploaded-file contents change.
- [x] Prepare a step-by-step user-run verification guide with launch instructions, scenarios, expected results, and a report format ([Manual Verification Guide](LotLens%20--%20Manual%20Verification%20Guide.md)).
- [x] User re-reviewed the AMD brief after the prompt/context tightening; the retest removed the unsupported “within typical ranges” claim and its recommendations cited procedure sources. See MV-06 in the [Manual Verification Guide](LotLens%20--%20Manual%20Verification%20Guide.md).
- [x] User manually recorded detector outcomes and completed the listed end-to-end checks, including the MV-06 retest, against the local build on 14 October 2026.
- [x] User manually reviewed the deployed app at https://lotlens.streamlit.app/ and reported that it worked as expected; hosted AMD brief details are recorded in the [Manual Verification Guide](LotLens%20--%20Manual%20Verification%20Guide.md).

## Phase 5 — Deploy and prepare the repository

- [x] Add a non-root Streamlit container definition and exclude local secrets from the build context.
- [x] Document local container run steps and deployment secret handling.
- [x] Prepare a host-agnostic deployment guide covering the container contract, runtime secrets, network needs, session data behavior, and release sequence.
- [x] Select Streamlit Community Cloud as the initial free hosting target and document its secret configuration and hibernation behavior.
- [x] Load AMD credentials from Streamlit `st.secrets` while preserving process-environment and local `.env` support.
- [x] Select Streamlit Community Cloud as the initial public host.
- [x] Confirm the deployed app can reach the selected AMD endpoint (user-reported hosted brief generation).
- [x] Configure deployment secrets outside the repository (user-reported deployed AMD brief succeeded).
- [x] Publish the public GitHub repository: https://github.com/khalid-hussain-dev/amd-act-iii (initial project commit pushed to `main`).
- [x] Deploy the public app and record its URL: https://lotlens.streamlit.app/.
- [x] Add local run instructions, configuration guidance, CSV schema, detector rule, and limitations to the README.
- [x] Keep the local `.env`, virtual environment, generated handoff/CSV outputs, and unrelated local files out of the initial repository commit.

## Phase 6 — Prepare submission and pitch

- [x] Prepare a working title, short and long descriptions, primary-track rationale, demo walkthrough, and pitch outline in [LotLens — Submission and Pitch Draft](LotLens%20--%20Submission%20and%20Pitch%20Draft.md). Local and hosted manual reviews are complete as user-reported; submission evidence and materials remain.
- [ ] Prepare the final title and short/long descriptions.
- [ ] Select the track(s) the completed product actually demonstrates.
- [ ] Add technology tags that match implemented and demonstrated technology.
- [ ] Create the submission cover from the approved visual direction/assets.
- [ ] Record a demo of input → alert → evidence → AMD explanation → human review.
- [ ] Prepare the pitch presentation and measured business-value claim.
- [ ] Complete all LabLabAI submission fields and submit with a deadline buffer.

## Reinvent Commerce extension — implementation status

The Commerce extension is now implemented locally in the same LotLens product. Checklist marks below mean implementation appears in project files; they are **not** evidence of runtime or manual verification.

- [x] Map an alerted production batch to SKU-level inventory rows.
- [x] Validate inventory and open-orders CSV schemas, counts, and reservation ranges.
- [x] Calculate affected units, unaffected available stock, allocation need, and any uncovered-unit gap deterministically.
- [x] Present the calculation and a human-reviewed stock/fulfillment recommendation in the app.
- [x] Provide synthetic sample inventory and open-orders downloads and document their meaning and calculation.
- [x] Keep the user-provided production workflow available when Commerce input is missing or invalid.
- [x] User manually reviews the seeded-drift Commerce view (MV-COM-01) and stable-process view (MV-COM-02).
- [x] User completes end-to-end upload review for mapped/unmapped alert batches and an invalid Commerce snapshot (MV-COM-03); the invalid-file case preserves the Industry chart and alert evidence.
- [ ] Decide whether the implemented and reviewed capability should be selected as Reinvent Commerce in the final submission.

**Current status:** Implemented and reviewed locally. The user-reviewed seeded/stable scenarios and mapped/unmapped/invalid-upload Commerce cases passed. A separate missing-file screenshot was not provided; the app displays a prompt asking for both Commerce files. The built-in sample uses an alerted lot with 180 units on hand (65 reserved), 230 available units in an unaffected lot, and 120 unallocated open-order units. The documented rule compares 185 units of reallocation need with 230 clean units. This example is synthetic and is not a demand forecast or proof of commercial savings.

## Remaining team inputs and actions

No additional local credentials or pre-build decisions are currently needed. The user completed local and hosted manual reviews. Remaining actions are:

- Finished logo file, when ready. Until then, the app uses text only.
- Any approved cover or other visual assets after you finalize them. Codex will implement and integrate them.
- Team workstream owners and an integration checkpoint, if PARALLAX wants the checklist to track named responsibilities.
- Finish the cover, demo video, slides, and any remaining evidence for the event submission.
- Confirm current submission requirements and deadline in the event dashboard, then submit.

No additional palette decisions or UI mockups are needed. The user completed the listed Track 1 local checks, focused AMD brief retest, hosted review, and Commerce upload review; results are in the [Manual Verification Guide](LotLens%20--%20Manual%20Verification%20Guide.md).
