"""Kapitel 2 - Kontrollstrukturen (if, schleifen)."""

CHAPTER = {
    "id": "ch02",
    "number": 2,
    "title": "Control Structures",
    "summary": "Making decisions with if/elif/else and repeating work with for and while loops.",
    "items": [
        {
            "id": "ch02-lesson",
            "type": "lesson",
            "title": "Decisions and loops",
            "body": r"""
## if: the program makes a choice

So far every line ran, top to bottom. `if` lets the program **choose**
what to do - like a fork in the road.

```python
number = int(input("Enter a number 1-10: "))
if number == 4:
    print("correct!")
else:
    print("wrong!")
```

> **What happens here**
>
> - `number == 4` asks a yes/no question (two `=` - one `=` stores!)
> - if the answer is yes, the indented line under `if` runs
> - otherwise the line under `else` runs
> - the `:` and the spaces at the line start (indentation) are required

With `elif` ("else if") you can check several doors in a row:

```python
number = 7                    # pretend the player typed 7
if number == 4:
    print("You won!")
elif number == 5 or number == 3:
    print("Close!")
else:
    print("You lost!")
```

> **What happens here**
>
> - line 1: this time we set `number` ourselves - no input needed
> - line 2: is it 4? No - so Python tries the next door
> - line 3: `elif` checks "is it 5 or 3?" - `or` means either counts;
>   7 fails this too
> - line 5: nothing matched, so `else` runs -> "You lost!"

Combine questions with `and`, `or`, `not`: `x > 5 and x < 10`.

### The switch replacement

Some languages have `switch`/`case`. In Python we use a **dictionary**
(a mini look-up table - more in chapter 6):

```python
switcher = {1: "January", 2: "February", 3: "March"}
month = 2
print(switcher.get(month, "invalid month"))   # February
```

## for: do it again and again

A `for` loop repeats work a known number of times. `range(5)` counts
0,1,2,3,4 - **the end is never included**:

```python
for i in range(5):        # 0..4
    print(i)
for i in range(5, 10):    # 5..9
    print(i)
for i in range(0, 10, 2): # 0,2,4,6,8 - every 2nd
    print(i)
for i in range(10, 0, -1):# 10..1 - backwards
    print(i)
```

## while: keep going until...

A `while` loop repeats *as long as* a condition is true - you don't need
to know how many rounds in advance:

```python
i = 10
while i > 0:
    print(i)
    i -= 1
print("Happy New Year!")
```

```python
won = False
guesses = [7, 3, 4]           # pretend the player typed these
i = 0
while not won:
    number = guesses[i]       # take the next guess from the list
    i += 1
    print("You typed", number)
    if number == 4:
        print("You won!")
        won = True
    else:
        print("Try again.")
print("Game over.")
```

> **What happens here**
>
> - line 1: `won` is a **flag** - a True/False variable that marks
>   "the game is over"
> - line 2-3: the list stands in for typed guesses; `i` is the position
> - line 4: `while not won` repeats until the flag flips
> - line 8-9: the right guess flips the flag - the loop ends
> - line 12: runs once the loop is done

> **Think of it like...** `for` is "run 10 laps" - you know the count.
> `while` is "keep swimming until you reach the shore" - you stop when
> something happens, not when a counter says so.

## break, continue and loop-else

- `break` - jump out of the loop immediately
- `continue` - skip the rest of this round, start the next one
- `else` on a loop runs only when it finished **without** `break`

```python
for letter in 'Python':
    if letter == 'h':
        continue
    print('Letter:', letter)
```

```python
for n in range(2, 10):
    for x in range(2, n // 2 + 1):
        if n % x == 0:
            break               # found a divisor -> not prime
    else:
        print(n, 'is prime')    # no break happened
```

## Rolling dice: the random module

`import random` loads Python's dice bag. `random.randint(1, 6)` gives a
random whole number between 1 and 6 - both ends included:

```python
import random
random.seed(7)                    # fixes the dice - same rolls every time
for i in range(4):
    print(random.randint(1, 6))
```

> **What happens here**
>
> - `seed(7)` puts the dice on rails - every run rolls the same
>   sequence, which is exactly what a test needs
> - `randint(1, 6)` picks one whole number from 1 to 6

## Handy built-ins

```python
print(min(3, 8))     # 3  - the smaller one
print(max(3, 8))     # 8  - the bigger one
print(abs(-5))       # 5  - distance from zero
print(round(3.7))    # 4  - nearest whole number
```

## Try it yourself

- Make a `for` loop that counts down from 5 to 1 and prints `Start!`.
- Change the guessing loop so the secret is 7 instead of 4.

## Key words

| Word | Meaning |
|---|---|
| if / elif / else | pick which code runs |
| == | "is equal to" (one `=` stores a value) |
| for / range | repeat a counted number of times |
| while | repeat while a condition is true |
| break / continue | leave the loop / skip to the next round |
""",
        },
        {
            "id": "ch02-quiz-1",
            "type": "quiz",
            "title": "range() boundaries",
            "question": "How many numbers does `range(5, 10)` produce?",
            "options": ["6", "5", "4", "10"],
            "answer": 1,
            "explanation": "range(5, 10) gives 5,6,7,8,9 - five numbers. The end value is never included, which is why '6' is the tempting wrong answer.",
        },
        {
            "id": "ch02-quiz-2",
            "type": "quiz",
            "title": "for/else",
            "question": "When does the `else` block of a `for` loop run?",
            "options": [
                "Always after the loop",
                "Only if the loop body ran at least once",
                "Only when the loop was not left via break",
                "Only when the iterable is empty",
            ],
            "answer": 2,
            "explanation": "The loop's `else` runs only when the loop finished on its own. If `break` kicked you out early, the else is skipped - 'always' sounds reasonable but is exactly what break prevents.",
        },
        {
            "id": "ch02-quiz-3",
            "type": "quiz",
            "title": "Truthy checks",
            "question": "What does `print('x' if 0 else 'y')` output?",
            "options": ["x", "y", "0", "Error"],
            "answer": 1,
            "explanation": "In yes/no questions the number 0 counts as 'no' (falsy). So the else part 'y' is printed. 'x' would need a true value like 1 or any non-zero number.",
        },
        {
            "id": "ch02-quiz-4",
            "type": "quiz",
            "title": "while",
            "question": "How many times does this loop print? `i = 3` -> `while i > 0: print(i); i -= 1`",
            "options": ["2", "3", "4", "forever"],
            "answer": 1,
            "explanation": "It prints for i = 3, 2 and 1 - then i is 0, the condition fails, and the loop stops. 'Forever' would be true only if we forgot `i -= 1` (a real classic bug!).",
        },
        {
            "id": "ch02-warm-1",
            "type": "task",
            "title": "Old enough?",
            "difficulty": 1,
            "plain": "Tell the user if they may ride the rollercoaster.",
            "instructions": r"""
Read an age (integer). If the age is **12 or more**, print `Allowed`,
otherwise print `Too young`.

For input `10` the output is just: `Too young`
""",
            "starter": """age = int(input("Your age: "))
# TODO: print "Allowed" (age >= 12) or "Too young"
""",
            "example": """Try the same trick on a different problem:

```python
temp = -3
if temp < 0:
    print("Ice on the road!")
else:
    print("All clear.")
```
""",

            "hints": [
                "You need an if/else comparing `age` with 12.",
                "`if age >= 12:` - >= means '12 or more'.",
                "Put the two prints indented under `if` and `else`.",
            ],
            "solution": """age = int(input("Your age: "))
if age >= 12:
    print("Allowed")
else:
    print("Too young")
""",
            "explanation": "`age >= 12` is a yes/no question: yes -> the line under `if` runs, no -> the `else` line runs. The colon and the 4-space indentation tell Python which lines belong to which branch.\n\nWhat you learned: `if` picks between two paths.",
            "tests": [
                {"kind": "program", "stdin": "10\n", "expected": "Too young"},
                {"kind": "program", "stdin": "12\n", "expected": "Allowed"},
                {"kind": "program", "stdin": "30\n", "expected": "Allowed"},
            ],
        },
        {
            "id": "ch02-warm-2",
            "type": "task",
            "title": "Count to five",
            "difficulty": 1,
            "plain": "Make a loop count from 1 to 5.",
            "instructions": r"""
Use a `for` loop with `range` to print the numbers 1 to 5, each on its
own line:

```
1
2
3
4
5
```
""",
            "starter": """# TODO: for-loop printing 1..5
""",
            "example": """Try the same trick on a different problem:

```python
for i in range(3):
    print("Push-up", i + 1)
print("Done!")
```
""",

            "hints": [
                "range(1, 6) gives 1,2,3,4,5 - the end is not included.",
                "The loop is `for i in range(1, 6):` with an indented print.",
                "Body: `print(i)`.",
            ],
            "solution": """for i in range(1, 6):
    print(i)""",
            "explanation": "`range(1, 6)` counts 1,2,3,4,5 - the 6 is a stop sign, not part of the list. Each number is placed into `i` in turn, and the indented `print(i)` runs once per number.\n\nWhat you learned: `for i in range(a, b)` repeats for every number in that range.",
            "tests": [
                {"kind": "program", "expected": "1\n2\n3\n4\n5",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch02-warm-3",
            "type": "task",
            "title": "Countdown",
            "difficulty": 1,
            "plain": "Count down from 5 to 1 with a while loop.",
            "instructions": "Print the numbers 5, 4, 3, 2, 1 - one per line - using a `while` loop, then print `Go!` on the last line.",
            "starter": """n = 5
while n > 0:
    print(n)
    n -= 1
# TODO: print "Go!" after the loop
""",
            "example": """A shorter countdown looks the same:

```python
n = 3
while n > 0:
    print(n)
    n -= 1
print("Go!")
```
""",
            "hints": [
                "`n -= 1` shrinks the counter every round.",
                "The loop runs while `n > 0`.",
                "The final `print(\"Go!\")` has no indent - it runs after the loop.",
            ],
            "solution": """n = 5
while n > 0:
    print(n)
    n -= 1
print("Go!")""",
            "explanation": "A while loop repeats as long as its condition stays true. n starts at 5, n -= 1 pulls it one step closer to zero each round, and when it hits 0 the loop ends and the unindented print fires Go! - the classic countdown pattern.",
            "tests": [
                {"kind": "program", "expected": "5\n4\n3\n2\n1\nGo!"},
            ],
        },
        {
            "id": "ch02-warm-4",
            "type": "task",
            "title": "Until stop",
            "difficulty": 1,
            "plain": "Repeat a question until the user says stop.",
            "instructions": "Keep asking `Word: `. Echo each word as `Echo: <word>` - but when the user types `stop`, print `Done!` and end the program.",
            "starter": """while True:
    word = input("Word: ")
    # TODO: if word is "stop", break out of the loop
    print("Echo:", word)
# TODO: print "Done!" after the loop
""",
            "example": """Same shape with dice instead of words:

```python
import random
random.seed(5)
rolls = 0
while True:
    rolls += 1
    if random.randint(1, 6) == 6:
        break
    print("roll", rolls, "- no six yet")
print("Six after", rolls, "rolls!")
```
""",
            "hints": [
                "`while True:` loops forever - `break` is the exit door.",
                "Check `word == \"stop\"` before echoing it.",
                "`Done!` prints after the loop, with no indent.",
            ],
            "solution": """while True:
    word = input("Word: ")
    if word == "stop":
        break
    print("Echo:", word)
print("Done!")""",
            "explanation": "while True spins forever, so the loop can only leave through break. Each round reads a word, checks for stop first - otherwise stop would be echoed too - then echoes the word. When break fires, Python jumps past the loop body to the final print.",
            "tests": [
                {"kind": "program", "stdin": "hi\nthere\nstop\n", "expected": "Done!"},
                {"kind": "program", "stdin": "stop\n", "expected": "Done!"},
            ],
        },
        {
            "id": "ch02-task-1",
            "type": "task",
            "title": "Spathiphyllum (if/elif/else)",
            "difficulty": 1,
            "plain": "A picky plant fan answers differently depending on the exact spelling.",
            "instructions": r"""
Your program loves the houseplant *Spathiphyllum*. It reads one word
and answers:

- `Spathiphyllum` (capital S) -> `Yes - Spathiphyllum is the best plant ever!`
- `spathiphyllum` (all lowercase) -> `No, I want a big Spathiphyllum!`
- anything else -> `Spathiphyllum! Not {input}!` (input included!)

Capital letters matter - `==` compares exactly.
""",
            "starter": """plant = input("Enter a plant name: ")
if plant == "Spathiphyllum":
    print("Yes - Spathiphyllum is the best plant ever!")
# TODO: elif plant == "spathiphyllum" (all lowercase)
#       -> "No, I want a big Spathiphyllum!"
# TODO: else -> print f"Spathiphyllum! Not {plant}!"
""",
            "example": """Same shape, different pet:

```python
pet = input("Pet? ")
if pet == "cat":
    print("Meow!")
elif pet == "CAT":
    print("Shouting at me?")
else:
    print(f"A {pet}? Nice too.")
```

Run it with `cat`, `CAT` and `dog` to see all three paths.
""",

            "hints": [
                "Three cases -> `if`, `elif`, `else`.",
                "Compare the input exactly: `plant == \"Spathiphyllum\"`.",
                "The last answer needs the input inside it: `f\"Spathiphyllum! Not {plant}!\"`.",
            ],
            "solution": """plant = input("Enter a plant name: ")
if plant == "Spathiphyllum":
    print("Yes - Spathiphyllum is the best plant ever!")
elif plant == "spathiphyllum":
    print("No, I want a big Spathiphyllum!")
else:
    print(f"Spathiphyllum! Not {plant}!")
""",
            "explanation": "Python checks the doors in order: first the exact capital-S spelling, then the all-lowercase one, and `else` catches everything else. The f-string in the else branch drops the typed word into the answer.\n\nWhat you learned: `elif` lets you test several exact cases in order.",
            "tests": [
                {"kind": "program", "stdin": "spathiphyllum\n",
                 "expected": "No, I want a big Spathiphyllum!"},
                {"kind": "program", "stdin": "Spathiphyllum\n",
                 "expected": "Yes - Spathiphyllum is the best plant ever!"},
                {"kind": "program", "stdin": "pelargonium\n",
                 "expected": "Spathiphyllum! Not pelargonium!"},
            ],
        },
        {
            "id": "ch02-task-2",
            "type": "task",
            "title": "Smallest of three numbers",
            "difficulty": 1,
            "plain": "Of three typed numbers, find the tiniest - without min().",
            "instructions": r"""
Read three integers and print the smallest one:

```
The smallest number is 2
```

Do **not** use `min()` - decide it yourself with `if`/`else`.
""",
            "starter": """print("This program finds the smallest number!")
a = int(input("Number 1: "))
b = int(input("Number 2: "))
c = int(input("Number 3: "))
if a < b:
    result = a
else:
    result = b
# TODO: if c is even smaller than result, put c into result
# TODO: print f"The smallest number is {result}"
""",
            "example": """Picking the winner of three:

```python
x, y, z = 7, 3, 5
m = x
if y < m:
    m = y
if z < m:
    m = z
print("Smallest:", m)
```
""",

            "hints": [
                "Keep a `result` box: first put the smaller of a and b inside.",
                "Then ask: is c smaller than result? If yes, replace it.",
                "Two if/else rounds are enough, then print the result.",
            ],
            "solution": """print("This program finds the smallest number!")
a = int(input("Number 1: "))
b = int(input("Number 2: "))
c = int(input("Number 3: "))
if a < b:
    result = a
else:
    result = b
if c < result:
    result = c
print(f"The smallest number is {result}")
""",
            "explanation": "Champion-style: `result` holds the smallest seen so far. Round 1 pits a against b and keeps the smaller. Round 2 asks if c can beat the champion - if yes, c takes over. What survives is the smallest of all three.\n\nWhat you learned: comparing pairwise in a variable finds minima without min().",
            "tests": [
                {"kind": "program", "stdin": "5\n2\n9\n",
                 "expected": "The smallest number is 2"},
                {"kind": "program", "stdin": "-3\n0\n-7\n",
                 "expected": "The smallest number is -7"},
                {"kind": "program", "stdin": "4\n4\n4\n",
                 "expected": "The smallest number is 4"},
            ],
        },
        {
            "id": "ch02-task-3",
            "type": "task",
            "title": "Tax calculator (if/else)",
            "difficulty": 2,
            "plain": "Work out a country's tax with two different formulas depending on income.",
            "instructions": r"""
In a happy country the income tax is:

- income **up to 85,528 thalers**: tax = 18% of income **minus 556.02**
- income **above**: tax = **14,839.02** + 32% of the part over 85,528
- the tax can never be below **0**

Read the income (float) and print `The tax is: X thalers` with X
rounded to whole thalers using `round(tax, 0)`.

Examples: `10000` -> `The tax is: 1244.0 thalers`,
`100000` -> `19470.0`, `1000` -> `0.0`.
""",
            "starter": """income = float(input("Enter the annual income: "))
if income <= 85528:
    tax = income * 0.18 - 556.02
# TODO: else -> tax = 14839.02 + 0.32 * (income - 85528)
# TODO: a negative tax becomes 0.0  (the tax office never pays you back)
# TODO: print f"The tax is: {round(tax, 0)} thalers"
""",
            "example": """Capping a discount instead of a tax:

```python
price = 120
discount = price * 0.20
if discount > 50:
    discount = 50.0
print(f"Discount: {round(discount, 0)} EUR")
```
""",

            "hints": [
                "One if decides which formula applies: `if income <= 85528:`.",
                "In the high bracket the extra part is `income - 85528`.",
                "After computing, clamp: `if tax < 0: tax = 0.0`.",
            ],
            "solution": """income = float(input("Enter the annual income: "))
if income <= 85528:
    tax = income * 0.18 - 556.02
else:
    tax = 14839.02 + 0.32 * (income - 85528)
if tax < 0:
    tax = 0.0
print(f"The tax is: {round(tax, 0)} thalers")
""",
            "explanation": "The if/else picks the right formula for the bracket: low incomes pay 18% minus a discount, high incomes pay a fixed chunk plus 32% of only the extra part. Small incomes would get a negative tax - the second if clamps that to 0. `round(tax, 0)` makes a whole thaler.\n\nWhat you learned: real-world rules often map to one if/else plus a safety clamp.",
            "tests": [
                {"kind": "program", "stdin": "10000\n",
                 "expected": "The tax is: 1244.0 thalers"},
                {"kind": "program", "stdin": "100000\n",
                 "expected": "The tax is: 19470.0 thalers"},
                {"kind": "program", "stdin": "1000\n",
                 "expected": "The tax is: 0.0 thalers"},
                {"kind": "program", "stdin": "-100\n",
                 "expected": "The tax is: 0.0 thalers"},
            ],
        },
        {
            "id": "ch02-task-4",
            "type": "task",
            "title": "Leap year (if/elif/else)",
            "difficulty": 2,
            "plain": "Check the calendar rules and say if a year is a leap year.",
            "instructions": r"""
Since 1582 the leap year rules are:

- year not divisible by 4 -> `Common year`
- else, not divisible by 100 -> `Leap year`
- else, not divisible by 400 -> `Common year`
- else -> `Leap year`

Read a year. Before 1582 print `Not within the Gregorian calendar
period` instead of the year kind.
""",
            "starter": """year = int(input("Enter a year: "))
if year < 1582:
    print("Not within the Gregorian calendar period")
elif year % 4 != 0:
    print("Common year")
# TODO: elif year % 100 != 0 -> print "Leap year"
# TODO: elif year % 400 != 0 -> print "Common year"
# TODO: else -> print "Leap year"
""",
            "example": """Early return with conditions:

```python
def season(month):
    if month in (12, 1, 2):
        return "winter"
    return "not winter"

print(season(1), season(7))
```
""",

            "hints": [
                "First rule out `year < 1582` with its own if.",
                "Then chain `% 4`, `% 100`, `% 400` with elif - `year % 4 != 0` means 'not divisible by 4'.",
                "Order matters: each elif only runs when all checks above failed.",
            ],
            "solution": """year = int(input("Enter a year: "))
if year < 1582:
    print("Not within the Gregorian calendar period")
elif year % 4 != 0:
    print("Common year")
elif year % 100 != 0:
    print("Leap year")
elif year % 400 != 0:
    print("Common year")
else:
    print("Leap year")
""",
            "explanation": "The checks form a sieve in exactly the order of the rules: too old -> era warning; not divisible by 4 -> common; divisible by 4 but not 100 -> leap; divisible by 100 but not 400 -> common; only the special 400-divisible years fall through to the final leap.\n\nWhat you learned: elif chains express 'first match wins' rulebooks.",
            "tests": [
                {"kind": "program", "stdin": "2000\n", "expected": "Leap year"},
                {"kind": "program", "stdin": "2015\n", "expected": "Common year"},
                {"kind": "program", "stdin": "1999\n", "expected": "Common year"},
                {"kind": "program", "stdin": "1996\n", "expected": "Leap year"},
                {"kind": "program", "stdin": "1900\n", "expected": "Common year"},
                {"kind": "program", "stdin": "1580\n",
                 "expected": "Not within the Gregorian calendar period"},
            ],
        },
        {
            "id": "ch02-task-5",
            "type": "task",
            "title": "GCD after Euclid",
            "difficulty": 2,
            "plain": "Two numbers take turns subtracting until one is left - that is their biggest shared divisor.",
            "instructions": r"""
The **greatest common divisor (GCD)** is the biggest number that divides
both numbers evenly. Euclid's subtraction algorithm:

1. `m = a`, `n = b`
2. if `m < n`, swap them
3. `r = m - n`
4. `m = n`, `n = r`
5. if `r != 0`, back to step 2

When `r` becomes 0, `m` holds the GCD. Read `a` and `b`, print:

```
GCD: 12
```
""",
            "starter": """print("Compute the GCD")
a = int(input("First number: "))
b = int(input("Second number: "))
m, n = a, b            # work on copies so a and b stay untouched
r = -1
while r != 0:
    if m < n:
        m, n = n, m    # swap so m is always the bigger one
    # TODO: r = m - n, then m = n, then n = r
print(f"GCD: {m}")
""",
            "example": """Same loop idea, with % instead of subtraction:

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

print(gcd(12, 8))
```
""",

            "hints": [
                "A `while r != 0:` loop repeats steps 2-4; start r with any non-zero value like -1.",
                "Inside: `if m < n: m, n = n, m` (Python swaps like that), then `r = m - n`, `m = n`, `n = r`.",
                "After the loop `m` is the answer.",
            ],
            "solution": """print("Compute the GCD")
a = int(input("First number: "))
b = int(input("Second number: "))
m, n = a, b
r = -1
while r != 0:
    if m < n:
        m, n = n, m
    r = m - n
    m = n
    n = r
print(f"GCD: {m}")
""",
            "explanation": "Each round replaces the bigger number with the difference - like sawing two planks to the same length: whatever finally remains evenly measures both originals. The loop stops when the difference is 0, and `m` holds the divisor. `m, n = n, m` is Python's one-line swap.\n\nWhat you learned: a 2300-year-old algorithm is just a while loop with a swap.",
            "tests": [
                {"kind": "program", "stdin": "48\n36\n", "expected": "GCD: 12"},
                {"kind": "program", "stdin": "7\n13\n", "expected": "GCD: 1"},
                {"kind": "program", "stdin": "100\n10\n", "expected": "GCD: 10"},
            ],
        },
        {
            "id": "ch02-task-6",
            "type": "task",
            "title": "Binary number",
            "difficulty": 2,
            "plain": "Write a number as 0s and 1s by dividing out powers of two.",
            "instructions": r"""
Convert a number into a binary string with exactly `a` digits -
**without** `bin()` or format specs.

The idea: for each position, ask "does the biggest remaining power of
two fit?" - `rest // 2**(a-1)` is the digit, `rest % 2**(a-1)` is what's
left.

Example: `z = 237`, `a = 8` -> `11101101` (237 = 128+64+32+8+4+1).

Write `binary(z, a)` returning the string, then print it for the two
numbers read from the console.
""",
            "starter": """def binary(z, a):
    rest = z
    output = ""
    while a > 0:
        digit = rest // 2**(a - 1)     # next binary digit, 0 or 1
        output += str(digit)
        # TODO: keep only the leftover: rest = rest % 2**(a - 1)
        a -= 1
    return output

z = int(input("Number: "))
a = int(input("Digits: "))
print(binary(z, a))
""",
            "example": """Peeling digits the other way round:

```python
n = 13
out = ""
while n:
    out = str(n % 2) + out
    n //= 2
print(out)
```
""",

            "hints": [
                "Loop `while a > 0:` and shrink a each round.",
                "Each round: digit = `rest // 2**(a-1)`, append it, then `rest = rest % 2**(a-1)`.",
                "Leading zeros happen automatically - `5` with 4 digits prints `0101`.",
            ],
            "solution": """def binary(z, a):
    rest = z
    output = ""
    while a > 0:
        digit = rest // 2**(a - 1)
        rest = rest % 2**(a - 1)
        output += str(digit)
        a -= 1
    return output

z = int(input("Number: "))
a = int(input("Digits: "))
print(binary(z, a))
""",
            "explanation": "Imagine paying 237 with binary coins (128, 64, 32, 16, 8, 4, 2, 1): for each coin `//` asks 'does it fit?' (the digit) and `%` is the change left. 237 takes 128 (change 109), 64 (45), 32 (13), skips 16, takes 8, 4, skips 2, takes 1 -> 11101101.\n\nWhat you learned: repeated division by powers of two builds binary digits one at a time.",
            "tests": [
                {"kind": "program", "stdin": "237\n8\n", "expected": "11101101"},
                {"kind": "program", "stdin": "5\n4\n", "expected": "0101"},
                {"kind": "expr", "expr": "binary(0, 4)", "expected": "\"0000\"",
                 "stdin": "0\n4\n"},
                {"kind": "expr", "expr": "binary(255, 8)", "expected": "\"11111111\""},
            ],
        },
        {
            "id": "ch02-task-7",
            "type": "task",
            "title": "ISBN check digit",
            "difficulty": 2,
            "plain": "Books have a safety digit - compute it from the first nine digits.",
            "instructions": r"""
An ISBN-10 ends with a **check digit** that catches typos. For a
9-digit number, multiply the digits (from the left) by 1, 2, ..., 9, add
the products, and take the sum `% 11`.

Example `312717700`:

```
1*3 + 2*1 + 3*2 + 4*7 + 5*1 + 6*7 + 7*7 + 8*0 + 9*0 = 135
135 % 11 = 3   -> check digit 3
```

Write `check_digit(z)` for a 9-digit integer, and print
`Check digit: 3` for a number read from the console.

Hint: peeling digits from the **right** (`z % 10`, `z //= 10`) gives
them in reverse order - the last digit gets weight 9, the first
weight 1.
""",
            "starter": """def check_digit(z):
    total = 0
    for i in range(9, 0, -1):
        p = z % 10           # rightmost digit
        z = z // 10          # chop it off
        # TODO: add p * i to total
    # TODO: return total % 11

z = int(input("9-digit number: "))
print("Check digit:", check_digit(z))
""",
            "example": """Counting a loop variable down:

```python
total = 0
for i in range(4, 0, -1):
    total += i
print(total)
```
""",

            "hints": [
                "`z % 10` gives the last digit, `z //= 10` chops it off - repeat 9 times.",
                "Count the weights down with `for i in range(9, 0, -1)` so the peeled digit gets weight i.",
                "Finally `return total % 11`.",
            ],
            "solution": """def check_digit(z):
    total = 0
    for i in range(9, 0, -1):
        p = z % 10
        z = z // 10
        total += p * i
    return total % 11

z = int(input("9-digit number: "))
print("Check digit:", check_digit(z))
""",
            "explanation": "`z % 10` peels the last digit, `z //= 10` removes it - nine rounds unpack the whole number, last digit first. Since we peel right to left, `range(9, 0, -1)` gives each digit its weight (9 down to 1). The sum modulo 11 is the check digit.\n\nWhat you learned: `% 10` and `// 10` walk through a number digit by digit.",
            "tests": [
                {"kind": "program", "stdin": "312717700\n",
                 "expected": "Check digit: 3"},
                {"kind": "expr", "expr": "check_digit(312717700)",
                 "expected": "3", "stdin": "312717700\n"},
                {"kind": "expr", "expr": "check_digit(389864513)",
                 "expected": "4"},
            ],
        },
        {
            "id": "ch02-task-8",
            "type": "task",
            "title": "Mäxchen dice game",
            "difficulty": 2,
            "plain": "Score a two-dice throw with three funny rules.",
            "instructions": r"""
The dice game *Mäxchen* scores a throw of two dice like this:

1. the throw 1 and 2 is "Mäxchen" and worth **1000** points
2. a double (two equal values) is worth **100 x value**
3. otherwise: **10 x higher die + lower die**

Read the two dice values and print the score.

Examples: `1 2` -> `1000`, `4 4` -> `400`, `3 5` -> `53`.
""",
            "starter": """a = int(input("first die: "))
b = int(input("second die: "))
mi = min(a, b)
ma = max(a, b)
if mi == 1 and ma == 2:
    print(1000)              # the mighty Maexchen!
# TODO: elif doubles (mi == ma) -> print 100 * mi
# TODO: else -> print 10 * ma + mi
""",
            "example": """Scoring a different dice roll:

```python
a, b = 4, 4
if a == b:
    print("doubles", 100 * a)
else:
    print(10 * max(a, b) + min(a, b))
```
""",

            "hints": [
                "`mi = min(a, b)` and `ma = max(a, b)` make the tests easy.",
                "Check the rules in order: Mäxchen (`mi == 1 and ma == 2`), then doubles, then the normal score.",
                "Normal score: `10 * ma + mi`.",
            ],
            "solution": """a = int(input("first die: "))
b = int(input("second die: "))
mi = min(a, b)
ma = max(a, b)
if mi == 1 and ma == 2:
    print(1000)
elif mi == ma:
    print(100 * mi)
else:
    print(10 * ma + mi)
""",
            "explanation": "Sorting the dice into `mi`/`ma` makes every rule simple: Mäxchen is 1+2, a double is `mi == ma`, and otherwise the bigger die counts as tens. The elif chain checks the rules top to bottom - order matters because Mäxchen must be caught before the normal score.\n\nWhat you learned: `min`/`max` plus an ordered if/elif chain encodes game rules.",
            "tests": [
                {"kind": "program", "stdin": "1\n2\n", "expected": "1000"},
                {"kind": "program", "stdin": "2\n1\n", "expected": "1000"},
                {"kind": "program", "stdin": "4\n4\n", "expected": "400"},
                {"kind": "program", "stdin": "3\n5\n", "expected": "53"},
                {"kind": "program", "stdin": "6\n6\n", "expected": "600"},
            ],
        },
        {
            "id": "ch02-task-9",
            "type": "task",
            "title": "Prime numbers up to n",
            "difficulty": 2,
            "plain": "Print every number that cannot be divided evenly - the primes.",
            "instructions": r"""
Read an upper bound `n` and print every prime from 2 up to `n`
(exclusive), one per line - using a `for`/`else` loop.

For input `10`:

```
2
3
5
7
```

A number `z` is prime when no `t` in `range(2, z // 2 + 1)` divides it.
""",
            "starter": """n = int(input("Find primes from 2 up to? "))
for z in range(2, n):
    for t in range(2, z // 2 + 1):
        if z % t == 0:
            break            # found a divisor -> not prime
    else:
        pass    # TODO: no break happened -> z is prime, print it
""",
            "example": """The same prime test in one line:

```python
for n in range(2, 10):
    print(n, "is prime" if all(n % d for d in range(2, n)) else "nope")
```
""",

            "hints": [
                "Outer loop `for z in range(2, n)`; inner loop tries divisors `for t in range(2, z // 2 + 1)`.",
                "If `z % t == 0` -> `break` (not prime). The `else` on the inner loop runs only when no divisor was found.",
                "Inside the else: `print(z)`.",
            ],
            "solution": """n = int(input("Find primes from 2 up to? "))
for z in range(2, n):
    for t in range(2, z // 2 + 1):
        if z % t == 0:
            break
    else:
        print(z)
""",
            "explanation": "For every candidate z the inner loop tries all possible divisors. Finding one (`z % t == 0`) breaks out - z is composite. The `else` on the inner loop is the clever bit: it only runs when the loop finished without break, i.e. no divisor was found - prime! We only test up to `z // 2` because bigger divisors can't divide evenly anyway.\n\nWhat you learned: `for`/`else` = 'do this when nothing interrupted the search'.",
            "tests": [
                {"kind": "program", "stdin": "10\n",
                 "expected": "2\n3\n5\n7"},
                {"kind": "program", "stdin": "20\n",
                 "expected": "2\n3\n5\n7\n11\n13\n17\n19"},
            ],
        },
        {
            "id": "ch02-task-10",
            "type": "task",
            "title": "Multiplication table",
            "difficulty": 1,
            "plain": "Print the times table for one number, nicely lined up.",
            "instructions": r"""
Read a number and print its multiplication table from 1 to 10,
right-aligned in columns. For input `7` the output must be exactly:

```
  1 * 7 =   7
  2 * 7 =  14
  3 * 7 =  21
  4 * 7 =  28
  5 * 7 =  35
  6 * 7 =  42
  7 * 7 =  49
  8 * 7 =  56
  9 * 7 =  63
 10 * 7 =  70
```

Use the format `f"{x:3} * {z} = {x*z:3}"` - `{x:3}` pads the left
number and `{x*z:3}` the result to width 3 (`:3` = at least 3
characters wide, padded with spaces on the left).
""",
            "starter": """z = int(input("Which number's table? "))
# one row looks like this:  print(f"{x:3} * {z} = {x * z:3}")
for x in range(1, 11):
    pass    # TODO: print the row for this x in exactly that format
""",
            "example": """Field widths in a small table:

```python
for i in range(1, 4):
    print(f"{i:3} squared is {i*i:3}")
```
""",

            "hints": [
                "One loop: `for x in range(1, 11)`.",
                "Inside the f-string `{x:3}` and `{x*z:3}` pad to width 3 for straight columns.",
                "Ten prints, nothing else.",
            ],
            "solution": """z = int(input("Which number's table? "))
for x in range(1, 11):
    print(f"{x:3} * {z} = {x * z:3}")
""",
            "explanation": "The loop counts x from 1 to 10 and prints one f-string per round. The `:3` format pads each number with spaces to width 3, which keeps all the `=` signs in a straight column - that is what makes the table tidy.\n\nWhat you learned: `range` + f-string padding = clean tables.",
            "tests": [
                {"kind": "program", "stdin": "7\n",
                 "expected": "1 * 7 =   7\n2 * 7 =  14\n5 * 7 =  35\n10 * 7 =  70"},
                {"kind": "program", "stdin": "3\n",
                 "expected": "3 * 3 =   9\n10 * 3 =  30"},
            ],
        },
        {
            "id": "ch02-task-11",
            "type": "task",
            "title": "Dice until six",
            "difficulty": 2,
            "plain": "Keep rolling a die until a six shows up, then report all rolls.",
            "instructions": r"""
Roll a die (`random.randint(1, 6)`) until a 6 comes up. Print all
rolled numbers on one line, then the count.

To keep it testable, **seed** the generator first with
`random.seed(7)` - the rolls are then fixed: `3 2 4 6` (4 rolls).

Output:

```
Rolled: 3 2 4 6
Rolls: 4
```
""",
            "starter": """import random
random.seed(7)
rolls = []
number = 0
while number != 6:
    number = random.randint(1, 6)
    rolls.append(number)
# TODO: print "Rolled:" then the rolls joined by spaces:
#       " ".join(str(r) for r in rolls)
# TODO: print "Rolls:" then len(rolls)
""",
            "example": """Two seeded dice rolls:

```python
import random
random.seed(7)
print(random.randint(1, 6))
print(random.randint(1, 6))
```
""",

            "hints": [
                "`number = 0` then `while number != 6:` - inside, roll and collect.",
                "Collect rolls in a list: `rolls.append(number)`.",
                "Join for printing: `' '.join(str(r) for r in rolls)`; count is `len(rolls)`.",
            ],
            "solution": """import random
random.seed(7)
rolls = []
number = 0
while number != 6:
    number = random.randint(1, 6)
    rolls.append(number)
print("Rolled:", " ".join(str(r) for r in rolls))
print("Rolls:", len(rolls))
""",
            "explanation": "The while loop has no fixed count - it rolls until the stop condition hits. Every roll is appended to the list so we can print them all at the end. `random.seed(7)` fixes the 'random' sequence, which makes the program repeatable and testable. `' '.join(...)` glues the numbers into one line.\n\nWhat you learned: `while` is the right loop when the number of rounds is unknown.",
            "tests": [
                {"kind": "program",
                 "expected": "Rolled: 3 2 4 6\nRolls: 4",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch02-boss",
            "type": "task",
            "title": "The guessing judge",
            "difficulty": 3,
            "boss": True,
            "plain": "Referee a number-guessing game: say too small / too big until the guess is right.",
            "instructions": r"""
**BOSS MISSION - you are the referee of a guessing game.**

Read a secret number, then guesses one by one (all integers). For each
guess print:

- `too small` - guess below the secret
- `too big` - guess above the secret
- `correct after N tries` - when it matches (N = count of guesses), then stop

Example - secret `42`, guesses `50 30 40 42` (the full output,
prompts included):

```
Secret number: 42
Guess: 50
too big
Guess: 30
too small
Guess: 40
too small
Guess: 42
correct after 4 tries
```
""",
            "starter": """secret = int(input("Secret number: "))
# TODO: read guesses until one equals secret; print the verdicts
""",
            "example": """A tiny judge with a fixed guess:

```python
target = 7
guess = 3
while guess != target:
    print("too small" if guess < target else "too big")
    guess += 1
print("correct!")
```
""",

            "hints": [
                "Count guesses in `tries = 0`; loop `while True:` and `break` on a hit.",
                "Read the guess inside the loop, add 1 to tries, then three cases: `==` / `<` / `>`.",
                "On a match print `f\"correct after {tries} tries\"` and break.",
            ],
            "solution": """secret = int(input("Secret number: "))
tries = 0
while True:
    guess = int(input("Guess: "))
    tries += 1
    if guess == secret:
        print(f"correct after {tries} tries")
        break
    elif guess < secret:
        print("too small")
    else:
        print("too big")
""",
            "explanation": "`while True` loops forever - the escape is the `break` when the guess matches. Each round reads a guess, counts it, and the if/elif/else prints the right verdict. The try counter only makes sense because it increments before the comparison.\n\nWhat you learned: `while True` + `break` is the standard pattern for 'loop until something happens'.",
            "tests": [
                {"kind": "program", "stdin": "42\n50\n30\n40\n42\n",
                 "expected": "Secret number: 42\nGuess: 50\ntoo big\nGuess: 30\ntoo small\nGuess: 40\ntoo small\nGuess: 42\ncorrect after 4 tries",
                 "match": "exact"},
                {"kind": "program", "stdin": "7\n7\n",
                 "expected": "Secret number: 7\nGuess: 7\ncorrect after 1 tries",
                 "match": "exact"},
                {"kind": "program", "stdin": "10\n1\n2\n10\n",
                 "expected": "Secret number: 10\nGuess: 1\ntoo small\nGuess: 2\ntoo small\nGuess: 10\ncorrect after 3 tries",
                 "match": "exact"},
            ],
        },
    ],
}
