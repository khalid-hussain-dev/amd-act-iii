# LOTLENS — VISUAL IDENTITY & COLOR SYSTEM
## Finalized Theme Specification v1.0

**Project:** LotLens — Quality Drift Investigator  
**Hackathon:** AMD Developer Hackathon: ACT III  
**Primary category:** Intelligent Industry  
**Document status:** Finalized — Creative Direction and Color Palette  
**Design direction:** Mineral Precision  
**Primary brand accent:** Mineral Sage — `#B8CBA8`

---

## 1. Purpose and Scope

This document defines the finalized visual identity and color system for LotLens. It is the authoritative creative reference for implementing the product's visual theme.

The purpose is to establish a recognizable, premium industrial identity that supports the application's actual function: detecting production-quality drift, examining affected batches, investigating supporting evidence, and helping quality professionals make informed decisions.

This document defines the visual direction, colors, semantic color roles, typography, surface treatments, interaction principles, and design constraints.

### Scope boundaries

**Included:**
- Overall visual philosophy and creative direction
- Primary and secondary color palettes
- Backgrounds, surfaces, borders, and typography colors
- Semantic status colors
- Chart and data-visualization colors
- Glassmorphism, lighting, shadows, and depth
- Typography and iconography direction
- Hover states, transitions, and interaction principles
- Accessibility and usability requirements
- Explicit design DON'Ts

**Not included:**
- Actual screen design, wireframes, or mockups
- Application layout and information architecture
- Logo or wordmark design
- Marketing website or promotional assets
- Detailed component-by-component implementation
- Backend logic, statistical detection, or AI architecture

Codex owns the implementation and detailed UI design. This document establishes the creative decisions that implementation must respect.

---

## 2. Creative Vision

### 2.1 The design direction: Mineral Precision

Mineral Precision combines industrial credibility, investigative intelligence, and premium visual sophistication.

The visual identity draws inspiration from:
- Dark mineral materials and graphite surfaces
- Precision-engineered instruments
- Restrained metallic highlights
- Subtle mineral-green undertones
- Dimensional translucent surfaces
- Clean, evidence-focused data visualization
- Fine borders, controlled illumination, and precise typography

The result should feel like a sophisticated industrial investigation product rather than a generic SaaS dashboard, a developer tool, or a futuristic science-fiction interface.

### 2.2 The intended personality

LotLens should feel:

- **Precise:** Measurements, thresholds, and evidence are presented clearly.
- **Investigative:** The interface supports tracing changes and examining why an alert occurred.
- **Dependable:** Calculated findings and source-backed information remain central.
- **Premium:** The visual execution feels deliberate, refined, and exceptionally well crafted.
- **Technically sophisticated:** Charts, timelines, and interactions communicate analytical capability.
- **Distinctive:** The product has a recognizable visual signature that avoids commonplace technology aesthetics.

The product should look impressive because its visual system is coherent and thoughtfully executed—not because it contains the largest number of effects.

### 2.3 The central design principle

**Premium visual expression must reinforce investigative clarity.**

LotLens may use glassmorphism, ambient lighting, layered surfaces, sophisticated hover effects, and refined motion. These are encouraged when they enhance the experience.

They must not obscure measurements, interfere with chart interpretation, hide uncertainty, or make it difficult to distinguish calculated facts from AI-generated interpretation and human decisions.

The objective is not minimalism at all costs. It is expressive design with disciplined execution.

---

## 3. Primary Color Palette

The following foundational colors are finalized.

### 3.1 Core backgrounds and surfaces

| Color name | Hex code | Role and rationale |
|---|---|---|
| Obsidian Mineral | `#101311` | Primary application background. A near-black with a subtle green undertone, providing depth without the sterile appearance of pure black. |
| Deep Graphite | `#171C19` | Primary workspace and major surface color. Establishes the industrial foundation and separates content from the background. |
| Raised Slate | `#202722` | Elevated cards, selected surfaces, and interactive content regions. Creates depth through tonal separation. |
| Mineral Edge | `#2B342D` | Emphasized surfaces, active containers, and stronger selected states. Introduces a richer mineral tone without excessive contrast. |

**Rationale:** These colors establish depth through controlled tonal variation rather than relying on heavy borders, strong gradients, or conspicuous shadows everywhere.

They should form a coherent hierarchy. The application should not become a collection of arbitrarily colored dark cards.

### 3.2 Primary brand accent

| Color name | Hex code | Role |
|---|---|---|
| Mineral Sage | `#B8CBA8` | Primary brand accent |

Mineral Sage is the defining color of the LotLens visual identity.

Its muted, mineral-like character distinguishes the product from the common electric-blue and cyan technology aesthetic. It introduces warmth and personality while remaining compatible with dark industrial surfaces.

**Use it for:**
- Primary actions
- Active navigation and selected controls
- Selected data points where appropriate
- Focus indicators
- Subtle highlights and restrained ambient lighting
- Important interface elements that need a recognizable brand signature

**Do not use it indiscriminately.** It should remain distinctive because it is applied deliberately.

Mineral Sage does not mean that a production process is operating normally. Brand identity and operational status are separate concerns.

### 3.3 Secondary brand accent

| Color name | Hex code | Role |
|---|---|---|
| Brushed Brass | `#D0B17A` | Secondary signature accent |

Brushed Brass introduces a warm metallic character that complements the mineral-green foundation.

It provides visual richness and contrast without introducing another dominant technology color.

**Use it for:**
- Selective highlights
- Important secondary metrics
- Fine decorative details
- Restrained emphasis within selected surfaces
- Occasional visual accents that benefit from warmth

**Do not use it as the default warning color.** Drift and severity indicators have their own semantic colors.

Brass should remain an accent, not a competing primary brand color.

### 3.4 Typography and neutral colors

| Color name | Hex code | Intended role |
|---|---|---|
| Porcelain | `#F0F1E9` | Primary headings and essential text |
| Mist | `#C1C8BF` | Secondary text and supporting information |
| Ash | `#929B92` | Muted metadata, timestamps, and tertiary labels |
| Mineral Border | `#343D36` | Standard borders and dividers |
| Deep Divider | `#272F29` | Subtle separators within dense layouts |
| Pure White | `#FFFFFF` | Reserved for contexts requiring additional contrast |

Porcelain provides a softer, more refined alternative to using pure white for all text.

Mist establishes the secondary text hierarchy, while Ash is reserved for less prominent information.

Essential content must not become difficult to read merely to achieve a muted aesthetic. Small labels, chart axes, timestamps, and citations require particular attention during contrast testing.

---

## 4. Semantic Color System

Semantic colors communicate the actual state or meaning of information. They must remain consistent across the application.

They are not interchangeable with brand accents.

### 4.1 Semantic colors

| State | Color name | Hex code | Meaning |
|---|---|---|---|
| Normal | Signal Green | `#75C69A` | Confirmed normal results under the configured detection rules |
| Drift detected | Signal Amber | `#E8B45D` | Detected drift, threshold crossings, and investigation-required conditions |
| Critical | Signal Vermilion | `#F0786B` | Explicitly defined high-severity findings or serious application errors |
| AI-generated | Insight Lavender | `#B6A4E0` | AI-written interpretation and generated investigation guidance |
| Informational | Signal Ice | `#9DBDD9` | Neutral system guidance and noncritical information |

### 4.2 Semantic surface colors

| State | Background | Border |
|---|---|---|
| Normal | `#192820` | `#315640` |
| Drift | `#30271A` | `#66502D` |
| Critical | `#321F1D` | `#74403A` |
| AI-generated | `#272333` | `#51466C` |
| Informational | `#1E2931` | `#3C5365` |

These backgrounds should remain subdued. Semantic colors can be used for icons, badges, borders, short labels, and selected highlights while the surrounding interface remains consistent with the primary palette.

### 4.3 Rules for semantic colors

1. **Never rely on color alone.** Every important state must also have a readable label and, where appropriate, an icon.
2. **Do not exaggerate severity.** A drift detection must not automatically be presented as a critical factory emergency.
3. **Reserve critical red for justified conditions.** Do not use it merely to make the interface feel dramatic.
4. **Keep AI attribution explicit.** AI-generated content must be distinguishable from calculated evidence.
5. **Represent uncertainty honestly.** Uncertainty must be communicated through clear language and information structure, not an invented severity color.
6. **Separate data errors from production findings.** An invalid CSV or insufficient evidence does not establish that a production line has failed.
7. **Keep the interface useful without AI.** An unavailable model must not erase already calculated findings or charts.
8. **Preserve human authority.** Suggestions must not be presented as completed actions, confirmed root causes, or autonomous operational decisions.

The semantic palette describes information states. The statistical detector and application logic determine which states are actually present.

---

## 5. Data Visualization Palette

Data visualization is a central part of LotLens, not a decorative addition to the dashboard.

Charts must make it easy to identify the actual readings, compare them with the baseline, understand thresholds, and locate the onset of detected drift.

### 5.1 Chart colors

| Chart element | Color | Hex code |
|---|---|---|
| Actual measurements | Porcelain variant | `#E0E7DD` |
| Stable baseline | Mineral Sage | `#B8CBA8` |
| Baseline range or confidence band | Muted Sage | `#647A60` |
| Drift threshold | Signal Amber | `#E8B45D` |
| Detected change point | Signal Vermilion | `#F0786B` |
| Secondary measurement series | Insight Lavender | `#B6A4E0` |
| Tertiary measurement series | Signal Ice | `#9DBDD9` |
| Grid lines | Deep Divider | `#272F29` |
| Axis labels | Ash | `#929B92` |
| Hover crosshair | Mist | `#C1C8BF` |

### 5.2 Chart design principles

- Actual readings and baselines must remain visually distinguishable.
- Thresholds must be visible without obscuring the measurements.
- Baseline ranges should use restrained transparency.
- Detected change points should have an unmistakable marker.
- Hover interactions should reveal useful evidence, including timestamps, readings, baseline comparisons, thresholds, and series identity where applicable.
- Multiple measurement series must be distinguishable without relying exclusively on color.
- Chart colors must remain consistent between the visualization, investigation summary, and supporting evidence.
- Axis labels, legends, and tooltips must remain readable against their backgrounds.

**Technical integrity is mandatory:** the frontend must not invent drift points, confidence ranges, statistical significance, or severity levels that the analysis engine did not calculate.

A confidence band may be shown only if the underlying analysis actually defines the range it represents.

A clear chart with two or three meaningful series is preferable to a visually impressive chart with unnecessary colors and clutter.

---

## 6. Glassmorphism and Surface Treatment

### 6.1 Visual approach

LotLens should use a sophisticated layered-glass aesthetic, combining smoked translucent surfaces, subtle mineral-green undertones, precise borders, restrained reflections, and ambient illumination.

Glassmorphism is an intentional part of the identity. It should not be removed simply to make the interface flat or conventional.

The treatment should feel like refined industrial instrumentation rather than a generic futuristic control panel.

### 6.2 Glass and lighting tokens

| Token | Value | Intended application |
|---|---|---|
| Glass fill | `rgba(32, 39, 34, 0.76)` | Floating panels and contextual overlays |
| Glass fill strong | `rgba(23, 28, 25, 0.92)` | Dialogs and important overlays |
| Glass border | `rgba(184, 203, 168, 0.14)` | Subtle illuminated edges |
| Glass highlight | `rgba(240, 241, 233, 0.07)` | Fine top-edge reflections |
| Sage glow | `rgba(184, 203, 168, 0.10)` | Selected states and restrained emphasis |
| Brass glow | `rgba(208, 177, 122, 0.09)` | Occasional visual highlights |
| Drift glow | `rgba(232, 180, 93, 0.12)` | Active drift indicators |
| Deep shadow | `rgba(0, 0, 0, 0.30)` | Elevation and separation |

These values are initial design tokens. They should be adjusted when necessary to maintain contrast, visual hierarchy, and consistency.

### 6.3 Appropriate uses

Glassmorphism and dimensional effects may be used for:

- Floating panels
- Dialogs and overlays
- Contextual menus and popovers
- Selected and elevated cards
- Filter interfaces
- Navigation highlights
- Interactive tooltips
- Focused investigation elements

Dense data tables, measurement readings, long procedure excerpts, and AI-generated briefs should use sufficiently opaque surfaces whenever transparency would compromise legibility.

### 6.4 Lighting principles

Lighting should be selective and purposeful.

Mineral Sage can provide a restrained ambient glow for selected interface elements. Brushed Brass can introduce occasional warmth. Signal Amber can emphasize an active drift state.

Avoid illuminating every card, border, button, and chart simultaneously. Visual emphasis only works when some elements remain quieter than others.

The result should feel dimensional and premium without turning into a neon spectacle.

---

## 7. Interaction and Motion

Interaction design is part of the visual identity and should receive the same level of care as static appearance.

### 7.1 Initial interaction tokens

| Property | Specification |
|---|---|
| Hover transition | 160–220 ms |
| Press transition | 90–140 ms |
| Standard control radius | 8–10 px |
| Standard card radius | 12–16 px |
| Large panel radius | 18–22 px |
| Standard border | 1 px |
| Focus ring | 2 px, `#B8CBA8` |
| Reduced motion | Respect operating-system preferences |

These are initial values for implementation, not reasons to force every interaction into identical timing.

### 7.2 Hover behavior

Hover states should communicate interactivity and reward exploration.

Appropriate effects include:

- Slight surface brightening
- A more visible border
- A subtle increase in elevation
- A restrained glow on selected controls
- Chart-point enlargement
- Highlighting related evidence
- Smooth tooltip appearances
- Clear visual feedback for clickable rows and cards

Hover effects should not dramatically change the component's size, shift surrounding content, or obscure adjacent information.

Important information must never be available exclusively through hover. Equivalent focus states and touch-friendly interactions are required.

### 7.3 Motion

Animations should clarify what is happening.

Useful examples include analysis progress, chart-point highlighting, contextual-panel transitions, and loading-state feedback.

Avoid continuous animation without a functional purpose. Do not make the entire interface pulse or glow simply to communicate that AI is involved.

Animations should remain smooth, restrained, and responsive. Respect reduced-motion preferences.

---

## 8. Typography

The selected typography direction combines clean contemporary sans-serif families with a technical monospace family for numerical and machine-oriented information.

### 8.1 Selected typefaces

| Typeface | Role |
|---|---|
| Manrope | Display typography and headings |
| Inter | Body text, navigation, forms, tables, and general interface text |
| IBM Plex Mono | Measurements, timestamps, batch identifiers, thresholds, and technical metadata |

### 8.2 Usage principles

**Manrope**
- Establishes the product's contemporary, premium character.
- Should be used for headings and prominent display text.
- Should remain controlled rather than excessively oversized.

**Inter**
- Provides readable, consistent interface typography.
- Should carry most descriptions, labels, forms, navigation, and investigation text.
- Must remain comfortable to read in dense evidence-heavy sections.

**IBM Plex Mono**
- Provides a technical character for values and identifiers.
- Should distinguish measurements and structured technical information.
- Must not be used for long paragraphs or general interface copy.

Use clear typographic hierarchy and comfortable line spacing. Typography should help users scan the investigation quickly.

Font files must be obtained from appropriate sources and used in accordance with their licenses. Provide sensible fallback fonts.

---

## 9. Iconography and Decorative Elements

Use a consistent line-icon family with restrained stroke weights and recognizable shapes.

Icons should communicate meaningful actions or states. Decorative elements must not compete with labels, measurements, or charts.

The visual language may include fine measurement lines, threshold markers, timeline annotations, subtle geometric details, and precision-inspired separators.

These details should emerge naturally from LotLens's investigative purpose. They should not be added simply to make the interface look technical.

The logo and wordmark are intentionally excluded from this document and will be discussed separately after the broader visual identity has been established.

---

## 10. Applying the Theme to LotLens

The same identity must work across every important application state.

### Main workspace

Use Obsidian Mineral as the foundation, Deep Graphite for primary surfaces, Raised Slate for elevated cards, Porcelain for essential text, and Mineral Sage for selected controls and primary actions.

### Drift investigation

Use neutral measurement lines, a clearly visible baseline, Signal Amber for the relevant threshold or drift state, and a distinct marker for the detected change point.

The visualization should make the evidence easy to interpret without relying on dramatic warning effects.

### AI investigation brief

Use a readable surface with a clear distinction between:
- Observed evidence
- Procedure-grounded possible checks
- Remaining uncertainty

Insight Lavender identifies AI-generated interpretation. Procedure references must be easy to inspect, and suggestions must not be presented as proven causes.

### Synthetic data

All sample records must carry a clear, persistent `SYNTHETIC DATA` label. This must not be represented solely by a color or an easily missed tooltip.

### Analysis in progress

Use restrained progress animation and meaningful progress labels where available. Avoid pretending the system is performing a particular analytical step if that step is not actually taking place.

### Normal results

Use Signal Green with clear wording that the detector found no qualifying drift under its configured rules. Do not imply that all aspects of production quality have been proven satisfactory.

### Invalid CSV and insufficient evidence

Use readable validation or informational treatments. Explain what is missing or invalid. Do not present input errors as evidence of manufacturing defects.

### AMD/model service unavailable

Keep existing calculated findings and charts available when possible. Clearly indicate that the generated brief is unavailable. Never fabricate an AI response to preserve the appearance of a complete interface.

### Human decisions

Clearly distinguish generated suggestions from actions the quality lead has actually taken. The interface must not imply that it controls machinery, stops production, confirms root causes, or issues work orders automatically.

---

## 11. Explicit DON'Ts

The following constraints protect the identity from becoming generic, visually excessive, or misleading.

### Color and branding

- Do not default to electric blue, cyan, or purple as the dominant brand palette.
- Do not introduce a new accent color without a clear functional or brand justification.
- Do not allow Mineral Sage, Brushed Brass, and semantic status colors to compete equally.
- Do not use Brushed Brass as a substitute for Signal Amber.
- Do not use Signal Green to imply broader production safety than the detector has established.
- Do not use Signal Vermilion merely to make alerts look more dramatic.
- Do not scatter arbitrary hexadecimal values throughout the codebase when an existing design token applies.

### Visual effects

- Do not eliminate glassmorphism merely for minimalism's sake.
- Do not apply glass effects where they compromise readability.
- Do not use excessive neon, bloom, glowing borders, or perpetual pulsing.
- Do not turn the interface into a generic futuristic control room.
- Do not use decorative gradients or ambient effects that compete with the actual data.
- Do not make every card look elevated or interactive.
- Do not use animation without a clear functional or experiential purpose.

### Information and usability

- Do not rely exclusively on color to communicate a state.
- Do not hide important evidence in hover-only interactions.
- Do not sacrifice text contrast to maintain a muted aesthetic.
- Do not present AI-generated interpretation as calculated fact.
- Do not imply that possible checks establish a confirmed root cause.
- Do not invent statistical findings or visual evidence in the frontend.
- Do not make essential functionality dependent on the availability of the AI service.
- Do not represent synthetic records as real factory data.
- Do not make an unavailable model appear to have completed its task.
- Do not confuse data validation failures with production-quality failures.

### Overall product character

- Do not turn LotLens into a generic SaaS dashboard.
- Do not add visual elements solely because they look fashionable.
- Do not mistake complexity for sophistication.
- Do not sacrifice clarity for a visually impressive screenshot.
- Do not treat the cover image, marketing appearance, or isolated dashboard as a substitute for consistent product-wide execution.

The standard is a distinctive, polished industrial investigation experience whose visual quality and functional clarity reinforce one another.

---

## 12. Accessibility and Validation

The specified colors and opacities must be tested in their actual UI combinations before the application is considered ready.

Required checks include:

- Text and background contrast
- Small labels and muted metadata
- Chart axes, legends, and tooltips
- Status badges and their tinted surfaces
- Translucent panels over varying backgrounds
- Focus indicators and keyboard navigation
- Touch interaction and hover alternatives
- Reduced-motion behavior
- Color-blind distinguishability of chart series and semantic states

Aim for WCAG 2.2 AA contrast requirements: at least 4.5:1 for normal text and 3:1 for large text, with applicable non-text contrast requirements for meaningful interface elements.

Do not assume that a text color passes contrast requirements merely because it appears readable in a screenshot.

Where a color combination fails, adjust the component-specific foreground, background, opacity, or treatment while preserving the overall identity and semantic meaning.

---

## 13. Implementation Principles

Codex should treat this document as the source of truth for the creative direction and foundational color tokens.

Implementation should:

1. Centralize colors, opacity values, borders, radii, shadows, typography, and transition values in reusable tokens.
2. Reuse the same semantic colors consistently across components.
3. Keep brand accents separate from operational-status colors.
4. Maintain readable, stable surfaces for evidence-heavy content.
5. Apply glassmorphism and lighting selectively but confidently.
6. Preserve a consistent visual language across loading, success, failure, and unavailable-service states.
7. Respect accessibility and reduced-motion preferences.
8. Avoid inventing findings or overstating what the analysis engine has established.
9. Test actual component combinations instead of relying on the appearance of isolated color swatches.
10. Keep implementation decisions within the established creative direction unless a genuine usability, technical, or accessibility issue requires a justified adjustment.

The foundational color tokens are specified below for convenient implementation.

```css
:root {
  color-scheme: dark;

  /* Foundation */
  --ll-bg: #101311;
  --ll-surface: #171C19;
  --ll-surface-raised: #202722;
  --ll-surface-emphasis: #2B342D;

  /* Brand */
  --ll-sage: #B8CBA8;
  --ll-brass: #D0B17A;

  /* Typography */
  --ll-text-primary: #F0F1E9;
  --ll-text-secondary: #C1C8BF;
  --ll-text-muted: #929B92;

  /* Borders */
  --ll-border: #343D36;
  --ll-divider: #272F29;
  --ll-focus: #B8CBA8;

  /* Semantic states */
  --ll-normal: #75C69A;
  --ll-drift: #E8B45D;
  --ll-critical: #F0786B;
  --ll-ai: #B6A4E0;
  --ll-info: #9DBDD9;

  /* Glass */
  --ll-glass: rgba(32, 39, 34, 0.76);
  --ll-glass-strong: rgba(23, 28, 25, 0.92);
  --ll-glass-border: rgba(184, 203, 168, 0.14);
  --ll-glass-highlight: rgba(240, 241, 233, 0.07);

  /* Ambient lighting */
  --ll-glow-sage: rgba(184, 203, 168, 0.10);
  --ll-glow-brass: rgba(208, 177, 122, 0.09);
  --ll-glow-drift: rgba(232, 180, 93, 0.12);

  /* Interaction */
  --ll-radius-control: 9px;
  --ll-radius-card: 14px;
  --ll-radius-panel: 20px;
  --ll-transition-fast: 120ms;
  --ll-transition-standard: 180ms;
  --ll-transition-emphasis: 220ms;

  /* Typography */
  --ll-font-display: "Manrope", sans-serif;
  --ll-font-body: "Inter", sans-serif;
  --ll-font-mono: "IBM Plex Mono", monospace;
}
```

This is the foundational token sheet. Semantic surface colors, chart colors, and additional component-specific tokens should be centralized alongside it rather than duplicated throughout the application.

---

## 14. Finalized Decisions and Future Scope

The following decisions are finalized for this phase:

- **Visual direction:** Mineral Precision
- **Primary background:** Obsidian Mineral — `#101311`
- **Primary brand accent:** Mineral Sage — `#B8CBA8`
- **Secondary brand accent:** Brushed Brass — `#D0B17A`
- **Surface hierarchy:** Deep Graphite, Raised Slate, and Mineral Edge
- **Typography:** Porcelain, Mist, and Ash
- **Semantic palette:** Signal Green, Signal Amber, Signal Vermilion, Insight Lavender, and Signal Ice
- **Data visualization palette:** Defined by the roles specified in Section 5
- **Surface treatment:** Layered glass, restrained lighting, subtle borders, and controlled shadows
- **Interaction style:** Refined hover states, clear focus states, and purposeful transitions
- **Typography families:** Manrope, Inter, and IBM Plex Mono
- **Accessibility:** Required contrast, keyboard, touch, and reduced-motion validation
- **Logo:** Deferred to a separate discussion
- **Actual UI implementation:** Assigned to Codex

The foundational palette and creative direction are finalized. Individual implementation details may be adjusted when necessary to preserve usability, accessibility, technical integrity, and consistency with this specification.

### Final creative statement

**LotLens — Mineral Precision**

A premium industrial investigation experience built around mineral-green graphite, warm metallic highlights, refined dimensional surfaces, and evidence-led data visualization.

Its visual identity should be distinctive without being distracting, expressive without being excessive, and sophisticated without compromising clarity.

The product's calculated evidence remains authoritative. AI contributes attributed interpretation. Human professionals retain decision-making authority.

**The goal is not simply to make LotLens look premium. The goal is to create a recognizable, coherent, exceptionally executed product identity that makes its technical purpose immediately understandable.**