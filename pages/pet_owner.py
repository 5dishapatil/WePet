"""
pages/pet_owner.py — Pet Owner mode for WePet MVP.
Breed-specific, weather-driven climate risk analysis.
"""
import streamlit as st

from services.weather_service import get_weather_for_location
from services.breed_profile_service import get_dog_breeds, get_cat_breeds, get_breed_profile
from services.risk_engine import (
    compute_pressures,
    compute_modifier_bonus,
    compute_heat_stress,
    compute_dehydration,
    compute_respiratory,
    compute_surface_burn,
    compute_indoor_heat,
    compute_overall_risk,
    risk_level_label,
    compute_hidden_risk_drivers,
    compute_safe_windows,
    compute_max_exposure,
)
from services.recommendation_engine import generate_recommendations, generate_emergency_signs
from components.ui import (
    render_page_header,
    render_section_label,
    render_risk_badge,
    render_exposure_card,
    render_info_banner,
    render_error_banner,
)
from components.cards import (
    render_weather_row,
    render_sub_scores_row,
    render_safe_windows_section,
    render_hidden_drivers_section,
    render_recommendations_section,
    render_emergency_section,
)


def render():
    render_page_header(
        title="Pet Owner",
        subtitle="Real-time, breed-specific climate risk analysis for your pet.",
        icon="🐾",
    )

    col_form, col_results = st.columns([1, 2.2], gap="large")

    # ── Input Form ─────────────────────────────────────────────────────────────
    with col_form:
        render_section_label("🐶 PET DETAILS")

        species = st.selectbox("Species", ["Dog", "Cat"], key="po_species")
        breeds = get_dog_breeds() if species == "Dog" else get_cat_breeds()
        breed_name = st.selectbox("Breed", breeds, key="po_breed")

        location = st.text_input(
            "City / Location",
            placeholder="e.g. Mumbai, Pune, Bengaluru",
            key="po_location",
        )

        render_section_label("⚙️ OPTIONAL MODIFIERS")

        age_group = st.selectbox(
            "Age Group",
            ["adult", "young", "senior"],
            key="po_age",
        )
        overweight = st.checkbox("Overweight / Obese", key="po_overweight")
        heat_sensitive = st.checkbox("Known heat sensitivity", key="po_heat_sensitive")

        render_section_label("📷 PET PHOTO (ASSISTIVE ONLY)")
        uploaded = st.file_uploader(
            "Upload photo — optional",
            type=["jpg", "jpeg", "png"],
            key="po_img",
        )
        if uploaded:
            st.image(uploaded, caption="Reference only.", use_column_width=True)
            render_info_banner(
                "Photo is for visual reference only — this MVP does not perform "
                "automatic breed detection. Please select your breed manually above."
            )

        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
        analyze = st.button(
            "🔍 Analyze Risk",
            use_container_width=True,
            key="po_analyze",
        )

    # ── Run Analysis on Button Click ───────────────────────────────────────────
    if analyze:
        if not location.strip():
            with col_form:
                render_error_banner("Please enter your city or location before analyzing.")
        else:
            with col_results:
                with st.spinner("Fetching live weather data…"):
                    weather_data = get_weather_for_location(location.strip())

            if "error" in weather_data:
                with col_results:
                    render_error_banner(
                        f"Could not fetch weather: {weather_data['error']}"
                    )
            else:
                try:
                    breed = get_breed_profile(breed_name)
                except ValueError as exc:
                    with col_results:
                        render_error_banner(str(exc))
                    return

                current = weather_data["current"]
                hourly = weather_data.get("hourly", [])
                location_display = weather_data["location"]["display"]

                pressures = compute_pressures(current, breed)
                mod_bonus = compute_modifier_bonus(age_group, overweight, heat_sensitive)

                sub_scores = {
                    "heat_stress": compute_heat_stress(pressures, breed, mod_bonus),
                    "dehydration": compute_dehydration(pressures, breed, mod_bonus),
                    "respiratory": compute_respiratory(pressures, breed, mod_bonus),
                    "surface_burn": compute_surface_burn(pressures, breed, current),
                    "indoor_heat": compute_indoor_heat(pressures, breed),
                }

                overall_risk = compute_overall_risk(sub_scores)
                risk_level = risk_level_label(overall_risk)
                drivers = compute_hidden_risk_drivers(current, breed, sub_scores)
                windows = compute_safe_windows(hourly, breed)
                exposure = compute_max_exposure(
                    risk_level, breed, sub_scores, age_group, overweight, heat_sensitive
                )
                recs = generate_recommendations(
                    breed=breed,
                    weather=current,
                    sub_scores=sub_scores,
                    overall_risk=overall_risk,
                    risk_level=risk_level,
                    age_group=age_group,
                    overweight=overweight,
                    heat_sensitive=heat_sensitive,
                )
                emergency = generate_emergency_signs(breed)

                st.session_state["pet_results"] = {
                    "current": current,
                    "location_display": location_display,
                    "sub_scores": sub_scores,
                    "overall_risk": overall_risk,
                    "risk_level": risk_level,
                    "drivers": drivers,
                    "windows": windows,
                    "exposure": exposure,
                    "recs": recs,
                    "emergency": emergency,
                    "species": breed["species_type"],
                }

    # ── Render Results ─────────────────────────────────────────────────────────
    results = st.session_state.get("pet_results")

    with col_results:
        if not results:
            st.markdown(
                """
                <div style="display:flex;flex-direction:column;align-items:center;
                     justify-content:center;height:320px;gap:12px;">
                    <div style="font-size:3rem;opacity:0.3;">🐾</div>
                    <div style="color:#475569;font-size:0.95rem;text-align:center;max-width:280px;line-height:1.6;">
                        Configure your pet details on the left and click
                        <strong style="color:#64748b;">Analyze Risk</strong> to get started.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        # Weather summary
        render_weather_row(results["current"], results["location_display"])

        st.markdown("<hr class='pt-divider'>", unsafe_allow_html=True)

        # Overall risk badge
        render_risk_badge(results["risk_level"], results["overall_risk"])

        # Sub-scores
        render_sub_scores_row(results["sub_scores"], results["species"])

        st.markdown("<hr class='pt-divider'>", unsafe_allow_html=True)

        # Safe windows + exposure side by side
        win_col, exp_col = st.columns(2, gap="medium")
        with win_col:
            render_safe_windows_section(results["windows"])
        with exp_col:
            render_section_label("⏱️ MAX OUTDOOR EXPOSURE")
            render_exposure_card(
                results["exposure"]["label"],
                results["exposure"]["description"],
            )

        # Hidden drivers
        render_hidden_drivers_section(results["drivers"])

        # Breed recommendations
        render_recommendations_section(results["recs"])

        # Emergency watch
        render_emergency_section(results["emergency"])