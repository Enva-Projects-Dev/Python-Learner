"""Gamification unit tests - run with a throwaway progress dir:

    python tools\\test_gamification.py
"""
import math
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_tmp = tempfile.mkdtemp(prefix="pl_test_")
os.environ["PYTHON_LEARNER_HOME"] = _tmp

from app import gamification as g          # noqa: E402
from app import progress                    # noqa: E402
from app.content import CHAPTERS            # noqa: E402

TASK = {"id": "t1", "type": "task", "title": "T", "difficulty": 2}
QUIZ = {"id": "q1", "type": "quiz", "title": "Q"}
LESSON = {"id": "l1", "type": "lesson", "title": "L"}


def fresh():
    return {k: (v.copy() if isinstance(v, dict) else list(v)
                if isinstance(v, list) else v)
            for k, v in progress._DEFAULT.items()}


def fake_chapters(items):
    return [{"id": "chT", "number": 99, "title": "Test", "items": items}]


def test_level_math():
    assert g.level_for(0) == 0
    assert g.level_for(29) == 0
    assert g.level_for(30) == 1
    assert g.level_for(3000) == 10
    assert g.xp_for_level(3) == 270


def test_rank_lookup():
    assert g.rank_for(0)["name"] == "Novice"
    assert g.rank_for(5)["name"] == "Apprentice"
    assert g.rank_for(14)["name"] == "Practitioner"
    assert g.rank_for(30)["name"] == "Master"
    assert g.rank_for(0)["next"]["name"] == "Apprentice"
    assert g.rank_for(30)["next"] is None


def test_task_xp_multipliers():
    chs = fake_chapters([TASK])

    d = fresh()
    r = g.award_task_pass(d, TASK, chs, today="2030-01-01")
    assert r["xp_gained"] == int(round(175 * 1.25)), r  # 219

    d = fresh()
    d["attempts"]["t1"] = {"fails": 0, "hints": 2, "solution_viewed": False}
    r = g.award_task_pass(d, TASK, chs, today="2030-01-01")
    assert r["xp_gained"] == int(round(175 * 1.25 * 0.80)), r  # 175

    d = fresh()
    d["attempts"]["t1"] = {"fails": 0, "hints": 0, "solution_viewed": True}
    r = g.award_task_pass(d, TASK, chs, today="2030-01-01")
    assert r["xp_gained"] == int(round(175 * 0.40)), r  # 70, first-try zählt hier nicht

    # hint-floor: ab 6 hints -> x0.50
    d = fresh()
    d["attempts"]["t1"] = {"fails": 3, "hints": 6, "solution_viewed": False}
    r = g.award_task_pass(d, TASK, chs, today="2030-01-01")
    assert r["xp_gained"] == int(round(175 * 0.50)), r


def test_boss_multiplier():
    boss = dict(TASK, id="b1", difficulty=3, boss=True)
    chs = fake_chapters([boss])
    d = fresh()
    r = g.award_task_pass(d, boss, chs, today="2030-01-01")
    assert r["xp_gained"] == int(round(250 * 1.5 * 1.25)), r  # 469
    labels = [b["label"] for b in r["breakdown"]]
    assert "Boss" in labels


def test_no_double_xp():
    chs = fake_chapters([TASK])
    d = fresh()
    g.award_task_pass(d, TASK, chs, today="2030-01-01")
    xp1 = d["xp"]
    r = g.award_task_pass(d, TASK, chs, today="2030-01-01")
    assert r["xp_gained"] == 0 and r["breakdown"] == []
    assert d["xp"] == xp1


def test_streak():
    chs = fake_chapters([TASK, QUIZ])
    d = fresh()
    g.award_task_pass(d, TASK, chs, today="2030-01-01")
    assert d["streak"]["count"] == 1
    # nächster tag: quiz kriegt streak-multi +10%
    r = g.award_quiz(d, QUIZ, chs, True, today="2030-01-02")
    assert d["streak"]["count"] == 2
    assert r["xp_gained"] == int(round(60 * 1.10)), r  # 66
    # lücke -> streak wieder auf 1
    d2 = fresh()
    g.award_task_pass(d2, TASK, chs, today="2030-01-01")
    r = g.award_quiz(d2, QUIZ, chs, True, today="2030-01-05")
    assert d2["streak"]["count"] == 1
    assert r["xp_gained"] == 60  # kein streak-multi am ersten tag


def test_chapter_cleared():
    chs = fake_chapters([TASK, QUIZ])
    d = fresh()
    r1 = g.award_task_pass(d, TASK, chs, today="2030-01-01")
    assert not r1["chapter_cleared"]
    r2 = g.award_quiz(d, QUIZ, chs, True, today="2030-01-01")
    assert r2["chapter_cleared"] is True
    ach_xp = sum(a["xp"] for a in g.ACHIEVEMENTS
                 if a["id"] in d["achievements"])
    assert d["xp"] == 219 + 60 + 300 + ach_xp, (d["xp"], ach_xp)


def test_quiz_first_try_and_lesson():
    chs = fake_chapters([QUIZ, LESSON])
    d = fresh()
    d["attempts"]["q1"] = {"fails": 1, "hints": 0, "solution_viewed": False}
    r = g.award_quiz(d, QUIZ, chs, True, today="2030-01-01")
    assert r["xp_gained"] == 40  # kein +20 mehr nach nem falschen versuch
    r = g.award_lesson_read(d, LESSON, chs, today="2030-01-01")
    assert r["xp_gained"] == 20
    r = g.award_lesson_read(d, LESSON, chs, today="2030-01-01")
    assert r["xp_gained"] == 0


def test_achievements():
    # first_steps: erster bestandener task
    chs = fake_chapters([TASK])
    d = fresh()
    r = g.award_task_pass(d, TASK, chs, today="2030-01-01")
    ids = [a["id"] for a in r["achievements_unlocked"]]
    assert "first_steps" in ids and "chapter_1" in ids
    # ein 1-task-kapitel unlocked auch halfway/completionist/night_shift
    expected = 219 + 300 + sum(a["xp"] for a in r["achievements_unlocked"])
    assert d["xp"] == expected, (d["xp"], expected)
    # gibts nicht nochmal, auch bei neuem fail
    d["completed"].pop("t1")
    d["attempts"]["t1"] = {"fails": 2, "hints": 0, "solution_viewed": False}
    r = g.award_task_pass(d, TASK, chs, today="2030-01-01")
    assert r["achievements_unlocked"] == []


def test_stats_shape():
    chs = fake_chapters([TASK, QUIZ, LESSON])
    d = fresh()
    g.award_task_pass(d, TASK, chs, today="2030-01-01")
    s = g.get_stats(d, chs, today="2030-01-01")
    assert s["xp"] > 0 and s["level"] >= 0
    assert s["rank"]["name"] == g.rank_for(s["level"])["name"]
    assert s["today_xp"] == s["xp"]
    assert s["totals"]["tasks_done"] == 1 and s["totals"]["tasks_total"] == 1
    assert len(s["achievements"]) == len(g.ACHIEVEMENTS)
    assert s["recent_events"][0]["xp"] > 0


def test_chapter_locks():
    d = fresh()
    locks = g.chapter_locks(d, CHAPTERS)
    ch0, ch1, ch2 = CHAPTERS[0], CHAPTERS[1], CHAPTERS[2]
    assert locks[ch0["id"]]["locked"] is False          # kapitel 0 immer offen
    assert locks[ch0["id"]]["prev_id"] is None
    assert locks[ch1["id"]]["locked"] is True           # 0% von ch00
    assert locks[ch1["id"]]["prev_id"] == ch0["id"]

    # genau 90% von ch00 reicht zum unlock
    total = len(ch0["items"])
    need = math.ceil(g.UNLOCK_THRESHOLD * total)
    d["completed"] = {it["id"]: "x" for it in ch0["items"][:need]}
    _, _, pct = g.chapter_completion(d, ch0)
    assert pct >= g.UNLOCK_THRESHOLD
    locks = g.chapter_locks(d, CHAPTERS)
    assert locks[ch1["id"]]["locked"] is False
    assert locks[ch1["id"]]["pct"] == int(round(pct * 100))
    assert locks[ch2["id"]]["locked"] is True           # ch01 noch bei 0%

    # knapp drunter bleibt locked
    d["completed"] = {it["id"]: "x" for it in ch0["items"][:need - 1]}
    _, _, pct2 = g.chapter_completion(d, ch0)
    if pct2 < g.UNLOCK_THRESHOLD:
        assert g.chapter_locks(d, CHAPTERS)[ch1["id"]]["locked"] is True

    # ch2 hängt nur an ch1, nicht an ch0
    d2 = fresh()
    d2["completed"] = {it["id"]: "x" for it in ch1["items"]}
    locks = g.chapter_locks(d2, CHAPTERS)
    assert locks[ch1["id"]]["locked"] is True           # ch00 leer
    assert locks[ch2["id"]]["locked"] is False          # ch1 voll -> offen

    # locks stecken auch in stats und message-felder sind da
    s = g.get_stats(d2, CHAPTERS)
    assert "locks" in s
    e = s["locks"][ch1["id"]]
    assert e["needed_pct"] == 90 and e["prev_title"] == ch0["title"]


def test_real_content_counts():
    s = g.get_stats(fresh(), CHAPTERS)
    assert s["totals"]["tasks_total"] == 170
    assert s["totals"]["quizzes_total"] == 79
    assert s["totals"]["lessons_total"] == 29


if __name__ == "__main__":
    for name, fn in sorted({k: v for k, v in globals().items()
                            if k.startswith("test_")}.items()):
        fn()
        print("ok   ", name)
    print("all gamification tests pass")
