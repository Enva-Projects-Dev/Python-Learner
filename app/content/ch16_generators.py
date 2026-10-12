"""Kapitel 16 - Generatoren."""

CHAPTER = {
    "id": "ch16",
    "number": 16,
    "title": "Generators",
    "summary": "Machines that hand you one item each time you ask - yield, laziness and infinite sequences.",
    "items": [
        {
            "id": "ch16-lesson",
            "type": "lesson",
            "title": "Iterators and yield",
            "body": r"""
You've looped over lists a hundred times - but HOW does `for` actually
get the items? Behind the scenes every `for` uses an **iterator**: an
object that hands out the next item each time you ask. Once you
understand that, you can build your own - even endless ones.

## What a for-loop really does

`iter()` makes the iterator; `next()` pulls one item; the
`StopIteration` error means "all out":

```python
container = {3, 7, -1, 2, 43}
iterator = iter(container)
while True:
    try:
        print(next(iterator), end=" ")
    except StopIteration:
        break
print()
```

> **What happens here**
>
> - line 2: `iter(container)` builds the iterator object - the thing
>   that remembers where it is
> - line 5: `next(iterator)` fetches the next item - each call moves
>   the pointer forward
> - line 6: when nothing's left, next() raises StopIteration - the
>   `for` loop normally catches this quietly and ends

> **Think of it like...** a vending machine: press the button (`next()`),
> one item drops; press it once too often -> "all out" (StopIteration).

## A class can be an iterator

Implement `__iter__` (start fresh) and `__next__` (one item please):

```python
class float_range:
    def __init__(self, start, stop, inc):
        self.start, self.stop, self.inc = start, stop, inc
    def __iter__(self):
        self.counter = self.start
        return self
    def __next__(self):
        if self.counter >= self.stop:
            raise StopIteration
        tmp = self.counter
        self.counter += self.inc
        return tmp

for x in float_range(0, 2, 0.5):
    print(x, end=" ")
print()
```

> **What happens here**
>
> - line 5: `for` calls `__iter__` once - it resets counter to start
>   and returns the object itself (this object IS its iterator)
> - line 8-9: `__next__` checks the stop bound - past it means
>   StopIteration
> - line 10-12: hand back the current value, then step forward by inc

## Generators: yield pauses the machine

Writing `__iter__`/`__next__` is clunky. A function containing `yield`
is a **generator** - calling it builds the machine; each `yield` hands
out one value and **freezes** the function mid-step, resuming right
there on the next ask:

```python
def fibonacci(maximum):
    x, y = 0, 1
    while x < maximum:
        yield x
        x, y = y, x + y

print(list(fibonacci(100)))
```

> **What happens here**
>
> - line 4: `yield x` hands out x and pauses - the loop variables stay
>   frozen between calls
> - line 5: `x, y = y, x + y` slides the window - the next pair of
>   Fibonacci numbers
> - line 7: `list(...)` keeps pressing next() until the generator
>   stops (when x >= maximum)

> **Watch out** - a generator is a one-shot stream: once used up it
> hands out nothing more. Call the function again for a fresh machine -
> and never wrap an endless one in `list()`!

## Try it yourself

- Write `def threes()` yielding 3, 6, 9 - try `list(threes())`.
- Call `iter()` on a list and `next()` it twice by hand.

## Key words

| Word | Meaning |
|---|---|
| iterator | an object with `__next__` - one item per ask |
| iterable | anything `iter()` accepts (lists, strings, sets...) |
| StopIteration | the 'no more items' signal |
| yield | hand out a value and pause the function |
| generator | a function with yield - a lazy item machine |
""",
        },
        {
            "id": "ch16-lesson-2",
            "type": "lesson",
            "title": "Lazy machines and generator expressions",
            "body": r"""
Generators compute values **only when asked** - they don't build a
list first. That laziness unlocks something wild: sequences that never
end.

> **Think of it like...** a recipe machine that makes one pancake only
> when you press the button. You could ask forever - the machine never
> runs out of batter.

## Infinite machines + the safety scoop

`itertools.islice` takes exactly n items from any generator:

```python
from itertools import islice

def fibonacci_forever():
    x, y = 0, 1
    while True:
        yield x
        x, y = y, x + y

print(list(islice(fibonacci_forever(), 10)))   # take only 10
```

> **What happens here**
>
> - line 5: `while True` - this machine truly never stops on its own
> - line 9: `islice(gen, 10)` pulls exactly 10 items then stops asking;
>   the generator just pauses forever, unused
> - `list(...)` collects the 10 that were handed out

> **Watch out** - `list(fibonacci_forever())` without islice would run
> forever. With infinite generators YOU must set the limit: islice or
> a `break`.

## Generator expressions

Like list comprehensions - but lazy - with round brackets:

```python
o1 = [n ** 2 for n in range(20) if n % 2 == 1]   # list - all at once
o2 = (n ** 2 for n in range(20) if n % 2 == 1)   # generator - on demand
print(sum(o1), sum(o2))
print(sum(n ** 2 for n in range(20)))   # parens may be dropped
```

> **What happens here**
>
> - line 1: `[...]` computes all 10 squares NOW and stores them
> - line 2: `(...)` builds a generator - nothing computed yet
> - line 3: `sum` pulls the values one by one - both give 1330
> - line 4: inside a call you can drop the extra parentheses

## Try it yourself

- Take 7 values from `fibonacci_forever()` with islice.
- Turn `[x*2 for x in range(5)]` into a generator and `sum` it.

## Key words

| Word | Meaning |
|---|---|
| lazy | computed only when requested |
| islice | 'take n items' - the scoop for endless streams |
| generator expression | comprehension with round brackets |
| infinite generator | a machine that never runs out |
""",
        },
        {
            "id": "ch16-quiz-1",
            "type": "quiz",
            "title": "yield",
            "question": "Calling a function containing `yield` returns...",
            "options": ["the first yielded value", "a list of all values", "a generator object", "None"],
            "answer": 2,
            "explanation": "The call only builds the machine - the body doesn't run until next() asks for a value.",
        },
        {
            "id": "ch16-quiz-2",
            "type": "quiz",
            "title": "StopIteration",
            "question": "A for loop over an iterator ends when...",
            "options": ["the iterator returns None", "next() raises StopIteration", "the list is empty", "iter() returns False"],
            "answer": 1,
            "explanation": "StopIteration is the 'all out' signal - for-loops catch it quietly and stop.",
        },
        {
            "id": "ch16-quiz-3",
            "type": "quiz",
            "title": "Infinite generators",
            "question": "Why is `for x in infinite_gen(): ...` not automatically an infinite loop?",
            "options": ["Generators cap at 1000 items", "Values are made only as consumed - break or islice stops the asking", "Python kills them after 5 s", "It always is an infinite loop"],
            "answer": 1,
            "explanation": "Laziness saves you: the generator only produces what you take; stop taking and it pauses forever.",
        },
        {
            "id": "ch16-quiz-4",
            "type": "quiz",
            "title": "Generator expression",
            "question": "`(x*2 for x in range(3))` creates...",
            "options": ["the list [0, 2, 4]", "a generator object", "a tuple", "a syntax error"],
            "answer": 1,
            "explanation": "Round brackets make it lazy - the values [0, 2, 4] exist only when consumed, e.g. by list() or sum().",
        },
        {
            "id": "ch16-warm-1",
            "type": "task",
            "title": "First yield",
            "difficulty": 1,
            "plain": "A tiny generator that yields the numbers 1, 2, 3.",
            "instructions": r"""
Write `def three()` yielding 1, 2, 3 - then print
`list(three())`.

Expected output: `[1, 2, 3]`
""",
            "starter": """# TODO: generator three() yielding 1, 2, 3

print(list(three()))
""",
            "hints": [
                "Three `yield` lines inside the function - or a small loop.",
                "`yield 1`, `yield 2`, `yield 3` works fine.",
                "list() collects everything the machine hands out.",
            ],
            "solution": """def three():
    yield 1
    yield 2
    yield 3

print(list(three()))""",
            "explanation": "Each `yield` emits one value and pauses - calling `three()` builds the generator, `list()` pulls all three items out of it.\n\nWhat you learned: yield turns a function into a pause-and-resume machine.",
            "tests": [
                {"kind": "program", "expected": "[1, 2, 3]", "match": "exact"},
            ],
        },
        {
            "id": "ch16-warm-2",
            "type": "task",
            "title": "Slice the infinity",
            "difficulty": 1,
            "plain": "Take only 4 items from an endless counter.",
            "instructions": r"""
`naturals()` (given) yields 1, 2, 3, ... forever. Print the first 4
items using `itertools.islice`.

Expected output: `[1, 2, 3, 4]`
""",
            "starter": """from itertools import islice

def naturals():
    n = 1
    while True:
        yield n
        n += 1

# TODO: print the first 4 values
""",
            "hints": [
                "`islice(gen, 4)` takes the first 4.",
                "Wrap it in `list(...)` to print.",
                "Never `list(naturals())` directly - it never ends!",
            ],
            "solution": """from itertools import islice

def naturals():
    n = 1
    while True:
        yield n
        n += 1

print(list(islice(naturals(), 4)))""",
            "explanation": "`islice` pulls exactly 4 items then stops asking - the infinite generator just pauses forever afterwards. Laziness is why `while True` is safe here.\n\nWhat you learned: islice is the scoop you dip into an endless stream.",
            "tests": [
                {"kind": "program", "expected": "[1, 2, 3, 4]", "match": "exact"},
            ],
        },
        {
            "id": "ch16-task-1",
            "type": "task",
            "title": "Reciprocals generator",
            "difficulty": 1,
            "plain": "Yield 1/1, 1/2, 1/3, ... - one fraction per ask.",
            "instructions": r"""
Write a generator `reciprocals(n)` yielding `1/1, 1/2, ..., 1/(n-1)`
for numbers 1 to n-1.

`list(reciprocals(5))` -> `[1.0, 0.5, 0.3333333333333333, 0.25]`
""",
            "starter": """def reciprocals(n):
    \"\"\"Generator producing 1/1, 1/2, ..., 1/(n-1).\"\"\"
    # TODO
    pass


for value in reciprocals(20):
    print(f"{value:.2f}", end=" ")
""",
            "hints": [
                "Loop `x` over `range(1, n)` and `yield 1 / x`.",
                "A generator needs no return - yield does the work.",
                "Check with `list(reciprocals(5))`.",
            ],
            "solution": """def reciprocals(n):
    \"\"\"Generator producing 1/1, 1/2, ..., 1/(n-1).\"\"\"
    for x in range(1, n):
        yield 1 / x


for value in reciprocals(20):
    print(f"{value:.2f}", end=" ")
""",
            "explanation": "Each loop round computes `1 / x` and hands it out with yield - the for-loop in the test program keeps asking until the generator's own loop ends (when x exhausts range(1, n)).\n\nWhat you learned: a generator's 'return list' is the sequence of its yields.",
            "tests": [
                {"kind": "expr", "expr": "list(reciprocals(5))",
                 "expected": "[1.0, 0.5, 0.3333333333333333, 0.25]"},
                {"kind": "expr", "expr": "list(reciprocals(2))", "expected": "[1.0]"},
                {"kind": "expr", "expr": "len(list(reciprocals(20)))", "expected": "19"},
            ],
        },
        {
            "id": "ch16-task-2",
            "type": "task",
            "title": "Fixed-length substrings",
            "difficulty": 1,
            "plain": "Slide a window over a word, yielding each piece.",
            "instructions": r"""
Write `substrings(text, length)` yielding every substring of `text`
of the given `length` - a sliding window:

```python
list(substrings("Python", 3))
# ['Pyt', 'yth', 'tho', 'hon']
```
""",
            "starter": """def substrings(text, length):
    \"\"\"Generator producing all substrings of text of the given length.\"\"\"
    # TODO
    pass
""",
            "hints": [
                "Window starts: `range(len(text) - length + 1)`.",
                "`yield text[i:i + length]`.",
                "If length > len(text), the range is empty - fine.",
            ],
            "solution": """def substrings(text, length):
    \"\"\"Generator producing all substrings of text of the given length.\"\"\"
    for i in range(len(text) - length + 1):
        yield text[i:i + length]
""",
            "explanation": "A window of `length` starting at i is just `text[i:i+length]`; the last legal start is `len(text)-length`, hence `+1` in the range. If the window is too big the range is empty and the generator yields nothing.\n\nWhat you learned: sliding windows = slice inside a range loop.",
            "tests": [
                {"kind": "expr", "expr": "list(substrings('Python', 3))",
                 "expected": "['Pyt', 'yth', 'tho', 'hon']"},
                {"kind": "expr", "expr": "list(substrings('abcde', 1))",
                 "expected": "['a', 'b', 'c', 'd', 'e']"},
                {"kind": "expr", "expr": "list(substrings('ab', 5))", "expected": "[]"},
            ],
        },
        {
            "id": "ch16-task-3",
            "type": "task",
            "title": "count_up with step",
            "difficulty": 2,
            "plain": "Like range() - but including the stop, and floats allowed.",
            "instructions": r"""
Write `count_up(start, stop, step=1)` yielding numbers from `start`
**up to and including** `stop`, stepping by `step` (floats allowed -
`range` can't do those).

```python
list(count_up(10, 20, 0.5))
# [10, 10.5, 11.0, ..., 20.0]  (21 values)
```
""",
            "starter": """def count_up(start, stop, step=1):
    # TODO
    pass


# print(list(count_up(100, 200, 5)))
""",
            "hints": [
                "`while number <= stop:` yield, then `number += step`.",
                "`step=1` is a default parameter in the signature.",
                "Float steps may accumulate tiny rounding - that's expected.",
            ],
            "solution": """def count_up(start, stop, step=1):
    number = start
    while number <= stop:
        yield number
        number += step
""",
            "explanation": "A while loop yields the current number then steps forward - `<= stop` is what makes the stop value included, unlike range. Float steps work because we never rely on integers.\n\nWhat you learned: a hand-rolled while+yield beats range when you need floats or inclusive ends.",
            "tests": [
                {"kind": "expr", "expr": "list(count_up(1, 5))",
                 "expected": "[1, 2, 3, 4, 5]"},
                {"kind": "expr", "expr": "list(count_up(0, 10, 5))",
                 "expected": "[0, 5, 10]"},
                {"kind": "expr", "expr": "len(list(count_up(10, 20, 0.5)))",
                 "expected": "21"},
            ],
        },
        {
            "id": "ch16-task-4",
            "type": "task",
            "title": "Infinite counter",
            "difficulty": 2,
            "plain": "Same counter - but it can count forever if you let it.",
            "instructions": r"""
Upgrade `count_up` to `count_up(start, stop=None, step=1)`: yields
`start, start+step, ...` up to `stop` - or **endlessly** when `stop`
is `None`.

```python
from itertools import islice
list(islice(count_up(0, step=7), 5))    # [0, 7, 14, 21, 28]
```
""",
            "starter": """from itertools import islice

def count_up(start, stop=None, step=1):
    # TODO: infinite when stop is None
    pass


print(list(islice(count_up(0, step=7), 10)))
""",
            "hints": [
                "One condition covers both: `while stop is None or number <= stop:`.",
                "`stop=None` is the default in the signature.",
                "Consumers must limit it - islice, never bare list().",
            ],
            "solution": """from itertools import islice

def count_up(start, stop=None, step=1):
    number = start
    while stop is None or number <= stop:
        yield number
        number += step


print(list(islice(count_up(0, step=7), 10)))
""",
            "explanation": "`stop is None or number <= stop` makes the loop condition vacuously true when no stop is given - the generator then runs forever, safely, because callers must use islice to take a limited scoop.\n\nWhat you learned: `None` as a default means 'no limit'.",
            "tests": [
                {"kind": "expr",
                 "expr": "list(islice(count_up(0, step=7), 5))",
                 "expected": "[0, 7, 14, 21, 28]"},
                {"kind": "expr", "expr": "list(count_up(1, 3))",
                 "expected": "[1, 2, 3]"},
                {"kind": "expr",
                 "expr": "list(islice(count_up(100, step=5), 10))",
                 "expected": "[100, 105, 110, 115, 120, 125, 130, 135, 140, 145]"},
            ],
        },
        {
            "id": "ch16-task-5",
            "type": "task",
            "title": "All substrings",
            "difficulty": 2,
            "plain": "Every possible piece of the word - all lengths, all positions.",
            "instructions": r"""
Write `all_substrings(text)` yielding **every** substring - all
lengths, in order of starting index:

```python
list(all_substrings("abc"))
# ['a', 'ab', 'abc', 'b', 'bc', 'c']
```
""",
            "starter": """def all_substrings(text):
    # TODO
    pass


print(", ".join(all_substrings("Python")))
""",
            "hints": [
                "Outer loop `start` in `range(len(text))`.",
                "Inner loop `end` in `range(start + 1, len(text) + 1)`.",
                "`yield text[start:end]` - the inner loop grows the window.",
            ],
            "solution": """def all_substrings(text):
    for start in range(len(text)):
        for end in range(start + 1, len(text) + 1):
            yield text[start:end]


print(", ".join(all_substrings("Python")))
""",
            "explanation": "For each start position, the inner loop extends the end from start+1 to the string end - generating 'a', 'ab', 'abc' before moving to 'b', 'bc', then 'c'. 'Python' (6 letters) produces 6+5+4+3+2+1 = 21 pieces.\n\nWhat you learned: nested loops enumerate every (start, end) pair.",
            "tests": [
                {"kind": "expr", "expr": "list(all_substrings('abc'))",
                 "expected": "['a', 'ab', 'abc', 'b', 'bc', 'c']"},
                {"kind": "expr", "expr": "len(list(all_substrings('Python')))",
                 "expected": "21"},
                {"kind": "expr", "expr": "list(all_substrings(''))", "expected": "[]"},
            ],
        },
        {
            "id": "ch16-boss",
            "type": "task",
            "title": "Infinite number machine",
            "difficulty": 3,
            "boss": True,
            "plain": "An endless stream of multiples - and a second machine that caps it.",
            "instructions": r"""
**BOSS MISSION - build the number machine.**

Two generators:

- `multiples(k)` - yields `k, 2k, 3k, ...` **forever**
- `take_below(gen, bound)` - yields values from `gen` while they are
  `< bound`, then stops (use a for loop + break)

```python
list(take_below(multiples(7), 50))
# [7, 14, 21, 28, 35, 42, 49]

list(islice(multiples(3), 5))
# [3, 6, 9, 12, 15]
```
""",
            "starter": """from itertools import islice

def multiples(k):
    # TODO: infinite generator
    pass


def take_below(gen, bound):
    # TODO: yield from gen while value < bound
    pass
""",
            "example": """An endless generator, five pulls:

```python
def evens():
    n = 0
    while True:
        yield n
        n += 2

g = evens()
print([next(g) for _ in range(5)])
```
""",

            "hints": [
                "multiples: `n = k; while True: yield n; n += k`.",
                "take_below: `for v in gen: if v >= bound: break; yield v`.",
                "A generator can wrap another generator - the for loop pulls items through.",
            ],
            "solution": """from itertools import islice

def multiples(k):
    n = k
    while True:
        yield n
        n += k


def take_below(gen, bound):
    for value in gen:
        if value >= bound:
            break
        yield value
""",
            "explanation": "`multiples` is an endless `while True` machine - safe because nobody can consume it all at once. `take_below` is a generator *wrapping* a generator: its for-loop pulls items, forwards the small ones, and breaks on the first oversized one, which also stops asking the inner machine.\n\nWhat you learned: generators compose - one lazy machine can feed another.",
            "tests": [
                {"kind": "expr",
                 "expr": "list(take_below(multiples(7), 50))",
                 "expected": "[7, 14, 21, 28, 35, 42, 49]"},
                {"kind": "expr",
                 "expr": "list(islice(multiples(3), 5))",
                 "expected": "[3, 6, 9, 12, 15]"},
                {"kind": "expr",
                 "expr": "list(take_below(multiples(10), 10))",
                 "expected": "[]"},
            ],
        },
    ],
}
