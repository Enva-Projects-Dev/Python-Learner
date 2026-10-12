"""Findet den python-interpreter, der learner-code ausführt.

Im normalen checkout einfach ``sys.executable``. Im frozen-build ist
``sys.executable`` die app selbst - user-code damit laufen lassen würde
die app rekursiv starten. Frozen builds kriegen deshalb eine mitgepackte
runtime unter ``<app dir>/runtime/`` (embeddable python auf windows,
framework-python auf macOS), mit PATH als fallback.
"""
import os
import shutil
import sys


def python_executable():
    if not getattr(sys, "frozen", False):
        return sys.executable

    app_dir = os.path.dirname(os.path.abspath(__file__))
    # im pyinstaller onedir-layout liegt __file__ in _internal/app/ und die
    # runtime kann neben der exe sein, in _internal/ oder direkt in app/
    roots = [app_dir,
             os.path.dirname(app_dir),
             os.path.dirname(os.path.dirname(app_dir))]
    rel = ("runtime", "python.exe") if os.name == "nt" else \
        ("runtime", "bin", "python3")
    candidates = [os.path.join(root, *rel) for root in roots]
    for path in candidates:
        if os.path.isfile(path):
            return path
    for name in ("python3", "python"):
        found = shutil.which(name)
        if found:
            return found
    raise RuntimeError(
        "No Python runtime found to run learner code: the bundled "
        "runtime is missing and neither 'python3' nor 'python' is on "
        "PATH. Reinstall the app or install Python from python.org.")
