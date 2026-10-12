"""Whats-new popup: show-logik, dismiss, reset."""
import json
import os
import sys
import tempfile

_tmp = tempfile.mkdtemp(prefix="pl_whatsnew_")
os.environ["PYTHON_LEARNER_HOME"] = _tmp

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import progress
from app.api import Api
from app.version import VERSION

api = Api()


def write(data):
    os.makedirs(_tmp, exist_ok=True)
    with open(os.path.join(_tmp, "progress.json"), "w",
              encoding="utf-8") as f:
        json.dump(data, f)


def fresh_progress(**kw):
    d = json.loads(json.dumps(progress._DEFAULT))
    d.update(kw)
    return d


def test_fresh_install_never_shows():
    write(fresh_progress())
    r = api.get_whats_new()
    assert r["show"] is False
    # frisch-installation wird direkt als gesehen gespeichert
    assert progress.load()["last_seen_version"] == VERSION


def test_updated_user_sees_popup():
    write(fresh_progress(xp=500,
                         completed={"ch00-task-1": "2026-01-01T00:00:00"}))
    r = api.get_whats_new()
    assert r["show"] is True
    assert r["version"] == VERSION
    assert r["notes"]["title"].startswith("Moin Leute")
    # noch nicht als gesehen markiert - das macht erst dismiss
    assert progress.load()["last_seen_version"] is None


def test_dismiss_marks_seen():
    write(fresh_progress(xp=100))
    api.dismiss_whats_new()
    r = api.get_whats_new()
    assert r["show"] is False
    assert progress.load()["last_seen_version"] == VERSION


def test_reset_keeps_theme_and_backups():
    write(fresh_progress(xp=900, theme="light",
                         completed={"ch00-task-1": "2026-01-01T00:00:00"}))
    r = api.reset_progress()
    assert r["ok"] is True
    backup = r["backup"]
    assert os.path.isfile(backup)
    old = json.load(open(backup, encoding="utf-8"))
    assert old["xp"] == 900  # backup hält den alten stand
    data = progress.load()
    assert data["xp"] == 0 and data["completed"] == {}
    assert data["theme"] == "light"
    assert data["last_seen_version"] == VERSION
    r2 = api.get_whats_new()
    assert r2["show"] is False


def test_unknown_seen_version_shows():
    write(fresh_progress(xp=50, last_seen_version="0.0.1"))
    r = api.get_whats_new()
    assert r["show"] is True


if __name__ == "__main__":
    for fn in (v for k, v in sorted(globals().items())
               if k.startswith("test_")):
        fn()
        print("ok   ", fn.__name__)
    print("all whats-new tests pass")
