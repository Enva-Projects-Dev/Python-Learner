"""API-Fläche fürs UI (über pywebview js_api bzw. den dev-server).

Jede Methode kriegt ein `params`-dict: pywebview reicht das js-call-argument
durch, der dev-server postet dasselbe json-objekt.
"""
from . import checker, gamification, progress, runner
from .content import CHAPTERS, find_item
from .release_notes import NOTES
from .version import VERSION


def _strip_item(item):
    out = {k: v for k, v in item.items()
           if k not in ("solution", "answer", "explanation", "hints")}
    if item["type"] == "task":
        out["tests"] = checker.public_tests(item)
        out["hint_count"] = len(item.get("hints", []))
        xp = gamification.XP_BY_DIFFICULTY.get(item.get("difficulty", 1), 100)
        if item.get("boss"):
            xp = int(round(xp * 1.5))
        out["xp"] = xp
    return out


def _p(params):
    return params if isinstance(params, dict) else {}


def _chapter_of(item_id):
    for ch in CHAPTERS:
        for it in ch["items"]:
            if it["id"] == item_id:
                return ch
    return None


def _locked(item_id):
    """None wenn offen, sonst die locked-antwort fürs item."""
    ch = _chapter_of(item_id)
    if not ch:
        return None
    entry = gamification.chapter_locks(progress.load(), CHAPTERS).get(ch["id"])
    if entry and entry["locked"]:
        return {"error": "locked",
                "message": (f"Finish {entry['needed_pct']}% of "
                            f"{entry['prev_title']} first "
                            f"({entry['pct']}% done).")}
    return None


class Api:
    def get_content(self, params=None):
        return {
            "version": VERSION,
            "chapters": [
                {**{k: v for k, v in ch.items() if k != "items"},
                 "items": [_strip_item(i) for i in ch["items"]]}
                for ch in CHAPTERS
            ],
            "locks": gamification.chapter_locks(progress.load(), CHAPTERS),
        }

    def run_code(self, params=None):
        p = _p(params)
        return runner.run(p.get("code") or "", p.get("stdin_text") or "")

    def check_task(self, params=None):
        p = _p(params)
        task_id = p.get("task_id")
        task = find_item(task_id)
        if not task or task.get("type") != "task":
            return {"passed": False, "results": [],
                    "error": f"unknown task {task_id}"}
        lock = _locked(task_id)
        if lock:
            return {"passed": False, "results": [], **lock}
        result = checker.check(task, p.get("code") or "")
        data = progress.load()
        if result["passed"]:
            reward = gamification.award_task_pass(data, task, CHAPTERS)
        else:
            if task_id not in data["completed"]:
                att = data["attempts"].setdefault(
                    task_id, {"fails": 0, "hints": 0,
                              "solution_viewed": False})
                att["fails"] = att.get("fails", 0) + 1
            reward = None
        data["last_task_id"] = task_id
        progress.save(data)
        if reward is not None:
            result["reward"] = reward
            result["stats"] = gamification.get_stats(data, CHAPTERS)
        return result

    def get_progress(self, params=None):
        return progress.load()

    def save_progress(self, params=None):
        p = _p(params)
        return progress.apply_patch(p.get("patch", p))

    def save_draft(self, params=None):
        p = _p(params)
        progress.save_draft(p.get("task_id"), p.get("code") or "")
        return {"ok": True}

    def check_quiz(self, params=None):
        p = _p(params)
        item = find_item(p.get("item_id"))
        if not item or item.get("type") != "quiz":
            return {"correct": False, "error": "unknown quiz"}
        lock = _locked(item["id"])
        if lock:
            return {"correct": False, **lock}
        try:
            choice = int(p.get("choice"))
        except (TypeError, ValueError):
            return {"correct": False, "error": "bad choice"}
        correct = choice == item.get("answer")
        data = progress.load()
        if not correct and item["id"] not in data["completed"]:
            att = data["attempts"].setdefault(
                item["id"], {"fails": 0, "hints": 0,
                             "solution_viewed": False})
            att["fails"] = att.get("fails", 0) + 1
        reward = gamification.award_quiz(data, item, CHAPTERS, correct)
        data.setdefault("quiz", {})[item["id"]] = choice
        data["last_task_id"] = item["id"]
        progress.save(data)
        return {"correct": correct, "answer": item.get("answer"),
                "explanation": item.get("explanation", ""),
                "reward": reward,
                "stats": gamification.get_stats(data, CHAPTERS)}

    def get_solution(self, params=None):
        p = _p(params)
        task = find_item(p.get("task_id"))
        if not task or task.get("type") != "task":
            return {"solution": None}
        lock = _locked(task["id"])
        if lock:
            return {"solution": None, **lock}
        progress.record_attempt(task["id"], "solution_viewed")
        return {"solution": task.get("solution", ""),
                "explanation": task.get("explanation", "")}

    def use_hint(self, params=None):
        p = _p(params)
        task = find_item(p.get("task_id"))
        if not task or task.get("type") != "task":
            return {"error": "unknown task"}
        lock = _locked(task["id"])
        if lock:
            return lock
        level = max(1, int(p.get("level") or 1))
        hints = task.get("hints", [])
        progress.record_attempt(task["id"], "hints", level)
        return {"hint": hints[level - 1] if level <= len(hints) else None,
                "level": level, "total": len(hints)}

    def mark_lesson_read(self, params=None):
        p = _p(params)
        item = find_item(p.get("item_id"))
        if not item or item.get("type") != "lesson":
            return {"error": "unknown lesson"}
        lock = _locked(item["id"])
        if lock:
            return {"ok": False, **lock}
        data = progress.load()
        reward = gamification.award_lesson_read(data, item, CHAPTERS)
        progress.save(data)
        return {"ok": True, "reward": reward,
                "stats": gamification.get_stats(data, CHAPTERS)}

    def get_stats(self, params=None):
        return gamification.get_stats(progress.load(), CHAPTERS)

    def get_whats_new(self, params=None):
        data = progress.load()
        seen = data.get("last_seen_version")
        # frische installation sieht das popup nie
        is_fresh = not data["completed"] and data["xp"] == 0 and seen is None
        if is_fresh or seen == VERSION:
            if seen != VERSION:
                data["last_seen_version"] = VERSION
                progress.save(data)
            return {"show": False, "version": VERSION,
                    "notes": NOTES.get(VERSION)}
        # update von älter/unbekannter version -> zeigen, aber erst bei
        # dismiss als gesehen markieren
        return {"show": NOTES.get(VERSION) is not None,
                "version": VERSION, "notes": NOTES.get(VERSION)}

    def dismiss_whats_new(self, params=None):
        data = progress.load()
        data["last_seen_version"] = VERSION
        progress.save(data)
        return {"ok": True}

    def reset_progress(self, params=None):
        backup = progress.reset()
        return {"ok": True, "backup": backup,
                "stats": gamification.get_stats(progress.load(), CHAPTERS)}
