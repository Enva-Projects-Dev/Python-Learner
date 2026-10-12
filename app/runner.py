"""User-code in einem frischen temp-verzeichnis als subprocess starten."""
import os
import re
import shutil
import subprocess
import tempfile
import time

from . import errors
from .pyexe import python_executable

DATA_DIR = os.path.join(os.path.dirname(__file__), "content", "data")
MAX_OUTPUT = 20000
TIMEOUT = 5

# kommt vor jeden run, damit input() prompts + eingetippte zeilen echot
# wie im terminal, auch wenn stdin gepiped is. bewusst auf wenige zeilen
# gequetscht, damit man den traceback-offset wieder abziehen kann
PREAMBLE = (
    'import builtins as _b, sys as _s\n'
    'def _input(prompt=""):\n'
    '    _s.stdout.write(str(prompt)); _s.stdout.flush()\n'
    '    line = _s.stdin.readline()\n'
    '    if not line: raise EOFError("No more input available (the program asked for more input than provided).")\n'
    '    line = line.rstrip("\\n"); _s.stdout.write(line + "\\n"); return line\n'
    '_b.input = _input\n'
)
PREAMBLE_LINES = PREAMBLE.count("\n")  # zeilen die vor user-zeile 1 belegt sind

_LINE_RE = re.compile(r'File "[^"]*main\.py", line (\d+)')


def _fix_line_numbers(stderr):
    def repl(m):
        n = int(m.group(1)) - PREAMBLE_LINES
        return f'File "main.py", line {max(n, 1)}'
    return _LINE_RE.sub(repl, stderr)


def _cap(text):
    if len(text) > MAX_OUTPUT:
        return text[:MAX_OUTPUT] + "\n... output truncated"
    return text


def run(code, stdin_text="", timeout=TIMEOUT, cwd=None):
    """Code im temp-dir laufen lassen (data-files werden reinkopiert). gibt dict zurück."""
    own_dir = cwd is None
    tmp = cwd or tempfile.mkdtemp(prefix="pl_run_")
    try:
        if os.path.isdir(DATA_DIR):
            for name in os.listdir(DATA_DIR):
                src = os.path.join(DATA_DIR, name)
                if os.path.isfile(src):
                    shutil.copy(src, os.path.join(tmp, name))
        with open(os.path.join(tmp, "main.py"), "w", encoding="utf-8") as f:
            f.write(PREAMBLE + code)

        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        start = time.monotonic()
        try:
            proc = subprocess.run(
                [python_executable(), "-I", "-X", "utf8", "main.py"],
                input=stdin_text, capture_output=True, text=True,
                encoding="utf-8", errors="replace",
                timeout=timeout, cwd=tmp, env=env,
            )
            duration = int((time.monotonic() - start) * 1000)
            stderr = _fix_line_numbers(_cap(proc.stderr or ""))
            return {
                "stdout": _cap(proc.stdout or ""),
                "stderr": stderr,
                "exit_code": proc.returncode,
                "timed_out": False,
                "friendly": errors.friendly(stderr),
                "duration_ms": duration,
            }
        except subprocess.TimeoutExpired as e:
            duration = int((time.monotonic() - start) * 1000)
            out = e.stdout or ""
            if isinstance(out, bytes):
                out = out.decode("utf-8", "replace")
            stderr = (f"Time limit ({timeout} s) exceeded - do you have "
                      "an infinite loop?")
            return {
                "stdout": _cap(out),
                "stderr": stderr,
                "exit_code": None,
                "timed_out": True,
                "friendly": errors.friendly(stderr, timed_out=True),
                "duration_ms": duration,
            }
    finally:
        if own_dir:
            shutil.rmtree(tmp, ignore_errors=True)
