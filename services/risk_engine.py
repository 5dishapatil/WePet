"""
risk_engine.py — Deterministic, explainable climate risk engine for PawTemp MVP.

Implements the exact logic formulas from the PawTemp Logic Pack.
"""
from typing import Optional


def clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    return max(min_value, min(max_value, value))


# ─── Weather Pressure Normalizers ─────────────────────────────────────────────

def compute_pressures(weather: dict, breed: dict) -> dict:
    temp = weather["temperature"]
    apparent = weather["apparent_temperature"]
    humidity = weather["humidity"]
    uv = weather.get("uv_index", 0) or 0
    wind = weather.get("wind_speed", 0) or 0
    is_day = weather.get("is_day", 1)

    temp_pressure = clamp((temp - breed["thermal_comfort_max"]) / 12)
    apparent_pressure = clamp((apparent - breed["safe_apparent_temp_limit"]) / 10)
    humidity_pressure = clamp((humidity - 55) / 35)
    uv_pressure = clamp((uv - 3) / 8) if is_day else 0.0
    wind_relief = clamp(wind / 25, 0, 0.25)

    return {
        "temp_pressure": temp_pressure,
        "apparent_pressure": apparent_pressure,
        "humidity_pressure": humidity_pressure,
        "uv_pressure": uv_pressure,
        "wind_relief": wind_relief,
    }


# ─── Modifier Bonus ────────────────────────────────────────────────────────────

def compute_modifier_bonus(age_group: str, overweight: bool, heat_sensitive: bool) -> float:
    bonus = 0.0
    if age_group == "senior":
        bonus += 0.08
    if overweight:
        bonus += 0.10
    if heat_sensitive:
        bonus += 0.10
    return bonus


# ─── Sub-Scores ───────────────────────────────────────────────────────────────

def compute_heat_stress(pressures: dict, breed: dict, modifier_bonus: float) -> float:
    raw = (
        0.30 * pressures["temp_pressure"]
        + 0.35 * pressures["apparent_pressure"]
        + 0.20 * pressures["humidity_pressure"] * breed["humidity_sensitivity"]
        + 0.10 * pressures["uv_pressure"]
        + 0.15 * breed["base_heat_sensitivity"]
        + modifier_bonus
        - pressures["wind_relief"]
    )
    return clamp(raw) * 100


def compute_dehydration(pressures: dict, breed: dict, modifier_bonus: float) -> float:
    raw = (
        0.35 * pressures["temp_pressure"]
        + 0.25 * pressures["apparent_pressure"]
        + 0.20 * pressures["humidity_pressure"]
        + 0.10 * breed["dehydration_sensitivity"]
        + 0.10 * pressures["uv_pressure"]
        + modifier_bonus * 0.5
    )
    return clamp(raw) * 100


def compute_respiratory(pressures: dict, breed: dict, modifier_bonus: float) -> float:
    raw = (
        0.30 * pressures["apparent_pressure"]
        + 0.25 * pressures["humidity_pressure"]
        + 0.25 * breed["respiratory_sensitivity"]
        + 0.10 * pressures["uv_pressure"]
        + modifier_bonus * 0.4
    )
    return clamp(raw) * 100


def compute_surface_burn(pressures: dict, breed: dict, weather: dict) -> float:
    temp = weather["temperature"]
    uv = weather.get("uv_index", 0) or 0

    raw = (
        0.45 * pressures["temp_pressure"]
        + 0.25 * pressures["uv_pressure"]
        + 0.20 * pressures["apparent_pressure"]
        + 0.10 * breed["surface_burn_sensitivity"]
    )
    score = clamp(raw) * 100
    if temp >= 30 and uv >= 6:
        score = min(score + 10, 100)
    return score


def compute_indoor_heat(pressures: dict, breed: dict) -> float:
    raw = (
        0.35 * pressures["temp_pressure"]
        + 0.30 * pressures["apparent_pressure"]
        + 0.10 * pressures["humidity_pressure"]
        + 0.25 * breed["indoor_heat_trap_sensitivity"]
    )
    return clamp(raw) * 100


# ─── Overall Risk ─────────────────────────────────────────────────────────────

def compute_overall_risk(sub_scores: dict) -> float:
    return (
        0.32 * sub_scores["heat_stress"]
        + 0.18 * sub_scores["dehydration"]
        + 0.22 * sub_scores["respiratory"]
        + 0.14 * sub_scores["surface_burn"]
        + 0.14 * sub_scores["indoor_heat"]
    )


def risk_level_label(score: float) -> str:
    if score < 25:
        return "Low"
    elif score < 50:
        return "Moderate"
    elif score < 75:
        return "High"
    else:
        return "Critical"


# ─── Hidden Risk Drivers ──────────────────────────────────────────────────────

def compute_hidden_risk_drivers(weather: dict, breed: dict, sub_scores: dict) -> list:
    drivers = []
    temp = weather["temperature"]
    apparent = weather["apparent_temperature"]
    humidity = weather["humidity"]
    uv = weather.get("uv_index", 0) or 0
    is_day = weather.get("is_day", 1)
    species = breed["species_type"]
    coat = breed.get("coat_type", "")

    if humidity > 75 and species == "dog":
        drivers.append("🌫️ High humidity reduces cooling efficiency through panting — a critical hidden risk for dogs.")

    if apparent - temp >= 3:
        drivers.append(
            f"🌡️ Apparent temperature ({apparent:.1f}°C) is significantly higher than air temperature ({temp:.1f}°C), "
            "increasing hidden heat load."
        )

    if breed.get("brachycephalic", False):
        drivers.append(
            "😮‍💨 Brachycephalic breed — shortened airway structure creates elevated respiratory risk "
            "in warm or humid conditions."
        )

    dense_coats = ["double_coat", "double_coat_heavy", "long_dense", "heavy_long", "dense_short"]
    if coat in dense_coats:
        drivers.append(
            "🧣 Dense or insulating coat retains body heat longer, especially after physical activity — "
            "risk persists even after returning indoors."
        )

    if uv >= 6 and is_day:
        drivers.append(
            "☀️ Strong UV index increases direct heat load and significantly elevates hot-surface risk "
            "for ground contact."
        )

    if sub_scores["surface_burn"] >= 65:
        drivers.append(
            "🔥 Ground and pavement surface temperatures may be dangerous even if the air feels manageable — "
            "paw burn risk is elevated."
        )

    if sub_scores["indoor_heat"] >= 60 and species == "cat":
        drivers.append(
            "🏠 Indoor spaces near sun-facing windows may trap heat significantly — "
            "indoor risk can exceed outdoor apparent conditions."
        )

    if breed["breed_name"] == "Sphynx" and uv >= 5 and is_day:
        drivers.append(
            "🦴 Despite minimal coat, Sphynx have high direct sun sensitivity — "
            "hairless skin absorbs UV and heat rapidly from sun patches."
        )

    if breed["breed_name"] == "Siberian Husky" and temp >= 26:
        drivers.append(
            "🐺 Cold-adapted breed — Siberian Huskies accumulate heat stress earlier than owners expect "
            "in seemingly tolerable temperatures."
        )

    return drivers[:5]  # Cap at 5 drivers


# ─── Safe Window Logic ────────────────────────────────────────────────────────

def _hourly_risk_simplified(hour: dict, breed: dict) -> float:
    """Compute a simplified hourly risk score for safe-window detection."""
    temp = hour.get("temperature") or 20
    apparent = hour.get("apparent_temperature") or temp
    humidity = hour.get("humidity") or 50
    uv = hour.get("uv_index") or 0
    is_day = hour.get("is_day", 1)

    temp_p = clamp((temp - breed["thermal_comfort_max"]) / 12)
    apparent_p = clamp((apparent - breed["safe_apparent_temp_limit"]) / 10)
    humidity_p = clamp((humidity - 55) / 35)
    uv_p = clamp((uv - 3) / 8) if is_day else 0

    raw = (
        0.35 * apparent_p
        + 0.25 * temp_p
        + 0.20 * humidity_p * breed["humidity_sensitivity"]
        + 0.10 * uv_p
        + 0.10 * breed["base_heat_sensitivity"]
    )
    return clamp(raw) * 100


def compute_safe_windows(hourly: list, breed: dict) -> dict:
    """Find 1–2 best time windows for outdoor activity from 12-hour forecast."""
    if not hourly:
        return {
            "windows": [],
            "message": "No forecast data available for window analysis.",
            "indoor_only": False,
        }

    scored = []
    for h in hourly:
        if h.get("temperature") is None:
            continue
        risk = _hourly_risk_simplified(h, breed)
        suitability = 100 - risk

        # Apply penalties
        uv = h.get("uv_index") or 0
        apparent = h.get("apparent_temperature") or h.get("temperature")
        humidity = h.get("humidity") or 50
        is_day = h.get("is_day", 1)

        if uv > 5:
            suitability -= 8
        if apparent > breed["safe_apparent_temp_limit"]:
            suitability -= 12
        if humidity > 75 and breed["species_type"] == "dog":
            suitability -= 8
        if is_day and uv > 5:
            suitability -= 5

        scored.append({
            "time": h["time"],
            "hour_label": h["hour_label"],
            "suitability": suitability,
            "risk": risk,
            "apparent": apparent,
        })

    # Find consecutive eligible windows (suitability >= 55)
    windows = []
    current_window = []

    for s in scored:
        if s["suitability"] >= 55:
            current_window.append(s)
        else:
            if current_window:
                windows.append(current_window)
                current_window = []
    if current_window:
        windows.append(current_window)

    # Sort windows by average risk (lowest first)
    windows.sort(key=lambda w: sum(h["risk"] for h in w) / len(w))
    top_windows = windows[:2]

    if not top_windows:
        return {
            "windows": [],
            "message": "No low-risk outdoor window detected in the next 12 hours. Indoor enrichment recommended.",
            "indoor_only": True,
        }

    formatted = []
    for w in top_windows:
        start = w[0]["hour_label"]
        end = w[-1]["hour_label"]
        avg_risk = sum(h["risk"] for h in w) / len(w)
        avg_apparent = sum(h["apparent"] for h in w) / len(w)
        label = f"{start}" if len(w) == 1 else f"{start} – {end}"
        formatted.append({
            "window": label,
            "avg_risk": avg_risk,
            "avg_apparent": avg_apparent,
            "hours": len(w),
        })

    return {
        "windows": formatted,
        "message": f"Best window(s) identified from next 12-hour forecast.",
        "indoor_only": False,
    }


# ─── Max Outdoor Exposure ─────────────────────────────────────────────────────

def compute_max_exposure(
    risk_level: str,
    breed: dict,
    sub_scores: dict,
    age_group: str,
    overweight: bool,
    heat_sensitive: bool,
) -> dict:
    base = {"Low": 25, "Moderate": 15, "High": 8, "Critical": 0}.get(risk_level, 0)

    breed_penalty = int(breed["base_heat_sensitivity"] * 8)

    resp = sub_scores["respiratory"]
    resp_penalty = 5 if resp >= 70 else (3 if resp >= 50 else 0)

    surf = sub_scores["surface_burn"]
    surf_penalty = 4 if surf >= 70 else (2 if surf >= 50 else 0)

    mod_penalty = 0
    if age_group == "senior":
        mod_penalty += 3
    if overweight:
        mod_penalty += 3
    if heat_sensitive:
        mod_penalty += 3

    final = max(base - breed_penalty - resp_penalty - surf_penalty - mod_penalty, 0)

    if final == 0:
        label = "🏠 Indoor-only today"
        desc = "Outdoor exposure not recommended under current conditions."
    elif final <= 5:
        label = f"⏱️ Very brief shaded exposure only ({final} min)"
        desc = "Essential relief breaks only. Full shade required. Carry water."
    elif final <= 10:
        label = f"⏱️ Short shaded outing only ({final} min)"
        desc = "Keep strictly shaded. Watch for warning signs throughout."
    elif final <= 20:
        label = f"⏱️ Short controlled outdoor time ({final} min)"
        desc = "Shade, water, and close monitoring required."
    else:
        label = f"⏱️ Moderate outdoor activity possible ({final} min)"
        desc = "Manageable with water access and shade. Avoid peak UV hours."

    return {"minutes": final, "label": label, "description": desc}


# ─── Community Heat Score ─────────────────────────────────────────────────────

def compute_community_heat_score(weather: dict) -> dict:
    """Standalone heat severity for community mode (no breed context)."""
    temp = weather["temperature"]
    apparent = weather["apparent_temperature"]
    humidity = weather["humidity"]
    uv = weather.get("uv_index", 0) or 0
    is_day = weather.get("is_day", 1)

    # Use generic animal comfort baseline
    temp_p = clamp((temp - 22) / 12)
    apparent_p = clamp((apparent - 28) / 10)
    humidity_p = clamp((humidity - 55) / 35)
    uv_p = clamp((uv - 3) / 8) if is_day else 0

    score = (
        0.35 * temp_p
        + 0.35 * apparent_p
        + 0.15 * humidity_p
        + 0.15 * uv_p
    ) * 100

    score = clamp(score, 0, 100)
    label = risk_level_label(score)

    return {"score": score, "level": label}


# ─── NGO Distress Severity ────────────────────────────────────────────────────

SYMPTOM_WEIGHTS = {
    "heavy_panting": 20,
    "lethargy": 15,
    "collapse": 40,
    "unable_to_stand": 35,
    "open_mouth_breathing": 25,
    "disorientation": 25,
}

WEATHER_BONUS = {"Low": 0, "Moderate": 5, "High": 10, "Critical": 15}
ANIMAL_BONUS = {"dog": 5, "cat": 3, "unknown": 0}

URGENCY_TEXT = {
    "Low": "Monitor / low-priority follow-up",
    "Moderate": "Needs review soon",
    "High": "Prioritize response",
    "Critical": "🚨 Urgent response recommended",
}


def compute_distress_severity(symptoms: list, animal_type: str, weather_level: str) -> dict:
    sym_score = sum(SYMPTOM_WEIGHTS.get(s, 0) for s in symptoms)
    weather_bonus = WEATHER_BONUS.get(weather_level, 0)
    animal_bonus = ANIMAL_BONUS.get(animal_type.lower(), 0)

    score = min(sym_score + weather_bonus + animal_bonus, 100)
    level = risk_level_label(score)
    urgency = URGENCY_TEXT.get(level, "")

    return {"score": score, "level": level, "urgency": urgency}