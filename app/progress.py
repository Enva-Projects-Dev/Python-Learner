"""Persistenter fortschritt als json.

Liegt unter $PYTHON_LEARNER_HOME/progress.json wenn die env-var gesetzt
ist (für tests), sonst im pro-user datenordner:
- Windows: %LOCALAPPDATA%\\PythonLearner\\progress.json
- macOS:   ~/Library/Application Support/PythonLearner/progress.json
- Linux:   ~/.local/share/PythonLearner/progress.json
"""
import json
import os
import sys
from datetime import datetime, timezone


def _data_dir():
    if os.environ.get("PYTHON_LEARNER_HOME"):
        return os.environ["PYTHON_LEARNER_HOME"]
    if sys.platform == "darwin":
        return os.path.join(os.path.expanduser("~"),
                            "Library", "Application Support", "PythonLearner")
    if sys.platform.startswith("linux"):
        return os.path.join(os.path.expanduser("~"),
                            ".local", "share", "PythonLearner")
    return os.path.join(
        os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"),
        "PythonLearner")


_DIR = _data_dir()
_PATH = os.path.join(_DIR, "progress.json")

_DEFAULT = {
    "completed": {},      # item_id -> iso-timestamp (tasks, quizzes, lessons)
    "drafts": {},         # task_id -> code-entwurf
    "quiz": {},           # task_id -> gewählter index
    "last_task_id": None,
    "theme": None,
    "xp": 0,
    "events": [],         # {ts, kind, item_id, xp, note}, neueste hinten, max 500
    "attempts": {},       # item_id -> {fails, hints, solution_viewed}
    "daily": {},          # "YYYY-MM-DD" -> verdiente xp
    "streak": {"count": 0, "last_day": None},
    "achievements": {},   # achievement_id -> iso-timestamp
    "daily_goal": 300,
    "last_seen_version": None,  # zuletzt gezeigte whats-new-version
}


def load():
    try:
        with open(_PATH, encoding="utf-8") as f:
            data = json.load(f)
        out = dict(_DEFAULT)
        out.update(data)
        out.setdefault("streak", {"count": 0, "last_day": None})
        return out
    except (OSError, json.JSONDecodeError):
        return dict(_DEFAULT)


def save(data):
    os.makedirs(_DIR, exist_ok=True)
    tmp = _PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    os.replace(tmp, _PATH)


def mark_completed(task_id):
    data = load()
    data["completed"][task_id] = datetime.now(timezone.utc).isoformat()
    save(data)
    return data


def save_draft(task_id, code):
    data = load()
    data["drafts"][task_id] = code
    save(data)
    return data


def apply_patch(patch):
    """Erlaubte top-level-felder aus einem patch-dict mergen."""
    data = load()
    if not isinstance(patch, dict):
        return data
    for key in ("quiz", "last_task_id", "theme", "daily_goal"):
        if key in patch:
            if key == "quiz" and isinstance(patch[key], dict):
                data["quiz"].update(patch[key])
            else:
                data[key] = patch[key]
    save(data)
    return data


def record_attempt(task_id, field, value=None):
    """attempts[task_id][field] updaten; gibt die progress-data zurück."""
    data = load()
    att = data["attempts"].setdefault(
        task_id, {"fails": 0, "hints": 0, "solution_viewed": False})
    if field == "fails":
        att["fails"] = att.get("fails", 0) + 1
    elif field == "hints":
        att["hints"] = max(att.get("hints", 0), int(value or 0))
    elif field == "solution_viewed":
        att["solution_viewed"] = True
    save(data)
    return data


def reset(keep_theme=True):
    """Backup bauen, dann frischen Stand speichern. Gibt den Backup-Pfad."""
    from .version import VERSION

    old = load()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = os.path.join(_DIR, f"progress.backup-{stamp}.json")
    os.makedirs(_DIR, exist_ok=True)
    try:
        with open(backup, "w", encoding="utf-8") as f:
            json.dump(old, f, indent=1)
    except OSError:
        pass
    fresh = json.loads(json.dumps(_DEFAULT))  # deep copy, keine shared refs
    if keep_theme:
        fresh["theme"] = old.get("theme")
    # direkt als gesehen markieren, sonst poppt whats-new gleich wieder auf
    fresh["last_seen_version"] = VERSION
    save(fresh)
    return backup
