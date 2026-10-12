"""Kapitel 1 - Variablen & Operatoren."""

CHAPTER = {
    "id": "ch01",
    "number": 1,
    "title": "Variables & Operators",
    "summary": "Labelled boxes for values, maths operators, f-strings and a peek at bits.",
    "items": [
        {
            "id": "ch01-lesson",
            "type": "lesson",
            "title": "Variables, operators and f-strings",
            "body": r"""
## Variables are labelled boxes

A **variable** is a box with a name on it. You put a value inside with
`=` and look inside by using the name:

```python
age = 10
name = "Ada"
print(age)
print(name)
age = 11          # a new value goes into the same box
print(age)
```

> **What happens here**
>
> - line 1: the box `age` gets the number 10
> - line 2: the box `name` gets the text Ada
> - line 6: `age` is overwritten - the old value is gone

Python decides on its own what *kind* of thing is in the box (number,
text...) - that is called **dynamic typing**. `type(x)` tells you the
kind: `int` (whole number), `float` (with a point), `str` (text),
`bool` (True/False).

## Doing maths

```python
print(5 / 2)    # 2.5 - / always gives a float
print(5 // 2)   # 2   - // is "how many whole times"
print(5 % 2)    # 1   - % is "what is left over"
print(3 ** 2)   # 9   - ** is "to the power of"
```

> **Think of it like...** sharing 5 cookies between 2 kids. `//` asks how
> many *whole* cookies each kid gets (2). `%` asks what is left in the
> jar afterwards (1).

> **Watch out** - `**` works right to left: `2**2**3` means
> `2**(2**3)` = 256, not `(2**2)**3` = 64.

`round(x, n)` cuts a decimal to n places: `round(3.14159, 2)` -> `3.14`.

## Updating a box: += and friends

`x = x + 5` ("take what is in the box and add 5") is so common that
Python has a shortcut for it - and for the other operators too:

```python
coins = 10
coins += 5     # coins = coins + 5
coins -= 2     # coins = coins - 2
coins *= 2     # coins = coins * 2
print(coins)

seconds = 3700
seconds %= 3600   # keep only the leftover
print(seconds)
```

> **What happens here**
>
> - `+=`, `-=`, `*=` change the box in place - same for `//=` and `%=`
> - `seconds %= 3600` keeps only what does not fit into whole hours

You can even fill or swap two boxes in one line:

```python
a, b = 1, 2
print(a, b)
a, b = b, a    # swap!
print(a, b)
```

## Asking the user: input()

`input("Question: ")` shows a question and waits for an answer. The
answer is **always text (str)** - turn it into a number with `int()`
or `float()` when you need maths:

```python
name = input("Your name: ")
print("Hello", name)

n = int(input("A number: "))
print("Double:", n * 2)
```

The three converters you will use all the time: `int()` makes a whole
number, `float()` a decimal number, and `str()` turns anything back
into text.

## print tricks: sep and end

`print` puts a space between values and ends with a new line. Both can
be changed:

```python
print("a", "b", "c", sep="-")   # a-b-c
print("one", end=" ")
print("two")                    # one two
```

## f-strings: text with holes

An **f-string** is text with little `{}` holes that get filled with
values:

```python
name = "Fred"
age = 42
print(f"My name is {name} and I am {age}.")
print(f"Dog years: {age * 7}")
print(f"Pi: {3.14159265:.2f}")   # .2f = two decimals
print(f"Padded: {7:03}")         # 003 = 3 digits, pad with zeros
print(f"Clock: {9:02}:{5:02}")   # 09:05 - :02 pads to 2 digits
print(f"Column: {7:3}|{42:3}")   # :3 = width 3, padded with spaces
```

> **What happens here**
>
> - line 3: `{name}` is replaced by Fred, `{age}` by 42
> - line 5: `:.2f` rounds Pi to 3.14
> - line 6: `:03` pads 7 to `007`

## Try it yourself

- Make a variable with your own name and print it three times.
- Print `17 // 5` and `17 % 5` - can you explain the answers?
- Write an f-string that prints `I am X years old` with your age.

## Key words

| Word | Meaning |
|---|---|
| variable | a named box that holds a value |
| int / float / str | whole number / decimal number / text |
| input() | asks the user a question, answer is always text |
| f-string | text with `{}` holes that get filled in |
| // and % | whole-times division and the leftover |
""",
        },
        {
            "id": "ch01-lesson-2",
            "type": "lesson",
            "title": "Bits and bitwise operators",
            "body": r"""
## Numbers made of switches

Inside the computer every number is a row of tiny switches that are
either on (1) or off (0). This is called **binary** or **bits**.

`5` in binary is `0b101` (4+1). `0b` in front means "binary number".

## Flipping switches: bitwise operators

Bitwise operators compare two numbers **switch by switch**:

```python
a = 0b1010   # 10
b = 0b1100   # 12
print(a | b)  # OR:  a switch on in EITHER  -> 0b1110 = 14
print(a & b)  # AND: a switch on in BOTH   -> 0b1000 = 8
print(a ^ b)  # XOR: a switch on in EXACTLY ONE -> 0b0110 = 6
print(~a)     # NOT: every switch flipped  -> -11
```

> **Think of it like...** two rows of light switches. OR lights a lamp if
> either switch is on, AND only if both are on, XOR only if exactly one
> is on.

## Sliding switches: shifts

`<<` pushes all bits left (adds zeros on the right - like adding a 0 in
normal maths, this multiplies by 2). `>>` pushes them right (divides
by 2, dropping leftovers):

```python
print(0b1010 << 2)   # 101000 = 40  (10 x 4)
print(0b1100 >> 2)   # 11     = 3   (12 ÷ 4)
```

This is how computers handle IP addresses - you will need it in the
chapter's final task.

## Text helpers for the IP task

Two string tricks make the final task much easier - cutting text into
pieces and gluing pieces back together:

```python
parts = "192.168.0.1".split(".")
print(parts)             # ['192', '168', '0', '1']
print(parts[0])          # '192'
print(int(parts[0]))     # 192 - a real number now

ip = ".".join(parts)     # glue back with dots between
print(ip)                # 192.168.0.1
```

> **What happens here**
>
> - `.split(".")` cuts the text at every dot -> a list of 4 strings
> - `".".join(parts)` glues the list back into one string
> - `int()` turns a text piece into a number for the bit maths

And one list trick: `parts.insert(0, "x")` pushes `"x"` in at the
*front* of a list instead of the end.

## Try it yourself

- Work out `0b0110 | 0b0011` by hand, then check with Run.
- What is `7 << 1`? And `7 >> 1`?

## Key words

| Word | Meaning |
|---|---|
| bit | one switch: 0 or 1 |
| binary | numbers written with only 0 and 1 (`0b...`) |
| `\|` `&` `^` `~` | OR, AND, XOR, NOT - bit by bit |
| `<<` `>>` | shift left/right - times or divide by 2 |
""",
        },
        {
            "id": "ch01-quiz-1",
            "type": "quiz",
            "title": "Power order",
            "question": "What does `2**2**3` evaluate to?",
            "options": ["64", "256", "12", "Error"],
            "answer": 1,
            "explanation": "Power ** works right to left: `2**2**3` is `2**(2**3)` = `2**8` = 256. 64 would be `(2**2)**3` - tempting but wrong, because Python does the right power first.",
        },
        {
            "id": "ch01-quiz-2",
            "type": "quiz",
            "title": "Whole times and leftovers",
            "question": "What does `print(17 // 5, 17 % 5)` output?",
            "options": ["3.4 2", "3 2", "3 3", "4 2"],
            "answer": 1,
            "explanation": "`//` is 'how many whole times' -> 3 (5 fits into 17 three times). `%` is the leftover -> 2. '3.4' is a trap - that would be the normal `/` division, which gives a decimal.",
        },
        {
            "id": "ch01-quiz-3",
            "type": "quiz",
            "title": "Quotes or no quotes",
            "question": "What does `print(\"4\" + \"5\")` show?",
            "options": ["9", "45", "4 5", "Error"],
            "answer": 1,
            "explanation": "Both values are text, and `+` on text glues the pieces together: '45'. Only numbers get added - '9' would be right for `print(4 + 5)` without quotes.",
        },
        {
            "id": "ch01-quiz-4",
            "type": "quiz",
            "title": "Shift left",
            "question": "What is `0b1010 << 2` in decimal?",
            "options": ["20", "40", "10", "8"],
            "answer": 1,
            "explanation": "Shifting left by 2 adds two zeros -> `0b101000` = 40, which is 10 x 4. '20' would be shifting by only 1 bit.",
        },
        {
            "id": "ch01-warm-1",
            "type": "task",
            "title": "A box called score",
            "difficulty": 1,
            "plain": "Put a number in a variable and print it.",
            "instructions": r"""
1. Make a variable called `score` and put the number `7` inside.
2. Print the variable (not the word "score" - the box's content!).

Expected output: `7`
""",
            "starter": """# TODO: create score = 7 and print it
""",
            "example": """Your favourite striker just scored:

```python
goals = 12
print(goals)
```
""",

            "hints": [
                "A variable is made with `name = value`.",
                "`score = 7` fills the box; `print(score)` looks inside.",
                "Do not put quotes around score - quotes would print the word itself.",
            ],
            "solution": """score = 7
print(score)""",
            "explanation": "`score = 7` creates a box named score holding the number 7. `print(score)` - without quotes - makes Python look inside the box and show what it finds. With quotes it would have printed the literal word 'score'.\n\nWhat you learned: `name = value` stores, `print(name)` shows.",
            "tests": [
                {"kind": "program", "expected": "7", "match": "exact"},
            ],
        },
        {
            "id": "ch01-warm-2",
            "type": "task",
            "title": "Fill the hole",
            "difficulty": 1,
            "plain": "Use an f-string to drop your name into a sentence.",
            "instructions": r"""
Given `name = "Ada"`, print exactly:

```
Ada is learning Python.
```

- use an **f-string** (`f"..."`) with `{name}` inside - do not just
  type the name again
""",
            "starter": """name = "Ada"
# TODO: print the sentence with an f-string
""",
            "example": """Try the same trick on a different problem:

```python
pet = "Rex"
print(f"{pet} is a good dog.")
```
""",

            "hints": [
                "An f-string starts with the letter f before the quote.",
                "`{name}` inside the string is a hole that gets filled with the variable's value.",
                "`print(f\"{name} is learning Python.\")`",
            ],
            "solution": """name = "Ada"
print(f"{name} is learning Python.")""",
            "explanation": "The `f` before the quote activates the holes: `{name}` is replaced by whatever the variable holds - Ada. The rest of the text is printed letter for letter.\n\nWhat you learned: `f\"...{variable}...\"` mixes text and values in one line.",
            "tests": [
                {"kind": "program", "expected": "Ada is learning Python.",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch01-warm-3",
            "type": "task",
            "title": "Double it",
            "difficulty": 1,
            "plain": "Ask for a number, then print it doubled.",
            "instructions": "Write a program that asks `Number: `, reads a whole number and prints `Double: ` followed by twice the number.",
            "starter": """n = int(input("Number: "))
# TODO: print "Double:" and n times 2
""",
            "example": """Same idea, already solved:

```python
pushups = 30
print(f"Double: {pushups * 2}")
```
""",
            "hints": [
                "`input()` gives text - `int()` makes it a number.",
                "`n * 2` doubles the number.",
                "`print(\"Double:\", n * 2)` prints text and result together.",
            ],
            "solution": """n = int(input("Number: "))
print("Double:", n * 2)""",
            "explanation": "input() always hands back text, so int() turns it into a real whole number first. Then n * 2 is the doubled value and print() shows it next to the label. That input->convert->calculate->print pattern is the heart of almost every task in this chapter.",
            "tests": [
                {"kind": "program", "stdin": "7\n", "expected": "Double: 14"},
                {"kind": "program", "stdin": "21\n", "expected": "Double: 42"},
            ],
        },
        {
            "id": "ch01-warm-4",
            "type": "task",
            "title": "Price tag",
            "difficulty": 1,
            "plain": "Print a price with exactly two decimals.",
            "instructions": "Store `3.5` in a variable `price` and print it as `3.50 EUR`.",
            "starter": """price = 3.5
# TODO: print the price as "3.50 EUR" - the :.2f format does the padding
""",
            "example": """A cheaper tag works the same way:

```python
snack = 0.8
print(f"{snack:.2f} EUR")
```
""",
            "hints": [
                "The format spec `:.2f` rounds and pads to two decimals.",
                "It goes inside the f-string braces: `f\"{price:.2f}\"`.",
                "Add ` EUR` after the braces: `print(f\"{price:.2f} EUR\")`.",
            ],
            "solution": """price = 3.5
print(f"{price:.2f} EUR")""",
            "explanation": "The format spec :.2f inside an f-string rounds a number to exactly two decimal places and pads with a zero when needed - 3.5 becomes 3.50. That is exactly what every price on a receipt needs, and the school tasks in this chapter lean on it heavily.",
            "tests": [
                {"kind": "program", "expected": "3.50 EUR"},
            ],
        },
        {
            "id": "ch01-task-1",
            "type": "task",
            "title": "Seconds to h:m:s",
            "difficulty": 1,
            "plain": "Turn a big number of seconds into hours, minutes and seconds.",
            "instructions": r"""
A number of seconds is typed in. Split it into **hours**, **minutes**
and leftover **seconds**, and print all three.

For input `3700` the output must be:

```
Hours: 1
Minutes: 1
Seconds: 40
```

- 1 hour = 3600 seconds, 1 minute = 60 seconds
- use `//` (whole times) and `%` (leftover)
- print exactly `Hours: X`, `Minutes: Y`, `Seconds: Z`
""",
            "starter": """seconds = int(input("Seconds: "))
hours = seconds // 3600
print("Hours:", hours)
seconds %= 3600          # keep only what didn't fit into whole hours
# TODO: minutes = whole minutes in the leftover, print "Minutes: ..."
# TODO: seconds %= 60, then print "Seconds: ..."
# TODO: bonus line f"It is {hours:02}:{minutes:02}:{seconds:02}"
""",
            "example": """A study timer uses the same // and % split:

```python
total = 200
hours = total // 60
minutes = total % 60
print(f"{hours}:{minutes:02}")
```
""",

            "hints": [
                "How many whole hours fit? `seconds // 3600`.",
                "After taking the hours away with `seconds %= 3600`, do the same trick with 60 for the minutes.",
                "Hours: `seconds // 3600`; update `seconds %= 3600`; minutes: `seconds // 60`; seconds: `seconds % 60`.",
            ],
            "solution": """seconds = int(input("Seconds: "))
hours = seconds // 3600
print("Hours:", hours)
seconds %= 3600
minutes = seconds // 60
print("Minutes:", minutes)
seconds %= 60
print("Seconds:", seconds)
print(f"It is {hours:02}:{minutes:02}:{seconds:02}")
""",
            "explanation": "Think of it like paying with coins: first take out as many 3600-coins (hours) as possible - `//` counts them, `%=` leaves the remainder in the box. Then do the same with 60-coins (minutes); whatever is left is the seconds. The last line is a bonus: `:02` pads each number to two digits.\n\nWhat you learned: `//` and `%` split a total into whole units plus leftovers.",
            "tests": [
                {"kind": "program", "stdin": "3700\n",
                 "expected": "Hours: 1\nMinutes: 1\nSeconds: 40"},
                {"kind": "program", "stdin": "3661\n",
                 "expected": "Hours: 1\nMinutes: 1\nSeconds: 1"},
                {"kind": "program", "stdin": "59\n",
                 "expected": "Hours: 0\nMinutes: 0\nSeconds: 59"},
                {"kind": "program", "stdin": "86399\n",
                 "expected": "Hours: 23\nMinutes: 59\nSeconds: 59"},
            ],
        },
        {
            "id": "ch01-task-2",
            "type": "task",
            "title": "Circle area and circumference",
            "difficulty": 1,
            "plain": "Given a circle's radius, print its area and its edge length.",
            "instructions": r"""
Read the radius `r` of a circle (a float) and compute:

- **area** = π - r² (`math.pi * radius**2`)
- **circumference** = 2 - π - r

Print both rounded to **two decimals**, exactly like this for radius 5:

```
Area: 78.54
Circumference: 31.42
```

Use `import math`, `math.pi` and the f-string format `{value:.2f}`.
""",
            "starter": """import math
radius = float(input("Radius: "))
area = math.pi * radius**2
print(f"Area: {area:.2f}")
# TODO: circumference = 2 * math.pi * radius
# TODO: print "Circumference: ..." with two decimals
""",
            "example": """A soup can works exactly like the circle:

```python
import math
r = 2
height = 5
volume = math.pi * r**2 * height
print(f"Can volume: {volume:.2f} ml")
```
""",

            "hints": [
                "Area = πxr², circumference = 2xπxr. π lives in `math.pi`.",
                "Store both results in variables, then print with f-strings.",
                "`print(f\"Area: {area:.2f}\")` gives exactly two decimals.",
            ],
            "solution": """import math
radius = float(input("Radius: "))
area = math.pi * radius**2
circumference = 2.0 * math.pi * radius
print(f"Area: {area:.2f}")
print(f"Circumference: {circumference:.2f}")
""",
            "explanation": "The maths is two formulas: πr² for the area and 2πr for the edge. `radius**2` squares the radius, and `math.pi` supplies π. `:.2f` inside the f-string rounds each number to two decimals - that is why 78.5398... prints as 78.54.\n\nWhat you learned: `import math` unlocks π and friends; `:.2f` rounds for printing.",
            "tests": [
                {"kind": "program", "stdin": "5\n",
                 "expected": "Area: 78.54\nCircumference: 31.42"},
                {"kind": "program", "stdin": "1\n",
                 "expected": "Area: 3.14\nCircumference: 6.28"},
                {"kind": "program", "stdin": "2.5\n",
                 "expected": "Area: 19.63\nCircumference: 15.71"},
            ],
        },
        {
            "id": "ch01-task-3",
            "type": "task",
            "title": "Shopping receipt",
            "difficulty": 1,
            "plain": "Print a mini receipt for apples and bread with tidy prices.",
            "instructions": r"""
A shop sells apples at **0.75 €** and bread at **2.40 €** per loaf.

Read two numbers: how many apples, how many loaves. Then print the
receipt using f-strings - every price with **exactly two decimals**:

```
Apples: 4 x 0.75 EUR = 3.00 EUR
Bread: 2 x 2.40 EUR = 4.80 EUR
Total: 7.80 EUR
```
""",
            "starter": """apples = int(input("How many apples? "))
bread = int(input("How many loaves of bread? "))
apple_price = 0.75
bread_price = 2.40
apple_total = apples * apple_price
# TODO: bread_total the same way

print(f"Apples: {apples} x {apple_price:.2f} EUR = {apple_total:.2f} EUR")
# TODO: print the Bread line in the same style
# TODO: print the Total line (apple_total + bread_total)
""",
            "example": """A cinema receipt:

```python
tickets = 2
price = 9.50
total = tickets * price
print(f"Tickets: {tickets} x {price:.2f} EUR = {total:.2f} EUR")
```
""",

            "hints": [
                "First work out `apples * 0.75` and `bread * 2.40` and keep them in variables.",
                "`{price:.2f}` prints 0.75 as `0.75` and 3 as `3.00`.",
                "The total line is the sum of the two line totals, also with `.2f`.",
            ],
            "solution": """apples = int(input("How many apples? "))
bread = int(input("How many loaves of bread? "))
apple_price = 0.75
bread_price = 2.40
apple_total = apples * apple_price
bread_total = bread * bread_price
print(f"Apples: {apples} x {apple_price:.2f} EUR = {apple_total:.2f} EUR")
print(f"Bread: {bread} x {bread_price:.2f} EUR = {bread_total:.2f} EUR")
print(f"Total: {apple_total + bread_total:.2f} EUR")
""",
            "explanation": "Each receipt line is one f-string mixing fixed text (`Apples:`) with holes (`{apples}`, `{apple_price:.2f}`). Count x price gives each line total; the last line adds them. The `.2f` format keeps every price looking like money - `3` becomes `3.00`.\n\nWhat you learned: f-strings make formatted, readable output easy.",
            "tests": [
                {"kind": "program", "stdin": "4\n2\n",
                 "expected": "Apples: 4 x 0.75 EUR = 3.00 EUR\nBread: 2 x 2.40 EUR = 4.80 EUR\nTotal: 7.80 EUR"},
                {"kind": "program", "stdin": "10\n1\n",
                 "expected": "Apples: 10 x 0.75 EUR = 7.50 EUR\nBread: 1 x 2.40 EUR = 2.40 EUR\nTotal: 9.90 EUR"},
                {"kind": "program", "stdin": "0\n3\n",
                 "expected": "Apples: 0 x 0.75 EUR = 0.00 EUR\nBread: 3 x 2.40 EUR = 7.20 EUR\nTotal: 7.20 EUR"},
            ],
        },
        {
            "id": "ch01-task-4",
            "type": "task",
            "title": "Division and remainder",
            "difficulty": 1,
            "plain": "For two numbers, show the whole division, the leftover, and if it splits evenly.",
            "instructions": r"""
Read two integers `a` and `b` and print three lines:

```
17 // 5 = 3
17 % 5 = 2
17 is divisible by 5: False
```

- line 1: `a // b` - how many whole times b fits into a
- line 2: `a % b` - the leftover
- line 3: `True` when `a % b == 0` (divides evenly), else `False`
""",
            "starter": """a = int(input("a: "))
b = int(input("b: "))
print(f"{a} // {b} = {a // b}")
# TODO: print the % line the same way
# TODO: print f"{a} is divisible by {b}: ..." - True when a % b == 0
""",
            "example": """Cookies for four friends:

```python
print(f"13 % 4 = {13 % 4}")
print(f"12 divisible by 4: {12 % 4 == 0}")
```
""",

            "hints": [
                "`a // b` is whole division, `a % b` is the leftover.",
                "`a % b == 0` is exactly True when nothing is left over.",
                "Put the maths inside the f-strings: `f\"{a} // {b} = {a // b}\"`.",
            ],
            "solution": """a = int(input("a: "))
b = int(input("b: "))
print(f"{a} // {b} = {a // b}")
print(f"{a} % {b} = {a % b}")
print(f"{a} is divisible by {b}: {a % b == 0}")
""",
            "explanation": "Three f-strings, each with the maths done inside the braces. The last one compares the leftover with zero - `a % b == 0` gives a `bool` (True/False), which prints directly. 17 and 5: three fives fit, two left over, so it is not divisible.\n\nWhat you learned: you can compute right inside an f-string's `{}` holes.",
            "tests": [
                {"kind": "program", "stdin": "17\n5\n",
                 "expected": "17 // 5 = 3\n17 % 5 = 2\n17 is divisible by 5: False"},
                {"kind": "program", "stdin": "20\n4\n",
                 "expected": "20 // 4 = 5\n20 % 4 = 0\n20 is divisible by 4: True"},
            ],
        },
        {
            "id": "ch01-task-5",
            "type": "task",
            "title": "IP to 32-bit integer",
            "difficulty": 3,
            "plain": "An IP address is secretly one big number - convert it there and back.",
            "instructions": r"""
IPv4 addresses like `192.168.27.101` are really 32-bit numbers: each of
the four parts fills one byte (8 bits).

Write **two functions**:

- `ip_to_bits(ip)` - takes a string like `"192.168.27.101"` and returns
  the 32-bit integer. For each part `p`: `bits = (bits << 8) + int(p)`.
- `bits_to_ip(bits)` - the way back: four times take `bits % 256`,
  then `bits //= 256`, collect the parts **in the right order** and
  join them with `.`.

Then print this report for IP `192.168.27.101` and mask
`255.255.255.0`:

```
IP: 192.168.27.101
IP bits: 11000000101010000001101101100101
Mask: 255.255.255.0
Mask bits: 11111111111111111111111100000000
Mask CIDR: 24
Network: 192.168.27.0
Broadcast: 192.168.27.255
```

- `{bits:032b}` formats an int as 32 binary digits
- CIDR = number of `1` bits in the mask: `f"{mask_bits:032b}".count("1")`
- network = `ip_bits & mask_bits`
- broadcast = `network + 2**(32 - cidr) - 1`
""",
            "starter": """ip = "192.168.27.101"
mask = "255.255.255.0"


def ip_to_bits(ip):
    bits = 0
    for part in ip.split("."):
        bits = (bits << 8) + int(part)
    return bits


def bits_to_ip(bits):
    parts = []
    for _ in range(4):
        parts.insert(0, str(bits % 256))
        bits //= 256
    return ".".join(parts)


# TODO: ip_bits = ip_to_bits(ip), print "IP: ..." and
#       "IP bits: {ip_bits:032b}" (the 032b format = 32 binary digits)
# TODO: the same two lines for the mask
# TODO: cidr = how many "1"s in the mask's bit string -> "Mask CIDR: ..."
# TODO: network = ip_bits & mask_bits -> print "Network: " + bits_to_ip(...)
# TODO: broadcast = network + 2**(32 - cidr) - 1 -> "Broadcast: ..."
""",
            "example": """Packing a simpler IP into one number:

```python
ip = "10.0.0.7"
bits = 0
for part in ip.split("."):
    bits = (bits << 8) + int(part)
print(bits)
print(f"{bits:032b}")
```
""",

            "hints": [
                "`ip.split(\".\")` gives you the four parts as text - `int()` makes them numbers.",
                "In `bits_to_ip`, collect `str(bits % 256)` four times with `bits //= 256` - you get the parts backwards, so `insert(0, ...)` or `reverse()` before joining.",
                "Network is `ip_bits & mask_bits`; the rest follows the formulas in the instructions.",
            ],
            "solution": """ip = "192.168.27.101"
mask = "255.255.255.0"

def ip_to_bits(ip):
    bits = 0
    for part in ip.split("."):
        bits = (bits << 8) + int(part)
    return bits

def bits_to_ip(bits):
    parts = []
    for _ in range(4):
        parts.insert(0, str(bits % 256))
        bits //= 256
    return ".".join(parts)

print(f"IP: {ip}")
ip_bits = ip_to_bits(ip)
print(f"IP bits: {ip_bits:032b}")
print(f"Mask: {mask}")
mask_bits = ip_to_bits(mask)
print(f"Mask bits: {mask_bits:032b}")
cidr = f"{mask_bits:032b}".count("1")
print(f"Mask CIDR: {cidr}")
network = ip_bits & mask_bits
print(f"Network: {bits_to_ip(network)}")
broadcast = network + 2**(32 - cidr) - 1
print(f"Broadcast: {bits_to_ip(broadcast)}")
""",
            "explanation": "Shifting left by 8 makes room for one more part: `bits << 8` slides everything up and `+ int(p)` fills the new slot - after four parts the 32-bit number is complete. Going back, `% 256` peels off the lowest 8 bits and `//= 256` shifts them away; the parts come out backwards, so `insert(0, ...)` un-reverses them. The report then uses the bit tools: AND of IP and mask gives the network, and the broadcast fills the host bits with ones via `2**(32-cidr) - 1`.\n\nWhat you learned: shifts and AND let you pack and unpack numbers inside numbers - exactly how computers store IP addresses.",
            "tests": [
                {"kind": "expr", "expr": 'ip_to_bits("192.168.27.101")',
                 "expected": "3232242533",
                 "desc": "ip_to_bits(\"192.168.27.101\") == 3232242533"},
                {"kind": "expr", "expr": 'ip_to_bits("0.0.0.0")',
                 "expected": "0"},
                {"kind": "expr", "expr": 'ip_to_bits("255.255.255.255")',
                 "expected": "4294967295"},
                {"kind": "expr", "expr": 'bits_to_ip(3232242533)',
                 "expected": "\"192.168.27.101\""},
                {"kind": "expr", "expr": 'bits_to_ip(ip_to_bits("10.20.30.40"))',
                 "expected": "\"10.20.30.40\""},
                {"kind": "program",
                 "expected": "Network: 192.168.27.0\nBroadcast: 192.168.27.255"},
            ],
        },
        {
            "id": "ch01-boss",
            "type": "task",
            "title": "Coin machine",
            "difficulty": 3,
            "boss": True,
            "plain": "Turn a pile of cents into euros + cents and print a tidy report.",
            "instructions": r"""
**BOSS MISSION - the coin machine.**

A machine counts a pile of cents. Read the number of cents (an integer)
and split it into whole euros and remaining cents, then print a report.

For input `367` the output must be exactly:

```
Coins: 367
Euros: 3
Cents: 67
Total: 3.67 EUR
```

- `Euros` = whole euros (`//`), `Cents` = leftover (`%`)
- `Total` rebuilds the amount as euros + cents/100, formatted `.2f`
- format every line exactly as shown
""",
            "starter": """cents = int(input("How many cents? "))
# TODO: split into euros and cents, print the 4-line report
""",
            "example": """A tiny coin converter:

```python
cents = 256
print(f"{cents // 100} euro(s) and {cents % 100} cent(s)")
print(f"{cents / 100:.2f} EUR")
```
""",

            "hints": [
                "100 cents make a euro: `cents // 100` whole euros, `cents % 100` leftover.",
                "The total in euros is `euros + cents_left / 100` - or `cents / 100`.",
                "Last line: `f\"Total: {total:.2f} EUR\"`.",
            ],
            "solution": """cents = int(input("How many cents? "))
euros = cents // 100
rest = cents % 100
total = cents / 100
print(f"Coins: {cents}")
print(f"Euros: {euros}")
print(f"Cents: {rest}")
print(f"Total: {total:.2f} EUR")
""",
            "explanation": "Same trick as the seconds task, but with money: `// 100` counts whole euros, `% 100` is what stays in the tray. `Total` is the amount as a decimal - dividing by 100 moves the point two places - and `.2f` prints it money-style. All four lines are f-strings so labels and values mix cleanly.\n\nWhat you learned: `//`, `%` and `:.2f` together solve most everyday number jobs.",
            "tests": [
                {"kind": "program", "stdin": "367\n",
                 "expected": "How many cents? 367\nCoins: 367\nEuros: 3\nCents: 67\nTotal: 3.67 EUR",
                 "match": "exact"},
                {"kind": "program", "stdin": "99\n",
                 "expected": "How many cents? 99\nCoins: 99\nEuros: 0\nCents: 99\nTotal: 0.99 EUR",
                 "match": "exact"},
                {"kind": "program", "stdin": "500\n",
                 "expected": "How many cents? 500\nCoins: 500\nEuros: 5\nCents: 0\nTotal: 5.00 EUR",
                 "match": "exact"},
            ],
        },
    ],
}
