"""XP, level, ränge, streaks und achievements.

Sämtliches xp wird hier gerechnet - das ui leitet selbst nichts ab. die
funktionen kriegen das progress-data-dict (von progress.load()), mutieren
es, und der aufrufer speichert mit progress.save(). `today` darf man als
date oder "YYYY-MM-DD"-string reinreichen, damit tests deterministisch sind.
"""
import math
from datetime import date, datetime, timedelta, timezone

XP_BY_DIFFICULTY = {1: 100, 2: 175, 3: 250}
QUIZ_XP = 40
QUIZ_FIRST_TRY_BONUS = 20
LESSON_XP = 20
CHAPTER_XP = 300
MAX_EVENTS = 500

RANKS = [
    {"min_level": 0,  "name": "Novice",
     "desc": "Syntax, variables and first programs"},
    {"min_level": 5,  "name": "Apprentice",
     "desc": "Control flow, lists and strings"},
    {"min_level": 10, "name": "Practitioner",
     "desc": "Functions, dictionaries and sets"},
    {"min_level": 15, "name": "Craftsman",
     "desc": "Classes, modules and exceptions"},
    {"min_level": 20, "name": "Specialist",
     "desc": "OOP design, generators and closures"},
    {"min_level": 25, "name": "Expert",
     "desc": "Files, labs and complete programs"},
    {"min_level": 30, "name": "Master",
     "desc": "Course complete - you can build anything here"},
]

ACHIEVEMENTS = [
    {"id": "first_steps",   "title": "First Steps",
     "desc": "Pass your first task", "xp": 50},
    {"id": "quiz_whiz",     "title": "Quiz Whiz",
     "desc": "Answer 10 quizzes correctly", "xp": 75},
    {"id": "flawless_5",    "title": "Flawless",
     "desc": "Pass 5 tasks on the first try", "xp": 100},
    {"id": "no_hints_10",   "title": "No Help Needed",
     "desc": "Pass 10 tasks without using hints", "xp": 100},
    {"id": "chapter_1",     "title": "Chapter Down",
     "desc": "Complete all tasks and quizzes of a chapter", "xp": 100},
    {"id": "halfway",       "title": "Halfway There",
     "desc": "Complete 50% of all tasks", "xp": 200},
    {"id": "streak_3",      "title": "Warming Up",
     "desc": "Earn XP on 3 consecutive days", "xp": 75},
    {"id": "streak_7",      "title": "On Fire",
     "desc": "Earn XP on 7 consecutive days", "xp": 200},
    {"id": "night_shift",   "title": "Night Shift",
     "desc": "Earn 500 XP in a single day", "xp": 100},
    {"id": "completionist", "title": "Completionist",
     "desc": "Complete every task in the course", "xp": 500},
]


def _today_str(today=None):
    if today is None:
        return date.today().isoformat()
    if isinstance(today, str):
        return today
    return today.isoformat()


def _ensure(data):
    for key, default in (
            ("xp", 0), ("events", []), ("attempts", {}), ("daily", {}),
            ("achievements", {}), ("daily_goal", 300), ("completed", {})):
        data.setdefault(key, default.copy() if isinstance(default, dict)
                        else list(default) if isinstance(default, list)
                        else default)
    data.setdefault("streak", {"count": 0, "last_day": None})
    return data


def level_for(xp):
    return int(math.floor(math.sqrt(max(0, xp) / 30)))


def xp_for_level(level):
    return 30 * level * level


def rank_for(level):
    current = RANKS[0]
    nxt = None
    for i, r in enumerate(RANKS):
        if level >= r["min_level"]:
            current = r
            nxt = RANKS[i + 1] if i + 1 < len(RANKS) else None
        else:
            break
    out = dict(current)
    out["next"] = {"name": nxt["name"], "level": nxt["min_level"]} if nxt else None
    return out


def _record_event(data, kind, item_id, xp, note=""):
    data["events"].append({
        "ts": datetime.now(timezone.utc).isoformat(),
        "kind": kind, "item_id": item_id, "xp": xp, "note": note,
    })
    if len(data["events"]) > MAX_EVENTS:
        del data["events"][:-MAX_EVENTS]


def _update_streak(data, today_s):
    """Bei jeder xp-vergabe aufrufen; der tag zählt einmal ab >=1 xp."""
    st = data["streak"]
    last = st.get("last_day")
    if last == today_s:
        return
    yesterday = (date.fromisoformat(today_s) - timedelta(days=1)).isoformat()
    st["count"] = st.get("count", 0) + 1 if last == yesterday else 1
    st["last_day"] = today_s


def _streak_multiplier(data):
    return 1.0 + min(0.5, 0.10 * max(0, data["streak"].get("count", 1) - 1))


def _add_xp(data, amount, today_s, kind, item_id, note=""):
    data["xp"] += amount
    data["daily"][today_s] = data["daily"].get(today_s, 0) + amount
    _record_event(data, kind, item_id, amount, note)


def _attempts(data, item_id):
    return data["attempts"].get(
        item_id, {"fails": 0, "hints": 0, "solution_viewed": False})


def _chapter_of(item_id, chapters):
    for ch in chapters:
        for it in ch["items"]:
            if it["id"] == item_id:
                return ch
    return None


def _chapter_cleared(data, chapter):
    return all(it["id"] in data["completed"]
               for it in chapter["items"]
               if it["type"] in ("task", "quiz"))


def _counts(data, chapters):
    tasks = quizzes = lessons = 0
    tasks_done = quizzes_done = lessons_done = cleared = 0
    for ch in chapters:
        ch_done = True
        has_checkable = False
        for it in ch["items"]:
            done = it["id"] in data["completed"]
            if it["type"] == "task":
                tasks += 1; tasks_done += done
                has_checkable = True; ch_done &= done
            elif it["type"] == "quiz":
                quizzes += 1; quizzes_done += done
                has_checkable = True; ch_done &= done
            elif it["type"] == "lesson":
                lessons += 1; lessons_done += done
        if has_checkable and ch_done:
            cleared += 1
    return {"tasks_done": tasks_done, "tasks_total": tasks,
            "quizzes_done": quizzes_done, "quizzes_total": quizzes,
            "lessons_read": lessons_done, "lessons_total": lessons,
            "chapters_cleared": cleared}


def _check_achievements(data, chapters, today_s):
    """Offene achievements freischalten; gibt die neuen als liste zurück."""
    c = _counts(data, chapters)
    att = data["attempts"]
    tasks = [it for ch in chapters for it in ch["items"]
             if it["type"] == "task" and it["id"] in data["completed"]]
    flawless = sum(1 for t in tasks
                   if att.get(t["id"], {}).get("fails", 0) == 0)
    no_hints = sum(1 for t in tasks
                   if att.get(t["id"], {}).get("hints", 0) == 0)
    unlocked = []
    checks = {
        "first_steps": len(tasks) >= 1,
        "quiz_whiz": c["quizzes_done"] >= 10,
        "flawless_5": flawless >= 5,
        "no_hints_10": no_hints >= 10,
        "chapter_1": c["chapters_cleared"] >= 1,
        "halfway": c["tasks_total"] > 0
                   and c["tasks_done"] >= c["tasks_total"] / 2,
        "streak_3": data["streak"].get("count", 0) >= 3,
        "streak_7": data["streak"].get("count", 0) >= 7,
        "night_shift": data["daily"].get(today_s, 0) >= 500,
        "completionist": c["tasks_total"] > 0
                         and c["tasks_done"] >= c["tasks_total"],
    }
    for a in ACHIEVEMENTS:
        if a["id"] in data["achievements"]:
            continue
        if checks.get(a["id"]):
            data["achievements"][a["id"]] = \
                datetime.now(timezone.utc).isoformat()
            _add_xp(data, a["xp"], today_s, "achievement", a["id"],
                    a["title"])
            unlocked.append(a)
    return unlocked


def _reward(data, xp_gained, breakdown, level_before, rank_before,
            chapters, today_s):
    level_after = level_for(data["xp"])
    rank_after = rank_for(level_after)
    return {
        "xp_gained": xp_gained,
        "breakdown": breakdown,
        "level_before": level_before,
        "level_after": level_after,
        "rank_before": rank_before["name"],
        "rank_after": rank_after["name"],
        "achievements_unlocked": data.pop("_just_unlocked", []),
        "chapter_cleared": data.pop("_chapter_cleared", False),
        "streak": dict(data["streak"]),
    }


def award_task_pass(data, task, chapters, today=None):
    """XP fürs erste bestehen einer task. mutiert data, gibt reward zurück."""
    _ensure(data)
    today_s = _today_str(today)
    item_id = task["id"]
    level_before = level_for(data["xp"])
    rank_before = rank_for(level_before)
    if item_id in data["completed"]:
        return _reward(data, 0, [], level_before, rank_before,
                       chapters, today_s)

    att = _attempts(data, item_id)
    base = XP_BY_DIFFICULTY.get(task.get("difficulty", 1), 100)
    breakdown = [{"label": "Base", "value": base}]
    if task.get("boss"):
        base *= 1.5
        breakdown.append({"label": "Boss", "value": "x1.5"})
    if att.get("solution_viewed"):
        xp = base * 0.40
        breakdown.append({"label": "Solution viewed", "value": "x0.40"})
    else:
        xp = float(base)
        if att.get("fails", 0) == 0:
            xp *= 1.25
            breakdown.append({"label": "First try", "value": "x1.25"})
        if att.get("hints", 0) > 0:
            m = max(0.50, 1.0 - 0.10 * att["hints"])
            xp *= m
            breakdown.append({"label": f'Hints ({att["hints"]})',
                              "value": f"x{m:.2f}"})
    _update_streak(data, today_s)
    sm = _streak_multiplier(data)
    if sm > 1.0:
        xp *= sm
        breakdown.append({"label": "Streak bonus",
                          "value": f"+{int(round((sm - 1) * 100))}%"})
    xp = int(round(xp))

    data["completed"][item_id] = datetime.now(timezone.utc).isoformat()
    _add_xp(data, xp, today_s, "task", item_id, task.get("title", ""))

    ch = _chapter_of(item_id, chapters)
    if ch and _chapter_cleared(data, ch):
        _add_xp(data, CHAPTER_XP, today_s, "chapter", ch["id"],
                ch.get("title", ""))
        data["_chapter_cleared"] = True

    data["_just_unlocked"] = _check_achievements(data, chapters, today_s)
    return _reward(data, xp, breakdown, level_before, rank_before,
                   chapters, today_s)


def award_quiz(data, item, chapters, correct, today=None):
    """XP für die erste richtige quiz-antwort."""
    _ensure(data)
    today_s = _today_str(today)
    item_id = item["id"]
    level_before = level_for(data["xp"])
    rank_before = rank_for(level_before)
    if not correct or item_id in data["completed"]:
        return _reward(data, 0, [], level_before, rank_before,
                       chapters, today_s)

    att = _attempts(data, item_id)
    xp = float(QUIZ_XP)
    breakdown = [{"label": "Quiz correct", "value": QUIZ_XP}]
    if att.get("fails", 0) == 0:
        xp += QUIZ_FIRST_TRY_BONUS
        breakdown.append({"label": "First try",
                          "value": f"+{QUIZ_FIRST_TRY_BONUS}"})
    _update_streak(data, today_s)
    sm = _streak_multiplier(data)
    if sm > 1.0:
        xp *= sm
        breakdown.append({"label": "Streak bonus",
                          "value": f"+{int(round((sm - 1) * 100))}%"})
    xp = int(round(xp))

    data["completed"][item_id] = datetime.now(timezone.utc).isoformat()
    _add_xp(data, xp, today_s, "quiz", item_id, item.get("title", ""))

    ch = _chapter_of(item_id, chapters)
    if ch and _chapter_cleared(data, ch):
        _add_xp(data, CHAPTER_XP, today_s, "chapter", ch["id"],
                ch.get("title", ""))
        data["_chapter_cleared"] = True

    data["_just_unlocked"] = _check_achievements(data, chapters, today_s)
    return _reward(data, xp, breakdown, level_before, rank_before,
                   chapters, today_s)


def award_lesson_read(data, item, chapters, today=None):
    """XP fürs erste gelesen-markieren einer lesson."""
    _ensure(data)
    today_s = _today_str(today)
    item_id = item["id"]
    level_before = level_for(data["xp"])
    rank_before = rank_for(level_before)
    if item["type"] != "lesson" or item_id in data["completed"]:
        return _reward(data, 0, [], level_before, rank_before,
                       chapters, today_s)
    _update_streak(data, today_s)
    xp = LESSON_XP
    breakdown = [{"label": "Lesson read", "value": xp}]
    data["completed"][item_id] = datetime.now(timezone.utc).isoformat()
    _add_xp(data, xp, today_s, "lesson", item_id, item.get("title", ""))
    data["_just_unlocked"] = _check_achievements(data, chapters, today_s)
    return _reward(data, xp, breakdown, level_before, rank_before,
                   chapters, today_s)


UNLOCK_THRESHOLD = 0.90


def chapter_completion(data, chapter):
    """(erledigt, gesamt, anteil) - zählt alle items des kapitels."""
    total = len(chapter["items"])
    done = sum(1 for it in chapter["items"]
               if it["id"] in data["completed"])
    pct = done / total if total else 1.0
    return done, total, pct


def chapter_locks(data, chapters):
    """chapter is locked wenn vorheriges < 90% erledigt ist."""
    needed = int(round(UNLOCK_THRESHOLD * 100))
    locks = {}
    prev = None
    for ch in chapters:
        entry = {"locked": False, "pct": 100, "needed_pct": needed,
                 "prev_title": None, "prev_id": None}
        if prev is not None:
            _, _, pct = chapter_completion(data, prev)
            entry.update({
                "locked": pct < UNLOCK_THRESHOLD,
                "pct": int(round(pct * 100)),
                "prev_title": prev.get("title"),
                "prev_id": prev["id"],
            })
        locks[ch["id"]] = entry
        prev = ch
    return locks


def get_stats(data, chapters, today=None):
    _ensure(data)
    today_s = _today_str(today)
    xp = data["xp"]
    level = level_for(xp)
    rank = rank_for(level)
    next_xp = xp_for_level(level + 1)
    cur_xp = xp_for_level(level)
    level_progress = (xp - cur_xp) / (next_xp - cur_xp) if next_xp > cur_xp else 1.0
    streak = dict(data["streak"])
    last = streak.get("last_day")
    yesterday = (date.fromisoformat(today_s) - timedelta(days=1)).isoformat()
    if last not in (today_s, yesterday):
        streak["count"] = 0
    return {
        "xp": xp,
        "level": level,
        "rank": rank,
        "ranks": RANKS,
        "next_level_xp": next_xp,
        "level_progress": round(level_progress, 4),
        "streak": streak,
        "today_xp": data["daily"].get(today_s, 0),
        "daily_goal": data.get("daily_goal", 300),
        "achievements": [
            {**a, "unlocked": data["achievements"].get(a["id"])}
            for a in ACHIEVEMENTS
        ],
        "recent_events": data["events"][-8:][::-1],
        "totals": _counts(data, chapters),
        "locks": chapter_locks(data, chapters),
    }
