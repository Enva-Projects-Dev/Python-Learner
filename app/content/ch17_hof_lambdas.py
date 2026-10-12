"""Kapitel 17 - Higher-Order Functions, Lambdas & Closures."""

CHAPTER = {
    "id": "ch17",
    "number": 17,
    "title": "Higher-Order Functions, Lambdas & Closures",
    "summary": "Functions as values: pass them around, write tiny lambdas, and functions that remember.",
    "items": [
        {
            "id": "ch17-lesson",
            "type": "lesson",
            "title": "Functions are objects",
            "body": r"""
In Python a function isn't special - it's a value like a number or a
string. You can store it, pass it to another function, even return it.
Functions that take or return functions are called **higher-order
functions**, and they let you customise behaviour without rewriting
code.

> **Think of it like...** a recipe card you can hand to a cook. The cook
> (the function `repeat`) does the work, but *which* recipe is up to
> you.

```python
def say_hello():
    print("Hello")

def repeat(count, fn):
    for i in range(count):
        fn()

repeat(3, say_hello)
```

> **What happens here**
>
> - line 1-2: a normal function definition
> - line 5: `fn()` calls whatever function was handed in - repeat
>   doesn't need to know its name
> - line 8: `say_hello` WITHOUT parentheses is the function itself -
>   with `()` you'd call it and pass the result instead!

## Sorting with a key - and tiny lambdas

`sorted` accepts a **key** - a function that picks out the thing to
compare by. A `lambda` is a one-line, nameless function:
`lambda params: expression` - perfect for keys:

```python
names = ['Tony Stark', 'Peter Parker', 'Wanda Maximoff', 'Bruce Banner']
print(sorted(names))
print(sorted(names, key=len))
print(sorted(names, key=lambda name: name.split()[-1]))
```

> **What happens here**
>
> - line 2: plain sorted -> alphabetical order
> - line 3: `key=len` means "compare the LENGTHS" - shortest name first
> - line 4: the lambda takes a name, splits it into words, and picks
>   the last one - so the heroes sort by surname

```python
def calculate(fn, a, b):
    return fn(a, b)

print(calculate(lambda a, b: a + b, 19, 23))
print(calculate(lambda c, d: c ** d, 3, 4))
```

> **What happens here**
>
> - line 1-2: calculate applies whatever function arrives
> - line 4: `lambda a, b: a + b` is an adder built on the spot -> 42
> - line 5: same function, different lambda -> 3⁴ = 81

> **Watch out** - `fn` vs `fn()` trips everyone: without parentheses
> you have the function itself; with them you're calling it. Passing
> `say_hello()` to repeat would break, because repeat receives the
> result (None), not the machine.

## Try it yourself

- Sort `names` by first-name length: `key=lambda n: len(n.split()[0])`.
- Write `triple = lambda x: 3*x` and call `triple(5)`.

## Key words

| Word | Meaning |
|---|---|
| higher-order function | a function taking or returning functions |
| lambda | a tiny nameless function: `lambda x: expr` |
| key= | the 'compare by this' function for sorted/min/max |
| fn without () | the function itself, not a call |
""",
        },
        {
            "id": "ch17-lesson-2",
            "type": "lesson",
            "title": "map, filter and closures",
            "body": r"""
Two ready-made higher-order functions do the most common jobs, and a
special trick - the **closure** - lets a function carry its own memory.

## map and filter - transform and select

- `map(fn, items)` applies `fn` to every element
- `filter(pred, items)` keeps elements where `pred` is truthy

> **Think of it like...** map is a conveyor belt that stamps each item
> with a new shape; filter is a bouncer who only lets some items
> through.

```python
names = ["Anna", "Bibi", "Clara", "Dora", "Emma"]
print(list(map(len, names)))
print(list(filter(lambda w: len(w) > 4, names)))
print(list(map(str.upper, names)))
```

> **What happens here**
>
> - line 2: map stamps every name with `len` -> [4, 4, 5, 4, 4]
> - line 3: filter keeps names where the lambda is True - longer than
>   4 -> ['Clara']
> - line 4: `str.upper` (a method used as a function!) uppercases all
> - `list(...)` because both return lazy iterators - they produce items
>   only when asked

## Closures: functions that remember

A function defined inside another can keep using the outer variables -
it **remembers the box it was born in**, even after the outer function
has finished. That's a closure:

```python
def incrementer(increment):
    def new_function(x):
        return x + increment   # remembers 'increment'
    return new_function

plus7 = incrementer(7)
plusplus = incrementer(1)
print(plus7(8), plus7(12), plusplus(99))
```

> **What happens here**
>
> - line 2-3: `new_function` is born inside incrementer and uses
>   `increment` - a variable from its birth-box
> - line 5: `return new_function` hands the inner function out
> - line 7: `plus7` is a function with 7 baked in; plusplus has 1
> - line 9: 8+7, 12+7, 99+1

`nonlocal` lets the inner function *write* to the birth-box - a private
counter:

```python
def new_counter():
    c = 0
    def f():
        nonlocal c      # may WRITE the outer variable
        c += 1
        return c
    return f

z = new_counter()
print(z(), z(), z())
```

> **What happens here**
>
> - line 2: `c` lives in new_counter's box - invisible outside
> - line 4: `nonlocal c` means "write to the outer c, don't create a
>   new local one"
> - line 9: three calls -> 1, 2, 3 - the counter survives between calls

> **Watch out** - each factory call creates a NEW box. Two counters
> from `new_counter()` count independently.

## Try it yourself

- `plus10 = incrementer(10)` - predict `plus10(5)` before running.
- Make two counters and check they don't share.

## Key words

| Word | Meaning |
|---|---|
| map / filter | transform every item / keep matching items |
| predicate | a function returning True/False |
| closure | a function that remembers its birth-box |
| nonlocal | write access to the enclosing variable |
| factory function | builds and returns custom functions |
""",
        },
        {
            "id": "ch17-quiz-1",
            "type": "quiz",
            "title": "Lambda",
            "question": "`(lambda a, b: a * b)(3, 4)` evaluates to...",
            "options": ["a function object", "12", "34", "an error"],
            "answer": 1,
            "explanation": "The lambda is built and called immediately with 3 and 4 - 12. A lambda alone is a function; with (...) after it, it's a call.",
        },
        {
            "id": "ch17-quiz-2",
            "type": "quiz",
            "title": "map/filter",
            "question": "`list(filter(lambda x: x > 2, [1, 2, 3, 4]))` gives...",
            "options": ["[3, 4]", "[1, 2]", "[True, False, True, True]", "[2, 3, 4]"],
            "answer": 0,
            "explanation": "filter keeps the ORIGINAL elements passing the test - not the True/False results (that's a common mix-up).",
        },
        {
            "id": "ch17-quiz-3",
            "type": "quiz",
            "title": "Closures",
            "question": "What makes a function a 'closure'?",
            "options": ["It has no parameters", "It uses a variable from the scope it was born in", "It is anonymous", "It cannot be called twice"],
            "answer": 1,
            "explanation": "A closure 'closes over' its birth variables - they stay alive privately, even after the outer function finished.",
        },
        {
            "id": "ch17-quiz-4",
            "type": "quiz",
            "title": "sorted key",
            "question": "To sort `['bbb', 'a', 'cc']` by length you write...",
            "options": ["sorted(words, 'len')", "sorted(words, key=len)", "sorted(words, len)", "words.sort(len)"],
            "answer": 1,
            "explanation": "The key must be passed as `key=len` - a named parameter; without the name sorted() would try to compare against the function itself.",
        },
        {
            "id": "ch17-warm-1",
            "type": "task",
            "title": "Sort by length",
            "difficulty": 1,
            "plain": "Sort words short-to-long using a key function.",
            "instructions": r"""
Sort `words = ['banana', 'kiwi', 'apple', 'fig']` by **length** and
print the result.

Expected output: `['fig', 'kiwi', 'apple', 'banana']`
""",
            "starter": """words = ['banana', 'kiwi', 'apple', 'fig']
# TODO: print sorted by length
""",
            "hints": [
                "`sorted` takes a `key=` argument.",
                "The built-in `len` is already a function - `key=len`.",
                "One line: `print(sorted(words, key=len))`.",
            ],
            "solution": """words = ['banana', 'kiwi', 'apple', 'fig']
print(sorted(words, key=len))""",
            "explanation": "`key=len` tells sorted to compare `len(word)` instead of the words themselves - 3 < 4 < 5 < 6 gives fig, kiwi, apple, banana.\n\nWhat you learned: `key=` swaps what sorted compares.",
            "tests": [
                {"kind": "program",
                 "expected": "['fig', 'kiwi', 'apple', 'banana']", "match": "exact"},
            ],
        },
        {
            "id": "ch17-warm-2",
            "type": "task",
            "title": "Make an adder",
            "difficulty": 1,
            "plain": "A function factory: build a 'plus 5' machine.",
            "instructions": r"""
Write `adder(n)` returning a function that adds `n` to its argument
(a closure). Then print `adder(5)(3)` and `adder(10)(1)`.

Expected output:

```text
8
11
```
""",
            "starter": """def adder(n):
    # TODO: return an inner function
    pass

print(adder(5)(3))
print(adder(10)(1))
""",
            "hints": [
                "Define `def inner(x): return x + n` inside and `return inner`.",
                "Or return a lambda: `return lambda x: x + n`.",
                "The inner function remembers `n` from its birth.",
            ],
            "solution": """def adder(n):
    def inner(x):
        return x + n
    return inner

print(adder(5)(3))
print(adder(10)(1))""",
            "explanation": "`adder(5)` returns `inner` with `n` baked in as 5 - calling that function with 3 gives 8. Each call to adder creates a fresh, independent `n`.\n\nWhat you learned: returning an inner function = building custom functions.",
            "tests": [
                {"kind": "program", "expected": "8\n11", "match": "exact"},
            ],
        },
        {
            "id": "ch17-task-1",
            "type": "task",
            "title": "filter and map on numbers",
            "difficulty": 1,
            "plain": "Keep the odd numbers; then flip every number's lowest bit.",
            "instructions": r"""
Given `numbers = [3, 14, -23, -24, 5, 18, 31]`:

1. `odd` - `filter` + lambda keeping odd numbers (`x % 2 != 0`)
2. `made_odd` - `map` + lambda applying `x | 1` (sets the lowest bit)

Both as **lists**, exact variable names.

Expected: `odd = [3, -23, 5, 31]`, `made_odd = [3, 15, -23, -23, 5, 19, 31]`
""",
            "starter": """numbers = [3, 14, -23, -24, 5, 18, 31]

odd = None        # TODO: filter(...)
made_odd = None   # TODO: map(...)

print("only odd:", odd)
print("all made odd:", made_odd)
""",
            "hints": [
                "`list(filter(lambda x: x % 2 != 0, numbers))`.",
                "`x | 1` sets the lowest bit - `list(map(lambda x: x | 1, numbers))`.",
                "map/filter return lazy iterators - always wrap in list().",
            ],
            "solution": """numbers = [3, 14, -23, -24, 5, 18, 31]

odd = list(filter(lambda x: x % 2 != 0, numbers))
made_odd = list(map(lambda x: x | 1, numbers))

print("only odd:", odd)
print("all made odd:", made_odd)
""",
            "explanation": "filter keeps elements where `x % 2 != 0` - Python's modulo gives -23 % 2 = 1, so negative odds pass too. `x | 1` flips the lowest bit on: even numbers grow by 1 (14->15, -24->-23), odd ones stay.\n\nWhat you learned: filter selects, map transforms - both lazily.",
            "tests": [
                {"kind": "expr", "expr": "odd", "expected": "[3, -23, 5, 31]"},
                {"kind": "expr", "expr": "made_odd",
                 "expected": "[3, 15, -23, -23, 5, 19, 31]"},
            ],
        },
        {
            "id": "ch17-task-2",
            "type": "task",
            "title": "Composing functions",
            "difficulty": 2,
            "plain": "Glue two functions into one: first g, then f.",
            "instructions": r"""
Write `compose(f, g)` returning a new function that computes
`f(g(x))`.

```python
compose(lambda x: 0.5 * x, lambda x: x * x)(3)      # 4.5
compose(lambda s: s.capitalize(),
        lambda s: s + s[::-1])("python")            # 'Pythonnohtyp'
```
""",
            "starter": """def compose(f, g):
    # TODO: return a function h with h(x) = f(g(x))
    pass


f = lambda x: 0.5 * x
g = lambda x: x * x
h = compose(f, g)
print(h(3))

f = lambda s: s.capitalize()
g = lambda s: s + s[::-1]
h = compose(f, g)
print(h("python"))
""",
            "hints": [
                "Return `lambda x: f(g(x))`.",
                "g runs first, f gets its result - order matters.",
                "This IS a closure: the returned function remembers f and g.",
            ],
            "solution": """def compose(f, g):
    return lambda x: f(g(x))


f = lambda x: 0.5 * x
g = lambda x: x * x
h = compose(f, g)
print(h(3))

f = lambda s: s.capitalize()
g = lambda s: s + s[::-1]
h = compose(f, g)
print(h("python"))
""",
            "explanation": "The lambda returned by compose captures f and g - when the new function finally runs, it feeds x through g and pipes the result into f. `h(3)` = f(g(3)) = 0.5-9 = 4.5.\n\nWhat you learned: functions can be built on the fly by remembering other functions.",
            "tests": [
                {"kind": "expr", "expr": "compose(lambda x: 0.5 * x, lambda x: x * x)(3)",
                 "expected": "4.5"},
                {"kind": "expr",
                 "expr": "compose(lambda s: s.capitalize(), lambda s: s + s[::-1])('python')",
                 "expected": "'Pythonnohtyp'"},
                {"kind": "expr", "expr": "compose(lambda x: x + 1, lambda x: x * 2)(5)",
                 "expected": "11"},
            ],
        },
        {
            "id": "ch17-task-3",
            "type": "task",
            "title": "Animals: filter + map",
            "difficulty": 1,
            "plain": "Long animal names, shouted - written two different ways.",
            "instructions": r"""
Given `animals = ["tiger", "hund", "katze", "maus", "schnabeltier",
"giraffe"]`, produce names longer than 4 characters, upper-cased -
**twice**:

1. `result` - using `filter` then `map`
2. `result2` - one list comprehension

Expected: `['TIGER', 'KATZE', 'SCHNABELTIER', 'GIRAFFE']`
""",
            "starter": """animals = ["tiger", "hund", "katze", "maus", "schnabeltier", "giraffe"]

result = []    # TODO: filter + map
result2 = []   # TODO: one list comprehension

print(result)
print(result2)
""",
            "hints": [
                "`filter(lambda t: len(t) > 4, animals)` piped into `map(str.upper, ...)`.",
                "Comprehension: `[t.upper() for t in animals if len(t) > 4]`.",
                "The functional pipeline needs list() at the end.",
            ],
            "solution": """animals = ["tiger", "hund", "katze", "maus", "schnabeltier", "giraffe"]

result = list(map(str.upper, filter(lambda t: len(t) > 4, animals)))
result2 = [t.upper() for t in animals if len(t) > 4]

print(result)
print(result2)
""",
            "explanation": "The functional version chains the machines: filter drops 'hund'/'maus', map uppercases the survivors, list collects. The comprehension does both in one line - `[transform for item if keep]`.\n\nWhat you learned: filter+map and comprehensions are two spellings of the same idea.",
            "tests": [
                {"kind": "expr", "expr": "result",
                 "expected": "['TIGER', 'KATZE', 'SCHNABELTIER', 'GIRAFFE']"},
                {"kind": "expr", "expr": "result2",
                 "expected": "['TIGER', 'KATZE', 'SCHNABELTIER', 'GIRAFFE']"},
            ],
        },
        {
            "id": "ch17-task-4",
            "type": "task",
            "title": "Closures: logger and counter",
            "difficulty": 2,
            "plain": "Two little factories: one stamps messages, one counts calls.",
            "instructions": r"""
Two closures:

1. `new_logger(level)` -> function `log(msg)` printing
   `'<LEVEL>: <msg>'`, mapping level via
   `{0: 'ALL', 1: 'DEBUG', 2: 'WARN', 3: 'ERROR'}`.
2. `new_counter()` -> a function that counts its own calls via
   `nonlocal` (first call returns 1).

```python
warn = new_logger(2)
warn("Something is off")   # WARN: Something is off
```
""",
            "starter": """def new_logger(level):
    level_strings = {0: "ALL", 1: "DEBUG", 2: "WARN", 3: "ERROR"}
    # TODO: return a function printing "LEVEL: msg"
    pass


def new_counter():
    # TODO: return a function that counts its own calls
    pass
""",
            "hints": [
                "Inner `def log(msg): print(f'{level_strings[level]}: {msg}')`, then `return log`.",
                "Counter: `c = 0` outside; `nonlocal c; c += 1` inside.",
                "Each new_counter() gets its own private c.",
            ],
            "solution": """def new_logger(level):
    level_strings = {0: "ALL", 1: "DEBUG", 2: "WARN", 3: "ERROR"}

    def log(msg):
        print(f"{level_strings[level]}: {msg}")

    return log


def new_counter():
    c = 0
    def f():
        nonlocal c
        c += 1
        return c
    return f
""",
            "explanation": "The logger's inner `log` remembers `level` (and the mapping table) from its birth; the counter's `f` remembers `c` - and `nonlocal` gives write access to it, so the count persists between calls. Two counters stay independent because each birth-box is separate.\n\nWhat you learned: closures = functions with private memory.",
            "tests": [
                {"kind": "stdout", "code": "w = new_logger(2)\nw('Something is off')\ne = new_logger(3)\ne('Crashed')",
                 "expected": "WARN: Something is off\nERROR: Crashed", "match": "exact"},
                {"kind": "expr",
                 "expr": "(lambda z: (z(), z(), z()))(new_counter())",
                 "expected": "(1, 2, 3)"},
                {"kind": "assert",
                 "code": "a = new_counter()\nb = new_counter()\na(); a()\nassert b() == 1",
                 "desc": "counters are independent"},
            ],
        },
        {
            "id": "ch17-task-5",
            "type": "task",
            "title": "Calculator with a lambda dict",
            "difficulty": 2,
            "plain": "Pick the right function from a dict of lambdas and run it.",
            "instructions": r"""
A dict maps operator symbols to lambdas (given). Write
`evaluate(term)` - takes `'840 * 20'` or `'2^8'`, finds the operator
character, parses both operands as ints, dispatches via `operation`,
returns the result. Spaces are optional.

```python
evaluate('840 * 20')   # 16800
evaluate('2^8')        # 256
```
""",
            "starter": """operation = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
           "^": lambda a, b: a ** b, "*": lambda a, b: a * b,
           "/": lambda a, b: a / b}


def evaluate(term):
    # TODO: split into operand, operator, operand; dispatch via operation
    pass
""",
            "hints": [
                "Strip spaces first: `term.replace(' ', '')`.",
                "The operator is the first char that isn't a digit or '.'.",
                "`operation[ch](a, b)` calls the stored lambda.",
            ],
            "solution": """operation = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
           "^": lambda a, b: a ** b, "*": lambda a, b: a * b,
           "/": lambda a, b: a / b}


def evaluate(term):
    compact = term.replace(" ", "")
    for i, ch in enumerate(compact):
        if not ch.isdigit() and ch != '.':
            a = int(compact[:i])
            b = int(compact[i + 1:])
            return operation[ch](a, b)
""",
            "explanation": "Scanning the compacted string, the first non-digit/non-dot character splits the term: digits before it are operand a, digits after are b, and the character itself selects the lambda in `operation`. Dicts of functions = a tiny dispatch table.\n\nWhat you learned: storing functions in a dict replaces long if-chains.",
            "tests": [
                {"kind": "expr", "expr": "evaluate('840 * 20')", "expected": "16800"},
                {"kind": "expr", "expr": "evaluate('2^8')", "expected": "256"},
                {"kind": "expr", "expr": "evaluate('10 - 4')", "expected": "6"},
                {"kind": "expr", "expr": "evaluate('10 / 4')", "expected": "2.5"},
            ],
        },
        {
            "id": "ch17-boss",
            "type": "task",
            "title": "Leaderboard sorter",
            "difficulty": 3,
            "boss": True,
            "plain": "A function factory that builds sorters for a game leaderboard.",
            "instructions": r"""
**BOSS MISSION - sort the leaderboard.**

Players are `(name, score)` tuples. Write `make_ranker(by)` - a
factory returning a sorter function:

- `make_ranker('score')` -> sorts players by score, **highest first**
- `make_ranker('name')` -> sorts alphabetically by name

Use `sorted` with a lambda `key`; the returned function is a closure
remembering `by`.

```python
players = [("Ana", 50), ("Bo", 90), ("Cy", 50)]
make_ranker('score')(players)
# [('Bo', 90), ('Ana', 50), ('Cy', 50)]
make_ranker('name')(players)
# [('Ana', 50), ('Bo', 90), ('Cy', 50)]
```
""",
            "starter": """def make_ranker(by):
    # TODO: return a function sorting a player list
    pass


players = [("Ana", 50), ("Bo", 90), ("Cy", 50)]
print(make_ranker("score")(players))
print(make_ranker("name")(players))
""",
            "example": """Sort with a lambda key:

```python
players = [("bo", 9), ("al", 15)]
by_score = sorted(players, key=lambda p: -p[1])
print(by_score)
```
""",

            "hints": [
                "Score descending: `key=lambda p: -p[1]` (negate flips the order).",
                "Name ascending: `key=lambda p: p[0]`.",
                "Pick the key inside an if on `by`, then `return lambda ps: sorted(ps, key=key)`.",
            ],
            "solution": """def make_ranker(by):
    if by == "score":
        key = lambda p: -p[1]
    else:
        key = lambda p: p[0]
    return lambda players: sorted(players, key=key)


players = [("Ana", 50), ("Bo", 90), ("Cy", 50)]
print(make_ranker("score")(players))
print(make_ranker("name")(players))
""",
            "explanation": "The factory chooses a key lambda once - `-p[1]` sorts scores descending because negating flips ascending into descending - then returns a closure that applies `sorted` with that remembered key. Equal scores keep input order because Python's sort is stable (Ana before Cy).\n\nWhat you learned: factories + keys + lambdas build reusable sorters.",
            "tests": [
                {"kind": "expr",
                 "expr": "make_ranker('score')([('Ana', 50), ('Bo', 90), ('Cy', 50)])",
                 "expected": "[('Bo', 90), ('Ana', 50), ('Cy', 50)]"},
                {"kind": "expr",
                 "expr": "make_ranker('name')([('Cy', 1), ('Ana', 2), ('Bo', 3)])",
                 "expected": "[('Ana', 2), ('Bo', 3), ('Cy', 1)]"},
                {"kind": "expr",
                 "expr": "make_ranker('score')([])", "expected": "[]"},
            ],
        },
    ],
}
