# LotLens — Quality Drift Investigator

## Project snapshot

**Team:** PARALLAX  
**Primary track:** Intelligent Industry  
**Optional secondary track:** Reinvent Commerce, only if the inventory-impact view is implemented and demonstrated  
**One-line pitch:** LotLens spots when a production batch starts drifting out of specification, shows the evidence behind the alert, and gives quality staff a source-backed next-step brief.

LotLens is one product and one submission. It may be entered in more than one challenge track if the same working product truly satisfies both briefs. The current plan is to build for Intelligent Industry first. A small inventory-impact feature could support Reinvent Commerce if the core industrial workflow is already complete.

### Current implementation status

- **Product contract:** One Intelligent Industry MVP, one synthetic quality-drift scenario, a deterministic alert, an evidence brief, and human review.
- **Phase 1:** Initial data validation, two synthetic scenarios (stable and seeded drift), the single-line drift detector, and procedure retrieval are implemented. User-reported manual results confirmed no stable-scenario alert and a seeded alert at 11:20, confirmed at 11:40 on 14 October 2026.
- **Phase 2:** The AMD Token Factory chat call, response validation, citation filtering, and UI fallback are implemented. The user configured the API key and completed a live brief call. The first response made an unsupported typical-range claim; after narrowing the request context and prompt, the user re-ran MV-06 successfully (892 tokens; endpoint-reported model `self-dploy/DeepSeek-V4-Flash`) with source-linked checks and no unsupported range claim.
- **Phase 3:** The Streamlit prototype, Mineral Precision theme, explicit analysis action, scenario selector, CSV upload, evidence, handoff, and input states are implemented. The user reported that visual interactions and CSV cases ran as expected. The logo remains a plain-text placeholder.
- **Manual review:** The user completed the listed local manual checks on 14 October 2026; outcomes are recorded in the [Manual Verification Guide](LotLens%20--%20Manual%20Verification%20Guide.md). This is a user-reported review, not a Codex rerun.
- **Next engineering gate:** Publish the public repository, deploy to the selected Streamlit Community Cloud host, review the hosted build, then complete the submission materials. Integrate approved visual assets when supplied.

## Vision

Manufacturing teams often have machine readings, inspection measurements, shift notes, and operating procedures, but those signals sit in separate places. Quality staff may notice a defect trend only after multiple batches are affected, and then have to reconstruct what changed and what the procedure recommends.

LotLens brings those signals into a single batch investigation. It detects a measurable change in production quality, ties the alert to the affected time window and batch, and presents a concise, reviewable explanation with links to relevant operating-procedure evidence.

### Intended users

- **Primary user:** A factory quality lead or process engineer monitoring production batches.
- **Secondary user:** A shift supervisor who needs a clear handoff for the next operator.
- **Optional commerce user:** An inventory or fulfilment manager who needs to know which stock may be affected by a quality alert.

### User problem

“A quality measure is starting to drift. Which batch is affected, when did the change begin, what readings support the alert, and what should a person check next?”

### Product promise

LotLens makes a potential quality drift visible early and gives the team a traceable starting point for investigation. It does not claim to prove a root cause, replace a qualified operator, or control factory equipment.

## How the product works

1. The user opens a built-in sample dataset or uploads a CSV of timestamped machine and inspection readings.
2. LotLens checks the data, separates a stable baseline from the monitored period, and applies deterministic statistical drift rules.
3. The app identifies the first alert window, affected line and batch, and the measurements that triggered the alert.
4. LotLens retrieves relevant excerpts from a small set of operating procedures or technical notes.
5. An open model running through an AMD-backed endpoint turns the calculated evidence and retrieved excerpts into a concise investigation brief.
6. The user sees the alert, trend chart, evidence, source excerpts, uncertainty, and suggested human checks in one interface.
7. The user can copy or download the brief as a shift handoff. Nothing is automatically changed in a production system.

### AI and deterministic responsibilities

| Component | Responsibility |
| --- | --- |
| Deterministic detector | Calculate quality rates, compare them to a baseline, detect sustained drift, and identify affected batches. |
| Evidence retrieval | Find relevant procedure sections and retain their source names and section/page labels. |
| AMD-hosted open model | Explain the already-calculated evidence in plain language and propose checks supported by retrieved sources. |
| Human operator | Review the alert, decide whether it is actionable, and choose any operational response. |

The language model must not invent measurements, calculate the alert threshold, or state an unverified root cause. The UI will distinguish **observed evidence** from **possible checks** and show when the source material does not support a confident suggestion.

## MVP scope

### Must have

- A clear sample-data path that works without uploading a file.
- CSV validation and a useful error message for malformed input.
- A transparent, deterministic drift detector.
- A batch and time-window alert with the readings that triggered it.
- At least one readable trend visualization.
- A small, versioned set of sample procedures or technical notes with source labels.
- AMD-backed model inference in the real product flow.
- A grounded investigation brief, including a clear uncertainty or insufficient-evidence state.
- A reviewable demo UI, public repository, runnable README, and public demo URL.

### Defer unless the MVP is complete

- A second track's inventory action.
- Multiple factory lines, user accounts, permissions, or persistent databases.
- Live equipment connections, PLC controls, or automatic work-order dispatch.
- Fine-tuning, model training, a multi-agent system, or a vector database.
- Extensive forecasting or a claim that the synthetic data proves real-world savings.

## Candidate technical stack

The stack is intentionally small so the team can finish a complete demo during the event. Validate AMD endpoint access and model availability before locking the serving details.

| Layer | Proposed choice | Why |
| --- | --- | --- |
| UI and app flow | Python + Streamlit | One deployable Python app can handle sample selection, upload, analysis, charts, and the final brief with little glue code. |
| Data handling | pandas + NumPy | CSV parsing, validation, time-window grouping, and numerical calculations. |
| Drift detection | Transparent Python implementation using a robust baseline and a sustained-change rule (for example, median/MAD plus EWMA) | Easy to explain, reproduce, and validate against seeded drift. The detector is not delegated to the LLM. |
| Visualization | Plotly | Interactive time-series chart with baseline, alert window, and affected batch markers. |
| Procedure retrieval | Lightweight section-based lexical matching for the MVP | Keeps retrieval inspectable and avoids unnecessary infrastructure. Upgrade only if the sample corpus makes this inadequate. |
| Model inference | Open instruction model through the AMD event's supported AMD-backed API or an AMD Developer Cloud/vLLM endpoint | Makes AMD inference part of the actual user workflow. Choose the concrete endpoint after access is verified. |
| Model client | OpenAI-compatible Python client or `httpx`, depending on the endpoint's documented interface | Keeps the provider boundary easy to configure. Verify request format and authentication before implementation. |
| Configuration | Environment variables and a local `.env` file excluded from Git | Keeps credentials out of source control. |
| Hosting | A public app host reachable by judges; select after checking its network access to the AMD endpoint | Provides the required demo URL. Keep inference on AMD infrastructure. |

### Required configuration boundary

Keep model integration behind one small function or module so the UI and detector do not depend on one provider's request format. The current AMD Radeon Cloud Token Factory guide documents an OpenAI-compatible chat endpoint at the URL below. Use the Base URL, model name, and key shown in the team's AMD account if its model details differ:

```text
AMD_CHAT_COMPLETIONS_URL=https://developer.amd.com.cn/radeon/api/v1/chat/completions
AMD_MODEL_NAME=DeepSeek-V4-Flash
AMD_API_KEY=
```

The Token Factory card displays `DeepSeek-V4-Flash`. AMD's current model reference identifies that as the Chat Completions API model ID; `DeepSeek-V4-Flash-0731` is the version of the served weights, not the `model` value for this API. The adapter uses AMD's documented Bearer-key Chat Completions request/response format. Never commit credentials, private endpoints, or real customer/factory data. See the [AMD Radeon Cloud model API guide](https://github.com/AMD-DEV-CONTEST/Radeon-hackathon-2026-07/blob/main/Radeon-Cloud-User%20Guide/README.md#-using-model-apis-openai-compatible), [Chat Completions API reference](https://amd-aim.github.io/radeon-cloud-docs/api/chat-completions/), and [DeepSeek-V4-Flash model reference](https://amd-aim.github.io/radeon-cloud-docs/models/deepseek-v4-flash/).

### Dataset shape

The demo CSV should have enough information to connect a quality change to a batch. A small initial schema could be:

```text
timestamp,line_id,batch_id,shift,temperature_c,vibration_mm_s,pressure_bar,units_inspected,defect_count,operator_note
```

Keep units, valid ranges, missing-value behavior, time zone, and the seeded drift interval documented. Mark all generated records clearly as **synthetic demo data**. Do not imply that generated records came from a real factory.

## UI: yes, it needs to be built

The hackathon asks for a working prototype and demo application, so a deck or static mockup alone will not meet the product expectation. Build a compact UI that lets a judge move through the actual workflow and see the AMD-backed inference contribute to the result.

### UI design ownership and handoff

The user will discuss and finalize palette and visual assets in web ChatGPT. Codex owns the product's visual and technical implementation, following the finalized color system and the approved assets the user supplies. The interface layout should serve the LotLens investigation workflow rather than copy a generic dashboard template.

The designed UI should communicate these capabilities in a way that suits the chosen workflow:

- Choose the sample dataset or upload a CSV, then run the analysis.
- See whether a qualifying drift was detected and, when applicable, the affected line/batch and onset time.
- Inspect a chart that distinguishes actual readings, baseline, threshold, and detected change point using the chart roles in the color-system document.
- Review which measurements triggered the alert and how they compare with the baseline.
- Read the AI-generated interpretation separately from calculated evidence, with procedure references and uncertainty visible.
- See clear normal, drift, invalid-input, insufficient-evidence, and unavailable-model states.
- Copy or download a shift-handoff summary without implying it was automatically sent or acted on.

Use plain text `LotLens` as the temporary header placeholder. Do not create or approximate logo artwork. Replace the placeholder only when the user supplies the finished logo.

## Project phases and completion steps

Track implementation progress in [LotLens — Phase Completion Checklist](LotLens%20--%20Completion%20Checklist.md). Checklist marks indicate implementation status only; they are not test or verification results.

### Phase 0 — Lock the product contract

**Goal:** Ensure the team is building one small, judgeable product.

1. Confirm the primary user: quality lead or process engineer.
2. Freeze the primary track as Intelligent Industry.
3. Write the exact alert scenario: one production line, one seeded drift, one affected batch.
4. Agree on what counts as an alert and what the AI brief may and may not claim.
5. Use the fixture-based acceptance target: no alert in the stable scenario; in the seeded-drift scenario, onset at the known change point and confirmation within three consecutive post-change readings (20 minutes at the sample's 10-minute cadence). The user reports that the local build met this target; see the manual verification record.
6. Use the configured AMD Token Factory endpoint and selected model. The user has added the API key locally and reports a successful brief call; capture suitable service/model evidence for the final submission. Do not record the secret in docs.
7. Assign one owner per workstream and agree on a short daily integration checkpoint.

**Done when:** The scenario, input schema, metric, track, and AMD access path fit on one page and everyone agrees on the MVP boundary.

### Phase 1 — Build the demo data and detector

**Goal:** Produce an alert from reproducible, understandable data.

1. Create a small synthetic dataset with a stable baseline, one known change point, and at least one unaffected batch or normal interval.
2. Add an accompanying data dictionary with units and generation notes.
3. Implement CSV validation: required columns, parseable timestamps, numeric fields, missing values, and invalid ranges.
4. Calculate the inspection defect rate from counts rather than accepting an unexplained precomputed score.
5. Implement a baseline and sustained-drift rule; record the exact threshold and window used.
6. Return structured output: alert state, onset time, affected batch, signals involved, values, threshold, and supporting rows.
7. Compare the detector's output with the known synthetic change point and record its detection delay and false alerts.

**Done when:** The sample case consistently identifies the intended drift and the result can be explained without calling a language model.

### Phase 2 — Add procedure evidence and AMD inference

**Goal:** Turn computed evidence into a grounded, useful investigation brief.

1. Write or select a few short synthetic SOP sections that match the demo incident; label every source and section clearly.
2. Implement transparent section retrieval and return the matched text and source labels to the app.
3. Confirm the actual AMD endpoint, model identifier, authentication, rate limits, and request/response format using official access instructions.
4. Implement the provider wrapper and keep credentials in environment variables.
5. Send only structured detector results and retrieved procedure excerpts to the model.
6. Require a response schema with a concise summary, possible checks, and uncertainty. Render observed evidence directly from deterministic detector output, and validate every suggested check's source label.
7. Handle endpoint failure, timeout, malformed output, and unsupported conclusions with a visible fallback; the deterministic alert should remain usable.
8. Capture proof that the demo's inference call uses the AMD-backed service selected for the event.

**Done when:** A real AMD-backed model call produces a source-grounded brief, and the app shows an honest fallback when inference is unavailable.

### Phase 3 — Build the UI around the investigation

**Goal:** Let a judge understand and operate the product in a few minutes.

1. Build the Streamlit application around the LotLens investigation workflow.
2. Implement tokens from [LotLens — Visual Identity & Color System](LotLens%20--%20Visual%20Identity%20%26%20Color%20System.md), the source of truth for type, colors, surfaces, status, charts, and interaction styling.
3. Add a ready-to-run sample dataset and a CSV upload path.
4. Add a clear analysis action and progress/error states.
5. Render the batch/alert summary and annotated time-series chart according to the supplied design.
6. Render the model brief and source excerpts, keeping calculated facts and AI-written interpretation clearly distinct.
7. Add the synthetic-data notice and human-review language.
8. Add a simple export/copy handoff action if it fits without destabilizing the core flow.
9. Walk through the demo from a fresh app load and remove confusing controls or blank panels.

**Done when:** A first-time viewer can load the sample, see the drift, inspect its evidence, and understand the next human step without explanation from the builder.

### Phase 4 — Integrate and prove the complete flow

**Goal:** Verify the complete product path and its claims.

1. Run the app from a clean environment using the documented setup.
2. Verify the sample path, upload path, invalid CSV state, detector result, AMD inference, source display, and inference failure fallback.
3. Check that charts and summaries use the same selected batch and time window.
4. Review model output for invented measurements, unsupported causes, or missing citations; tighten prompt or output validation if needed.
5. Measure the chosen demo metric on the seeded scenario and capture the result honestly.
6. Remove unused experimental features and sample secrets.

**Done when:** The entire demo works from a clean start and every claim shown in the interface is backed by visible data or a labeled source.

### Phase 5 — Deploy and prepare the repository

**Goal:** Give judges a usable public demo and a repository they can run.

1. Pick a public hosting target and verify outbound access to the AMD endpoint.
2. Configure secrets through the host's secret manager/environment settings.
3. Deploy and open the public application URL in a fresh browser session.
4. Add a README with the problem, architecture, AMD component, setup, environment variables, sample data, run steps, and limitations.
5. Ensure no API keys, credentials, or non-public source data are committed.
6. Confirm the repository is public and the app URL remains available during judging.

**Done when:** A judge can open the demo and the README explains how to run the project without asking the team for missing setup steps.

### Phase 6 — Prepare the submission and pitch

**Goal:** Make the submission communicate the working product clearly.

1. Write the title, short description, and long description around the quality-drift user problem.
2. Select Intelligent Industry. Select Reinvent Commerce only if the inventory feature is implemented and demonstrated.
3. Add technology tags that match actual use, including the specific AMD technology used.
4. Create a cover image using the visual brief below.
5. Record a short product demo showing input → alert → evidence → AMD-backed explanation → human next step.
6. Prepare a concise pitch deck: problem, user, workflow, architecture/AMD role, measured demo result, business value, and limitations.
7. Recheck the live submission deadline and submit with a buffer.

**Done when:** The LabLabAI submission has all required fields, links, media, and track selections, and the video and app tell the same story.

## Optional second-track gate: Reinvent Commerce

Do not start this until Phases 1–3 for the Industry workflow are stable.

1. Add a small inventory table mapping affected batches to SKUs and on-hand quantities.
2. Show which sellable stock may be affected by the alert.
3. Use a simple, disclosed rule for a human-reviewed hold/replenishment recommendation; do not ask the language model to invent demand forecasts.
4. Explain the merchant or fulfilment user and the commercial outcome the feature supports.
5. Demonstrate that action end to end and select the second track only if it is a genuine product capability.

If this gate would delay or weaken the primary demo, omit the second track.

## Success measures for the demo

Choose a small number of measured outcomes and label them as results on the synthetic scenario, not as proven factory-wide gains.

- **Detection delay:** Samples or minutes from the seeded change point to the alert.
- **False alerts:** Alerts during the stable segment.
- **Traceability:** Percentage of brief statements linked to computed evidence or a displayed procedure source.
- **Usability:** A first-time viewer can identify the affected batch and next human check from the screen.
- **AMD proof:** The working flow makes an inference request to the AMD-backed endpoint and displays the returned brief.

## Workstream split

Use these as responsibility lanes; combine lanes if the team is small.

- **Data and detection:** Synthetic data, schema, validation, baseline, alert output, demo metrics.
- **AMD and evidence:** AMD endpoint access, model wrapper, SOP retrieval, grounding and fallback.
- **UI and integration:** Streamlit flow, charts, alert card, evidence panel, usability walkthrough.
- **Release and presentation:** Hosting, README, submission fields, cover, slides, and recorded demo.

Integrate at least once per day. Agree early on a shared detector-output schema so the UI and model work can proceed independently.

## Visual asset brief

### Concept description

LotLens is a quality investigation workspace for manufacturing teams. It turns a stream of machine readings and inspection results into a clear view of a production lot's health. When a process begins to drift, the interface marks the affected batch and time window, shows the readings that triggered the alert, and pairs them with relevant procedure guidance. An AMD-hosted AI model helps write the evidence-based handoff, while the quality lead remains in control of any decision.

### Copy-ready UI design handoff

Use this description as product context when exploring the UI in a separate design tool. It describes the product and its behavior without prescribing a specific page layout.

> **Project:** LotLens — Quality Drift Investigator
>
> LotLens is a web application for factory quality leads and process engineers. It helps them catch when a production process starts drifting out of specification and investigate the affected batch before the issue spreads. The MVP uses clearly labeled synthetic factory data: timestamped machine readings, inspection counts, batch and shift identifiers, operator notes, and a small set of sample operating procedures.
>
> A user can choose a sample dataset or upload a CSV, then run an analysis. LotLens uses transparent statistical rules—not a language model—to compare the monitored readings with a stable baseline and detect sustained changes in quality. When it finds a drift, it identifies the affected production line and batch, when the change began, which measurements contributed to the alert, and how those values compare with the baseline or alert threshold. The user should be able to inspect the trend over time and understand why LotLens raised the alert.
>
> An open AI model running through an AMD-backed service receives the detector’s structured findings and relevant excerpts from sample procedures. It writes a concise interpretation, **possible checks grounded in the source material**, and **what remains uncertain**. The application presents **observed evidence** directly from its deterministic detector output instead of asking the model to restate measurements. The interface must show the procedure source and section for each cited recommendation. If the model or AMD service is unavailable, the underlying alert and chart should still work, and the interface should say that the generated brief could not be produced.
>
> The product supports human investigation; it does not diagnose a root cause, control machinery, stop a production line, or automatically issue a work order. The user reviews the alert and decides what to do. A useful output is a shift-handoff summary that can be copied or downloaded, containing the affected batch, alert time, evidence, linked procedure guidance, and suggested checks.
>
> Design for a busy quality lead who needs to understand the alert quickly, then examine the evidence in more detail. Make the distinction between calculated facts, AI-written interpretation, and human decisions visible. Include UI states for: no dataset selected, sample data ready, analysis in progress, normal results, drift detected, invalid CSV, insufficient evidence, and AMD/model service unavailable. Label sample records as synthetic. The visual tone should be precise, calm, and trustworthy for an industrial setting; alerts should be noticeable without making the whole interface feel alarmed.
>
> Follow **Mineral Precision** from `LotLens -- Visual Identity & Color System.md` as the authoritative visual theme. It defines the exact palette and semantic roles, Manrope/Inter/IBM Plex Mono typography, selective glassmorphism and lighting, readable evidence surfaces, chart treatment, interaction, and accessibility rules. Keep the product name as plain text in a logo placeholder until the user supplies finished artwork; do not create or approximate a logo.
>
> The primary hackathon category is **Intelligent Industry**. The current MVP does not need a commerce workflow, customer-facing features, inventory decisions, authentication, live factory connections, or automated equipment control. Those are outside the first version.

### Visual direction

- **Authoritative theme:** Mineral Precision, finalized in [LotLens — Visual Identity & Color System](LotLens%20--%20Visual%20Identity%20%26%20Color%20System.md). Use that document's exact palette roles and tokens rather than inventing new colors.
- **Personality:** Premium, investigative, dependable, technically sophisticated, and distinctive. Expressiveness and glassmorphism are welcome when they reinforce investigative clarity; evidence-heavy panels must remain readable.
- **Color roles:** Mineral Sage (`#B8CBA8`) is the primary brand accent, not a normal-status color. Brushed Brass (`#D0B17A`) is a secondary accent, not a warning color. Use the semantic status colors and chart roles defined in the color-system document.
- **Typography:** Manrope for display and headings, Inter for interface text, and IBM Plex Mono for measurements, timestamps, thresholds, and identifiers, with appropriate fallbacks.
- **Logo:** Keep a plain-text `LotLens` placeholder for now. The supplied logo direction is reference only; do not create, redraw, or approximate a logo. Replace the placeholder when the user provides finished artwork.
- **Avoid:** Dominant electric blue/cyan, generic sci-fi control-room styling, excessive neon or glow, illegible tiny labels, ungrounded chart marks, and imagery implying autonomous equipment control.

### Useful assets to prepare

1. Keep the app-header brand area as a plain-text `LotLens` placeholder until the user supplies the finished logo; do not create logo artwork.
2. A submission cover illustration showing a production line, a highlighted batch path, and a clear quality-trend inflection, styled with the Mineral Precision color system.
3. A small diagram showing the product flow: readings + inspections + SOP → drift detection → evidence brief → human review.
4. Optional UI state icons for normal, drift, AI-generated, and informational states, using the semantic palette and labels specified by the color system.

### Copy-ready visual prompt

> Create a polished hackathon cover illustration for **LotLens — Quality Drift Investigator**, a manufacturing quality-investigation product. Show a refined, dark industrial setting with a single production lot represented as a traceable path and a subtle shift in a quality trend from stable to drift. The image should communicate precise investigation and evidence reviewed by a human quality engineer, without implying automated machine control. Follow the **Mineral Precision** palette: Obsidian Mineral `#101311`, Deep Graphite `#171C19`, Mineral Sage `#B8CBA8`, Brushed Brass `#D0B17A`, Porcelain `#F0F1E9`, and Signal Amber `#E8B45D` for drift. Keep the composition clear, premium, and restrained; reserve readable negative space for the project title. Do not create or approximate a logo or wordmark, add fake data labels, use illegible UI text, include robot/AI clichés, or add AMD branding.

## Visual asset handoff

The user will use web ChatGPT to discuss and finalize the palette and visual assets. Codex implements the application's visual layout and interactions from the LotLens workflow, following the finalized color system. Integrate supplied approved visuals as they become available. Keep the app header as plain-text `LotLens` until the user supplies the finished logo; do not generate or approximate logo artwork.

## Risks and decisions to verify

- **AMD deployment access:** Local AMD inference has been manually reviewed. Confirm outbound access and configure the secret variables when the deployment host is selected.
- **Deadline discrepancy:** The live schedule showed 18 October at 3:00 PM Pakistan time while the event header showed 8:00 PM PST. Use the earlier time as the internal deadline until the organizers clarify.
- **Synthetic data:** Clearly label it and avoid real-world performance claims based only on generated data.
- **Model reliability:** Keep calculated values deterministic, show source excerpts, and make uncertainty visible.
- **Scope:** Build the Intelligent Industry workflow before considering commerce inventory functionality.
- **Manual verification:** The user completed the listed local-build checks. Keep those results distinct from any future review of the deployed build.

## Event reference

This brief is the working product plan for LotLens. Use [LotLens — Visual Identity & Color System](LotLens%20--%20Visual%20Identity%20%26%20Color%20System.md) as the authoritative product theme. For current event requirements, tracks, judging criteria, and submission details, consult the [AMD ACT III event page](https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-iii) before submission.
