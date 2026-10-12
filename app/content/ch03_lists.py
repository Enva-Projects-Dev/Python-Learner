"""Kapitel 3 - Listen, Tuples & Comprehensions."""

CHAPTER = {
    "id": "ch03",
    "number": 3,
    "title": "Lists, Tuples & Comprehensions",
    "summary": "Rows of lockers (lists), unchangeable records (tuples) and one-line list builders.",
    "items": [
        {
            "id": "ch03-lesson",
            "type": "lesson",
            "title": "Lists: rows of lockers",
            "body": r"""
## A list is a row of numbered lockers

A **list** keeps many things in one variable, in order. Each thing sits
in a numbered slot - counting starts at **0**:

```python
numbers = [2, 3, 5, 7, 11, 13]
names = ["Anna", "Berta", "Carla", "Doris"]

print(numbers[0])     # first locker: 2
print(names[3])       # Doris - slot 3 is the 4th!
numbers[0] = 42       # lockers can be refilled ("mutable")
print(len(names))     # 4 lockers in total
```

> **Think of it like...** a row of lockers. `names[2]` opens locker
> number 2 - the third one, since the first is number 0.

Adding, removing and sorting:

```python
names = ["Anna", "Berta", "Carla"]
names.append("Doris")            # add at the end
names = names + ["Emilia"]       # glue another list on
names.remove("Carla")            # take out by value
names.sort()                     # sort in place
print(names[-1])                 # -1 = the last locker
```

## Slicing: cut out a piece

`list[start:stop:step]` copies out a section - `stop` is **not**
included:

```python
names = ["Anna", "Berta", "Carla", "Doris", "Emilia"]
print(names[1:3])      # ['Berta', 'Carla'] - lockers 1 and 2
print(names[::2])      # every 2nd: Anna, Carla, Emilia
print(names[::-1])     # the whole row backwards
```

## Lists inside lists

Lockers can contain whole rows of lockers:

```python
grid = [[0, 1], [2, 3], [4, 5]]
print(grid[1][0])    # 2 - row 1, then its locker 0
```

## Walking the row: for, enumerate, zip

```python
names = ["Anna", "Berta", "Carla"]
for name in names:                 # visit each element
    print("Hello", name)

for i, name in enumerate(names):   # index + element together
    print(f"{i}: {name}")
```

`zip` walks two lists side by side like closing a zipper:

```python
first = ["Anna", "Berta"]
last = ["Adler", "Baer"]
for f, l in zip(first, last):
    print(f, l)                    # Anna Adler, Berta Baer
```

## Built-ins that love lists

```python
numbers = [4, 1, 9, 2]
print(len(numbers))      # 4   - how many lockers
print(min(numbers))      # 1   - smallest
print(max(numbers))      # 9   - biggest
print(sum(numbers))      # 16  - all added up
print(sorted(numbers))   # [1, 2, 4, 9] - a NEW sorted list
print(numbers)           # still unsorted - sorted() doesn't change it
```

> **Watch out** - `sorted(numbers)` hands you a *new* list and leaves
> the old one alone, while `numbers.sort()` rearranges the original.

## Try it yourself

- Make a list of your three favourite foods and print the second one.
- Print the list backwards with one slice.
- Use `enumerate` to number your foods starting at 1.

## Key words

| Word | Meaning |
|---|---|
| list | an ordered row of values in `[ ]` |
| index | the number of a locker, starting at 0 |
| slice | a cut-out piece `a[start:stop:step]` |
| append / remove / sort | add at end / delete by value / sort |
| enumerate / zip | loop with index / loop two lists together |
""",
        },
        {
            "id": "ch03-lesson-2",
            "type": "lesson",
            "title": "Tuples, copies and comprehensions",
            "body": r"""
## Tuples: sealed records

A **tuple** is like a list you cannot change - a sealed envelope. It
uses round brackets:

```python
person = ("Harry", "Potter", 11)
print(person[0])
# person[0] = "James"   # ERROR - tuples are immutable!

first, last, age = person   # unpacking into three boxes
print(first, age)

a, b = 1, 2
a, b = b, a                 # the famous one-line swap
print(a, b)
```

> **Think of it like...** a list is a pencil-written list you can erase
> and edit; a tuple is the same list carved in stone.

## Copies: a second name is not a copy!

```python
a = [1, 2, 3]
b = a        # NOT a copy - just a second label on the same list
c = a[:]     # real copy
a[0] = 99
print(b)     # [99, 2, 3] - changed!
print(c)     # [1, 2, 3] - untouched
```

> **Watch out** - `b = a` puts a second sticker on the same box. To get
> an independent copy use `a[:]` or `list(a)`.

## Comprehensions: build a list in one line

A **list comprehension** describes *what* you want instead of writing a
loop:

```python
squares = [x**2 for x in range(10, 20)]
print(squares)
```

Pattern: `[ expression for var in iterable if condition ]`

```python
names = ["Anna", "Berta", "Carla", "Doris"]

# the loop way
result = []
for name in names:
    if len(name) > 4:
        result.append(name.upper())

# the one-line way - same result
result = [name.upper() for name in names if len(name) > 4]
print(result)
```

## A few string helpers

Comprehension tasks often need the same handful of string methods
(more in the next chapter - just meet them here):

```python
name = "  obelIX  "
print(name.strip())        # 'obelIX' - edges shaved
print(name.strip().lower())  # 'obelix'
print(name.strip().title())  # 'Obelix' - capitalised
print("asterix".endswith("x"))    # True
print("hello".startswith("he"))   # True
```

## Reading a text file

`open(path, encoding="utf-8")` opens a file; looping over it hands you
one line at a time. `with` closes it for you automatically:

```python
with open("adressen.txt", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(";")
        print(parts[0], "lives in", parts[2])
```

> **What happens here**
>
> - the `for` visits every line of the file, one after another
> - `line.strip()` removes the invisible newline at the end
> - `.split(";")` cuts each line at the semicolons into a list
> - `parts[0]` is the first field, `parts[2]` the third

## Try it yourself

- Swap two variables in one line.
- Build `[x * 10 for x in range(5)]` and predict the result before Run.

## Key words

| Word | Meaning |
|---|---|
| tuple | an unchangeable record in `( )` |
| unpacking | `a, b = (1, 2)` - one value per box |
| comprehension | one-line list builder `[x for x in ...]` |
""",
        },
        {
            "id": "ch03-quiz-1",
            "type": "quiz",
            "title": "Slicing",
            "question": "For `xs = [10, 20, 30, 40, 50]`, what is `xs[1:4]`?",
            "options": ["[10, 20, 30]", "[20, 30, 40]", "[20, 30, 40, 50]", "[10, 20, 30, 40]"],
            "answer": 1,
            "explanation": "The slice starts at index 1 (that's 20 - remember index 0 is first!) and stops *before* index 4. So 20, 30, 40. Including the 50 is the classic trap - the stop number is never part of the slice.",
        },
        {
            "id": "ch03-quiz-2",
            "type": "quiz",
            "title": "Two stickers, one box",
            "question": "After `a = [1, 2]; b = a; b.append(3)`, what is `a`?",
            "options": ["[1, 2]", "[1, 2, 3]", "Error", "[3]"],
            "answer": 1,
            "explanation": "`b = a` puts a second name on the *same* list - appending through b changes what a sees. For a real copy you need `b = a[:]`.",
        },
        {
            "id": "ch03-quiz-3",
            "type": "quiz",
            "title": "Comprehension",
            "question": "What does `[x * x for x in range(4)]` produce?",
            "options": ["[0, 1, 4, 9]", "[1, 4, 9, 16]", "[0, 1, 2, 3]", "[4, 9, 16]"],
            "answer": 0,
            "explanation": "range(4) gives 0,1,2,3 and each gets squared: 0, 1, 4, 9. '[1, 4, 9, 16]' would need `range(1, 5)` - an easy off-by-one.",
        },
        {
            "id": "ch03-quiz-4",
            "type": "quiz",
            "title": "Tuples",
            "question": "What happens for `t = (1, 2); t[0] = 9`?",
            "options": ["t becomes (9, 2)", "an error - tuples are immutable", "t becomes [9, 2]", "nothing"],
            "answer": 1,
            "explanation": "Tuples are sealed - changing an element raises a TypeError. Only lists allow `t[0] = 9`.",
        },
        {
            "id": "ch03-warm-1",
            "type": "task",
            "title": "Locker check",
            "difficulty": 1,
            "plain": "Grab things out of a list by their locker numbers.",
            "instructions": r"""
For the given list, print three lines:

1. the first element
2. the last element
3. how many elements the list has

Expected output:

```
pen
ruler
5
```
""",
            "starter": """items = ["pen", "book", "glue", "eraser", "ruler"]
# TODO: print first, last and the length
""",
            "example": """Try the same trick on a different problem:

```python
tools = ["hammer", "nail"]
print(tools[0])
print(len(tools))
```
""",

            "hints": [
                "Lockers count from 0: `items[0]` is first.",
                "`items[-1]` is the last one - no counting needed.",
                "`len(items)` is the locker count.",
            ],
            "solution": """items = ["pen", "book", "glue", "eraser", "ruler"]
print(items[0])
print(items[-1])
print(len(items))""",
            "explanation": "Index 0 opens the first locker, index -1 the last, and `len` counts the lockers. 'ruler' is at index 4 - the last of 5 - which is why -1 finds it without any counting.\n\nWhat you learned: `list[i]` picks, `list[-1]` takes the last, `len(list)` counts.",
            "tests": [
                {"kind": "program", "expected": "pen\nruler\n5",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch03-warm-2",
            "type": "task",
            "title": "Grow the list",
            "difficulty": 1,
            "plain": "Put two more names into the list, then print it.",
            "instructions": r"""
1. Append `"Zoe"` to the list with `.append(...)`.
2. Append `"Max"` the same way.
3. Print the whole list.

Expected output:

```
['Ada', 'Tom', 'Zoe', 'Max']
```
""",
            "starter": """friends = ["Ada", "Tom"]
# TODO: append "Zoe" and "Max", then print friends
""",
            "example": """Try the same trick on a different problem:

```python
bag = ["map"]
bag.append("rope")
for thing in bag:
    print("packed:", thing)
```
""",

            "hints": [
                "`list.append(x)` adds x at the end.",
                "Two appends, one after the other.",
                "`print(friends)` shows the list as Python sees it.",
            ],
            "solution": """friends = ["Ada", "Tom"]
friends.append("Zoe")
friends.append("Max")
print(friends)""",
            "explanation": "`append` tacks a new locker onto the end of the row - twice here, so the list grows from 2 to 4 elements. Printing a list shows it with brackets and quotes, exactly how Python stores it.\n\nWhat you learned: `append` grows a list at the end.",
            "tests": [
                {"kind": "program",
                 "expected": "['Ada', 'Tom', 'Zoe', 'Max']",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch03-warm-3",
            "type": "task",
            "title": "Double each",
            "difficulty": 1,
            "plain": "Double every number in a list with a comprehension.",
            "instructions": "Given `numbers = [1, 2, 3]`, build a new list where every number is doubled and print it. Output: `[2, 4, 6]`.",
            "starter": """numbers = [1, 2, 3]
doubled = [x * 2 for x in numbers]
# TODO: print the doubled list
""",
            "example": """Halving a list works identically:

```python
prices = [2, 4, 6]
print([p // 2 for p in prices])
```
""",
            "hints": [
                "A comprehension is a for-loop in brackets: `[x * 2 for x in numbers]`.",
                "Store it in a variable, then print that variable.",
                "`print(doubled)` shows `[2, 4, 6]`.",
            ],
            "solution": """numbers = [1, 2, 3]
doubled = [x * 2 for x in numbers]
print(doubled)""",
            "explanation": "A list comprehension builds a fresh list in one line: take each x out of numbers and put x * 2 into the new list. Nothing is modified in the original - numbers stays [1, 2, 3] while doubled becomes [2, 4, 6].",
            "tests": [
                {"kind": "program", "expected": "[2, 4, 6]"},
            ],
        },
        {
            "id": "ch03-task-1",
            "type": "task",
            "title": "Indexing and slicing",
            "difficulty": 1,
            "plain": "Pick exact pieces out of the names list - single lockers and slices.",
            "instructions": r"""
For the given list, print each of these on its own line:

1. the 7th element
2. the first three elements (positions 0 to 2) - as a list
3. the second-to-last element
4. every second element - as a list
5. the middle element

Expected output:

```
Gabi
['Anna', 'Berta', 'Carla']
Hannah
['Anna', 'Carla', 'Emilia', 'Gabi', 'Iris']
Emilia
```
""",
            "starter": """print(names[6])                    # locker number 6
# TODO: print the slice for the first three names: names[0:3]
# TODO: print the second name from the end (negative index)
# TODO: print every second name with names[::2]
# TODO: middle = len(names) // 2, print names[middle]
""",
            "example": """Slice gymnastics on a small list:

```python
letters = ["a", "b", "c", "d", "e"]
print(letters[1:3])    # b, c
print(letters[::2])    # a, c, e
```
""",

            "hints": [
                "Counting starts at 0 - the 7th name is `names[6]`, the first three are `names[0:3]`.",
                "`names[-2]` is second-to-last; `names[::2]` every second one.",
                "Middle index: `len(names) // 2`.",
            ],
            "solution": """names = ["Anna", "Berta", "Carla", "Doris", "Emilia", "Franziska", "Gabi", "Hannah", "Iris"]
print(names[6])
print(names[0:3])
print(names[-2])
print(names[::2])
middle = len(names) // 2
print(names[middle])
""",
            "explanation": "Five different ways to look into the list: `names[6]` is the 7th locker (counting from 0), `names[0:3]` a slice of the first three, `-2` counts from the back, `::2` takes every second locker, and `len // 2` finds the middle of 9 - index 4, Emilia.\n\nWhat you learned: indices pick one element, slices pick whole sections.",
            "tests": [
                {"kind": "program",
                 "expected": "Gabi\n['Anna', 'Berta', 'Carla']\nHannah\n['Anna', 'Carla', 'Emilia', 'Gabi', 'Iris']\nEmilia",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch03-task-2",
            "type": "task",
            "title": "Largest, average, median",
            "difficulty": 2,
            "plain": "Three questions about a number list: biggest, average, middle.",
            "instructions": r"""
For the given list of numbers, compute and print:

1. the largest element - **without `max()`**, use a loop
2. the average
3. the median (the middle element of the *sorted* list)

Print exactly:

```
Largest element: 99
Average: 12.041373247863246
Median: 3.14159
```
""",
            "starter": """largest = numbers[0]
total = 0
for n in numbers:
    total += n
    if n > largest:
        largest = n
print("Largest element:", largest)
# TODO: print "Average:" -> total / len(numbers)
# TODO: ordered = sorted(numbers), the median is ordered[len(ordered) // 2]
""",
            "example": """Finding the warmest day by hand:

```python
temps = [4, 9, 2, 7]
big = temps[0]
for t in temps:
    if t > big:
        big = t
print(big)
```
""",

            "hints": [
                "Champion trick: `largest = numbers[0]`, then replace it whenever a bigger number shows up while you also add to `total`.",
                "Average = `total / len(numbers)`.",
                "`sorted(numbers)` makes a sorted copy - median is `ordered[len(ordered) // 2]`.",
            ],
            "solution": """numbers = [2, 3.14159, -12, 99, 42/13, 0.0, 10, -1, 4]

largest = numbers[0]
total = 0
for n in numbers:
    total += n
    if n > largest:
        largest = n

print("Largest element:", largest)
print("Average:", total / len(numbers))

ordered = sorted(numbers)
middle = len(ordered) // 2
print("Median:", ordered[middle])
""",
            "explanation": "One loop does two jobs at once: `total += n` accumulates the sum for the average, and the champion check `if n > largest` keeps track of the biggest seen. The median needs sorted data - `sorted()` gives a copy - and `len // 2` is its middle index (9 elements -> index 4).\n\nWhat you learned: a single loop can gather several answers at once.",
            "tests": [
                {"kind": "program",
                 "expected": "Largest element: 99\nAverage: 12.041373247863246\nMedian: 3.14159",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch03-task-3",
            "type": "task",
            "title": "Three new lists",
            "difficulty": 2,
            "plain": "Fill three lists in one walk: squares, numbers between 30 and 50, and the odd ones.",
            "instructions": r"""
From `numbers`, build three **new** lists inside one loop:

- `squares` - each number squared
- `between_30_50` - only numbers with `30 < n < 50`
- `odd` - only the odd numbers

The variables must be named exactly `squares`, `between_30_50`, `odd`.
Print all three at the end.
""",
            "starter": """squares = []
between_30_50 = []
odd = []
for n in numbers:
    squares.append(n * n)
    # TODO: if 30 < n < 50 -> between_30_50.append(n)
    # TODO: if n % 2 == 1 -> odd.append(n)
# TODO: print all three lists
""",
            "example": """Sorting items into two baskets:

```python
nums = [1, 2, 3, 4]
big = []
small = []
for n in nums:
    if n > 2:
        big.append(n)
    else:
        small.append(n)
print(big, small)
```
""",

            "hints": [
                "Every n goes into squares as `n * n`; the other two only under conditions.",
                "`30 < n < 50` is a valid chained comparison; odd means `n % 2 == 1`.",
                "One `for n in numbers:` with one append + two ifs inside.",
            ],
            "solution": """numbers = [13, 47, 4, 12, 23, 17, 83, 45, 52, 63, 37, 94, 49, 8, 11, 31, 44, 72, 47]

squares, between_30_50, odd = [], [], []
for n in numbers:
    squares.append(n * n)
    if 30 < n < 50:
        between_30_50.append(n)
    if n % 2 == 1:
        odd.append(n)

print(squares)
print(between_30_50)
print(odd)
""",
            "explanation": "Every element visits the loop once and gets sorted into the right buckets: always the squared value into `squares`, conditionally into the other two. `30 < n < 50` checks both bounds in one go, and `n % 2 == 1` is the odd test.\n\nWhat you learned: one pass can fill several result lists.",
            "tests": [
                {"kind": "expr", "expr": "squares",
                 "expected": "[169, 2209, 16, 144, 529, 289, 6889, 2025, 2704, 3969, 1369, 8836, 2401, 64, 121, 961, 1936, 5184, 2209]"},
                {"kind": "expr", "expr": "between_30_50",
                 "expected": "[47, 45, 37, 49, 31, 44, 47]"},
                {"kind": "expr", "expr": "odd",
                 "expected": "[13, 47, 23, 17, 83, 45, 63, 37, 49, 11, 31, 47]"},
            ],
        },
        {
            "id": "ch03-task-4",
            "type": "task",
            "title": "Palindrome check",
            "difficulty": 2,
            "plain": "Does a sequence read the same forwards and backwards?",
            "instructions": r"""
For each sequence in `lists`, print whether it is a **palindrome** -
the same forwards and backwards:

```
[1, 2, 3, 2, 1] is a palindrome.
[1, 2, 3, 1] is not a palindrome.
```

The last entry is a **string**, not a list - slicing works on strings
too (`"LAGERREGAL"` is a German palindrome word, by the way!).
""",
            "starter": """for seq in lists:
    verdict = "a" if seq[::-1] == seq else "not a"
    # TODO: print f"{seq} is {verdict} palindrome."
""",
            "example": """Check a word against its mirror:

```python
for w in ["wow", "nope"]:
    print(w, w[::-1], w == w[::-1])
```
""",

            "hints": [
                "`seq[::-1]` is the sequence backwards - compare it with the original.",
                "A conditional expression picks the word: `\"a\" if seq[::-1] == seq else \"not a\"`.",
                "The whole line is one f-string: `f\"{seq} is {verdict} palindrome.\"`.",
            ],
            "solution": """lists = [[1, 2, 3, 2, 1], [1, 2, 3, 1], ["ich", "bin", "ich"], "LAGERREGAL"]

for seq in lists:
    verdict = "a" if seq[::-1] == seq else "not a"
    print(f"{seq} is {verdict} palindrome.")
""",
            "explanation": "`[::-1]` is the backwards slice - comparing it with the original answers the palindrome question in one step. The conditional expression picks `a` or `not a`, and the f-string assembles the sentence. It works for lists *and* strings because slicing is shared.\n\nWhat you learned: `x if cond else y` chooses between two values inline.",
            "tests": [
                {"kind": "program",
                 "expected": "[1, 2, 3, 2, 1] is a palindrome.\n[1, 2, 3, 1] is not a palindrome.\n['ich', 'bin', 'ich'] is a palindrome.\nLAGERREGAL is a palindrome.",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch03-task-5",
            "type": "task",
            "title": "Comprehension: squares & filters",
            "difficulty": 1,
            "plain": "Same three lists as before - now built in one line each.",
            "instructions": r"""
Build the same three lists as the earlier task, but each with **one
list comprehension**:

- `squares` - the squares
- `between_30_50` - only `30 < n < 50`
- `odd` - only odd numbers
""",
            "starter": """squares = [n * n for n in numbers]
# TODO: between_30_50 = [n for n in numbers if 30 < n < 50]
# TODO: odd = [n for n in numbers if n % 2 == 1]
# TODO: print all three lists
""",
            "example": """Filter with a comprehension:

```python
nums = [5, 12, 17, 22]
evens = [n for n in nums if n % 2 == 0]
print(evens)
```
""",

            "hints": [
                "Transform: `[expr for n in numbers]`; filter: `[n for n in numbers if cond]`.",
                "`squares = [n * n for n in numbers]`.",
                "The `if` goes at the end of each comprehension.",
            ],
            "solution": """numbers = [13, 47, 4, 12, 23, 17, 83, 45, 52, 63, 37, 94, 49, 8, 11, 31, 44, 72, 47]

squares = [n * n for n in numbers]
between_30_50 = [n for n in numbers if 30 < n < 50]
odd = [n for n in numbers if n % 2 == 1]
""",
            "explanation": "The comprehension packs the whole loop into one line: `n * n` is the expression computed per element, `for n in numbers` the source, and the optional `if` at the end filters. Same result as the loop version - just shorter to write and read.\n\nWhat you learned: comprehensions turn 'build a list' loops into one-liners.",
            "tests": [
                {"kind": "expr", "expr": "squares",
                 "expected": "[169, 2209, 16, 144, 529, 289, 6889, 2025, 2704, 3969, 1369, 8836, 2401, 64, 121, 961, 1936, 5184, 2209]"},
                {"kind": "expr", "expr": "between_30_50",
                 "expected": "[47, 45, 37, 49, 31, 44, 47]"},
                {"kind": "expr", "expr": "odd",
                 "expected": "[13, 47, 23, 17, 83, 45, 63, 37, 49, 11, 31, 47]"},
            ],
        },
        {
            "id": "ch03-task-6",
            "type": "task",
            "title": "Comprehension: Gallic names",
            "difficulty": 1,
            "plain": "Pick the names ending in x and fix their capital letters.",
            "instructions": r"""
Build `heroes`: the names from `gauls` that end with `x` - written
properly (first letter capital, rest lowercase).

Expected: `['Asterix', 'Obelix', 'Miraculix', 'Troubadix']`

One comprehension, using string methods.
""",
            "starter": """heroes = [name.title() for name in gauls]
# TODO: heroes works, but keeps EVERYONE. Add the filter at the end:
#       ... if name.lower().endswith('x')
print(heroes)
""",
            "example": """Keep only names ending in o:

```python
pets = ["Rex", "Minka", "Bello"]
heroes = [p for p in pets if p.endswith("o")]
print(heroes)
```
""",

            "hints": [
                "Test case-insensitively with `name.lower().endswith('x')`.",
                "`name.title()` fixes the capitalisation.",
                "Pattern: `[name.title() for name in gauls if ...]`.",
            ],
            "solution": """gauls = ["asterix", "OBELIX", "Miraculix", "CaEsaR", "TROUBADIX", "Gutemine"]

heroes = [name.title() for name in gauls if name.lower().endswith('x')]
""",
            "explanation": "The `if` part lower-cases each name only for the *test*, so 'OBELIX' also passes the ends-with-x check. The expression `name.title()` then writes the name with a capital first letter. Filtering and fixing happen in the same comprehension.\n\nWhat you learned: the test and the transformation can use different methods.",
            "tests": [
                {"kind": "expr", "expr": "heroes",
                 "expected": "['Asterix', 'Obelix', 'Miraculix', 'Troubadix']"},
            ],
        },
        {
            "id": "ch03-task-7",
            "type": "task",
            "title": "Comprehension: name swap",
            "difficulty": 2,
            "plain": "Turn 'First Last' names into 'Last, First' format.",
            "instructions": r"""
Turn `["Harry Potter", "Albus Dumbledore", "Severus Snape"]` into
`['Potter, Harry', 'Dumbledore, Albus', 'Snape, Severus']`.

Store the result in `formatted` - comprehensions welcome.
""",
            "starter": """parts = [name.split() for name in names]
# TODO: formatted = [f"{p[1]}, {p[0]}" for p in parts]
# TODO: print the formatted list
""",
            "example": """Flip two fields after split:

```python
raw = "Meyer Frank"
first, last = raw.split()[::-1]
print(f"{first}, {last}")
```
""",

            "hints": [
                "`name.split()` cuts a name into `[first, last]`.",
                "You can split in one comprehension, then format in a second.",
                "Final f-string: `f\"{p[1]}, {p[0]}\"`.",
            ],
            "solution": """names = ["Harry Potter", "Albus Dumbledore", "Severus Snape"]

parts = [name.split() for name in names]
formatted = [f"{p[1]}, {p[0]}" for p in parts]
""",
            "explanation": "Two small steps: the first comprehension splits every name into a `[first, last]` pair, the second swaps the order inside an f-string. You could do it in one line - two short lines are easier to read.\n\nWhat you learned: `split()` turns text into a list you can index.",
            "tests": [
                {"kind": "expr", "expr": "formatted",
                 "expected": "['Potter, Harry', 'Dumbledore, Albus', 'Snape, Severus']"},
            ],
        },
        {
            "id": "ch03-task-8",
            "type": "task",
            "title": "Comprehension: flat 5x5",
            "difficulty": 1,
            "plain": "The whole 5x5 times table as one flat list.",
            "instructions": r"""
Build the flat multiplication table `1..5 x 1..5` as one list:

`[1, 2, 3, 4, 5, 2, 4, 6, 8, 10, ..., 25]`

Store it in `table` - one comprehension with **two** `for` parts.
""",
            "starter": """# a comprehension with TWO for-parts does both loops at once:
#   [a * b for a in range(1, 6) for b in range(1, 6)]
table = []     # TODO: build it with that comprehension
print(table)
""",
            "example": """Two loops in one comprehension:

```python
pairs = [a + b for a in range(3) for b in range(3)]
print(pairs)
```
""",

            "hints": [
                "Two for-parts act like nested loops: `for a ... for b ...`.",
                "a is the outer (row), b the inner - check the expected order: row 1 first.",
                "`[a * b for a in range(1, 6) for b in range(1, 6)]` gives 25 values.",
            ],
            "solution": """table = [a * b for a in range(1, 6) for b in range(1, 6)]
""",
            "explanation": "Two `for` parts nest inside the comprehension: for each `a` (the row), `b` runs 1-5 - exactly the order of the flat table. 5 x 5 = 25 products.\n\nWhat you learned: comprehensions can nest loops just like `for` statements.",
            "tests": [
                {"kind": "expr", "expr": "table",
                 "expected": "[1, 2, 3, 4, 5, 2, 4, 6, 8, 10, 3, 6, 9, 12, 15, 4, 8, 12, 16, 20, 5, 10, 15, 20, 25]"},
            ],
        },
        {
            "id": "ch03-task-9",
            "type": "task",
            "title": "Comprehension: nested 5x5",
            "difficulty": 2,
            "plain": "The same table - now as a list of rows.",
            "instructions": r"""
Build the 5x5 table as a **nested** list (a list of row lists):

```
[[1, 2, 3, 4, 5],
 [2, 4, 6, 8, 10],
 [3, 6, 9, 12, 15],
 [4, 8, 12, 16, 20],
 [5, 10, 15, 20, 25]]
```

Store it in `table` - a comprehension whose element is itself a
comprehension.
""",
            "starter": """# nested comprehension = an inner comprehension inside an outer one
# inner row:   [a * b for a in range(1, 6)]
table = []     # TODO: [[inner row] for b in range(1, 6)]
for row in table:
    print(row)
""",
            "example": """A nested grid in one line:

```python
grid = [[r * c for c in range(3)] for r in range(3)]
for row in grid:
    print(row)
```
""",

            "hints": [
                "The outer comprehension produces rows - its element is a whole inner list.",
                "One row for fixed b: `[a * b for a in range(1, 6)]`.",
                "Wrap it: `[[a * b for a in range(1, 6)] for b in range(1, 6)]`.",
            ],
            "solution": """table = [[a * b for a in range(1, 6)] for b in range(1, 6)]
""",
            "explanation": "The inner comprehension builds one row for a fixed `b`; the outer one repeats that for b = 1..5 and collects the rows. The result is a grid you can index with `table[row][col]`.\n\nWhat you learned: comprehension elements can be comprehensions themselves - grids in one line.",
            "tests": [
                {"kind": "expr", "expr": "table",
                 "expected": "[[1, 2, 3, 4, 5], [2, 4, 6, 8, 10], [3, 6, 9, 12, 15], [4, 8, 12, 16, 20], [5, 10, 15, 20, 25]]"},
            ],
        },
        {
            "id": "ch03-task-10",
            "type": "task",
            "title": "Comprehension: words in a text",
            "difficulty": 2,
            "plain": "Cut a poem into clean words - no punctuation stuck to them.",
            "instructions": r"""
Extract all words from the text (the opening of Goethe's *Faust*) into
a list `words`, stripped of surrounding punctuation.

Expected: **54 words**, starting `['Habe', 'nun', 'ach', 'Philosophie', ...]`.

Tip: `split()` and `strip(string.punctuation)` do the work.
""",
            "starter": """import string
TEXT = "Programming is a craft. Practice the craft, and the code gets better."
words = []    # TODO: [word.strip(string.punctuation) for word in TEXT.split()]
# TODO: print len(words) -> "words", then the first 20 words
""",
            "example": """Shaving punctuation off words:

```python
import string
for w in "hi, you!".split():
    print(w.strip(string.punctuation))
```
""",

            "hints": [
                "`TEXT.split()` splits on any whitespace into raw words like `'Philosophie,'`.",
                "`word.strip(string.punctuation)` shaves punctuation off both ends.",
                "Combine: `[w.strip(string.punctuation) for w in TEXT.split()]`.",
            ],
            "solution": """import string

TEXT = \"\"\"
Habe nun, ach! Philosophie,
Juristerei und Medizin,
Und leider auch Theologie
Durchaus studiert, mit heissem Bemuehn.
Da steh ich nun, ich armer Tor,
Und bin so klug als wie zuvor!
Heisse Magister, heisse Doktor gar,
Und ziehe schon an die zehen Jahr
Herauf, herab und quer und krumm
Meine Schueler an der Nase herum.
\"\"\"

words = [word.strip(string.punctuation) for word in TEXT.split()]
print(len(words), "words")
""",
            "explanation": "`split()` with no argument cuts at every whitespace into raw words, but commas and exclamation marks stay attached. `strip(string.punctuation)` removes those edge characters - `string.punctuation` is a ready-made list of all of them. The comprehension applies it to every word.\n\nWhat you learned: `split` + `strip` is the basic text-cleaning combo.",
            "tests": [
                {"kind": "expr", "expr": "len(words)", "expected": "54"},
                {"kind": "expr", "expr": "words[:6]",
                 "expected": "['Habe', 'nun', 'ach', 'Philosophie', 'Juristerei', 'und']"},
            ],
        },
        {
            "id": "ch03-task-11",
            "type": "task",
            "title": "Comprehension: Faust word list",
            "difficulty": 3,
            "plain": "Do the same word-cleaning on a whole book - Goethe's Faust.",
            "instructions": r"""
The complete text of Goethe's *Faust* sits in `Goethe--Faust.txt`
(already in your program's folder).

Load it (UTF-8) and build `words`: all words, stripped of punctuation -
the same trick as the previous task, scaled up.

The list must contain **31161 words** and start:
`['Goethe', 'Faust', 'Johann', 'Wolfgang', 'von', 'Goethe', ...]`
""",
            "starter": """import string
words = []
with open("Goethe--Faust.txt", encoding="utf-8") as f:
    for line in f:
        for word in line.split():
            words.append(word.strip(string.punctuation))
# TODO: print f"{len(words)} words"
# TODO: print the first 20: words[:20]
""",
            "example": """Counting lines of a small file:

```python
with open("adressen.txt", encoding="utf-8") as f:
    count = len(f.readlines())
print(count, "lines")
```
""",

            "hints": [
                "`open(\"Goethe--Faust.txt\", encoding=\"utf-8\")` - a `for` loop reads it line by line.",
                "Per line: `line.split()`, then strip each word as before.",
                "Or in one comprehension: `[w.strip(string.punctuation) for line in f for w in line.split()]`.",
            ],
            "solution": """import string

words = []
with open("Goethe--Faust.txt", encoding="utf-8") as f:
    for line in f:
        for word in line.split():
            words.append(word.strip(string.punctuation))

print(f"{len(words)} words")
print(words[:20])
""",
            "explanation": "Files behave like lists of lines - `for line in f` walks the whole book. Every line gets split and every word stripped, exactly like the small poem task; the only new piece is `with open(...)` which opens the file and closes it safely. 31161 words prove it worked on real data.\n\nWhat you learned: looping over a file gives you its lines one by one.",
            "tests": [
                {"kind": "expr", "expr": "len(words)", "expected": "31161"},
                {"kind": "expr", "expr": "words[:6]",
                 "expected": "['Goethe', 'Faust', 'Johann', 'Wolfgang', 'von', 'Goethe']"},
            ],
        },
        {
            "id": "ch03-boss",
            "type": "task",
            "title": "Class list report",
            "difficulty": 3,
            "boss": True,
            "plain": "Turn a class list into a mini report card.",
            "instructions": r"""
**BOSS MISSION - the class report.**

A class list holds `(name, score)` tuples. Print this exact report:

```
Students: 4
Best: Max (97)
Average: 78.5
Passed: ['Ada', 'Max', 'Tom']
```

- `Best`: the name and score of the top student - find it with a loop,
  not `max()`
- `Average`: sum of scores ÷ count (a float, printed as is)
- `Passed`: a list of names with score >= 50, in list order -
  a comprehension is perfect
""",
            "starter": """students = [("Ada", 92), ("Ben", 40), ("Max", 97), ("Tom", 85)]

# TODO: print the 4-line report
""",
            "example": """A mini report over a small dict:

```python
grades = {"Ada": [1, 2], "Bo": [3]}
for name, notes in grades.items():
    print(name, "avg:", sum(notes) / len(notes))
```
""",

            "hints": [
                "Loop the tuples: `for name, score in students:` - sum scores and keep the best pair.",
                "The average needs the sum you already collected divided by `len(students)`.",
                "`passed = [name for name, score in students if score >= 50]`.",
            ],
            "solution": """students = [("Ada", 92), ("Ben", 40), ("Max", 97), ("Tom", 85)]

best_name, best_score = students[0]
total = 0
for name, score in students:
    total += score
    if score > best_score:
        best_name, best_score = name, score

passed = [name for name, score in students if score >= 50]

print(f"Students: {len(students)}")
print(f"Best: {best_name} ({best_score})")
print(f"Average: {total / len(students)}")
print(f"Passed: {passed}")
""",
            "explanation": "One champion-loop collects the sum *and* the best student - unpacking `for name, score in students` reads each tuple directly. `passed` is a filter comprehension keeping only scores >= 50. The f-strings then lay out the report; the list prints with Python's own brackets, which is what the expected output shows.\n\nWhat you learned: tuples + unpacking make small records easy, and one loop can gather everything a report needs.",
            "tests": [
                {"kind": "program",
                 "expected": "Students: 4\nBest: Max (97)\nAverage: 78.5\nPassed: ['Ada', 'Max', 'Tom']",
                 "match": "exact"},
            ],
        },
    ],
}
