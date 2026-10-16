# LotLens — Integrated UI Redesign Blueprint

**Status:** Proposed screen structure and demo flow; planning only  
**Product scope:** Intelligent Industry + Reinvent Commerce  
**Visual theme:** Mineral Precision remains fixed. This document changes no colors, code, styles, or assets.

**Implementation note (17 October 2026):** The current app presents one scrollable investigation page with in-page Quality, Commerce, Handoff, and Meet the team links. The quality-to-commerce flow remains connected to the same analysis. The supplied horizontal LotLens lockup and aperture favicon are integrated. This blueprint describes intended content and workflow; it is not a claim that every suggested navigation or layout detail is implemented.

## Design goal

Present LotLens as one connected manufacturing investigation: a quality alert identifies an affected lot, evidence and an AMD-generated brief help a quality lead investigate it, and an inventory snapshot shows what that alert could mean for stock and open orders. The user should be able to follow that chain without mistaking a suggestion for an action or a synthetic scenario for a validated factory result.

The interface should feel like a focused investigation workspace, with clear hierarchy, useful density, and purposeful interaction. Avoid presenting the product as a collection of generic metric cards.

## Information architecture

Use one active investigation with four destinations in a compact workspace navigation:

1. **Overview** — the outcome and current investigation state.
2. **Quality investigation** — trend, calculated evidence, procedure sources, and AMD interpretation.
3. **Inventory impact** — alerted-lot mapping, affected allocations, unaffected stock, and any gap.
4. **Handoff** — a reviewable summary and download action.

Keep the active dataset, line, time window, and synthetic/uploaded provenance visible across destinations. Commerce must remain connected to the lot identified by the quality result. Do not create separate product experiences that make the relationship between tracks unclear.

## Screen structure

### 0. Investigation setup

**Purpose:** Make the input and readiness legible before analysis.

- Keep data-source selection and controls in a compact setup rail or drawer.
- For samples, offer **Seeded drift** and **Stable process**. For uploads, show the required readings template and field guide.
- Show inventory and open-orders inputs as optional Commerce context for uploaded readings; explain that both are needed for uploaded-data impact analysis.
- Show a concise data-readiness summary: reading count, line, batches, and time window. Identify sample data as synthetic and uploaded data as origin-unverified.
- Use one primary **Run analysis** action with a clear in-progress state.

Do not show result cards or imply an analysis has run before the user starts it.

### 1. Investigation overview

**Purpose:** Give a quality lead a fast, trustworthy summary and a route into the supporting detail.

- Start with an incident header: normal or drift state, affected line and lot when present, onset and confirmation when detected, and data provenance.
- Under it, show a short journey indicator: **Quality signal → Evidence review → Inventory impact → Human handoff**. Mark unavailable or not-applicable steps honestly.
- Make the defect-rate trend the main visual anchor. Mark actual readings, baseline, threshold, and onset with the existing chart roles; include readable labels and useful hover details.
- Pair the chart with a compact set of calculated facts: baseline, threshold, latest rate, and sustained-reading rule. Keep these facts visibly distinct from AI interpretation.
- Show a concise Commerce outcome: coverage available, uncovered units, lot mapping needed, input needed, or no implicated lot. Link to Inventory impact for the full calculation.
- Keep a persistent **Review handoff** action available after a result exists.

### 2. Quality investigation

**Purpose:** Explain why the alert appeared and what a person can inspect next.

- Provide the trend at a larger reading size, with alert markers tied to actual detector output.
- Present the supporting readings in a compact evidence table with timestamp, batch, defect count, rate, and supplied sensor context. Sensor values remain descriptive and do not imply limits or causes.
- Present procedure excerpts with source IDs and section labels, visibly marked as synthetic examples.
- Place the AMD-generated summary, possible checks, and uncertainty in a clearly attributed panel. Keep the measured facts outside the model-written text.
- Keep **Generate investigation brief** as an explicit action. Show endpoint-reported model attribution after success; show a useful failure state while retaining the detector result and sources.

### 3. Inventory impact

**Purpose:** Connect the affected quality lot to a transparent stock review.

- Begin with the linked alerted batch and its SKU mapping. If the batch maps to more than one SKU, make each mapping explicit.
- Show the calculation as a reconciliation: affected on-hand and reserved units; unaffected available stock; reserved units plus unallocated open orders; reallocated amount; uncovered gap; remaining clean stock.
- Use a lot-level table to show which inventory rows are counted as affected or unaffected.
- State the data source and snapshot limitation beside the calculation.
- Phrase the recommendation as a human-reviewed option. Clearly say LotLens has not placed a hold, changed an order, or allocated stock.

### 4. Handoff

**Purpose:** Make the investigation easy to pass to the next person without implying that it was sent or acted on.

- Preview the affected lot, status, time window, calculated evidence, procedure references, AMD interpretation if available, uncertainty, and Commerce snapshot result if assessed.
- Retain provenance labels and human-review language in the exported summary.
- Offer copy/download controls. Do not imply that LotLens sent the handoff to another system or person.

## Interaction and state behavior

- Changing the sample scenario or uploaded readings invalidates the previous result and generated brief until analysis runs again.
- A stable result shows **No qualifying drift under this rule** and makes clear that it does not prove all quality conditions are normal. Commerce reports that no lot is implicated; it must not recommend holding a lot.
- A detected drift links the same batch ID from the detector to the inventory mapping and handoff.
- Missing or invalid Commerce files leave the Industry result intact and explain which Commerce input is needed or invalid.
- Invalid CSV, too few readings, or an unavailable AMD service are input/service states, not manufacturing findings.
- Model failure leaves the chart, calculated evidence, and procedure excerpts usable.
- Color is never the only state signal. Preserve labels, keyboard focus, touch-accessible controls, reduced-motion support, and the existing contrast requirements.

## Suggested demo flow

1. Introduce the quality lead's question: which lot changed, when did it begin, and what evidence should be reviewed?
2. Show **Stable process** briefly to demonstrate a no-alert result.
3. Switch to **Seeded drift** and run the analysis. Point out the onset, confirmation, threshold, and affected lot on the trend.
4. Inspect the three supporting readings and synthetic procedure references.
5. Generate the AMD brief and show its source-linked checks, model attribution, and uncertainty. Keep API credentials off-screen.
6. Open **Inventory impact** for that same lot. Walk through reservations, unallocated orders, unaffected stock, and the resulting coverage or gap.
7. Close on the handoff and the human review boundary: no cause is confirmed and no stock or equipment action was executed.

## Visual and product constraints

- Keep Mineral Precision's finalized palette, semantic roles, typography direction, and accessibility rules unchanged. This blueprint addresses layout and interaction, not theme revision.
- Use the supplied horizontal LotLens lockup in the navbar and the supplied aperture mark as the favicon. Do not create a substitute mark as part of this planning step.
- Use the current deterministic detector and Commerce calculations as the source of displayed facts. Do not add invented scores, causes, forecasts, or operational actions.
- Label built-in data and sample procedures as synthetic. The local `LINE-04_Production_Quality_Log.csv` is a factory-derived synthetic fixture per user confirmation; do not present it as a raw or independent factory export.

## Completion criterion for this planning step

The redesign is ready to implement when the team agrees that the four destinations, the linked quality-to-inventory journey, the major states, and the demo sequence represent the intended LotLens story. No application files or visual assets are changed by this blueprint.
