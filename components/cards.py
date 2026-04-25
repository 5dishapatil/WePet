"""
cards.py — Higher-level card compositions for WePet MVP.
"""
import streamlit as st
from components.ui import (
    render_section_label,
    render_sub_score_card,
    render_driver_card,
    render_recommendation_card,
    render_safe_window_card,
    render_exposure_card,
    render_emergency_card,
    render_weather_metric,
    render_risk_badge,
)


def render_weather_row(current: dict, location_display: str):
    """Render the weather summary metrics row."""
    render_section_label("📡 LIVE WEATHER CONDITIONS")
    st.markdown(f"""
    <div style="font-size:0.88rem;color:#64748b;margin-bottom:14px;">
        📍 {location_display}
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(6)
    with cols[0]:
        render_weather_metric("Temperature", f"{current['temperature']:.1f}", "°C", "🌡️")
    with cols[1]:
        render_weather_metric("Feels Like", f"{current['apparent_temperature']:.1f}", "°C", "🤔")
    with cols[2]:
        render_weather_metric("Humidity", f"{current['humidity']:.0f}", "%", "💧")
    with cols[3]:
        render_weather_metric("Wind", f"{current['wind_speed']:.0f}", " km/h", "💨")
    with cols[4]:
        render_weather_metric("UV Index", f"{current.get('uv_index', 0) or 0:.0f}", "", "☀️")
    with cols[5]:
        condition = current.get("condition", "—")
        is_day = current.get("is_day", 1)
        icon = "🌙" if not is_day else "🌤️"
        render_weather_metric("Condition", condition[:10], "", icon)


def render_sub_scores_row(sub_scores: dict, species: str):
    """Render the 5 sub-score cards."""
    render_section_label("📊 RISK SUB-SCORES")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        render_sub_score_card("Heat Stress", sub_scores["heat_stress"], "🌡️")
    with c2:
        render_sub_score_card("Dehydration", sub_scores["dehydration"], "💧")
    with c3:
        render_sub_score_card("Respiratory", sub_scores["respiratory"], "😮‍💨")
    with c4:
        label = "Paw Burn" if species == "dog" else "Surface Heat"
        render_sub_score_card(label, sub_scores["surface_burn"], "🔥")
    with c5:
        render_sub_score_card("Indoor Heat", sub_scores["indoor_heat"], "🏠")


def render_safe_windows_section(windows_data: dict):
    """Render safe window + indoor-only fallback."""
    render_section_label("🕐 BEST SAFE WINDOWS TODAY")

    if windows_data["indoor_only"]:
        st.markdown(f"""
        <div style="background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.15);
             border-radius:12px;padding:16px 20px;text-align:center;">
            <div style="font-size:1.1rem;font-weight:600;color:#f87171;">🏠 No safe outdoor window today</div>
            <div style="font-size:0.85rem;color:#64748b;margin-top:6px;">{windows_data['message']}</div>
        </div>
        """, unsafe_allow_html=True)
    elif not windows_data["windows"]:
        st.markdown(f"""
        <div class="pt-card-sm" style="text-align:center;">
            <div style="color:#64748b;font-size:0.88rem;">{windows_data['message']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(len(windows_data["windows"]))
        for i, w in enumerate(windows_data["windows"]):
            with cols[i]:
                render_safe_window_card(w["window"], w["avg_apparent"], w["avg_risk"])


def render_hidden_drivers_section(drivers: list):
    """Render hidden risk drivers."""
    if not drivers:
        return
    render_section_label("🔍 HIDDEN RISK DRIVERS")
    for d in drivers:
        render_driver_card(d)


def render_recommendations_section(recs: list):
    """Render breed-specific recommendations."""
    if not recs:
        return
    render_section_label("💡 BREED-SPECIFIC RECOMMENDATIONS")
    for r in recs:
        render_recommendation_card(r["icon"], r["category"], r["advice"], r["why"])


def render_emergency_section(emergency: dict):
    """Render emergency watch signs."""
    render_section_label("🚨 EMERGENCY WATCH")
    render_emergency_card(
        emergency["signs"],
        emergency["safe_note"],
        emergency["disclaimer"],
    )