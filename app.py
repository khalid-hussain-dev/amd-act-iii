from __future__ import annotations

import hashlib
import html
import os
import base64
from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dotenv import dotenv_values
from streamlit.errors import StreamlitSecretNotFoundError

from lotlens.amd_client import describe_inference_error, generate_investigation_brief, is_configured, missing_settings
from lotlens.commerce import calculate_inventory_impact, sample_inventory, sample_orders, validate_commerce_inputs
from lotlens.detector import CSV_TEMPLATE_COLUMNS, DetectionResult, detect_quality_drift, validate_dataframe
from lotlens.evidence import build_retrieval_query, retrieve_procedures
from lotlens.sample_data import build_sample_dataset


ROOT = Path(__file__).resolve().parent


def _load_runtime_env() -> None:
    """Fill missing AMD settings from Streamlit secrets or local .env.

    Explicit process environment values take precedence, followed by hosted
    Streamlit secrets and then local dotenv values. This keeps credentials out
    of the repository and avoids replacing host-provided configuration.
    """
    try:
        hosted_secrets = st.secrets
        for name in ("AMD_CHAT_COMPLETIONS_URL", "AMD_MODEL_NAME", "AMD_API_KEY"):
            value = hosted_secrets.get(name)
            if value is not None and not os.environ.get(name, "").strip():
                os.environ[name] = str(value)
    except StreamlitSecretNotFoundError:
        # Streamlit's secrets mapping can raise lazily on .get() when no
        # secrets.toml exists. Local development can continue via .env.
        pass

    for name, value in dotenv_values(ROOT / ".env").items():
        if value is not None and not os.environ.get(name, "").strip():
            os.environ[name] = value


_load_runtime_env()

st.set_page_config(
    page_title="LotLens — Quality Drift Investigator",
    page_icon=str(ROOT / "logos" / "LotLens Aperture Favicon.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)


def _inject_theme() -> None:
    css = (ROOT / "assets" / "theme.css").read_text(encoding="utf-8")
    aperture_icon = base64.b64encode((ROOT / "logos" / "LotLens Aperture Favicon.png").read_bytes()).decode("ascii")
    css = css.replace("__LL_APERTURE_ICON__", f"data:image/png;base64,{aperture_icon}")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def _metric_card(label: str, value: str, note: str, accent: str = "") -> None:
    style = f"border-top:2px solid {accent};" if accent else ""
    st.markdown(
        f'<div class="ll-card" style="{style}">'
        f'<div class="ll-card-title">{html.escape(label)}</div>'
        f'<div class="ll-card-value">{html.escape(value)}</div>'
        f'<div class="ll-card-note">{html.escape(note)}</div></div>',
        unsafe_allow_html=True,
    )


def _section_heading(anchor: str, index: str, eyebrow: str, title: str, subtitle: str) -> None:
    """Render a consistent, linkable workspace section heading."""
    st.markdown(
        f'<div class="ll-section-head" id="{html.escape(anchor)}">'
        f'<div class="ll-section-index">{html.escape(index)}</div>'
        f'<div class="ll-section-copy"><div class="ll-kicker">{html.escape(eyebrow)}</div>'
        f'<div class="ll-panel-heading">{html.escape(title)}</div>'
        f'<div class="ll-panel-sub">{html.escape(subtitle)}</div></div></div>',
        unsafe_allow_html=True,
    )


def _action_panel(eyebrow: str, title: str, detail: str) -> None:
    """Add a dedicated visual home for a primary workspace action."""
    st.markdown(
        f'<div class="ll-action-panel">'
        f'<div class="ll-action-eyebrow">{html.escape(eyebrow)}</div>'
        f'<div class="ll-action-title">{html.escape(title)}</div>'
        f'<div class="ll-action-detail">{html.escape(detail)}</div></div>',
        unsafe_allow_html=True,
    )


def _render_team_section() -> None:
    cover = base64.b64encode((ROOT / "assets" / "team" / "parallax-cover.jpg").read_bytes()).decode("ascii")
    portrait = base64.b64encode((ROOT / "assets" / "team" / "khalid-hussain.jpg").read_bytes()).decode("ascii")
    st.markdown(
        '<section class="ll-team-section" id="team" aria-labelledby="ll-team-title">'
        f'<div class="ll-team-cover" style="background-image:linear-gradient(90deg,rgba(12,16,14,.94) 0%,rgba(12,16,14,.67) 52%,rgba(12,16,14,.1) 100%),url(data:image/jpeg;base64,{cover})">'
        '<div class="ll-team-cover-copy"><div class="ll-team-eyebrow">THE PEOPLE BEHIND LOTLENS</div>'
        '<h2 id="ll-team-title">Meet the team</h2>'
        '<p>PARALLAX turns interesting problems into meaningful, well-executed solutions.</p></div></div>'
        '<div class="ll-team-intro"><span>PARALLAX</span><p>We bring together AI, software development, design, and creative problem-solving to build something useful, original, and impactful.</p></div>'
        '<div class="ll-team-list-label">TEAM DIRECTORY <span>01 MEMBER</span></div>'
        '<article class="ll-team-member"><img class="ll-team-portrait" src="data:image/jpeg;base64,' + portrait + '" alt="Khalid Hussain, PARALLAX team lead" />'
        '<div class="ll-team-member-copy"><div class="ll-team-member-role">TEAM LEAD <span>·</span> MEMBER 01</div>'
        '<h3>Khalid Hussain</h3><p>Building at the intersection of AI, software, and thoughtful product design.</p>'
        '<div class="ll-team-handle">@sheikh_khalid_hussain837</div>'
        '<div class="ll-team-socials" aria-label="Khalid Hussain social links">'
        '<a href="https://github.com/khalid-hussain-dev" target="_blank" rel="noopener noreferrer" aria-label="GitHub">'
        '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .9a11.1 11.1 0 0 0-3.51 21.63c.55.1.76-.24.76-.54v-2.1c-3.1.67-3.76-1.32-3.76-1.32-.5-1.29-1.24-1.64-1.24-1.64-1.01-.69.08-.68.08-.68 1.12.08 1.71 1.15 1.71 1.15 1 .1.76 2.09 3.2 1.59.1-.72.4-1.21.7-1.49-2.48-.28-5.09-1.24-5.09-5.52 0-1.22.44-2.21 1.15-2.99-.11-.28-.5-1.42.11-2.95 0 0 .94-.3 3.05 1.14a10.6 10.6 0 0 1 5.55 0c2.12-1.44 3.05-1.14 3.05-1.14.61 1.53.23 2.67.12 2.95.71.78 1.14 1.77 1.14 2.99 0 4.29-2.61 5.23-5.1 5.51.4.35.75 1.03.75 2.08v3.08c0 .3.2.65.77.54A11.1 11.1 0 0 0 12 .9Z"/></svg><span>GitHub</span></a>'
        '<a href="https://www.linkedin.com/in/khalid-hussain-dev" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">'
        '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5.1 3.2a2.1 2.1 0 1 1 0 4.2 2.1 2.1 0 0 1 0-4.2ZM3.3 9h3.6v11.7H3.3V9Zm5.8 0h3.5v1.6h.05a3.85 3.85 0 0 1 3.47-1.91c3.71 0 4.4 2.44 4.4 5.61v6.4h-3.65v-5.67c0-1.35-.02-3.08-1.88-3.08s-2.17 1.47-2.17 2.98v5.77H9.1V9Z"/></svg><span>LinkedIn</span></a>'
        '<a href="https://play.google.com/store/apps/developer?id=13+Dimensions+Studio" target="_blank" rel="noopener noreferrer" aria-label="Google Play developer page">'
        '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.1 2.6c-.36.38-.56.97-.56 1.73v15.34c0 .76.2 1.35.56 1.73L13 12 4.1 2.6Zm1.05-.7L15.1 10.6l2.42-2.42L7.07 1.44c-.68-.4-1.37-.31-1.92.46Zm11.08 9.5 3.16 1.78c.98.55.98 1.44 0 1.99l-3.16 1.78L13.8 12l2.43-2.43Zm-1.14 2.43L5.15 21.99c.55.77 1.24.86 1.92.46l10.45-6.74-2.43-1.88Z"/></svg><span>Google Play</span></a>'
        '<a href="https://khalid-hussain-portfolio.vercel.app/" target="_blank" rel="noopener noreferrer" aria-label="Portfolio">'
        '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.25"/><path d="M2.9 12h18.2M12 2.75c2.35 2.5 3.53 5.58 3.53 9.25S14.35 18.75 12 21.25C9.65 18.75 8.47 15.67 8.47 12S9.65 5.25 12 2.75Z"/></svg><span>Portfolio</span></a>'
        '<a href="mailto:sheikhkhalidhussain1234@gmail.com" aria-label="Email Khalid Hussain">'
        '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.7" y="4.7" width="18.6" height="14.6" rx="2"/><path d="m3.5 6 8.5 7 8.5-7"/></svg><span>Email</span></a>'
        '</div></div></article></section>',
        unsafe_allow_html=True,
    )


def _render_footer(provenance: str) -> None:
    _render_team_section()
    st.markdown(
        '<div class="ll-footnote" style="margin-top:1rem">'
        f"LotLens provides an investigation aid, not a confirmed root-cause diagnosis or authorization to act. {html.escape(provenance)}"
        "</div>"
        '<footer class="ll-footer">'
        '<div class="ll-footer-identity">'
        '<div class="ll-footer-eyebrow">OPERATIONS INTELLIGENCE</div>'
        '<div class="ll-footer-brand">LotLens</div>'
        '<div class="ll-footer-meta">Quality Drift Investigator</div>'
        '</div>'
        '<div class="ll-footer-promise">Intelligent Industry <span>\u00d7</span> Reinvent Commerce</div>'
        '<a class="ll-footer-top" href="#top" style="color:#edf2e8!important;text-decoration:none!important">Back to top <span>\u2191</span></a>'
        '</footer>',
        unsafe_allow_html=True,
    )


def _render_preanalysis_sections(provenance: str) -> None:
    st.markdown(
        '<div class="ll-preanalysis-grid">'
        '<section class="ll-preanalysis-card" id="quality"><span>01 · INTELLIGENT INDUSTRY</span><h3>Quality investigation</h3><p>Run the local detector to reveal the measured baseline, alert status, and production evidence.</p></section>'
        '<section class="ll-preanalysis-card" id="commerce"><span>02 · REINVENT COMMERCE</span><h3>Inventory impact</h3><p>Review stock exposure after the quality signal has been calculated.</p></section>'
        '<section class="ll-preanalysis-card" id="handoff"><span>03 · SHIFT HANDOFF</span><h3>Evidence & procedure context</h3><p>Prepare a review-ready handoff with supporting readings and procedure excerpts.</p></section>'
        '</div>',
        unsafe_allow_html=True,
    )
    _render_footer(provenance)


def _fmt_pct(value: float | None) -> str:
    return "—" if value is None else f"{value:.2f}%"


def _fmt_timestamp(value: str | None) -> str:
    if not value:
        return "—"
    return pd.Timestamp(value).strftime("%b %d · %H:%M")


def _sensor_context_parts(row: dict) -> list[tuple[str, str]]:
    """Format only sensor measurements that were actually supplied."""
    fields = (
        ("temperature_c", "Temperature", "°C", 1),
        ("vibration_mm_s", "Vibration", "mm/s", 2),
        ("pressure_bar", "Pressure", "bar", 2),
    )
    parts = []
    for key, label, unit, precision in fields:
        value = row.get(key)
        if value is None or pd.isna(value):
            continue
        parts.append((label, f"{float(value):.{precision}f} {unit}"))
    return parts


def _build_chart(result: DetectionResult) -> go.Figure:
    data = result.chart_data
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["timestamp"],
            y=data["defect_rate_pct"],
            mode="lines+markers",
            name="Inspection defect rate",
            line={"color": "#E0E7DD", "width": 2.3},
            marker={"color": "#E0E7DD", "size": 5},
            hovertemplate="%{x|%b %d, %H:%M}<br>Defect rate: %{y:.2f}%<extra>Inspection sample</extra>",
        )
    )
    fig.add_hline(y=result.baseline_rate_pct, line_color="#B8CBA8", line_dash="dot", line_width=1.5,
                  annotation_text="Stable baseline", annotation_position="bottom right",
                  annotation_font_color="#B8CBA8")
    fig.add_hline(y=result.threshold_rate_pct, line_color="#E8B45D", line_dash="dash", line_width=1.4,
                  annotation_text="Alert threshold", annotation_position="top right",
                  annotation_font_color="#E8B45D")
    if result.onset_time:
        onset = pd.Timestamp(result.onset_time)
        point = data.loc[data["timestamp"] == onset].iloc[0]
        fig.add_trace(go.Scatter(
            x=[onset], y=[point["defect_rate_pct"]], mode="markers", name="Detected change point",
            marker={"color": "#F0786B", "size": 12, "line": {"color": "#101311", "width": 2}},
            hovertemplate="Change point<br>%{x|%b %d, %H:%M}<br>%{y:.2f}%<extra></extra>",
        ))
        fig.add_vline(x=onset, line_color="#F0786B", line_dash="dot", line_width=1)

    fig.update_layout(
        height=340, margin={"l": 8, "r": 12, "t": 24, "b": 8},
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif", "color": "#C1C8BF", "size": 11},
        legend={"orientation": "h", "y": 1.13, "x": 0, "font": {"size": 10}},
        hoverlabel={"bgcolor": "#202722", "bordercolor": "#343D36", "font": {"color": "#F0F1E9"}},
        xaxis={"showgrid": False, "showline": True, "linecolor": "#343D36",
               "tickfont": {"color": "#929B92", "family": "IBM Plex Mono, monospace", "size": 9}, "title": None},
        yaxis={"ticksuffix": "%", "showgrid": True, "gridcolor": "#272F29", "zeroline": False,
               "tickfont": {"color": "#929B92", "family": "IBM Plex Mono, monospace", "size": 9}, "title": None},
    )
    return fig


def _build_sensor_chart(result: DetectionResult, column: str, label: str, units: str, color: str) -> go.Figure:
    data = result.chart_data
    baseline_values = data.iloc[: result.baseline_points][column].dropna()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["timestamp"],
            y=data[column],
            mode="lines+markers",
            name=label,
            line={"color": color, "width": 2},
            marker={"color": color, "size": 5},
            hovertemplate=f"%{{x|%b %d, %H:%M}}<br>{label}: %{{y:.2f}} {units}<extra></extra>",
        )
    )
    if not baseline_values.empty:
        fig.add_hline(
            y=float(baseline_values.mean()),
            line_color="#B8CBA8",
            line_dash="dot",
            line_width=1.3,
            annotation_text="Baseline mean",
            annotation_position="bottom right",
            annotation_font_color="#B8CBA8",
        )
    if result.onset_time:
        fig.add_vline(x=pd.Timestamp(result.onset_time), line_color="#F0786B", line_dash="dot", line_width=1)
    fig.update_layout(
        height=250,
        margin={"l": 8, "r": 12, "t": 16, "b": 4},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif", "color": "#C1C8BF", "size": 11},
        showlegend=False,
        hoverlabel={"bgcolor": "#202722", "bordercolor": "#343D36", "font": {"color": "#F0F1E9"}},
        xaxis={"showgrid": False, "showline": True, "linecolor": "#343D36", "title": None},
        yaxis={"ticksuffix": f" {units}", "showgrid": True, "gridcolor": "#272F29", "zeroline": False, "title": None},
    )
    return fig


def _handoff_text(
    result: DetectionResult,
    sources: list[dict],
    brief: dict | None,
    *,
    synthetic: bool,
    included_production_log: bool = False,
    commerce: dict | None = None,
    commerce_origin: str = "Not assessed",
) -> str:
    title = "SYNTHETIC DEMO SHIFT HANDOFF" if synthetic else "PRODUCTION QUALITY LOG SHIFT HANDOFF" if included_production_log else "UPLOADED DATA SHIFT HANDOFF"
    lines = [
        f"LOTLENS - {title}", "",
        f"Status: {'Drift detected' if result.status == 'drift' else 'No qualifying drift detected'}",
        f"Line: {result.line_id or 'Not identified'}",
        f"Affected batch: {result.batch_id or 'None identified'}",
        f"Drift onset: {_fmt_timestamp(result.onset_time)}",
        f"Alert confirmed: {_fmt_timestamp(result.confirmed_time)}",
        f"Baseline defect rate: {_fmt_pct(result.baseline_rate_pct)}",
        f"Alert threshold: {_fmt_pct(result.threshold_rate_pct)}",
        f"Latest defect rate: {_fmt_pct(result.current_rate_pct)}",
        f"Baseline readings: {result.baseline_points}",
        f"Required sustained crossings: {result.sustained_points}",
        "", "Detector finding:", result.message, "", "Supporting readings:",
    ]
    if result.evidence:
        for row in result.evidence:
            sensor_context = ", ".join(f"{label}: {value}" for label, value in _sensor_context_parts(row))
            if not sensor_context:
                sensor_context = "No sensor context supplied"
            lines.append(
                f"- {_fmt_timestamp(row['timestamp'])} | {row['batch_id']} | "
                f"{row['defect_count']}/{row['units_inspected']} defects ({row['defect_rate_pct']:.2f}%) | "
                f"{sensor_context}"
            )
            if row.get("operator_note"):
                lines.append(f"  Operator note: {row['operator_note']}")
    else:
        lines.append("No sustained threshold-crossing readings were recorded by the detector.")

    lines += ["", "Procedure references (synthetic excerpts):"]
    for source in sources:
        lines += [f"- {source['title']} [{source['source_id']}]"]
        lines.append(f"  {source['text'].replace(chr(10), chr(10) + '  ')}")

    if brief:
        lines += ["", "AI-generated interpretation (review before use):", brief.get("summary", "")]
        provider = brief.get("_provider", {})
        if provider.get("model"):
            lines.append(f"AMD endpoint model: {provider['model']}")
        lines.append("Possible checks (source-grounded; human review required):")
        if brief.get("possible_checks"):
            lines.extend(f"- {item.get('text', '')} [{item.get('source_id', '')}]" for item in brief["possible_checks"])
        else:
            lines.append("- No procedure-grounded checks were returned.")
        lines += ["Uncertainty:", brief.get("uncertainty", "")]

    lines += ["", "Commerce inventory impact (human review only):", f"Snapshot: {commerce_origin or 'Not supplied'}"]
    if commerce and commerce.get("status") == "no_alert":
        lines.append("No qualifying quality alert; no lot is implicated in this analysis.")
    elif commerce and commerce.get("status") == "unmapped":
        lines.append(f"Alerted batch {commerce.get('affected_batch', 'unknown')} was not mapped to a SKU in the supplied inventory snapshot.")
    elif commerce and commerce.get("status") == "mapped":
        for product in commerce.get("products", []):
            lines.append(
                f"- {product['product_name']} ({product['sku']}): {product['affected_on_hand']} units in the alerted lot, "
                f"{product['affected_reserved']} reserved; {product['clean_available']} units available in unaffected lots."
            )
            lines.append(
                f"  Reallocation need: {product['reallocation_need']} units; covered: {product['reallocated']}; "
                f"uncovered: {product['shortfall']}; clean units remaining: {product['clean_remaining']}."
            )
            lines.append(
                "  Suggested review: hold release from the alerted lot pending quality disposition; a quality or fulfillment lead "
                "must approve any reallocation. No inventory or order was changed."
            )
    else:
        lines.append("No complete inventory and open-orders snapshot was available, so stock impact was not assessed.")

    if synthetic:
        lines += ["", "All readings and procedure excerpts in this handoff are synthetic demo material."]
    elif included_production_log:
        lines += ["", "This handoff uses LotLens's included factory-derived synthetic LINE-04 fixture, based on the project owner's confirmation. It is not an independent production export; procedure excerpts are synthetic demo material."]
    else:
        lines += ["", "This handoff was generated from an uploaded CSV; its origin has not been verified by LotLens."]
    lines.append("Human review is required. LotLens does not confirm root cause or authorize operational actions.")
    return "\n".join(lines)


st.session_state.setdefault("sidebar_open", False)


def _toggle_sidebar() -> None:
    st.session_state["sidebar_open"] = not st.session_state.get("sidebar_open", False)


_inject_theme()

with st.sidebar:
    st.markdown('<div class="ll-kicker">Investigation setup</div>', unsafe_allow_html=True)
    source_mode = st.radio("Data source", ["Sample scenario", "Upload CSV"], label_visibility="collapsed")
    uploaded_file = None
    inventory_file = None
    orders_file = None
    if source_mode == "Upload CSV":
        uploaded_file = st.file_uploader("Upload production readings", type=["csv"])
        st.caption("CSV stays in this app session. Use synthetic or non-sensitive data only.")
        st.download_button(
            "Download CSV template",
            data=pd.DataFrame(columns=CSV_TEMPLATE_COLUMNS).to_csv(index=False).encode("utf-8"),
            file_name="lotlens-production-template.csv",
            mime="text/csv",
            use_container_width=True,
        )
        with st.expander("CSV format and field guide"):
            st.markdown(
                "**Required columns**: `timestamp`, `line_id`, `batch_id`, `shift`, `units_inspected`, `defect_count`. "
                "Use one production line per file and at least 12 timestamped readings."
            )
            st.markdown(
                "**Optional context**: `temperature_c` (°C), `vibration_mm_s` (mm/s), `pressure_bar` (bar), and `operator_note`. "
                "Omit these columns or leave their cells blank when unavailable. Sensors are shown as context; defect counts drive the alert."
            )
            st.markdown(
                "Use consistent timestamps/timezone and units. `units_inspected` must be a positive whole number; "
                "`defect_count` must be a whole number from 0 through `units_inspected`. LotLens analyzes one line at a time."
            )
            st.caption("Columns not listed above are ignored. Different source column names or units must be mapped/converted before upload.")
        st.markdown('<div class="ll-kicker" style="margin-top:.8rem">Commerce context (optional)</div>', unsafe_allow_html=True)
        inventory_file = st.file_uploader("Upload inventory snapshot CSV", type=["csv"], key="inventory_snapshot")
        orders_file = st.file_uploader("Upload open-orders CSV", type=["csv"], key="open_orders")
        st.caption("Both files are needed to show Commerce impact for uploaded production data.")
    else:
        sample_scenario = st.selectbox(
            "Scenario",
            ["Seeded drift", "Stable process", "Production quality log"],
            index=2,
            key="scenario_selector_v2",
        )
        sample_scenario_key = {
            "Seeded drift": "drift",
            "Stable process": "stable",
            "Production quality log": "production",
        }[sample_scenario]
        st.caption(
            "Factory-derived synthetic LINE-04 fixture"
            if sample_scenario_key == "production"
            else "Seeded scenario · one stable interval and one quality drift"
        )

    if source_mode == "Sample scenario":
        st.download_button(
            "Download sample CSV",
            data=build_sample_dataset(scenario=sample_scenario_key).to_csv(index=False).encode("utf-8"),
            file_name=f"lotlens-demo-{sample_scenario_key}.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.download_button(
            "Download sample inventory CSV",
            data=sample_inventory().to_csv(index=False).encode("utf-8"),
            file_name="lotlens-synthetic-inventory.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.download_button(
            "Download sample open-orders CSV",
            data=sample_orders().to_csv(index=False).encode("utf-8"),
            file_name="lotlens-synthetic-open-orders.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.divider()
    st.markdown('<div class="ll-kicker">Detector rule</div>', unsafe_allow_html=True)
    st.caption("Baseline: first 60% of readings")
    st.caption("Alert: 3 consecutive defect-rate readings above baseline + max(3σ, 2 pp)")
    st.caption("Statistical findings are calculated locally. The model does not calculate the alert.")
    st.divider()
    if is_configured():
        st.markdown(
            '<div class="ll-config-state ll-config-ready">'
            '<span class="ll-config-dot"></span><div>'
            '<div class="ll-config-title">AMD inference ready</div>'
            '<div class="ll-config-copy">Endpoint, model, and API key are available to this app.</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )
    else:
        missing = missing_settings()
        missing_label = ", ".join(name.removeprefix("AMD_").replace("_", " ").lower() for name in missing)
        missing_display = html.escape(missing_label or "configuration")
        st.markdown(
            '<div class="ll-config-state ll-config-pending">'
            '<span class="ll-config-dot"></span><div>'
            '<div class="ll-config-title">AMD brief awaiting credentials</div>'
            f'<div class="ll-config-copy">Missing: {missing_display}. The detector and evidence stay available.</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )
        if st.button(
            "Reload AMD settings from .env",
            use_container_width=True,
            help="After adding the API key, select this to load it without restarting the app.",
        ):
            _load_runtime_env()
            st.rerun()

st.markdown('<div id="top"></div>', unsafe_allow_html=True)
sidebar_state_class = "ll-sidebar-open-state" if st.session_state.get("sidebar_open", False) else "ll-sidebar-closed-state"
st.markdown(f'<div class="{sidebar_state_class}" aria-hidden="true"></div>', unsafe_allow_html=True)
with st.container(key="ll-navbar"):
    st.button("\u2630", key="ll-sidebar-toggle", help="Show or hide investigation setup", on_click=_toggle_sidebar)
    lockup = base64.b64encode((ROOT / "logos" / "LotLens Horizontal Lockup.png").read_bytes()).decode("ascii")
    st.markdown(
        '<div class="ll-navbar-html">'
        f'<img src="data:image/png;base64,{lockup}" alt="LotLens" />'
        '<nav class="ll-navbar-links" aria-label="Main sections">'
        '<a href="#quality">Quality</a>'
        '<a href="#commerce">Commerce</a>'
        '<a href="#handoff">Handoff</a>'
        '<a href="#team">Meet the team</a>'
        '</nav></div>',
        unsafe_allow_html=True,
    )

with st.container(key="ll-hero"):
    st.markdown(
        '<div class="ll-hero-body"><div class="ll-kicker">QUALITY INVESTIGATION &middot; INTELLIGENT INDUSTRY + REINVENT COMMERCE</div>'
        '<h1>From quality signal to confident action.</h1>'
        '<p>Trace a sustained production change to its evidence, understand potential inventory exposure, '
        'and prepare a human-reviewed shift handoff.</p></div>'
        '<nav class="ll-workflow" aria-label="Investigation workflow">'
        '<a href="#quality"><span>01</span><b>Quality</b><i>Measured signal</i></a>'
        '<span class="ll-workflow-link">&rsaquo;</span>'
        '<a href="#commerce"><span>02</span><b>Commerce</b><i>Stock exposure</i></a>'
        '<span class="ll-workflow-link">&rsaquo;</span>'
        '<a href="#handoff"><span>03</span><b>Handoff</b><i>Evidence & context</i></a>'
        '</nav>',
        unsafe_allow_html=True,
    )
if source_mode == "Sample scenario" and sample_scenario_key == "production":
    dataset_notice = "LINE-04 production log · factory-derived synthetic fixture"
    footer_provenance = "This included LINE-04 fixture is factory-derived and synthetic, based on the project owner's confirmation; it is not an independent production export. Procedure excerpts are synthetic demo material."
elif source_mode == "Sample scenario":
    dataset_notice = f"Synthetic demo data - {sample_scenario}"
    footer_provenance = "The dataset and procedure excerpts are synthetic demo material."
else:
    dataset_notice = "Uploaded dataset - origin not verified"
    footer_provenance = "The uploaded dataset's origin is not verified; the procedure excerpts are synthetic demo material."
st.markdown(
    f'<div class="ll-status" style="margin:.4rem 0 1.2rem"><span class="ll-status-dot"></span>{html.escape(dataset_notice)}</div>',
    unsafe_allow_html=True,
)

read_error = None
if source_mode == "Sample scenario":
    current_data = build_sample_dataset(scenario=sample_scenario_key)
    validation = validate_dataframe(current_data)
    dataset_key = f"sample-scenario-v2:{sample_scenario_key}"
else:
    current_data = None
    validation = None
    dataset_key = None
    if uploaded_file is not None:
        uploaded_bytes = uploaded_file.getvalue()
        content_digest = hashlib.sha256(uploaded_bytes).hexdigest()
        dataset_key = f"{uploaded_file.name}:{content_digest}"
        try:
            current_data = pd.read_csv(BytesIO(uploaded_bytes))
            validation = validate_dataframe(current_data)
        except Exception as error:
            validation = None
            read_error = f"LotLens could not read this CSV ({type(error).__name__}). Check that it is a valid UTF-8 CSV file."

if dataset_key != st.session_state.get("dataset_key"):
    st.session_state["dataset_key"] = dataset_key
    st.session_state["detection"] = None
    st.session_state["sources"] = []
    st.session_state["brief"] = None
    st.session_state["brief_error"] = None
    st.session_state["run_attempted"] = False

if read_error:
    st.error(read_error)
    st.caption("The file could not be parsed. This is an input-format issue, not evidence of a production-quality problem.")
    _render_preanalysis_sections(footer_provenance)
    st.stop()

if current_data is None:
    st.info("Choose a CSV file to begin. The sample scenario remains available from the data-source selector.")
    _render_preanalysis_sections(footer_provenance)
    st.stop()

if validation is not None and not validation.valid:
    if current_data is not None and len(current_data) < 12:
        st.info("Insufficient evidence: LotLens needs at least 12 readings to form a baseline and monitored period.")
    else:
        st.error("Input validation needs attention: " + " ".join(validation.errors))
    st.caption("Input errors do not indicate a production-quality failure.")
    _render_preanalysis_sections(footer_provenance)
    st.stop()

analysis_input = validation.data
input_start = analysis_input["timestamp"].iloc[0].strftime("%b %d, %H:%M")
input_end = analysis_input["timestamp"].iloc[-1].strftime("%b %d, %H:%M")
input_batches = int(analysis_input["batch_id"].nunique())
input_summary_columns = st.columns(3, gap="medium")
with input_summary_columns[0]:
    _metric_card("Readings", f"{len(analysis_input):,}", "Timestamped inspection samples")
with input_summary_columns[1]:
    _metric_card("Production line", str(analysis_input["line_id"].iloc[0]), f"{input_batches} batch(es) in this file")
with input_summary_columns[2]:
    _metric_card("Time window", input_start, f"Through {input_end}")

st.markdown('<div class="ll-stack-gap"></div>', unsafe_allow_html=True)
with st.container(border=True):
    _action_panel(
        "Ready for analysis",
        "Calculate the measured quality signal",
        "LotLens establishes the baseline locally, then retrieves relevant procedure context for review.",
    )
    action_col, description_col = st.columns([1.2, 3.8], vertical_alignment="center")
    with action_col:
        if st.button("Run analysis", type="primary", use_container_width=True):
            try:
                with st.spinner("Calculating the quality baseline and checking for sustained drift..."):
                    st.session_state["detection"] = detect_quality_drift(validation.data)
                    detection = st.session_state["detection"]
                    st.session_state["sources"] = retrieve_procedures(build_retrieval_query(detection.to_public_dict()))
                    st.session_state["brief"] = None
                    st.session_state["brief_error"] = None
                    st.session_state["run_attempted"] = True
                st.rerun()
            except ValueError as error:
                st.error(str(error))
    with description_col:
        st.markdown('<div class="ll-footnote">The detector compares inspection defect rates against a stable baseline. A generated explanation is optional and never replaces the measured evidence.</div>', unsafe_allow_html=True)

detection = st.session_state.get("detection")
sources = st.session_state.get("sources", [])
brief = st.session_state.get("brief")
if detection is None:
    st.info("Dataset ready. Select **Run analysis** to calculate the baseline and inspect this dataset for sustained drift.")
    _render_preanalysis_sections(footer_provenance)
    st.stop()

status_class = "ll-status" if detection.status == "drift" else "ll-status ll-status-normal"
status_label = "Drift detected" if detection.status == "drift" else "No qualifying drift"
_section_heading("quality", "01", "INTELLIGENT INDUSTRY", "Quality investigation", "The measured signal, its production context, and the supporting evidence.")
st.markdown(
    f'<div class="ll-alert-banner {"ll-alert-drift" if detection.status == "drift" else "ll-alert-clear"}">'
    f'<div class="{status_class}"><span class="ll-status-dot"></span>{status_label}</div>'
    f'<div class="ll-alert-message">{html.escape(detection.message)}</div></div>',
    unsafe_allow_html=True,
)

metric_columns = st.columns(4, gap="medium")
with metric_columns[0]:
    _metric_card("Affected production lot", detection.batch_id or "None identified", detection.line_id or "Line not identified", "#E8B45D" if detection.status == "drift" else "#75C69A")
with metric_columns[1]:
    _metric_card("Drift onset", _fmt_timestamp(detection.onset_time), f"Confirmed at {_fmt_timestamp(detection.confirmed_time)}" if detection.confirmed_time else "No sustained threshold crossing")
with metric_columns[2]:
    _metric_card("Stable baseline", _fmt_pct(detection.baseline_rate_pct), f"First {detection.baseline_points} readings")
with metric_columns[3]:
    delta = f"{detection.current_rate_pct - detection.baseline_rate_pct:+.2f} percentage points vs baseline" if detection.current_rate_pct is not None and detection.baseline_rate_pct is not None else "No comparable readings"
    _metric_card("Latest defect rate", _fmt_pct(detection.current_rate_pct), delta)

st.write("")
chart_col, brief_col = st.columns([1.65, 1], gap="large")
with chart_col:
    st.markdown('<div class="ll-panel-heading">Quality trend</div><div class="ll-panel-sub">Inspection defects over time · baseline and alert threshold</div>', unsafe_allow_html=True)
    st.plotly_chart(_build_chart(detection), use_container_width=True, config={"displayModeBar": False})
    with st.expander("Inspect machine signal context"):
        signal_options = {
            "Temperature": ("temperature_c", "Temperature", "deg C", "#B6A4E0"),
            "Vibration": ("vibration_mm_s", "Vibration", "mm/s", "#9DBDD9"),
            "Pressure": ("pressure_bar", "Pressure", "bar", "#D0B17A"),
        }
        available_signals = {
            label: option
            for label, option in signal_options.items()
            if analysis_input[option[0]].notna().any()
        }
        if available_signals:
            selected_signal = st.selectbox("Machine signal", list(available_signals), key="machine_signal")
            column, label, units, color = available_signals[selected_signal]
            st.plotly_chart(
                _build_sensor_chart(detection, column, label, units, color),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            baseline_has_signal = analysis_input.iloc[: detection.baseline_points][column].notna().any()
            if baseline_has_signal:
                st.caption("Signal context only. The alert rule uses inspection defect rate; this baseline mean is descriptive and is not an operating limit.")
            else:
                st.caption("No readings for this signal were supplied in the baseline interval; the alert rule uses inspection defect rate only.")
        else:
            st.info("No machine sensor readings were supplied. Quality analysis still uses inspection defect counts.")
    st.markdown('<div class="ll-footnote">The threshold is calculated as baseline mean + max(3 population standard deviations, 2 percentage points). An alert requires three consecutive readings above it.</div>', unsafe_allow_html=True)

with brief_col:
    facts = []
    if detection.status == "drift":
        facts.append(
            f"Lot {html.escape(detection.batch_id or 'not identified')} on line "
            f"{html.escape(detection.line_id or 'not identified')} crossed the threshold at "
            f"{html.escape(_fmt_timestamp(detection.onset_time))} and was confirmed at "
            f"{html.escape(_fmt_timestamp(detection.confirmed_time))}."
        )
    else:
        facts.append("No qualifying sustained increase was found under the configured detector rule.")
    facts.append(
        f"Baseline {_fmt_pct(detection.baseline_rate_pct)} | threshold {_fmt_pct(detection.threshold_rate_pct)} | "
        f"latest {_fmt_pct(detection.current_rate_pct)}"
    )

    panel = [
        '<div class="ll-ai-box">',
        '<div class="ll-ai-label">AMD-backed AI interpretation</div>',
        '<div class="ll-ai-facts"><div class="ll-ai-section-title">Calculated evidence</div>',
        f"<p>{'<br>'.join(facts)}</p></div>",
    ]
    if brief:
        panel.extend([
            '<div class="ll-ai-content"><div class="ll-ai-section-title">AMD-generated investigation summary</div>',
            f"<p>{html.escape(brief['summary']).replace(chr(10), '<br>')}</p>",
            '<div class="ll-ai-section-title">Possible checks | human review required</div>',
        ])
        provider = brief.get("_provider", {})
        if provider.get("model"):
            usage_text = ""
            if isinstance(provider.get("total_tokens"), int):
                usage_text = f" | {provider['total_tokens']:,} tokens"
            panel.append(
                f"<div class='ll-ai-meta'>AMD model: {html.escape(str(provider['model']))}{usage_text}</div>"
            )
        if brief.get("possible_checks"):
            panel.append("<ul>")
            for check in brief["possible_checks"]:
                panel.append(
                    f"<li>{html.escape(check.get('text', ''))} "
                    f"<span class='ll-ai-source-tag'>[{html.escape(check.get('source_id', ''))}]</span></li>"
                )
            panel.append("</ul>")
        else:
            panel.append("<p>The supplied procedures did not support a specific check.</p>")
        panel.extend([
            '<div class="ll-ai-section-title">Uncertainty</div>',
            f"<p>{html.escape(brief['uncertainty']).replace(chr(10), '<br>')}</p></div>",
        ])
    elif st.session_state.get("brief_error"):
        panel.append(f"<div class='ll-ai-notice'>{html.escape(st.session_state['brief_error'])}</div>")
        panel.append("<p class='ll-footnote'>The calculated alert and source excerpts remain available.</p>")
    else:
        panel.append(
            '<div class="ll-ai-content"><p>The model will summarize the calculated finding, suggest only checks tied to the supplied procedure excerpts, and state what remains uncertain.</p></div>'
        )
    panel.append("</div>")
    st.markdown("".join(panel), unsafe_allow_html=True)

    if is_configured():
        st.markdown('<div class="ll-stack-gap ll-stack-gap-compact"></div>', unsafe_allow_html=True)
        with st.container(border=True):
            _action_panel(
                "AMD interpretation",
                "Generate investigation brief",
                "Turn the calculated finding and retrieved excerpts into a review-ready brief.",
            )
            if st.button("Generate investigation brief", use_container_width=True, key="generate_brief"):
                try:
                    with st.spinner("Requesting an investigation brief from the AMD model..."):
                        st.session_state["brief"] = generate_investigation_brief(detection.to_public_dict(), sources)
                        st.session_state["brief_error"] = None
                except Exception as error:
                    st.session_state["brief"] = None
                    st.session_state["brief_error"] = describe_inference_error(error)
                st.rerun()
    else:
        missing_label = ", ".join(name.removeprefix("AMD_").replace("_", " ").lower() for name in missing_settings())
        st.markdown(
            '<div class="ll-ai-connect">'
            '<div class="ll-ai-connect-title">Connect the AMD investigation brief</div>'
            '<p>The local detector, charts, and source evidence are ready now. Add the missing '
            f"{html.escape(missing_label)} setting(s) to the project-root `.env`, then select "
            '<b>Reload AMD settings from .env</b> in the sidebar. The brief action will become available automatically.</p>'
            '</div>',
            unsafe_allow_html=True,
        )

_section_heading("commerce", "02", "REINVENT COMMERCE", "Inventory impact", "Connect the alerted lot to available stock and open orders. Recommendations remain subject to human review.")

if source_mode == "Sample scenario":
    commerce_input = validate_commerce_inputs(sample_inventory(), sample_orders())
    commerce_origin = "Synthetic commerce snapshot"
    commerce_parse_error = None
elif inventory_file is not None and orders_file is not None:
    try:
        commerce_inventory = pd.read_csv(BytesIO(inventory_file.getvalue()))
        commerce_orders = pd.read_csv(BytesIO(orders_file.getvalue()))
        commerce_input = validate_commerce_inputs(commerce_inventory, commerce_orders)
        commerce_origin = "Uploaded commerce snapshots · origin not verified"
        commerce_parse_error = None
    except Exception as error:
        commerce_input = None
        commerce_origin = "Uploaded commerce snapshots · origin not verified"
        commerce_parse_error = f"LotLens could not read the commerce CSVs ({type(error).__name__}). Industry analysis remains available."
else:
    commerce_input = None
    commerce_origin = ""
    commerce_parse_error = None

commerce_impact = None
if detection.status != "drift":
    commerce_impact = {"status": "no_alert"}
    st.markdown(
        '<div class="ll-commerce-state ll-commerce-clear"><b>No lot is currently implicated.</b> '
        'The selected inspection dataset has no qualifying sustained quality alert under the configured rule.</div>',
        unsafe_allow_html=True,
    )
elif commerce_input is None:
    if commerce_parse_error:
        st.warning(commerce_parse_error)
    else:
        st.info("Upload both an inventory snapshot and an open-orders CSV to connect this production alert to Commerce data.")
elif not commerce_input.valid:
    st.warning("Commerce context needs attention: " + " ".join(commerce_input.errors))
else:
    impact = calculate_inventory_impact(detection.batch_id or "", commerce_input.inventory, commerce_input.orders)
    st.caption(commerce_origin)
    if impact["status"] == "unmapped":
        commerce_impact = impact
        st.warning(f"Alerted batch `{detection.batch_id}` is not mapped to a SKU in this inventory snapshot. Add the lot-to-SKU mapping to assess stock impact.")
    else:
        commerce_impact = impact
        for product in impact["products"]:
            st.markdown(
                f"<strong>{html.escape(product['product_name'])}</strong> · SKU "
                f"<code>{html.escape(product['sku'])}</code> · quality-alert batch "
                f"<code>{html.escape(impact['affected_batch'])}</code>",
                unsafe_allow_html=True,
            )
            commerce_metrics = st.columns(4, gap="medium")
            with commerce_metrics[0]:
                _metric_card("Units in alerted lot", f"{product['affected_on_hand']:,}", f"{product['affected_reserved']:,} already reserved", "#E8B45D")
            with commerce_metrics[1]:
                _metric_card("Clean stock available", f"{product['clean_available']:,}", "On hand minus reserved in unaffected lots", "#75C69A")
            with commerce_metrics[2]:
                _metric_card("Reallocation need", f"{product['reallocation_need']:,}", f"{product['affected_reserved']:,} reserved + {product['unallocated_open_orders']:,} unallocated orders")
            with commerce_metrics[3]:
                _metric_card("Uncovered units", f"{product['shortfall']:,}", "After using available unaffected stock", "#F0786B" if product['shortfall'] else "#75C69A")

            lot_view = commerce_input.inventory.copy()
            lot_view["available_units"] = lot_view["on_hand_units"] - lot_view["reserved_units"]
            lot_view["quality_status"] = lot_view["batch_id"].map(
                lambda batch: "Alerted · review before release" if batch == impact["affected_batch"] else "Unaffected in this analysis"
            )
            lot_view = lot_view.loc[lot_view["sku"] == product["sku"], ["batch_id", "on_hand_units", "reserved_units", "available_units", "quality_status"]]
            st.markdown('<div class="ll-stack-gap ll-stack-gap-compact"></div>', unsafe_allow_html=True)
            st.dataframe(lot_view, use_container_width=True, hide_index=True)

            if product["shortfall"]:
                commerce_message = (
                    f"<strong>Proposed human-reviewed action:</strong> Hold release of stock from "
                    f"<code>{html.escape(impact['affected_batch'])}</code> pending quality disposition. "
                    f"Allocate up to {product['reallocated']:,} units from unaffected stock and notify fulfillment about the remaining "
                    f"{product['shortfall']:,}-unit gap. The snapshot has no demand forecast, so LotLens does not estimate future sales or promise delivery dates."
                )
                commerce_class = "ll-commerce-state ll-commerce-gap"
            else:
                commerce_message = (
                    f"<strong>Proposed human-reviewed action:</strong> Hold release of stock from "
                    f"<code>{html.escape(impact['affected_batch'])}</code> pending quality disposition. "
                    f"The current snapshot has enough unaffected stock to cover {product['reallocation_need']:,} reserved and unallocated units, "
                    f"leaving {product['clean_remaining']:,} clean units available. A quality or fulfillment lead must approve any reallocation."
                )
                commerce_class = "ll-commerce-state ll-commerce-covered"
            st.markdown(f'<div class="{commerce_class}">{commerce_message}</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="ll-footnote" style="margin:.55rem 0 1.4rem">Rule: exclude the alerted lot from sellable stock, then compare '
    'its reserved units plus unallocated open orders with available units in unaffected lots. This is a synthetic snapshot, '
    'not a demand forecast or an automated hold/replenishment action.</div>',
    unsafe_allow_html=True,
)

_section_heading("handoff", "03", "SHIFT HANDOFF", "Evidence & procedure context", "Review the readings and reference excerpts that support a clear, human-reviewed handoff.")
evidence_col, source_col = st.columns([1, 1], gap="large")
with evidence_col:
    st.markdown('<div class="ll-panel-heading">Alert evidence</div><div class="ll-panel-sub">Readings from the first sustained threshold crossing</div>', unsafe_allow_html=True)
    if detection.evidence:
        for row in detection.evidence:
            note = f" · Note: {row['operator_note']}" if row.get("operator_note") else ""
            sensor_context = " · ".join(
                f"{label} {value}" for label, value in _sensor_context_parts(row)
            ) or "Sensor context unavailable"
            st.markdown(
                '<div class="ll-evidence">'
                f"<b>{html.escape(_fmt_timestamp(row['timestamp']))}</b> · {html.escape(row['batch_id'])}<br>"
                f"Defects: {row['defect_count']} / {row['units_inspected']} ({row['defect_rate_pct']:.2f}%) · "
                f"{html.escape(sensor_context)}{html.escape(note)}"
                "</div><div style='height:.45rem'></div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown('<div class="ll-source"><div class="ll-source-text">No sustained drift evidence was found under the configured rule. This does not prove that every quality condition is normal.</div></div>', unsafe_allow_html=True)

with source_col:
    st.markdown('<div class="ll-panel-heading">Procedure references</div><div class="ll-panel-sub">Synthetic demo excerpts · not approved operating procedures</div>', unsafe_allow_html=True)
    for source in sources:
        st.markdown(
            '<div class="ll-source">'
            f"<div class='ll-source-id'>{html.escape(source['source_id'])}</div>"
            f"<div class='ll-source-title'>{html.escape(source['title'])}</div>"
            f"<div class='ll-source-text'>{html.escape(source['text'])}</div>"
            "</div><div style='height:.5rem'></div>",
            unsafe_allow_html=True,
        )

with st.expander("Inspect input readings"):
    st.dataframe(validation.data, use_container_width=True, hide_index=True)

st.download_button(
    "Download shift handoff",
    data=_handoff_text(
        detection,
        sources,
        brief,
        synthetic=source_mode == "Sample scenario" and sample_scenario_key != "production",
        included_production_log=source_mode == "Sample scenario" and sample_scenario_key == "production",
        commerce=commerce_impact,
        commerce_origin=commerce_origin,
    ),
    file_name="lotlens-shift-handoff.txt",
    mime="text/plain",
)
_render_footer(footer_provenance)

