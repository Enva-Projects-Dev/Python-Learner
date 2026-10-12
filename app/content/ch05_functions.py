"""Kapitel 5 - Funktionen."""

CHAPTER = {
    "id": "ch05",
    "number": 5,
    "title": "Functions",
    "summary": "Named recipes: define once, call anywhere - inputs in, answers out.",
    "items": [
        {
            "id": "ch05-lesson",
            "type": "lesson",
            "title": "Defining and calling functions",
            "body": r"""
## A function is a named recipe

A **function** packs code under a name so you can reuse it - like
writing a recipe once and cooking it as often as you like.

```python
def square(x):
    return x * x

print(square(5))   # 25 - the recipe runs with x = 5
```

> **What happens here**
>
> - `def` + name + `(inputs)` declares the recipe
> - `return` hands the finished result back to whoever called
> - `square(5)` calls it - x becomes 5 inside

> **Watch out** - a function without `return` gives back `None`
> (Python's "nothing"). Calculating `x * 2` without returning it
> throws the answer away!

## Docstrings: the recipe's sticky note

A string right under `def` explains the function - readable via
`help()`:

```python
def cube(x):
    '''Return x raised to the third power.'''
    return x ** 3

print(cube(3))         # 27
print(cube.__doc__)    # shows the explanation string
```

> **What happens here**
>
> - line 2: a string sitting right under `def` is a **docstring** -
>   the function's built-in help text (triple single quotes work the
>   same as triple double quotes)
> - line 5: the function runs normally -> 27
> - line 6: `__doc__` is where the docstring lives - `help(cube)`
>   would show the same text

## Arguments with defaults

You can pre-fill ingredients - callers may override them:

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Anna"))                      # Hello, Anna!
print(greet("Tom", "Hi"))                 # positional: Hi, Tom!
print(greet(greeting="Hey", name="Ute"))  # keyword: any order
```

## Returning several things at once

`return a, b` hands back a **tuple** - unpack it right at the call:

```python
def min_max(values):
    return min(values), max(values)

lo, hi = min_max([3, 1, 4, 1, 5])
print(lo, hi)              # 1 5
```

Python even has one built in: `divmod` gives quotient and remainder
together:

```python
q, r = divmod(17, 5)
print(q, r)     # 3 2
```

## Letters are secretly numbers: ord and chr

Inside the computer every letter is stored as a number. `ord` reveals
it, `chr` turns a number back into a letter:

```python
print(ord('A'))            # 65
print(chr(65))             # 'A'
print(chr(ord('A') + 1))   # 'B' - the next letter!
```

> **What happens here**
>
> - `ord('A')` gives the code of the letter A -> 65
> - `chr(66)` gives the letter for code 66 -> 'B'
> - `ord('A') + pos` is how you walk through the alphabet

## Try it yourself

- Write `def double(x)` that returns `x * 2`, then print `double(21)`.
- Call `greet` from the example with only your name - then with both.

## Key words

| Word | Meaning |
|---|---|
| def | declares a function (recipe) |
| argument / parameter | the input value / its name inside |
| return | hands a result back (missing -> None) |
| default argument | a pre-filled input you may override |
| docstring | a description string under `def` |
| divmod | built-in: quotient + remainder as a tuple |
""",
        },
        {
            "id": "ch05-quiz-1",
            "type": "quiz",
            "title": "return vs print",
            "question": "`def f(x): x * 2` - what does `print(f(3))` show?",
            "options": ["6", "None", "Error", "3"],
            "answer": 1,
            "explanation": "Computing `x * 2` throws the 6 away - without `return` the function hands back None. print then shows 'None'.",
        },
        {
            "id": "ch05-quiz-2",
            "type": "quiz",
            "title": "Default arguments",
            "question": "Given `def f(a, b=2): return a * b`, what is `f(3)`?",
            "options": ["Error: missing argument", "6", "3", "5"],
            "answer": 1,
            "explanation": "b is pre-filled with 2, so f(3) is 3 * 2 = 6. A default only kicks in when the caller gives nothing.",
        },
        {
            "id": "ch05-quiz-3",
            "type": "quiz",
            "title": "divmod",
            "question": "What does `divmod(17, 5)` return?",
            "options": ["(3, 2)", "(2, 3)", "3.4", "(3.4, 0)"],
            "answer": 0,
            "explanation": "divmod returns a tuple: (quotient, remainder) = (17 // 5, 17 % 5) = (3, 2). Order matters - quotient first.",
        },
        {
            "id": "ch05-quiz-4",
            "type": "quiz",
            "title": "Unpacking returns",
            "question": "`def f(): return 1, 2` - what does `a, b = f()` do?",
            "options": ["error", "a=1, b=2", "a=(1,2), b=(1,2)", "b=1, a=2"],
            "answer": 1,
            "explanation": "The tuple (1, 2) gets unpacked left-to-right: a=1, b=2 - same as tuple unpacking from chapter 3.",
        },
        {
            "id": "ch05-warm-1",
            "type": "task",
            "title": "Double it",
            "difficulty": 1,
            "plain": "Write your first function: it doubles a number.",
            "instructions": r"""
Write a function `double(x)` that **returns** `x * 2`, then print
`double(21)`.

Expected output: `42`
""",
            "starter": """# TODO: def double(x): ...

print(double(21))
""",
            "example": """Try the same trick on a different problem:

```python
def cheer():
    return "Go team!"

print(cheer())
```
""",

            "hints": [
                "`def double(x):` starts the recipe.",
                "Inside: `return x * 2`.",
                "The test call at the bottom prints the returned value.",
            ],
            "solution": """def double(x):
    return x * 2


print(double(21))""",
            "explanation": "`def` names the recipe and `x` is its ingredient. `return x * 2` hands back the doubled value, which the print at the call site displays - 42.\n\nWhat you learned: `def` + `return` is the smallest useful function.",
            "tests": [
                {"kind": "program", "expected": "42", "match": "exact"},
                {"kind": "expr", "expr": "double(5)", "expected": "10"},
            ],
        },
        {
            "id": "ch05-warm-2",
            "type": "task",
            "title": "Greeter with a default",
            "difficulty": 1,
            "plain": "A greeting function where the greeting is pre-filled.",
            "instructions": r"""
Write `greet(name, greeting="Hi")` that returns `f"{greeting}, {name}!"`,
then print `greet("Ada")`.

Expected output: `Hi, Ada!`
""",
            "starter": """# TODO: def greet(name, greeting="Hi"): ...

print(greet("Ada"))
""",
            "example": """Try the same trick on a different problem:

```python
def add(a, b):
    return a + b

print(add(3, 4))
```
""",

            "hints": [
                "The parameter list can pre-fill values: `greeting=\"Hi\"`.",
                "Body: one f-string, returned.",
                "`return f\"{greeting}, {name}!\"`.",
            ],
            "solution": """def greet(name, greeting="Hi"):
    return f"{greeting}, {name}!"


print(greet("Ada"))""",
            "explanation": "The default `greeting=\"Hi\"` means callers can pass just a name. The f-string assembles the sentence and `return` hands it to the print.\n\nWhat you learned: default arguments make parameters optional.",
            "tests": [
                {"kind": "program", "expected": "Hi, Ada!", "match": "exact"},
                {"kind": "expr", "expr": "greet('Tom', 'Hey')", "expected": "'Hey, Tom!'"},
            ],
        },
        {
            "id": "ch05-warm-3",
            "type": "task",
            "title": "Stars",
            "difficulty": 1,
            "plain": "A function that returns n stars.",
            "instructions": "Write a function `stars(n)` that returns a string of `n` asterisks. `stars(5)` gives `*****`. Print `stars(5)` to prove it.",
            "starter": """def stars(n):
    # TODO: return "*" multiplied by n
    pass

print(stars(5))
""",
            "example": """A twin function with dashes:

```python
def dashes(n):
    return "-" * n

print(dashes(4))
```
""",
            "hints": [
                "`\"*\" * n` repeats the star n times.",
                "Use `return`, not `print` - the caller decides what to do.",
                "`print(stars(5))` shows `*****`.",
            ],
            "solution": """def stars(n):
    return "*" * n

print(stars(5))""",
            "explanation": "Multiplying a string repeats it, so \"*\" * n builds the whole line at once. The function returns it - printing is the caller's job. This little recipe shows up again inside the square-drawing task.",
            "tests": [
                {"kind": "program", "expected": "*****"},
            ],
        },
        {
            "id": "ch05-task-1",
            "type": "task",
            "title": "print_cubed",
            "difficulty": 1,
            "plain": "A function that prints x cubed - no return needed.",
            "instructions": r"""
Write `print_cubed(x)` that computes `x ** 3` and **prints** it (the
function itself does not return anything).

```python
print_cubed(4)   # prints 64
```
""",
            "starter": """def print_cubed(x):
    # TODO: print x ** 3  (print, not return - this one shows the answer)
    pass

# test call:
print_cubed(4)
""",
            "example": """Printing inside a function:

```python
def show_square(n):
    print(n * n)

show_square(5)
```
""",

            "hints": [
                "`def print_cubed(x):` and inside `print(...)`.",
                "The power operator is `**`.",
                "Print inside the function - the call stays bare.",
            ],
            "solution": """def print_cubed(x):
    print(x ** 3)


print_cubed(4)
""",
            "explanation": "This function shows its answer instead of returning it: `print` inside the body does the displaying, so the call `print_cubed(4)` prints 64 all by itself.\n\nWhat you learned: functions can *do* something (print) or *give back* something (return) - or both.",
            "tests": [
                {"kind": "program", "expected": "64", "match": "exact"},
                {"kind": "stdout", "code": "print_cubed(3)", "expected": "27", "match": "exact"},
            ],
        },
        {
            "id": "ch05-task-2",
            "type": "task",
            "title": "cubed (return value)",
            "difficulty": 1,
            "plain": "Same cube - but this time return it, don't print.",
            "instructions": r"""
Write `cubed(x)` that **returns** `x ** 3` (unlike the previous task it
must not print).

Test data - `cubed(x)` must return the second value for each pair:

```
(-2, -8) (-1.5, -3.375) (-1, -1) (-0.5, -0.125) (0, 0)
(0.5, 0.125) (1, 1) (1.5, 3.375) (2, 8) (2.5, 15.625) (3, 27)
```
""",
            "starter": """def cubed(x):
    # TODO: return x ** 3  (return, not print - this one hands it back)
    pass

# test call:
print(cubed(4))
""",
            "example": """Returning from a function:

```python
def square(n):
    return n * n

print(square(5))
```
""",

            "hints": [
                "`return`, not `print` - the tests call your function and check what comes back.",
                "`return x ** 3`.",
                "Negatives and decimals work automatically - `**` handles them.",
            ],
            "solution": """def cubed(x):
    return x ** 3
""",
            "explanation": "`x ** 3` computes the cube and `return` hands it back - the tests call `cubed(2.5)` and compare against 15.625. Returning (not printing) is what lets other code use the result.\n\nWhat you learned: `return` values can flow into variables, other calls, and tests.",
            "tests": [
                {"kind": "expr", "expr": "cubed(-2)", "expected": "-8"},
                {"kind": "expr", "expr": "cubed(-1.5)", "expected": "-3.375"},
                {"kind": "expr", "expr": "cubed(-0.5)", "expected": "-0.125"},
                {"kind": "expr", "expr": "cubed(0)", "expected": "0"},
                {"kind": "expr", "expr": "cubed(2.5)", "expected": "15.625"},
                {"kind": "expr", "expr": "cubed(3)", "expected": "27"},
            ],
        },
        {
            "id": "ch05-task-3",
            "type": "task",
            "title": "full_name",
            "difficulty": 2,
            "plain": "Assemble a full name - with or without a middle name.",
            "instructions": r"""
Write `full_name(first, last, middle=None)` returning the complete
name as one string, parts separated by spaces. `middle` is optional.

```python
full_name("Guido", "van Rossum")                        # 'Guido van Rossum'
full_name("Wolfgang", "Mozart", middle="Amadeus")       # 'Wolfgang Amadeus Mozart'
```
""",
            "starter": """def full_name(first, last, middle=None):
    parts = [first]
    # TODO: if middle is not None, append it to parts
    parts.append(last)
    return " ".join(parts)
""",
            "example": """An optional greeting part:

```python
def greet(name, title=None):
    if title:
        return f"Hi {title} {name}"
    return f"Hi {name}"

print(greet("Ada"), greet("Ada", "Dr."))
```
""",

            "hints": [
                "The default `middle=None` detects 'no middle name'.",
                "Collect parts in a list, then `' '.join(parts)`.",
                "Or: `if middle is None: return f'{first} {last}'` else include it.",
            ],
            "solution": """def full_name(first, last, middle=None):
    parts = [first]
    if middle is not None:
        parts.append(middle)
    parts.append(last)
    return " ".join(parts)
""",
            "explanation": "The parts list always holds first and last; the middle name is inserted only when the caller gave one (`middle is not None`). `' '.join(parts)` glues the pieces with single spaces - no stray double space when the middle is missing.\n\nWhat you learned: `join` is the clean way to assemble variable-length text.",
            "tests": [
                {"kind": "expr", "expr": "full_name('Guido', 'van Rossum')",
                 "expected": "'Guido van Rossum'"},
                {"kind": "expr", "expr": "full_name('Wolfgang', 'Mozart', middle='Amadeus')",
                 "expected": "'Wolfgang Amadeus Mozart'"},
                {"kind": "expr", "expr": "full_name('Ada', 'Lovelace', 'Augusta')",
                 "expected": "'Ada Augusta Lovelace'"},
            ],
        },
        {
            "id": "ch05-task-4",
            "type": "task",
            "title": "square(n, inner, border)",
            "difficulty": 2,
            "plain": "Draw a hollow square with two changeable characters.",
            "instructions": r"""
Write `square(n, inner=" ", border="*")` that prints a hollow square
of side `n`:

- First and last row: `n` copies of `border`, each followed by a
  space (e.g. `* * * `).
- Each of the `n - 2` middle rows: one `border`, then `2*n - 3` copies
  of `inner`, then one `border` (`*   *` for n = 3).
- `inner` and `border` are keyword arguments with the defaults shown.

```python
square(3)
# * * *
# *   *
# * * *

square(4, inner="-", border="#")
# # # #
#-----#
#-----#
# # # #
```
""",
            "starter": """def square(n, inner=" ", border="*"):
    print((border + " ") * n)          # top edge
    for _ in range(n - 2):
        pass    # TODO: print border + inner * (2 * n - 3) + border
    if n > 1:
        pass    # TODO: print the bottom edge - same as the top
""",
            "example": """One line of the square:

```python
def row(n, edge="o", fill="."):
    return edge + fill * (n - 2) + edge

print(row(6))
```
""",

            "hints": [
                "Top/bottom row: `print((border + ' ') * n)` - multiplication repeats the string.",
                "Middle row: `border + inner * (2 * n - 3) + border`.",
                "`for _ in range(n - 2)` prints the middle rows.",
            ],
            "solution": """def square(n, inner=" ", border="*"):
    print((border + " ") * n)
    for _ in range(n - 2):
        print(border + inner * (2 * n - 3) + border)
    if n > 1:
        print((border + " ") * n)


square(3)
square(4, inner="-", border="#")
""",
            "explanation": "String multiplication builds each row: `(border + ' ') * n` for the frame edges, and `border + inner * (2*n - 3) + border` for the hollow middle - that formula keeps the width matching the spaced top row. The loop runs n-2 times, and the `if n > 1` prevents a double bottom row for tiny squares.\n\nWhat you learned: `str * n` repeats text - handy for drawing.",
            "tests": [
                {"kind": "stdout", "code": "square(3)",
                 "expected": "* * *\n*   *\n* * *", "match": "exact"},
                {"kind": "stdout", "code": "square(4, inner='-', border='#')",
                 "expected": "# # # #\n#-----#\n#-----#\n# # # #", "match": "exact"},
                {"kind": "stdout", "code": "square(6, inner='.', border='o')",
                 "expected": "o o o o o o\no.........o\no.........o\no.........o\no.........o\no o o o o o",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch05-task-5",
            "type": "task",
            "title": "Chess coordinates",
            "difficulty": 2,
            "plain": "Turn a square number into a chess coordinate like ('E', 4).",
            "instructions": r"""
On our chess board every square is a number 0-63: column A is `0..7`
(top = rank 8, down to rank 1), column B `8..15`, ..., column H `56..63`.

Write `coordinates(pos)` returning the pair `(file_letter, rank)` as a
**tuple**:

```python
coordinates(0)    # ('A', 8)
coordinates(7)    # ('A', 1)
coordinates(63)   # ('H', 1)
```

The file letter is `'A' + pos // 8`, the rank is `8 - pos % 8`.
""",
            "starter": """def coordinates(pos):
    letter = chr(ord('A') + pos // 8)
    # TODO: rank = 8 - pos % 8
    # TODO: return (letter, rank)
""",
            "example": """Letter and rank maths:

```python
print(chr(ord("A") + 3))
print(8 - 11 % 8)
```
""",

            "hints": [
                "`pos // 8` is the column 0..7 -> a letter via `chr(ord('A') + col)` or `'ABCDEFGH'[col]`.",
                "`pos % 8` is the position inside the column; rank = `8 - pos % 8`.",
                "`return (letter, rank)` - a tuple.",
            ],
            "solution": """def coordinates(pos):
    letter = chr(ord('A') + pos // 8)
    rank = 8 - pos % 8
    return (letter, rank)
""",
            "explanation": "Integer division `pos // 8` tells you which column (0-7) the square is in - `ord('A') + column` converted back with `chr` gives the letter. The remainder `pos % 8` counts downward inside the column, so the rank is `8 -` that. Returning `(letter, rank)` gives the caller a tidy tuple.\n\nWhat you learned: `//` and `%` split a flat index into row/column parts.",
            "tests": [
                {"kind": "expr", "expr": "coordinates(0)", "expected": "('A', 8)", "expected_type": "tuple"},
                {"kind": "expr", "expr": "coordinates(7)", "expected": "('A', 1)"},
                {"kind": "expr", "expr": "coordinates(8)", "expected": "('B', 8)"},
                {"kind": "expr", "expr": "coordinates(36)", "expected": "('E', 4)"},
                {"kind": "expr", "expr": "coordinates(63)", "expected": "('H', 1)"},
            ],
        },
        {
            "id": "ch05-boss",
            "type": "task",
            "title": "Exam report card",
            "difficulty": 3,
            "boss": True,
            "plain": "Three small functions team up to build a report line.",
            "instructions": r"""
**BOSS MISSION - build a report card generator.**

Write **three** functions that work together:

1. `exam_stats(scores)` - returns a tuple
   `(count, best, average)` where `average` is a float.
2. `grade(avg, pass_mark=60)` - returns
   `"Distinction"` for `avg >= 90`, `"Pass"` for `avg >= pass_mark`,
   else `"Fail"`.
3. `report(name, scores)` - uses both and returns exactly:

   `"Ada: 3 exams, best 97, avg 92.3, Distinction"`

   (avg formatted with one decimal, e.g. `{avg:.1f}`)

```python
report("Ada", [92, 97, 88])  # 'Ada: 3 exams, best 97, avg 92.3, Distinction'
report("Ben", [40, 55, 65])  # 'Ben: 3 exams, best 65, avg 53.3, Fail'
report("Tom", [70, 80, 90])  # 'Tom: 3 exams, best 90, avg 80.0, Pass'
```
""",
            "starter": """def exam_stats(scores):
    # TODO: return (count, best, average)
    pass


def grade(avg, pass_mark=60):
    # TODO: "Distinction" / "Pass" / "Fail"
    pass


def report(name, scores):
    # TODO: unpack exam_stats, format the line
    pass
""",
            "example": """Two tiny functions teaming up:

```python
def average(nums):
    return sum(nums) / len(nums)

def report(name, nums):
    return f"{name}: avg {average(nums)}"

print(report("Ada", [80, 90]))
```
""",

            "hints": [
                "`exam_stats` is just `(len(s), max(s), sum(s)/len(s))` as a tuple.",
                "`grade`: two ifs or a chained conditional - check 90 first!",
                "`report`: `n, best, avg = exam_stats(scores)`, then one f-string ending with `{grade(avg)}`.",
            ],
            "solution": """def exam_stats(scores):
    return len(scores), max(scores), sum(scores) / len(scores)


def grade(avg, pass_mark=60):
    if avg >= 90:
        return "Distinction"
    if avg >= pass_mark:
        return "Pass"
    return "Fail"


def report(name, scores):
    n, best, avg = exam_stats(scores)
    return f"{name}: {n} exams, best {best}, avg {avg:.1f}, {grade(avg)}"


# quick check:
# print(report("Ada", [92, 97, 88]))
""",
            "explanation": "Each function does one job: `exam_stats` packs three numbers into a tuple, `grade` maps an average to a label (the 90-check must come first - a 95 would otherwise be caught by the pass-mark check), and `report` unpacks the tuple and fills the f-string. `:.1f` rounds the average to one decimal.\n\nWhat you learned: small functions that return values snap together like building blocks.",
            "tests": [
                {"kind": "expr", "expr": "report('Ada', [92, 97, 88])",
                 "expected": "'Ada: 3 exams, best 97, avg 92.3, Distinction'"},
                {"kind": "expr", "expr": "report('Ben', [40, 55, 65])",
                 "expected": "'Ben: 3 exams, best 65, avg 53.3, Fail'"},
                {"kind": "expr", "expr": "report('Tom', [70, 80, 90])",
                 "expected": "'Tom: 3 exams, best 90, avg 80.0, Pass'"},
                {"kind": "expr", "expr": "exam_stats([10, 20])",
                 "expected": "(2, 20, 15.0)", "expected_type": "tuple"},
            ],
        },
    ],
}
