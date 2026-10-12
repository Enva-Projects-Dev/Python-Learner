"""Lesson-codeblöcke checken: jeder ```python-block muss standalone laufen."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import runner
from app.content import CHAPTERS

BLOCK_RE = re.compile(r"```python\n(.*?)```", re.S)
DEF_RE = re.compile(r"(?:def|class)\s+(\w+)|^(\w+)\s*=", re.M)

# wird an blöcke gefüttert die input() aufrufen, damit kein EOFError kommt
STDIN = "7\n3\nhello\n5\n2\n1\n4\n6\n8\n9\n10\nyes\n"


def defined_names(code):
    names = set()
    for m in DEF_RE.finditer(code):
        names.add(m.group(1) or m.group(2))
    return names


def main():
    failures = 0
    total = 0
    for ch in CHAPTERS:
        for item in ch["items"]:
            if item["type"] != "lesson":
                continue
            blocks = BLOCK_RE.findall(item["body"])
            for i, code in enumerate(blocks):
                total += 1
                label = f"{item['id']} block {i}"
                stdin = STDIN if "input(" in code else ""
                res = runner.run(code, stdin_text=stdin)
                if res["timed_out"]:
                    failures += 1
                    print(f"FAIL  {label}: timed out")
                    continue
                if res["exit_code"] != 0:
                    failures += 1
                    tail = res["stderr"].strip().splitlines()
                    print(f"FAIL  {label}: exit {res['exit_code']}")
                    print("      " + "\n      ".join(tail[-4:]))
                    continue
                silent = not res["stdout"].strip()
                interactive = "print" in code or "input(" in code
                if silent and not interactive:
                    # nur ok wenn ein SPÄTERER block einen der namen wieder benutzt
                    reused = any(
                        defined_names(code) & set(re.findall(r"\w+", b))
                        for b in blocks[i + 1:]
                    )
                    if not reused:
                        failures += 1
                        print(f"FAIL  {label}: silent block (no output, "
                              "no print/input, defines nothing reused)")
    # task-"example"-blöcke laufen genauso standalone
    ex_total = 0
    for ch in CHAPTERS:
        for item in ch["items"]:
            ex = item.get("example")
            if not ex:
                continue
            for i, code in enumerate(BLOCK_RE.findall(ex)):
                ex_total += 1
                total += 1
                label = f"{item['id']} example block {i}"
                stdin = STDIN if "input(" in code else ""
                res = runner.run(code, stdin_text=stdin)
                if res["timed_out"]:
                    failures += 1
                    print(f"FAIL  {label}: timed out")
                    continue
                if res["exit_code"] != 0:
                    failures += 1
                    tail = res["stderr"].strip().splitlines()
                    print(f"FAIL  {label}: exit {res['exit_code']}")
                    print("      " + "\n      ".join(tail[-4:]))
                    continue
                silent = not res["stdout"].strip()
                has_io = "print" in code or "input(" in code
                defines = "def " in code or "class " in code
                if silent and not has_io and not defines:
                    failures += 1
                    print(f"FAIL  {label}: silent example "
                          "(no output, defines nothing)")

    print(f"\n{total - failures}/{total} blocks pass "
          f"({ex_total} of them task examples), {failures} failures")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
