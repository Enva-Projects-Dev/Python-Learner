"""Audit: stimmt das beispiel-output in den instructions mit dem überein,
was die solution bei den test-inputs wirklich ausgibt?

Für jeden task mit program-tests: solution mit stdin von test 1 laufen
lassen, dann jeden fenced block (ohne ```python) aus den instructions
gegen den output prüfen. Alles was nicht als ganzes drin ist -> melden.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import runner
from app.content import iter_tasks

FENCE = re.compile(r"```([a-zA-Z]*)\n(.*?)```", re.S)

# bewusst nur skizzenhafte blöcke - die fenced examples sind hier
# absichtlich kein 1:1-output (mit grund, sonst wandert der task raus)
IGNORE = {
    "ch02-task-7": "zeigt die rechnung, nicht den programm-output (als 'Example' gelabelt)",
    "ch04-task-1": "erster block = dateiformat, zweiter mit '...' abgekürzt",
    "ch04-boss":   "output bewusst mit '...' abgekürzt",
    "ch06-task-1": "'input: X -> output: Y'-skizze (als 'Example runs' gelabelt)",
    "ch10-warm-2": "'input: ... -> ...'-skizze (als 'Examples' gelabelt)",
    "ch10-boss":   "'input: ... -> ...'-skizze (als 'Examples' gelabelt)",
    "ch18-task-1": "zeigt das dateiformat von Kunden.txt, nicht den output",
}


def norm(s):
    return "\n".join(l.rstrip() for l in s.replace("\r\n", "\n").strip().split("\n"))


def main():
    flagged = 0
    ignored = 0
    for ch, task in iter_tasks():
        tests = [t for t in task.get("tests", []) if t["kind"] == "program"]
        blocks = [norm(b) for lang, b in FENCE.findall(task["instructions"])
                  if lang.lower() not in ("python", "py") and b.strip()]
        if not tests or not blocks:
            continue
        outputs = []
        for t in tests:
            res = runner.run(task["solution"], stdin_text=t.get("stdin", ""))
            outputs.append(norm(res["stdout"]))
        bad = [b for b in blocks if not any(b in o for o in outputs)]
        if not bad:
            continue
        if task["id"] in IGNORE:
            ignored += 1
            print(f"-- {task['id']} ignored ({IGNORE[task['id']]})")
            continue
        flagged += 1
        print(f"\n== {task['id']}  ({task['title']})")
        for b in bad:
            print("  instructions show:")
            for l in b.splitlines():
                print(f"    | {l}")
        print("  solution actually prints (test 1 input "
              f"{(tests[0].get('stdin') or '').strip()!r}):")
        for l in outputs[0].splitlines():
            print(f"    > {l}")
    print(f"\n{flagged} tasks where an instruction example is not in the "
          f"solution output ({ignored} ignored)")
    if flagged:
        sys.exit(1)


if __name__ == "__main__":
    main()
