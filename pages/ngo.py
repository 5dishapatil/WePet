"""
pages/ngo.py — NGO / Shelter mode for WePet MVP.
Distress report submission + severity dashboard.
"""
import streamlit as st

from services.distress_service import submit_distress_report, get_all_reports_sorted
from components.styles import RISK_COLORS, RISK_BG
from components.ui import (
    render_page_header,
    render_section_label,
    render_report_card,
    render_error_banner,
    render_info_banner,
)


# Symptom options — keys match SYMPTOM_WEIGHTS in risk_engine.py
SYMPTOM_OPTIONS = {
    "Heavy Panting": "heavy_panting",
    "Lethargy": "lethargy",
    "Collapse": "collapse",
    "Unable to Stand": "unable_to_stand",
    "Open-Mouth Breathing": "open_mouth_breathing",
    "Disorientation": "disorientation",
}

HEAT_LEVEL_OPTIONS = ["Low", "Moderate", "High", "Critical"]


def _render_severity_result(report: dict):
    level = report.get("severity_level", "Low")
    score = report.get("severity_score", 0)
    urgency = report.get("urgency", "")
    report_id = report.get("report_id", "—")
    color = RISK_COLORS.get(level, "#94a3b8")
    bg = RISK_BG.get(level, "rgba(148,163,184,0.1)")

    st.markdown(
        f"""
        <div style="background:{bg};border:1px solid {color}40;border-radius:14px;
             padding:20px 24px;margin-top:16px;">
            <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                 color:#64748b;font-weight:600;margin-bottom:10px;">REPORT SUBMITTED</div>
            <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:10px;">
                <span style="font-size:1.5rem;font-weight:700;color:{color};">
                    {level} Severity
                </span>
                <span style="background:{bg};color:{color};border:1px solid {color}40;
                     border-radius:999px;padding:4px 14px;font-size:0.8rem;font-weight:600;">
                    Score: {score}/100
                </span>
                <span style="font-size:0.8rem;color:#64748b;">ID: {report_id}</span>
            </div>
            <div style="font-size:0.9rem;color:{color};font-weight:500;">→ {urgency}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_submit_tab():
    render_section_label("🐾 ANIMAL DETAILS")

    col_a, col_b = st.columns(2)
    with col_a:
        location = st.text_input(
            "Location of animal",
            placeholder="e.g. Near Shivaji Chowk, Koregaon Park",
            key="ngo_location",
        )
    with col_b:
        animal_type = st.selectbox(
            "Animal Type",
            ["Dog", "Cat", "Unknown"],
            key="ngo_animal_type",
        )

    render_section_label("🌡️ OBSERVED CONDITIONS")
    heat_level = st.selectbox(
        "Current heat conditions in area",
        HEAT_LEVEL_OPTIONS,
        index=1,
        key="ngo_heat_level",
    )

    render_section_label("🩺 OBSERVED SYMPTOMS")

    render_info_banner(
        "Select all symptoms you can observe. This helps compute urgency for NGO response."
    )

    selected_symptoms = []
    sym_cols = st.columns(2)
    for i, (label, key) in enumerate(SYMPTOM_OPTIONS.items()):
        col = sym_cols[i % 2]
        with col:
            if st.checkbox(label, key=f"ngo_sym_{key}"):
                selected_symptoms.append(key)

    render_section_label("📝 ADDITIONAL NOTES")
    notes = st.text_area(
        "Notes (optional)",
        placeholder="Any additional observations — location details, visibility, approachability, etc.",
        key="ngo_notes",
        height=90,
    )

    render_section_label("📷 ATTACH PHOTO (OPTIONAL)")
    uploaded_img = st.file_uploader(
        "Upload a photo of the animal",
        type=["jpg", "jpeg", "png"],
        key="ngo_img",
    )
    if uploaded_img:
        st.image(uploaded_img, caption="Attached photo preview.", width=240)

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    submit = st.button(
        "📩 Submit Distress Report",
        use_container_width=True,
        key="ngo_submit",
    )

    if submit:
        if not location.strip():
            render_error_banner("Please enter the location where the animal was spotted.")
            return

        image_bytes = None
        image_name = None
        if uploaded_img:
            image_bytes = uploaded_img.read()
            image_name = uploaded_img.name

        try:
            report = submit_distress_report(
                location=location.strip(),
                animal_type=animal_type.lower(),
                symptoms=selected_symptoms,
                notes=notes.strip(),
                weather_level=heat_level,
                image_bytes=image_bytes,
                image_name=image_name,
            )
            st.session_state["ngo_last_report"] = report
        except Exception as exc:
            render_error_banner(f"Submission failed: {str(exc)}")
            return

    last = st.session_state.get("ngo_last_report")
    if last:
        _render_severity_result(last)


def _render_dashboard_tab():
    render_section_label("📋 ALL SUBMITTED REPORTS")

    try:
        reports = get_all_reports_sorted()
    except Exception as exc:
        render_error_banner(f"Could not load reports: {str(exc)}")
        return

    if not reports:
        st.markdown(
            """
            <div style="text-align:center;padding:60px 20px;color:#475569;font-size:0.92rem;">
                <div style="font-size:2.5rem;opacity:0.3;margin-bottom:12px;">📋</div>
                No distress reports submitted yet.<br>
                Use the <strong>Submit Report</strong> tab to add the first one.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Summary counts
    level_counts = {"Critical": 0, "High": 0, "Moderate": 0, "Low": 0}
    for r in reports:
        lvl = r.get("severity_level", "Low")
        level_counts[lvl] = level_counts.get(lvl, 0) + 1

    s_cols = st.columns(4)
    for i, (lvl, cnt) in enumerate(level_counts.items()):
        color = RISK_COLORS.get(lvl, "#94a3b8")
        bg = RISK_BG.get(lvl, "rgba(148,163,184,0.1)")
        with s_cols[i]:
            st.markdown(
                f"""
                <div style="background:{bg};border:1px solid {color}40;border-radius:10px;
                     padding:12px 16px;text-align:center;">
                    <div style="font-size:1.5rem;font-weight:700;color:{color};">{cnt}</div>
                    <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;
                         color:#64748b;margin-top:2px;">{lvl}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    for report in reports:
        render_report_card(report)


def render():
    render_page_header(
        title="NGO / Shelter",
        subtitle="Submit animal distress reports and monitor severity across your area.",
        icon="🏥",
    )

    tab_submit, tab_dashboard = st.tabs(["📩 Submit Report", "📋 View Reports"])

    with tab_submit:
        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        _render_submit_tab()

    with tab_dashboard:
        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        _render_dashboard_tab()