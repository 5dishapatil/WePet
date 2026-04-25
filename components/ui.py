"""
ui.py — Reusable Streamlit UI helpers for PawTemp MVP.
"""
import streamlit as st
from components.styles import RISK_COLORS, RISK_BG


def render_logo():
    st.markdown("""
    <div style="margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.06);">
        <div class="logo-text">🐾 Paw<span class="logo-accent">Temp</span></div>
        <div class="logo-sub">Climate Risk Intelligence</div>
    </div>
    """, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str, icon: str = ""):
    st.markdown(f"""
    <div class="page-header">
        <p class="page-title">{icon} {title}</p>
        <p class="page-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_section_label(label: str):
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)


def render_risk_badge(level: str, score: float):
    color = RISK_COLORS.get(level, "#94a3b8")
    bg = RISK_BG.get(level, "rgba(148,163,184,0.1)")
    icons = {"Low": "🟢", "Moderate": "🟡", "High": "🟠", "Critical": "🔴"}
    icon = icons.get(level, "⚪")
    st.markdown(f"""
    <div style="background:{bg}; border:1px solid {color}40; border-radius:14px; padding:20px 24px; margin-bottom:16px;">
        <div style="display:flex; align-items:center; gap:12px;">
            <span style="font-size:2rem;">{icon}</span>
            <div>
                <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em; color:#64748b; font-weight:600;">Overall Risk Level</div>
                <div style="font-size:1.8rem; font-weight:700; color:{color}; line-height:1.1;">{level}</div>
                <div style="font-size:0.8rem; color:#64748b; margin-top:2px;">Risk score: {score:.0f}/100</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sub_score_card(title: str, score: float, icon: str, note: str = ""):
    color = _score_color(score)
    bar_pct = min(score, 100)
    st.markdown(f"""
    <div class="sub-score-card">
        <div class="sub-score-title">{icon} {title}</div>
        <div class="sub-score-value" style="color:{color};">{score:.0f}<span style="font-size:0.9rem;color:#475569;">/100</span></div>
        <div class="score-bar-wrap">
            <div class="score-bar-fill" style="width:{bar_pct}%; background:{color};"></div>
        </div>
        {f'<div style="font-size:0.74rem;color:#64748b;margin-top:6px;">{note}</div>' if note else ''}
    </div>
    """, unsafe_allow_html=True)


def render_weather_metric(label: str, value: str, unit: str = "", icon: str = ""):
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size:1.3rem; margin-bottom:4px;">{icon}</div>
        <div class="metric-value">{value}<span class="metric-unit">{unit}</span></div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_driver_card(text: str):
    st.markdown(f'<div class="driver-card">{text}</div>', unsafe_allow_html=True)


def render_recommendation_card(icon: str, category: str, advice: str, why: str):
    st.markdown(f"""
    <div class="rec-card">
        <div class="rec-category">{icon} {category}</div>
        <div class="rec-advice">{advice}</div>
        <div class="rec-why">Why: {why}</div>
    </div>
    """, unsafe_allow_html=True)


def render_safe_window_card(window_label: str, avg_apparent: float, avg_risk: float):
    st.markdown(f"""
    <div class="window-card">
        <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#4ade80;font-weight:600;margin-bottom:6px;">SAFE WINDOW</div>
        <div class="window-time">{window_label}</div>
        <div style="font-size:0.8rem;color:#64748b;margin-top:6px;">
            Avg apparent temp: {avg_apparent:.1f}°C · Risk score: {avg_risk:.0f}/100
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_exposure_card(label: str, description: str):
    st.markdown(f"""
    <div class="exposure-card">
        <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#90cdf4;font-weight:600;margin-bottom:8px;">MAX OUTDOOR EXPOSURE</div>
        <div class="exposure-label">{label}</div>
        <div style="font-size:0.8rem;color:#64748b;margin-top:6px;">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def render_emergency_card(signs: list, safe_note: str, disclaimer: str):
    signs_html = "".join(f'<span class="warning-sign">⚠ {s}</span>' for s in signs)
    st.markdown(f"""
    <div class="emergency-card">
        <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#f87171;font-weight:600;margin-bottom:12px;">🚨 EMERGENCY WATCH SIGNS</div>
        <div style="margin-bottom:12px;">{signs_html}</div>
        <div style="font-size:0.85rem;color:#fca5a5;line-height:1.6;margin-bottom:8px;">{safe_note}</div>
        <div style="font-size:0.76rem;color:#64748b;font-style:italic;">{disclaimer}</div>
    </div>
    """, unsafe_allow_html=True)


def render_report_card(report: dict):
    level = report.get("severity_level", "Low")
    color = RISK_COLORS.get(level, "#94a3b8")
    bg = RISK_BG.get(level, "rgba(148,163,184,0.1)")
    symptoms = ", ".join(report.get("symptoms", []))
    submitted = report.get("submitted_at", "")[:16].replace("T", " ")

    st.markdown(f"""
    <div class="report-card" style="border-left: 3px solid {color};">
        <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:10px;">
            <div>
                <span style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;color:#475569;font-weight:600;">
                    {report.get('report_id','—')}
                </span>
                <span style="font-size:0.78rem;color:#475569;margin-left:12px;">{submitted}</span>
            </div>
            <span style="background:{bg};color:{color};border:1px solid {color}40;border-radius:999px;padding:3px 12px;font-size:0.78rem;font-weight:600;">
                {level}
            </span>
        </div>
        <div style="display:flex;gap:16px;margin-bottom:8px;flex-wrap:wrap;">
            <span class="info-chip">📍 {report.get('location','—')}</span>
            <span class="info-chip">🐾 {report.get('animal_type','—').title()}</span>
            <span class="info-chip">Score: {report.get('severity_score',0)}/100</span>
        </div>
        <div style="font-size:0.82rem;color:#94a3b8;margin-bottom:6px;"><strong style="color:#64748b;">Symptoms:</strong> {symptoms or 'None selected'}</div>
        {f'<div style="font-size:0.82rem;color:#94a3b8;margin-bottom:6px;"><strong style="color:#64748b;">Notes:</strong> {report.get("notes","")}</div>' if report.get('notes') else ''}
        <div style="font-size:0.82rem;color:{color};font-weight:500;">→ {report.get('urgency','')}</div>
    </div>
    """, unsafe_allow_html=True)


def render_info_banner(text: str, color: str = "#3b82f6"):
    st.markdown(f"""
    <div style="background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.2);
         border-radius:10px;padding:12px 16px;font-size:0.86rem;color:#93c5fd;margin-bottom:16px;">
        ℹ️ {text}
    </div>
    """, unsafe_allow_html=True)


def render_error_banner(text: str):
    st.markdown(f"""
    <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);
         border-radius:10px;padding:12px 16px;font-size:0.86rem;color:#fca5a5;margin-bottom:16px;">
        ❌ {text}
    </div>
    """, unsafe_allow_html=True)


def _score_color(score: float) -> str:
    if score < 25:
        return "#22c55e"
    elif score < 50:
        return "#f59e0b"
    elif score < 75:
        return "#f97316"
    else:
        return "#ef4444"