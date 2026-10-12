"""Kapitel 9 - Module & Pakete."""

CHAPTER = {
    "id": "ch09",
    "number": 9,
    "title": "Modules & Packages",
    "summary": "Python's toolbox: borrowing ready-made code with import.",
    "items": [
        {
            "id": "ch09-lesson",
            "type": "lesson",
            "title": "Modules: borrowing tools",
            "body": r"""
You don't have to write everything yourself - Python ships with
hundreds of ready-made toolboxes. A **module** is just a Python file
full of tools (functions, values) you can borrow with `import`.

> **Think of it like...** borrowing a toolbox from the library. `math`,
> `random`, `datetime` are boxes on the shelf - you just have to check
> them out.

```python
import math                 # borrow the whole box: math.sqrt(9)
from math import sqrt       # take just one tool: sqrt(9)
from math import pi as PI   # take it and rename it

print(math.floor(3.7), math.ceil(3.7), math.gcd(12, 18))
print(math.pi, PI)
```

> **What happens here**
>
> - line 1: `import math` gives you the whole box - every tool needs
>   `math.` in front
> - line 2: `from math import sqrt` borrows only that tool - no prefix
> - line 3: `as PI` renames the borrowed thing to your own name
> - line 5: floor drops to the lower integer (3), ceil rounds up (4),
>   gcd is the biggest shared divisor (6)

## The standard library's greatest hits

```python
import random
random.seed(7)                  # fixes the dice sequence
print(random.randint(1, 6))     # a die roll
print(random.choice(["a", "b", "c"]))
print(random.random())          # float in [0.0, 1.0)

import datetime
d = datetime.date(2021, 9, 2)
print(d.year, d.month, d.day)
print(d.weekday())              # 0 = Monday ... 6 = Sunday
print(d.strftime("%d.%m.%Y"))   # '02.09.2021'
```

> **What happens here**
>
> - line 2: `seed` sets the random machine to a known state - same
>   seed, same "random" numbers every run (great for tests!)
> - line 3-5: randint picks a whole number 1-6, choice picks from a
>   list, random() gives a decimal from 0.0 up to (not including) 1.0
> - line 8: `datetime.date` builds a calendar date object
> - line 10: `weekday()` returns a number - 0 is Monday

> **Think of it like...** `random.seed` is like agreeing on the same
> shuffled deck - whoever uses seed 7 gets the exact same cards.

## __name__ == "__main__"

A file can be a program *and* a toolbox for others. This trick runs
code only when the file is started directly, not when it's imported:

```python
def square(x):
    return x * x

if __name__ == "__main__":
    print(square(5))    # demo code, skipped on import
```

> **What happens here** - `__name__` is a built-in variable: it's
> `"__main__"` when you run the file yourself, but the file's own name
> when someone imports it. The `if` hides demo code from importers.

## Packages

A **package** is a folder full of modules - a whole toolbox shelf. A
file named `__init__.py` marks the folder as a package:

```
mypackage/
    __init__.py
    helpers.py      # -> import mypackage.helpers
```

> **Watch out** - naming your own file `random.py` or `math.py` shadows
> the real module and breaks your imports in confusing ways.

## Try it yourself

- `import math` and print `math.factorial(5)`.
- `random.seed(1)` then print two `randint(1, 6)` rolls - run twice,
>  same result?

## Key words

| Word | Meaning |
|---|---|
| module | a Python file you can import |
| import / from ... import | borrow the box / borrow one tool |
| `as` | rename an import |
| standard library | the modules that ship with Python |
| random.seed | fixes the random sequence |
| `__name__` | file's name - `"__main__"` when run directly |
| package | a folder of modules with `__init__.py` |
""",
        },
        {
            "id": "ch09-quiz-1",
            "type": "quiz",
            "title": "Import forms",
            "question": "After `from math import sqrt`, how do you compute √16?",
            "options": ["math.sqrt(16)", "sqrt(16)", "import sqrt(16)", "math().sqrt(16)"],
            "answer": 1,
            "explanation": "The from-import puts `sqrt` directly into your code - call it bare. `math.sqrt(16)` would need `import math` instead.",
        },
        {
            "id": "ch09-quiz-2",
            "type": "quiz",
            "title": "__main__",
            "question": "Code under `if __name__ == '__main__':` runs when...",
            "options": ["the module is imported", "the file is executed directly", "always", "never"],
            "answer": 1,
            "explanation": "Importing sets __name__ to the module's name; only direct execution makes it '__main__'. That's how demos don't fire on import.",
        },
        {
            "id": "ch09-quiz-3",
            "type": "quiz",
            "title": "random.seed",
            "question": "Why call `random.seed(7)` before generating numbers?",
            "options": ["It makes them truly random", "It makes the sequence reproducible", "It is faster", "randint requires it"],
            "answer": 1,
            "explanation": "Seeding locks the pseudo-random script - same seed, same numbers. Essential for testing dice games.",
        },
        {
            "id": "ch09-quiz-4",
            "type": "quiz",
            "title": "datetime",
            "question": "`datetime.date(2021, 9, 2).weekday()` returns what for that Thursday?",
            "options": ["4", "3", "2", "'Thursday'"],
            "answer": 1,
            "explanation": "weekday() counts 0=Monday ... 6=Sunday, so Thursday is 3. It returns a number, not the name.",
        },
        {
            "id": "ch09-warm-1",
            "type": "task",
            "title": "Square root",
            "difficulty": 1,
            "plain": "Borrow math's square-root tool and use it.",
            "instructions": r"""
Print the square root of 144 using `math.sqrt` (import `math` first).

Expected output: `12.0`
""",
            "starter": """# TODO: import math, then print math.sqrt(144)
""",
            "hints": [
                "`import math` on the first line.",
                "`print(math.sqrt(144))`.",
                "sqrt returns a float - 12.0, not 12.",
            ],
            "solution": """import math

print(math.sqrt(144))""",
            "explanation": "`import math` borrows the toolbox; `math.sqrt(144)` uses the tool with the `math.` prefix. It returns 12.0 - sqrt always gives a float.\n\nWhat you learned: `import module` then `module.tool(...)`.",
            "tests": [
                {"kind": "program", "expected": "12.0", "match": "exact"},
            ],
        },
        {
            "id": "ch09-warm-2",
            "type": "task",
            "title": "Seeded coin flip",
            "difficulty": 1,
            "plain": "Flip a seeded coin - the same flip every time.",
            "instructions": r"""
Seed `random` with `7`, then use `random.choice` on `["heads",
"tails"]` and print the result. Seeded, so the answer is fixed!

Expected output: `tails`
""",
            "starter": """import random

# TODO: seed(7), then print random.choice(["heads", "tails"])
""",
            "hints": [
                "`random.seed(7)` first.",
                "`random.choice(list)` picks one element.",
                "Seed 7 picks 'tails' here - try other seeds after checking.",
            ],
            "solution": """import random

random.seed(7)
print(random.choice(["heads", "tails"]))""",
            "explanation": "`random.choice` picks one element - with seed 7 the pick is scripted and always 'tails'. Without a seed each run could differ, which is exactly why tests seed first.\n\nWhat you learned: `random.choice` + `seed` = reproducible randomness.",
            "tests": [
                {"kind": "program", "expected": "tails", "match": "exact"},
            ],
        },
        {
            "id": "ch09-task-1",
            "type": "task",
            "title": "math module: hypotenuse & circle",
            "difficulty": 1,
            "plain": "Two tiny functions powered by the math toolbox.",
            "instructions": r"""
Write two functions using `math`:

- `hypotenuse(a, b)` - hypotenuse of a right triangle (use
  `math.hypot`)
- `circle_area(r)` - circle area (use `math.pi`)

```python
hypotenuse(3, 4)   # 5.0
circle_area(1)     # 3.141592653589793
```
""",
            "starter": """import math

def hypotenuse(a, b):
    # TODO
    pass

def circle_area(r):
    # TODO
    pass
""",
            "hints": [
                "`math.hypot(a, b)` computes √(a²+b²) for you.",
                "Area = `math.pi * r ** 2`.",
                "`return`, not `print`.",
            ],
            "solution": """import math

def hypotenuse(a, b):
    return math.hypot(a, b)

def circle_area(r):
    return math.pi * r ** 2
""",
            "explanation": "Both functions are one return each: `math.hypot` does the Pythagoras math (safer and shorter than sqrt(a²+b²)), and `math.pi` supplies π to full precision.\n\nWhat you learned: the standard library already solved common math - reach for it first.",
            "tests": [
                {"kind": "expr", "expr": "hypotenuse(3, 4)", "expected": "5.0"},
                {"kind": "expr", "expr": "hypotenuse(0, 0)", "expected": "0.0"},
                {"kind": "expr", "expr": "circle_area(1)", "expected": "3.141592653589793"},
                {"kind": "expr", "expr": "circle_area(10)", "expected": "314.1592653589793"},
            ],
        },
        {
            "id": "ch09-task-2",
            "type": "task",
            "title": "random module: seeded dice",
            "difficulty": 1,
            "plain": "Roll a die n times - but on a fixed script so tests can check.",
            "instructions": r"""
Write `roll_dice(n, seed_value)`:

1. call `random.seed(seed_value)` (makes it deterministic)
2. roll `n` times with `random.randint(1, 6)`
3. return the rolls as a **list**

```python
roll_dice(3, 42)   # [6, 1, 1]
```
""",
            "starter": """import random

def roll_dice(n, seed_value):
    # TODO: seed, roll n times, return the list
    pass
""",
            "hints": [
                "Seed first, then roll.",
                "A comprehension collects rolls: `[random.randint(1, 6) for _ in range(n)]`.",
                "`_` as the loop variable means 'I don't need the counter'.",
            ],
            "solution": """import random

def roll_dice(n, seed_value):
    random.seed(seed_value)
    return [random.randint(1, 6) for _ in range(n)]
""",
            "explanation": "Seeding inside the function makes every call with the same seed_value follow the same script - that's why `roll_dice(3, 42)` is always `[6, 1, 1]`. The comprehension collects n rolls into a list.\n\nWhat you learned: seeding inside a function makes its randomness testable.",
            "tests": [
                {"kind": "expr", "expr": "roll_dice(3, 42)", "expected": "[6, 1, 1]"},
                {"kind": "expr", "expr": "roll_dice(5, 7)", "expected": "[3, 2, 4, 6, 1]"},
                {"kind": "assert",
                 "code": "assert roll_dice(4, 1) == roll_dice(4, 1)",
                 "desc": "same seed produces the same rolls"},
            ],
        },
        {
            "id": "ch09-task-3",
            "type": "task",
            "title": "datetime: fixed dates",
            "difficulty": 2,
            "plain": "Ask the calendar: which weekday, how many days apart.",
            "instructions": r"""
Write two functions using `datetime.date`:

- `weekday_name(year, month, day)` - English weekday name.
  `date.weekday()` gives `0`-`6`; map it through a name list.
- `days_between(y1, m1, d1, y2, m2, d2)` - days between the two dates
  (subtract two `date` objects, return `.days`).

```python
weekday_name(2021, 9, 2)                 # 'Thursday'
days_between(2021, 1, 1, 2021, 12, 31)   # 364
```
""",
            "starter": """import datetime

def weekday_name(year, month, day):
    # TODO
    pass

def days_between(y1, m1, d1, y2, m2, d2):
    # TODO
    pass
""",
            "hints": [
                "Names list `['Monday', ..., 'Sunday']` indexed by `.weekday()`.",
                "`date2 - date1` gives a `timedelta` - its `.days` is the answer.",
                "Build two `datetime.date(...)` objects inside `days_between`.",
            ],
            "solution": """import datetime

def weekday_name(year, month, day):
    names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
             'Friday', 'Saturday', 'Sunday']
    return names[datetime.date(year, month, day).weekday()]

def days_between(y1, m1, d1, y2, m2, d2):
    a = datetime.date(y1, m1, d1)
    b = datetime.date(y2, m2, d2)
    return (b - a).days
""",
            "explanation": "`weekday()` returns an index 0-6 - feeding it into a names list turns the number into 'Thursday'. Subtracting dates yields a `timedelta` object whose `.days` is the gap, no manual month-counting needed.\n\nWhat you learned: date arithmetic is built in - subtract dates, read `.days`.",
            "tests": [
                {"kind": "expr", "expr": "weekday_name(2021, 9, 2)", "expected": "'Thursday'"},
                {"kind": "expr", "expr": "weekday_name(2000, 1, 1)", "expected": "'Saturday'"},
                {"kind": "expr", "expr": "days_between(2021, 1, 1, 2021, 12, 31)", "expected": "364"},
                {"kind": "expr", "expr": "days_between(2020, 1, 1, 2020, 1, 1)", "expected": "0"},
            ],
        },
        {
            "id": "ch09-boss",
            "type": "task",
            "title": "Dice tournament",
            "difficulty": 3,
            "boss": True,
            "plain": "A seeded dice match: roll, total, and crown the winner - all from the toolbox.",
            "instructions": r"""
**BOSS MISSION - run a tiny dice tournament.**

Write `tournament(players, rounds, seed_value)`:

- `players` is a list of names; seed `random` once with `seed_value`.
- Each player rolls `random.randint(1, 6)` `rounds` times **in order**
  (all of player 1's rolls, then player 2's, ...).
- Return a list of `"<name>: <total>"` strings, sorted by total,
  **highest first** (ties keep the players' order).

```python
tournament(["Ada", "Ben"], 2, 42)   # ['Ada: 7', 'Ben: 7']  (a tie - first player stays first)
```
""",
            "starter": """import random

def tournament(players, rounds, seed_value):
    # TODO: seed, roll per player, return sorted "name: total" lines
    pass
""",
            "example": """A seeded mini-tournament:

```python
import random
random.seed(3)
rolls = [random.randint(1, 6) for _ in range(3)]
print(rolls, "sum:", sum(rolls))
```
""",

            "hints": [
                "Seed once, then `for name in players:` with an inner `for _ in range(rounds):` summing `randint(1, 6)` - or `sum(...)`.",
                "Collect `(name, total)` pairs first, sort, then format.",
                "`sorted(pairs, key=lambda p: p[1], reverse=True)` - Python's sort is stable, so ties keep order.",
            ],
            "solution": """import random

def tournament(players, rounds, seed_value):
    random.seed(seed_value)
    pairs = []
    for name in players:
        total = sum(random.randint(1, 6) for _ in range(rounds))
        pairs.append((name, total))
    pairs = sorted(pairs, key=lambda p: p[1], reverse=True)
    return [f"{name}: {total}" for name, total in pairs]
""",
            "explanation": "One seed at the top scripts the whole match. The nested structure - outer loop per player, inner `sum` of `rounds` randint calls - fixes the roll order, so results are reproducible. `sorted` with `key=lambda p: p[1]` ranks by total, `reverse=True` puts the winner first, and Python's stable sort keeps ties in original order.\n\nWhat you learned: `key=` + `reverse=True` sorts by any rule you choose.",
            "tests": [
                {"kind": "expr", "expr": "tournament(['Ada', 'Ben'], 2, 42)",
                 "expected": "['Ada: 7', 'Ben: 7']"},
                {"kind": "expr", "expr": "tournament(['A', 'B', 'C'], 3, 1)",
                 "expected": "['C: 14', 'A: 8', 'B: 8']"},
            ],
        },
    ],
}
