"""
distress_service.py — NGO distress report management for PawTemp MVP.
"""
import base64
from pathlib import Path
from services.risk_engine import compute_distress_severity
from services.storage_service import save_distress_report, load_distress_reports

UPLOADS_DIR = Path(__file__).parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


def submit_distress_report(
    location: str,
    animal_type: str,
    symptoms: list,
    notes: str,
    weather_level: str,
    image_bytes: bytes = None,
    image_name: str = None,
) -> dict:
    """Process and store a distress report. Returns report dict with severity."""
    severity = compute_distress_severity(symptoms, animal_type, weather_level)

    image_path = None
    if image_bytes and image_name:
        safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in image_name)
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = UPLOADS_DIR / f"{ts}_{safe_name}"
        with open(save_path, "wb") as f:
            f.write(image_bytes)
        image_path = str(save_path)

    report = {
        "location": location,
        "animal_type": animal_type,
        "symptoms": symptoms,
        "notes": notes,
        "severity_score": severity["score"],
        "severity_level": severity["level"],
        "urgency": severity["urgency"],
        "weather_level_at_time": weather_level,
        "image_path": image_path,
    }

    report_id = save_distress_report(report)
    report["report_id"] = report_id
    return report


def get_all_reports_sorted() -> list:
    """Load all distress reports sorted by severity (Critical first)."""
    reports = load_distress_reports()
    level_order = {"Critical": 0, "High": 1, "Moderate": 2, "Low": 3}
    reports.sort(key=lambda r: (level_order.get(r.get("severity_level", "Low"), 4), -r.get("severity_score", 0)))
    return reports