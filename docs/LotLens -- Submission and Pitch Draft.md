# LotLens — Submission and Pitch Draft

**Status:** Working draft. The user reports a successful local AMD inference call and completed local manual review. Final submission claims remain gated on suitable AMD service evidence, approved visual assets, a deployed public demo, and a public repository.

## Project title

**LotLens — Quality Drift Investigator**

## Short description

LotLens detects sustained quality drift in manufacturing data, traces the alert to its batch and evidence, and prepares a source-grounded investigation brief for human review.

## Long description

Manufacturing quality teams can spend valuable time reconstructing which production lot changed, when the shift began, and what evidence supports an alert. LotLens brings timestamped inspection results and machine readings into one investigation workspace.

Choose a clearly labeled synthetic scenario or upload a CSV. LotLens validates the readings, calculates a stable baseline, and applies an explainable rule that flags a sustained increase in the inspection defect rate. The interface identifies the affected line and batch, marks the onset and confirmation times, and shows the readings behind the alert alongside the trend and relevant procedure excerpts.

When AMD model access is configured, an AMD-hosted open model turns the calculated findings and supplied procedure excerpts into a concise investigation brief. The app keeps detector-calculated facts separate from model-written interpretation, shows the sources for proposed checks, and makes uncertainty visible. A quality lead reviews the handoff and decides what to do; LotLens does not diagnose a confirmed root cause or control production equipment.

The current prototype uses synthetic demo data and sample procedure excerpts. It is an investigation aid, not a validated industrial quality-control system.

## Challenge track

**Intelligent Industry** — primary and intended track. The prototype focuses on manufacturing process-quality monitoring, batch traceability, and a human-reviewed investigation workflow.

Do not select **Reinvent Commerce** for this submission unless an inventory-impact workflow is implemented and demonstrated end to end. The current MVP does not include that feature.

## Technology tags

Use only tags that are available in the live submission form and accurately describe the finished demo:

- Python
- Streamlit
- Plotly
- AMD Developer Cloud or the exact AMD-backed inference service label shown in the team's account

Before finalizing the tags, confirm the event's current tag list and verify the exact AMD service used. Do not claim ROCm, AMD GPUs, model training, or local hardware acceleration unless those technologies are actually used and demonstrated.

## Demo walkthrough draft

Suggested order; adjust the final duration to the event form and team's recording plan.

1. **Set context:** Introduce the quality lead's question: which lot is drifting, when did it start, and what evidence should be reviewed?
2. **Show the normal case:** Select **Stable process**, run analysis, and show that the configured rule finds no qualifying sustained drift.
3. **Show the incident:** Select **Seeded drift**, run analysis, and show the affected lot, onset, confirmation time, baseline, threshold, and trend.
4. **Inspect evidence:** Show the supporting inspection readings, machine-signal context, and clearly labeled synthetic procedure excerpts.
5. **Show AMD's role:** Generate a brief through the configured AMD endpoint. Show the returned model attribution, source-linked possible checks, and uncertainty. Do not present a fallback or an unverified response as a successful AMD call.
6. **Close with human review:** Download the shift handoff and explain that a qualified person reviews the finding; the app does not assert a root cause or control machinery.

## Pitch presentation outline

1. **Problem and user:** Quality leads must connect a changing defect trend to a production lot and reconstruct supporting evidence.
2. **LotLens workflow:** Data input → deterministic drift alert → batch and time-window evidence → procedure excerpts → human-reviewed handoff.
3. **Product demonstration:** Use the stable and seeded-drift synthetic scenarios and show the real working UI.
4. **AMD integration:** Explain the exact AMD-hosted model endpoint's role after a successful live call is available; distinguish it from the deterministic detector.
5. **Measured demo result:** Report the seeded fixture's detection delay and stable-scenario false alerts only after the user manually verifies them. Label these as synthetic-demo results, not factory-wide performance.
6. **Limitations and next steps:** Synthetic data, sample procedures, no confirmed root-cause diagnosis, no live factory connections, and human decision authority.

## Claims and evidence to finalize for submission

- **AMD:** The manual review record captures the endpoint-reported model and token usage. Add suitable presentation evidence that the successful call used the event-eligible AMD service; do not expose the API key.
- **Behavior:** The user-reported local manual review recorded that the stable fixture did not alert and the seeded fixture met its onset/confirmation target. Repeat on the hosted build if its configuration differs.
- **Grounding:** The user-reported MV-06 retest found source-linked checks and no unsupported sensor-range claim. Recheck if the model configuration or prompt changes.
- **Demo access:** Add the public app URL and source repository URL only after they are available and reviewed.
- **Visuals:** Add the approved cover and any presentation assets. Keep the plain-text `LotLens` placeholder until the finished logo is supplied.
- **Event form:** Confirm the live submission deadline, title/description limits, required media, and available technology tags in the dashboard before submitting.

## Submission readiness

- [x] Draft project title and descriptions prepared.
- [x] Primary track rationale recorded; no unsupported second-track claim.
- [x] Demo order and pitch structure drafted.
- [x] Local AMD call completed and reviewed by the user; outcome and model attribution are recorded in the Manual Verification Guide.
- [x] Local synthetic demo metrics manually recorded: stable scenario produced no alert; seeded drift onset was at 11:20 and confirmation at 11:40 (20-minute delay).
- [ ] Final technology tags checked against the live dashboard.
- [ ] Cover, video, slides, public repository, and public demo URL supplied.
- [ ] Current submission requirements and deadline confirmed; submission completed by the team.
