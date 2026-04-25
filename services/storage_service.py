"""
storage_service.py — Safe JSON read/write for PawTemp MVP persistence.
"""
import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DISTRESS_FILE = DATA_DIR / "distress_reports.json"
TASKS_FILE = DATA_DIR / "citizen_tasks.json"


def _ensure_file(path: Path, default: dict):
    """Create file with default content if it doesn't exist."""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(default, f, indent=2)


def _read_json(path: Path, default: dict) -> dict:
    _ensure_file(path, default)
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default


def _write_json(path: Path, data: dict):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except IOError:
        return False


# ─── Distress Reports ──────────────────────────────────────────────────────────

def load_distress_reports() -> list:
    data = _read_json(DISTRESS_FILE, {"reports": [], "next_id": 1001})
    return data.get("reports", [])


def save_distress_report(report: dict) -> str:
    data = _read_json(DISTRESS_FILE, {"reports": [], "next_id": 1001})
    report_id = f"PT-{data.get('next_id', 1001)}"
    report["report_id"] = report_id
    report["submitted_at"] = datetime.now().isoformat()
    data["reports"].append(report)
    data["next_id"] = data.get("next_id", 1001) + 1
    _write_json(DISTRESS_FILE, data)
    return report_id


# ─── Community Tasks ───────────────────────────────────────────────────────────

def load_task_log() -> list:
    data = _read_json(TASKS_FILE, {"tasks": {}, "completion_log": []})
    return data.get("completion_log", [])


def log_task_completion(task_id: str, task_text: str, points: int, location: str) -> dict:
    data = _read_json(TASKS_FILE, {"tasks": {}, "completion_log": []})
    entry = {
        "task_id": task_id,
        "task": task_text,
        "points": points,
        "location": location,
        "completed_at": datetime.now().isoformat(),
    }
    data.setdefault("completion_log", []).append(entry)
    _write_json(TASKS_FILE, data)
    return entry


def get_total_points() -> int:
    log = load_task_log()
    return sum(e.get("points", 0) for e in log)


def get_streak_days() -> int:
    log = load_task_log()
    if not log:
        return 0
    from datetime import date
    dates = set()
    for e in log:
        try:
            d = datetime.fromisoformat(e["completed_at"]).date()
            dates.add(d)
        except Exception:
            pass
    if not dates:
        return 0
    today = date.today()
    streak = 0
    current = today
    while current in dates:
        streak += 1
        current = current.replace(day=current.day - 1) if current.day > 1 else current
        break  # simple streak for MVP
    return max(streak, 1) if dates else 0