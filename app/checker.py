"""Baut den test-harness und wertet die ergebnisse aus."""
import json

from . import errors, runner

SENTINEL = "__PL_RESULTS__"

# harness läuft in-process: exec'd den user-code (kommt als string rein),
# danach expr/stdout/assert tests, ergebnisse als json hinterm sentinel
_HARNESS = r'''
import ast as _ast, io as _io, json as _json, math as _math, re as _re
import contextlib as _cl

def _eq(got, exp):
    if isinstance(exp, float) or isinstance(got, float):
        try:
            return _math.isclose(float(got), float(exp), rel_tol=1e-9, abs_tol=1e-9)
        except (TypeError, ValueError):
            return False
    if isinstance(exp, (list, tuple)) and isinstance(got, (list, tuple)):
        return len(got) == len(exp) and all(_eq(g, e) for g, e in zip(got, exp))
    if isinstance(exp, dict) and isinstance(got, dict):
        return got.keys() == exp.keys() and all(_eq(got[k], exp[k]) for k in exp)
    if isinstance(exp, (set, frozenset)) and isinstance(got, (set, frozenset)):
        return got == exp
    return got == exp

def _match_lines(expected, actual):
    exp = [l.strip() for l in expected.splitlines() if l.strip()]
    act = [l.strip() for l in actual.splitlines() if l.strip()]
    it = iter(act)
    return all(any(l == e for l in it) for e in exp)

def _match_exact(expected, actual):
    def norm(t):
        lines = [l.rstrip() for l in t.replace("\r\n", "\n").split("\n")]
        while lines and not lines[-1]:
            lines.pop()
        return lines
    return norm(expected) == norm(actual)

def _match(expected, actual, mode):
    if mode == "exact":
        return _match_exact(expected, actual)
    if mode == "contains":
        return expected in actual
    if mode == "regex":
        return _re.search(expected, actual) is not None
    return _match_lines(expected, actual)

_USER_CODE = __USER_CODE__
_TESTS = __TESTS__
_STDIN = __STDIN__

_results = []
_ns = {"__name__": "__main__"}
_s.stdin = _io.StringIO(_STDIN)
try:
    exec(compile(_USER_CODE, "main.py", "exec"), _ns)
except Exception:
    import traceback as _tb
    _results.append({
        "desc": "Your code raised an error before the tests ran",
        "passed": False, "expected": "", "actual": "",
        "error": "".join(_tb.format_exc().splitlines(keepends=True)[-6:]),
    })
    print("__PL_RESULTS__")
    print(_json.dumps(_results))
    raise SystemExit(0)

for _t in _TESTS:
    _kind = _t["kind"]; _desc = _t.get("desc") or ""
    try:
        if _kind == "expr":
            _exp = _ast.literal_eval(_t["expected"])
            _got = eval(_t["expr"], _ns)
            if not _desc:
                _desc = f'{_t["expr"]} == {_t["expected"]}'
            _ok = _eq(_got, _exp)
            _err = ""
            if _ok and _t.get("expected_type"):
                _ok = type(_got).__name__ == _t["expected_type"]
                if not _ok:
                    _err = f'expected type {_t["expected_type"]}, got {type(_got).__name__}'
            _results.append({"desc": _desc, "passed": _ok,
                             "expected": repr(_exp), "actual": repr(_got),
                             "error": _err})
        elif _kind == "stdout":
            _buf = _io.StringIO()
            with _cl.redirect_stdout(_buf):
                exec(_t["code"], _ns)
            _actual = _buf.getvalue()
            if not _desc:
                _desc = f'output of {_t["code"]}'
            _ok = _match(_t["expected"], _actual, _t.get("match", "lines"))
            _results.append({"desc": _desc, "passed": _ok,
                             "expected": _t["expected"], "actual": _actual,
                             "error": ""})
        elif _kind == "assert":
            if not _desc:
                _desc = _t["code"]
            exec(_t["code"], _ns)
            _results.append({"desc": _desc, "passed": True,
                             "expected": "no error", "actual": "no error",
                             "error": ""})
    except Exception as _e:
        import traceback as _tb
        _results.append({"desc": _desc or _t.get("code", _t.get("expr", "test")),
                         "passed": False, "expected": _t.get("expected", ""),
                         "actual": "",
                         "error": "".join(_tb.format_exc().splitlines(keepends=True)[-4:])})

print("__PL_RESULTS__")
print(_json.dumps(_results))
'''


def _result(desc, passed, expected="", actual="", error=""):
    return {"desc": desc, "passed": bool(passed),
            "expected": expected, "actual": actual, "error": error}


def _auto_desc(t):
    if t.get("desc"):
        return t["desc"]
    if t["kind"] == "program":
        stdin = (t.get("stdin") or "").strip()
        if not stdin:
            return "program output (no input)"
        joined = ", ".join(stdin.splitlines())
        if len(joined) > 40:
            joined = joined[:37] + "..."
        return f"output for input: {joined}"
    if t["kind"] == "expr":
        return f'{t["expr"]} == {t["expected"]}'
    return t.get("code", "test")


def _run_program_test(t, code):
    res = runner.run(code, stdin_text=t.get("stdin", ""))
    if res["timed_out"] or res["exit_code"]:
        r = _result(_auto_desc(t), False, t.get("expected", ""),
                    res["stdout"], res["stderr"])
        fr = errors.friendly(res["stderr"], res["timed_out"])
        if fr:
            r["friendly"] = fr
        return r
    actual = res["stdout"]
    mode = t.get("match", "lines")
    ok = _match(t.get("expected", ""), actual, mode)
    return _result(_auto_desc(t), ok, t.get("expected", ""), actual, "")


def _match(expected, actual, mode):
    import re
    if mode == "exact":
        def norm(x):
            lines = [l.rstrip() for l in x.replace("\r\n", "\n").split("\n")]
            while lines and not lines[-1]:
                lines.pop()
            return lines
        return norm(expected) == norm(actual)
    if mode == "contains":
        return expected in actual
    if mode == "regex":
        return re.search(expected, actual) is not None
    exp = [l.strip() for l in expected.splitlines() if l.strip()]
    act = [l.strip() for l in actual.splitlines() if l.strip()]
    it = iter(act)
    return all(any(l == e for l in it) for e in exp)


def check(task, code):
    """Alle tests einer task gegen den user-code. gibt {passed, results} zurück."""
    tests = task.get("tests", [])
    program_tests = [t for t in tests if t["kind"] == "program"]
    inline_tests = [t for t in tests if t["kind"] != "program"]

    results = []
    for t in program_tests:
        results.append(_run_program_test(t, code))

    if inline_tests:
        stdin = next((t.get("stdin", "") for t in inline_tests if t.get("stdin")), "")
        harness = (_HARNESS
                   .replace("__USER_CODE__", json.dumps(code))
                   .replace("__TESTS__", json.dumps(inline_tests))
                   .replace("__STDIN__", json.dumps(stdin)))
        res = runner.run(harness)
        if SENTINEL in res["stdout"]:
            payload = res["stdout"].split(SENTINEL, 1)[1].strip().splitlines()[0]
            try:
                results.extend(json.loads(payload))
            except json.JSONDecodeError:
                results.append(_result("test harness", False, "", "",
                                       "Could not parse harness output"))
        else:
            msg = res["stderr"] or "no output"
            results.append(_result("test harness", False, "", "",
                                   f"Test harness did not finish: {msg}"))
    for r in results:
        if not r["passed"] and "friendly" not in r:
            fr = errors.friendly(r.get("error", ""))
            if fr:
                r["friendly"] = fr
    passed = bool(results) and all(r["passed"] for r in results)
    return {"passed": passed, "results": results}


def public_tests(task):
    """Test-beschreibungen, die ans ui dürfen (ohne expectations)."""
    return [{"desc": _auto_desc(t)} for t in task.get("tests", [])]
