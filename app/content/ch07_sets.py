"""Kapitel 7 - Sets."""

CHAPTER = {
    "id": "ch07",
    "number": 7,
    "title": "Sets",
    "summary": "Bags of unique things - no order, no doubles - and the operators that compare them.",
    "items": [
        {
            "id": "ch07-lesson",
            "type": "lesson",
            "title": "Sets and set algebra",
            "body": r"""
Sometimes you don't care about order or duplicates - you just want to
know *who is in the group*. A **set** is Python's collection for that:
every item can appear at most once, and it has no positions.

> **Think of it like...** a party bag. Tossing the same name card in
> twice doesn't give you two cards - the bag holds each name once.

```python
m1 = {1, 2, 3}
m2 = {3, 2, 1}
m3 = {1, 1, 1, 1, 2, 3}
print(m1 == m2 == m3)     # True - same bag!
print(1 in m1)            # is it inside?
print(m1.issubset({5, 2, 1, 4, 3}))
```

> **What happens here**
>
> - line 1-3: three sets built with curly braces - order and repeats
>   don't matter, so all three are equal
> - line 5: `in` asks "is 1 inside the bag?" -> True
> - line 6: `issubset` asks "is everything in m1 also in the bigger
>   set?" -> True

> **Watch out** - `{}` creates an empty **dict**, not a set! The empty
> set is `set()`:

```python
print(type({}), type({1, 2}), type(set()))
print(set([10, 11, 12]))   # a set built from a list
```

> **What happens here**
>
> - line 1: `{}` reports dict, `{1, 2}` reports set, `set()` reports set
> - line 2: `set(...)` converts a list into a set - duplicates vanish

## Changing the bag

```python
m = {1, 2, 3, 4}
m.add(5)             # toss one card in
m.remove(1)          # take one out
m |= {6, 7, 8}       # pour another bag in
print(m)
```

> **What happens here**
>
> - line 2: `add` puts one new item in
> - line 3: `remove` takes one out - it **crashes** if the item isn't
>   there; `discard` does the same job quietly
> - line 4: `|=` adds a whole other set at once

## Comparing two bags

Three operators answer the classic questions:

```python
friends = {"Tina", "Tom", "Anna", "Otto", "Tim", "Sandra"}
classmates = {"Horst", "Theo", "Anna", "Zara", "Tom", "Mike", "Tina"}

print(friends & classmates)   # in BOTH bags      {'Anna', 'Tom', 'Tina'}
print(friends | classmates)   # in EITHER bag     (everyone)
print(friends - classmates)   # friends, but NOT classmates
```

> **What happens here**
>
> - `&` (**intersection**): only names in both sets
> - `|` (**union**): everyone from both bags, duplicates merged
> - `-` (**difference**): friends minus whoever is also a classmate

## Set comprehensions

Sets have the same one-line builder as lists - just curly braces.
Duplicates simply can't exist:

```python
friends = {"Tina", "Tom", "Anna"}
classmates = {"Theo", "Anna", "Tom"}
print({a * a for a in range(1, 10)})
print({n for n in friends | classmates if n.startswith('T')})
```

> **What happens here**
>
> - line 1-2: rebuild the two name sets so this example stands alone
> - line 3: squares 1-9 in one line - `{x ... }` builds a set
> - line 4: everyone whose name starts with 'T', out of both groups

## Try it yourself

- Make `{1, 1, 2, 2}` and print it - how many items survive?
- Check whether `{"a", "b"}` is a subset of `{"a", "b", "c"}`.
- Try `{"x", "y"} & {"y", "z"}`.

## Key words

| Word | Meaning |
|---|---|
| set | unordered bag, each value at most once |
| intersection `&` | items in BOTH sets |
| union `|` | items in EITHER set |
| difference `-` | left set minus the right |
| add / remove / discard | put in / take out / take out safely |
| issubset | is one bag entirely inside another |
| `in` | membership test |
| set() | the empty set - `{}` is a dict! |
| set comprehension | one-line set builder |
""",
        },
        {
            "id": "ch07-quiz-1",
            "type": "quiz",
            "title": "Duplicates",
            "question": "What is `len({1, 1, 2, 2, 3, 3})`?",
            "options": ["6", "3", "2", "Error"],
            "answer": 1,
            "explanation": "A set keeps each value once - the bag holds only 1, 2, 3, so length 3. '6' is the trap: it would be right for a list.",
        },
        {
            "id": "ch07-quiz-2",
            "type": "quiz",
            "title": "Set operators",
            "question": "`{1, 2, 3} - {2}` equals...",
            "options": ["{1, 3}", "{2}", "{1, 2, 3}", "Error"],
            "answer": 0,
            "explanation": "`-` takes everything in the left set that is NOT in the right: 1 and 3 stay, 2 goes.",
        },
        {
            "id": "ch07-quiz-3",
            "type": "quiz",
            "title": "Empty set",
            "question": "Which expression creates an empty set?",
            "options": ["{}", "set()", "{set()}", "[]"],
            "answer": 1,
            "explanation": "`{}` is an empty *dict* - Python can't tell otherwise. Empty sets need `set()`. '[]' is a list.",
        },
        {
            "id": "ch07-quiz-4",
            "type": "quiz",
            "title": "Intersection",
            "question": "`{'a', 'b', 'c'} & {'b', 'c', 'd'}` gives...",
            "options": ["{'a', 'b', 'c', 'd'}", "{'b', 'c'}", "{'a', 'd'}", "{'a'}"],
            "answer": 1,
            "explanation": "`&` keeps only what is in BOTH sets - b and c. {'a','b','c','d'} would be the union `|`.",
        },
        {
            "id": "ch07-warm-1",
            "type": "task",
            "title": "Squash the doubles",
            "difficulty": 1,
            "plain": "Turn a list with doubles into a set and count what's really there.",
            "instructions": r"""
The list `votes` has lots of repeats. Make a set `unique` from it and
print the set and how many different votes there were.

Expected output:

```
{'yes', 'no', 'maybe'}
3
```

(Your set may print in a different order - that's fine, sets have no
order. The test only checks `unique` and the count.)
""",
            "starter": """votes = ["yes", "no", "yes", "maybe", "no", "yes", "yes"]

unique = set()  # TODO: make a set from votes, then print it and its size
""",
            "hints": [
                "`set(votes)` turns the list into a bag without doubles.",
                "Print `unique`, then `len(unique)`.",
                "Two prints total.",
            ],
            "solution": """votes = ["yes", "no", "yes", "maybe", "no", "yes", "yes"]

unique = set(votes)
print(unique)
print(len(unique))
""",
            "explanation": "`set(votes)` pours the list into a bag - 'yes' appears 4 times in the list but once in the set. `len` then counts the 3 distinct values. Order in the printout is unpredictable and doesn't matter.\n\nWhat you learned: `set(list)` is the fastest way to drop duplicates.",
            "tests": [
                {"kind": "expr", "expr": "unique == {'yes', 'no', 'maybe'}", "expected": "True"},
                {"kind": "expr", "expr": "len(unique)", "expected": "3"},
            ],
        },
        {
            "id": "ch07-warm-2",
            "type": "task",
            "title": "Shared pizza toppings",
            "difficulty": 1,
            "plain": "Which toppings do both friends want?",
            "instructions": r"""
Two friends wrote topping lists as sets. Print the toppings they
**both** want (the intersection).

```python
tina = {"cheese", "mushrooms", "olives"}
tom  = {"cheese", "salami", "olives"}
```

Expected output: a set containing `cheese` and `olives` -
e.g. `{'cheese', 'olives'}` (order doesn't matter; the test checks
the set, not the printout).
""",
            "starter": """tina = {"cheese", "mushrooms", "olives"}
tom = {"cheese", "salami", "olives"}

# TODO: print the intersection
""",
            "hints": [
                "The 'in both bags' operator is `&`.",
                "`print(tina & tom)`.",
                "One line does it.",
            ],
            "solution": """tina = {"cheese", "mushrooms", "olives"}
tom = {"cheese", "salami", "olives"}

both = tina & tom
print(both)
""",
            "explanation": "`tina & tom` keeps only toppings on both lists - cheese and olives. Mushrooms (Tina only) and salami (Tom only) fall away.\n\nWhat you learned: `a & b` answers 'what do they have in common?'.",
            "tests": [
                {"kind": "expr", "expr": "tina & tom == {'cheese', 'olives'}", "expected": "True"},
                {"kind": "assert", "code": "assert 'mushrooms' not in (tina & tom)", "desc": "mushrooms not shared"},
            ],
        },
        {
            "id": "ch07-task-1",
            "type": "task",
            "title": "Five sets of numbers",
            "difficulty": 1,
            "plain": "Build two sets of numbers, then compare them five ways.",
            "instructions": r"""
Build these five sets (exact variable names):

1. `evens` - all even numbers below 100
2. `div3` - all numbers below 100 divisible by 3
3. `both` - numbers with **both** properties
4. `either` - numbers with **at least one** property
5. `exactly_one` - numbers with **exactly one** of the two

Set comprehensions for the first two, operators for the rest.
""",
            "starter": """evens = set()       # TODO: even numbers < 100
div3 = set()        # TODO: numbers < 100 divisible by 3
both = set()        # TODO: intersection
either = set()      # TODO: union
exactly_one = set() # TODO: exactly one property
""",
            "hints": [
                "`{n for n in range(100) if n % 2 == 0}` builds evens - same pattern for div3.",
                "`both = evens & div3`, `either = evens | div3`.",
                "Exactly-one is `either - both`.",
            ],
            "solution": """evens = {n for n in range(100) if n % 2 == 0}
div3 = {n for n in range(100) if n % 3 == 0}
both = evens & div3
either = evens | div3
exactly_one = either - both
""",
            "explanation": "Two comprehensions build the base sets (`% 2 == 0` = even, `% 3 == 0` = divisible by 3). Then pure set algebra: `&` keeps numbers divisible by 6, `|` everything matching either rule, and removing the overlap from the union leaves exactly the numbers satisfying just one rule.\n\nWhat you learned: &, | and - turn membership questions into one-liners.",
            "tests": [
                {"kind": "expr", "expr": "len(evens)", "expected": "50"},
                {"kind": "expr", "expr": "len(div3)", "expected": "34"},
                {"kind": "expr", "expr": "len(both)", "expected": "17"},
                {"kind": "expr", "expr": "len(either)", "expected": "67"},
                {"kind": "expr", "expr": "len(exactly_one)", "expected": "50"},
                {"kind": "assert", "code": "assert 6 in both and 4 in exactly_one and 2 not in div3",
                 "desc": "membership checks: 6 in both, 4 in exactly_one, 2 not in div3"},
            ],
        },
        {
            "id": "ch07-task-2",
            "type": "task",
            "title": "Dice until a repeat",
            "difficulty": 2,
            "plain": "Roll a die until a number shows up twice - a set tracks what was rolled.",
            "instructions": r"""
Roll a die until a number occurs for the **second** time. Every roll
is printed on its own line and added to the sum (the repeat counts
too). Then print `You rolled X a second time. Final sum: S`.

Example - with `random.seed(42)` the rolls are fixed, so your
output must look exactly like this:

```
6
1
1
You rolled 1 a second time. Final sum: 8
```

Use `random.seed(42)` before the first roll (deterministic!) and
`randint(1, SIDES)` per roll. Keep rolled numbers in a `set` -
`in` checks are what sets are made for.
""",
            "starter": """from random import randint, seed

SIDES = 6   # sides of the die
seed(42)

rolled = set()
total = 0
# TODO: roll until a number repeats
""",
            "hints": [
                "`while True:` - roll `randint(1, SIDES)`, print it, add to total.",
                "If `n in rolled` -> print the final message and `break`.",
                "Otherwise `rolled.add(n)` and the loop continues.",
            ],
            "solution": """from random import randint, seed

SIDES = 6
seed(42)

rolled = set()
total = 0
while True:
    n = randint(1, SIDES)
    print(n)
    total += n
    if n in rolled:
        print(f"You rolled {n} a second time. Final sum: {total}")
        break
    rolled.add(n)
""",
            "explanation": "The set `rolled` answers 'have we seen this?' instantly - `n in rolled` is the stop check, `rolled.add(n)` records new faces. `seed(42)` makes the dice follow a fixed script (so the test always sees the same rolls), and `break` ends the while-True loop on the repeat.\n\nWhat you learned: `in` on a set is the textbook 'already seen?' check.",
            "tests": [
                {"kind": "program",
                 "expected": "You rolled 1 a second time. Final sum: 8",
                 "match": "lines"},
            ],
        },
        {
            "id": "ch07-task-3",
            "type": "task",
            "title": "Rook moves",
            "difficulty": 2,
            "plain": "Collect every square a rook can reach - a set of targets.",
            "instructions": r"""
A rook on square `pos` (e.g. `"C4"`) can move along its whole file and
its whole rank. Collect all target squares in a set `moves` -
excluding `pos` itself. Squares look like `"C4"`: file `A`-`H`, then
rank `1`-`8`.

`moves` must contain exactly **14** squares.
""",
            "starter": """pos = "C4"

moves = set()
# TODO: add all target squares of a rook on pos
""",
            "hints": [
                "`pos[0]` is the file letter, `pos[1]` the rank digit.",
                "Same file: `{pos[0] + str(r) for r in range(1, 9)}`.",
                "Same rank: `{f + pos[1] for f in 'ABCDEFGH'}` - union them (`|=`), then `discard(pos)`.",
            ],
            "solution": """pos = "C4"

moves = {pos[0] + str(r) for r in range(1, 9)}
moves |= {f + pos[1] for f in "ABCDEFGH"}
moves.discard(pos)
""",
            "explanation": "Two comprehensions build the two directions: the C-file squares C1-C8 and the rank-4 squares A4-H4. `|=` merges them (C4 is in both but sets dedupe it to one), and `discard` removes the starting square - 8 + 8 - 1 - 1 = 14 targets.\n\nWhat you learned: `discard` removes without erroring on missing elements.",
            "tests": [
                {"kind": "expr", "expr": "len(moves)", "expected": "14"},
                {"kind": "assert", "code": "assert 'C8' in moves and 'H4' in moves and 'A4' in moves",
                 "desc": "'C8', 'H4', 'A4' in moves"},
                {"kind": "assert", "code": "assert 'C4' not in moves and 'B3' not in moves",
                 "desc": "'C4' and 'B3' not in moves"},
            ],
        },
        {
            "id": "ch07-task-4",
            "type": "task",
            "title": "Rook vs pawn",
            "difficulty": 2,
            "plain": "Can the rook grab the pawn? Same column or same row says yes.",
            "instructions": r"""
A white rook stands on `rook_pos`, a black pawn on `pawn_pos`.

Write `can_capture(rook_pos, pawn_pos)` returning `True` when the rook
reaches the pawn in one move - same file or same rank:

```python
can_capture("C4", "C7")   # True  (same file)
can_capture("C4", "G4")   # True  (same rank)
can_capture("C4", "B6")   # False
```
""",
            "starter": """def can_capture(rook_pos, pawn_pos):
    # TODO: True iff rook and pawn share file or rank
    pass
""",
            "hints": [
                "`rook_pos[0]` is the file, `rook_pos[1]` the rank - same for the pawn.",
                "Two comparisons joined by `or`.",
                "The `or` expression already gives True/False - return it.",
            ],
            "solution": """def can_capture(rook_pos, pawn_pos):
    return rook_pos[0] == pawn_pos[0] or rook_pos[1] == pawn_pos[1]
""",
            "explanation": "A rook moves in straight lines, so capture is possible exactly when a coordinate matches: index 0 compares files, index 1 compares ranks, `or` accepts either. The combined comparison is already a True/False value, so it can be returned directly.\n\nWhat you learned: many yes/no questions collapse into one boolean expression.",
            "tests": [
                {"kind": "expr", "expr": "can_capture('C4', 'C7')", "expected": "True"},
                {"kind": "expr", "expr": "can_capture('C4', 'G4')", "expected": "True"},
                {"kind": "expr", "expr": "can_capture('C4', 'B6')", "expected": "False"},
                {"kind": "expr", "expr": "can_capture('A1', 'H8')", "expected": "False"},
            ],
        },
        {
            "id": "ch07-boss",
            "type": "task",
            "title": "Guest list clash",
            "difficulty": 3,
            "boss": True,
            "plain": "Two party lists arrived - work out who's coming, who's double-booked, who's missing.",
            "instructions": r"""
**BOSS MISSION - the party clash.**

Ada and Ben each wrote an invitation set. The class roster is a third
set. Print this exact report:

```
Both parties: 2
Only Ada: ['Sandra', 'Tina']
Only Ben: ['Mike', 'Theo']
Anyone: 6
Not invited: ['Otto', 'Zara']
```

- `Both parties` - count of `ada & ben`
- `Only Ada` / `Only Ben` - **sorted lists** of the two differences
- `Anyone` - count of the union
- `Not invited` - sorted list of class members in neither set
""",
            "starter": """ada = {"Tina", "Tom", "Anna", "Sandra"}
ben = {"Anna", "Tom", "Mike", "Theo"}
klasse = {"Tina", "Tom", "Anna", "Sandra", "Mike", "Theo", "Zara", "Otto"}

# TODO: print the 5-line report
""",
            "example": """Set maths with music tastes:

```python
anna = {"rock", "pop"}
ben = {"pop", "jazz"}
print("both:", anna & ben)
print("all:", anna | ben)
```
""",

            "hints": [
                "`ada & ben` is the overlap - `len` it. The only-* sets are `ada - ben` and `ben - ada`.",
                "`sorted(set)` turns a set into an alphabetical list for printing.",
                "Neither = `klasse - (ada | ben)`.",
            ],
            "solution": """ada = {"Tina", "Tom", "Anna", "Sandra"}
ben = {"Anna", "Tom", "Mike", "Theo"}
klasse = {"Tina", "Tom", "Anna", "Sandra", "Mike", "Theo", "Zara", "Otto"}

print(f"Both parties: {len(ada & ben)}")
print(f"Only Ada: {sorted(ada - ben)}")
print(f"Only Ben: {sorted(ben - ada)}")
print(f"Anyone: {len(ada | ben)}")
print(f"Not invited: {sorted(klasse - (ada | ben))}")
""",
            "explanation": "Five lines, all set algebra: `&` finds the double-invited, `-` finds the exclusive guests each way, `|` counts everyone invited, and subtracting the union from the class leaves the uninvited. `sorted` turns each answer set into a printable alphabetical list.\n\nWhat you learned: `sorted(set)` is the standard way to show a set's contents readably.",
            "tests": [
                {"kind": "program",
                 "expected": "Both parties: 2\nOnly Ada: ['Sandra', 'Tina']\nOnly Ben: ['Mike', 'Theo']\nAnyone: 6\nNot invited: ['Otto', 'Zara']",
                 "match": "exact"},
            ],
        },
    ],
}
