"""Checkt den kurs-inhalt: struktur + jede solution besteht ihre tests."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import checker
from app.content import iter_tasks, validate_structure


# starter darf kaputt sein, ist ein fix-the-bugs task
STARTER_MAY_BE_BROKEN = {"ch00-task-4"}


def main():
    errors = validate_structure()
    for e in errors:
        print(f"STRUCTURE  {e}")

    starter_failed = 0
    starter_total = 0
    for ch, task in iter_tasks():
        starter_total += 1
        if task["id"] in STARTER_MAY_BE_BROKEN:
            continue
        try:
            compile(task.get("starter") or "", task["id"], "exec")
        except SyntaxError as e:
            starter_failed += 1
            print(f"STARTER FAIL  {task['id']}: {e}")

    failed = 0
    total = 0
    for ch, task in iter_tasks():
        total += 1
        result = checker.check(task, task["solution"])
        if not result["passed"]:
            failed += 1
            print(f"FAIL  {task['id']} ({task['title']})")
            for r in result["results"]:
                if not r["passed"]:
                    print(f"   - {r['desc']}")
                    print(f"     expected: {r['expected']!r}")
                    print(f"     actual:   {r['actual']!r}")
                    if r["error"]:
                        print(f"     error:    {r['error'][:400]}")
        else:
            print(f"ok    {task['id']}")

    print(f"\n{total - failed}/{total} task solutions pass, "
          f"{starter_total - starter_failed}/{starter_total} starters compile, "
          f"{len(errors)} structure errors")
    sys.exit(1 if (failed or errors or starter_failed) else 0)


if __name__ == "__main__":
    main()
