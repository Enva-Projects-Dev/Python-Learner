"""Kapitel 0 - Getting Started (erste Schritte, print, wie die App tickt)."""

CHAPTER = {
    "id": "ch00",
    "number": 0,
    "title": "Getting Started",
    "summary": "What a program is, how to print your first lines, and how this course works.",
    "items": [
        {
            "id": "ch00-lesson-1",
            "type": "lesson",
            "title": "What is a program?",
            "body": r"""
## A program is a list of instructions

A computer is very fast but not very clever. It cannot guess what you
want. A **program** is a list of instructions you write down, and the
computer follows them exactly, one after another, top to bottom.

> **Think of it like...** a recipe. "Break 2 eggs. Stir. Fry." If you write
> the steps in the wrong order - fry first, break eggs later - the recipe
> goes wrong. Programs are the same: order matters.

**Python** is the language we use to write those instructions. It reads
almost like English.

## Saying something: print

The most important instruction for us is `print`. It makes the program
write a line of text on the screen:

```python
print("Hello!")
print("I am a program.")
```

> **What happens here**
>
> - line 1: prints `Hello!` - the quotes tell Python "this is text, not
>   an instruction"
> - line 2: prints the second line right under the first

Every `print` writes one line. Whatever sits inside the round brackets
`( )` gets printed - always with quotes around text.

## How this course works

- **Lessons** (like this one) explain ideas. Every code block has a
  **Run** button - press it and see what the code does.
- **Tasks** ask you to write code yourself. **Run** tries your code,
  **Check** runs the tests and marks the task done when it is right.
- **Quizzes** are little puzzles - no code needed, just thinking.

You earn **XP** for finishing things: tasks are worth the most, quizzes
and lessons a bit less. XP levels you up - from **Novice** all the way
to **Master**.

## Try it yourself

- Change `print("Hello!")` to print your own name and press **Run**.
- Add a third `print` line and Run again.
- Remove one of the quotes on purpose - what does the red error say?

## Key words

| Word | Meaning |
|---|---|
| program | a list of instructions the computer follows |
| print | the instruction that writes text on the screen |
| run | start the program and watch it work |
| XP | points you earn for finishing tasks, quizzes and lessons |
""",
        },
        {
            "id": "ch00-lesson-2",
            "type": "lesson",
            "title": "Your first program",
            "body": r"""
## Text vs numbers

`print` can show two different kinds of things:

```python
print("Hello")     # text - always inside quotes
print(42)          # a number - no quotes
print(6 + 7)
```

> **What happens here**
>
> - line 1: prints the word Hello (the quotes are not shown)
> - line 2: prints the number 42
> - line 3: Python first does the maths, then prints 13

> **Watch out** - `print("6 + 7")` prints the *text* `6 + 7`, not 13.
> Quotes turn maths into plain text.

## Comments: notes for humans

A `#` starts a **comment**. Python ignores everything after it - it is a
note for you and other readers:

```python
# This program says hi
print("Hi!")  # this part is real code
```

## Errors are normal - read them!

Everyone writes broken code. When Python cannot understand a line, it
prints an **error message** in red. Read the red text **from the bottom
up**: the last line tells you what went wrong, the line above shows
where.

```python
# print("Oops)   <- broken on purpose: the closing quote is missing!
print("Oops")    # fixed - now it runs
```

> **What happens here**
>
> - line 1: the `#` makes this a comment - Python skips the broken line
> - line 2: with both quotes in place, it prints Oops

Remove the `#` on line 1 and run again - Python prints something like
`SyntaxError: unterminated string literal`: it found the opening quote
but never the closing one.

> **Think of it like...** the error message is the program raising its
> hand and saying "I don't understand this part!" - it is helping you,
> not scolding you.

## Try it yourself

- Print `10 * 5` with quotes and without - spot the difference.
- Write a comment above a print line.
- Break a print on purpose and read the red message from the bottom up.

## Key words

| Word | Meaning |
|---|---|
| string | text inside quotes |
| comment | a note after `#` that Python ignores |
| error message | the red text Python prints when code breaks |
| SyntaxError | "I can't even read this line" - often a missing quote or bracket |
""",
        },
        {
            "id": "ch00-quiz-1",
            "type": "quiz",
            "title": "What prints?",
            "question": "What does `print(\"2 + 2\")` show on the screen?",
            "options": ["4", "2 + 2", "22", "Nothing - it is an error"],
            "answer": 1,
            "explanation": "The quotes turn `2 + 2` into text, so Python prints it exactly as written. `4` would be the answer to `print(2 + 2)` *without* quotes - then Python does the maths first.",
        },
        {
            "id": "ch00-quiz-2",
            "type": "quiz",
            "title": "Spot the bug",
            "question": "This line fails: `print(\"Good morning)` - why?",
            "options": ["print is spelled wrong", "the closing quote is missing", "the brackets are wrong", "Python does not allow capital letters"],
            "answer": 1,
            "explanation": "Text needs an opening *and* a closing quote. Here the closing `\"` is missing, so Python reports `unterminated string literal`. The spelling of print is fine - that is the other classic beginner bug.",
        },
        {
            "id": "ch00-quiz-3",
            "type": "quiz",
            "title": "Comments",
            "question": "What does this print? `print(\"Hi\") # print(\"Bye\")`",
            "options": ["Hi", "Bye", "Hi then Bye", "Nothing"],
            "answer": 0,
            "explanation": "Everything after `#` is a comment - Python ignores it completely, so only Hi is printed. 'Hi then Bye' would be right if the second print were on its own line.",
        },
        {
            "id": "ch00-task-1",
            "type": "task",
            "title": "Say hello",
            "difficulty": 1,
            "plain": "Make the computer say hello to the world.",
            "instructions": r"""
Write a program that prints this exact line:

```
Hello, world!
```

- use `print` with the text inside double quotes
- the capital H, the comma and the `!` all matter
""",
            "starter": """# TODO: print "Hello, world!" on the screen
""",
            "hints": [
                "print writes a line of text to the screen.",
                "Put the text inside the brackets, wrapped in double quotes.",
                "The whole line is: `print(\"Hello, world!\")`.",
            ],
            "solution": """print("Hello, world!")""",
            "explanation": "One line does everything. `print` is the instruction that shows something on the screen. The round brackets hold *what* to show, and the double quotes tell Python it is plain text. Python prints the words exactly as they are between the quotes - capital H, comma, exclamation mark and all.\n\nWhat you learned: `print(\"text\")` writes one line of text.",
            "tests": [
                {"kind": "program", "expected": "Hello, world!",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch00-task-2",
            "type": "task",
            "title": "Print three lines",
            "difficulty": 1,
            "plain": "Print three color names, each on its own line.",
            "instructions": r"""
Print these three lines, in this order - one `print` per line:

```
Red
Green
Blue
```
""",
            "starter": """# TODO: three print lines
""",
            "hints": [
                "Each print writes exactly one line.",
                "Write three `print(\"...\")` lines, one under the other.",
                "First `print(\"Red\")`, then Green, then Blue - order matters.",
            ],
            "solution": """print("Red")
print("Green")
print("Blue")""",
            "explanation": "Programs run top to bottom, so the three prints happen in order: Red first, Blue last. Each `print` starts a new line on the screen, which is why the words are stacked instead of in one row.\n\nWhat you learned: one `print` = one line, and code runs in order.",
            "tests": [
                {"kind": "program", "expected": "Red\nGreen\nBlue",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch00-task-3",
            "type": "task",
            "title": "Name tag",
            "difficulty": 1,
            "plain": "Print a name tag: two lines about yourself.",
            "instructions": r"""
Print a little name tag for **Ada** - exactly these two lines:

```
Name: Ada
Age: 36
```

- line 1: the word `Name:`, a space, then `Ada`
- line 2: `Age:` and the number `36`
""",
            "starter": """# TODO: print the two-line name tag
""",
            "hints": [
                "Two prints, one for each line.",
                "You can put the whole line - label and value - inside one pair of quotes.",
                "`print(\"Name: Ada\")` then `print(\"Age: 36\")`.",
            ],
            "solution": """print("Name: Ada")
print("Age: 36")""",
            "explanation": "Each print writes one line, and both lines live fully inside their own quotes - so whatever you type appears exactly. The labels `Name:` and `Age:` are just text like any other.\n\nWhat you learned: a print line can hold any text, including labels and numbers written as text.",
            "tests": [
                {"kind": "program", "expected": "Name: Ada\nAge: 36",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch00-task-4",
            "type": "task",
            "title": "Fix the broken program",
            "difficulty": 1,
            "plain": "Two tiny bugs hide in the code - find and fix them.",
            "instructions": r"""
The program below should print:

```
Hello
World
```

but it has **two bugs**. Find them, fix them, and Run to check.

Bug hunting tip: read the red error message - it tells you which line
is confused and why.
""",
            "starter": """print("Hello)
prnt("World")
""",
            "hints": [
                "Line 1: compare the quotes with a working print - something is missing at the end.",
                "Line 2: look at the instruction's spelling very carefully.",
                "Fix: add the closing `\"` after Hello, and spell it `print`, not `prnt`.",
            ],
            "solution": """print("Hello")
print("World")""",
            "explanation": "Two classic bugs. First, the opening quote before Hello had no closing partner, so Python reported an unterminated string - add the missing `\"`. Second, `prnt` is not an instruction Python knows (a `NameError`) - the right name is `print`. Fixing both makes both lines print.\n\nWhat you learned: error messages point at the line and say what is wrong - read them, they are your friend.",
            "tests": [
                {"kind": "program", "expected": "Hello\nWorld",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch00-boss",
            "type": "task",
            "title": "Mini poster",
            "difficulty": 3,
            "boss": True,
            "plain": "Draw a little poster frame around a message - only with print.",
            "instructions": r"""
**BOSS MISSION - print a poster.**

Use only `print` to draw this exact 4-line poster:

```
+------------+
| HI, ADA!   |
| YOU DID IT |
+------------+
```

- lines 1 and 4: `+`, then 12 `-`, then `+`
- line 2: `|`, a space, `HI, ADA!`, 3 spaces, `|` (12 chars inside)
- line 3: `|`, a space, `YOU DID IT`, a space, `|` (12 chars inside)

The easiest way: print each line as one piece of text in quotes.
Watch the spaces inside the `| |` bars - they must match exactly!
""",
            "starter": """# BOSS: print the 4-line poster exactly as shown
""",
            "hints": [
                "The top and bottom borders are identical: `+` + 12 dashes + `+`.",
                "Inside the bars the text field is 12 characters wide: ` HI, ADA!   ` and ` YOU DID IT ` - count the spaces.",
                "Four prints: `\"+------------+\"`, `\"| HI, ADA!   |\"`, `\"| YOU DID IT |\"`, then `\"+------------+\"` again.",
            ],
            "solution": """print("+------------+")
print("| HI, ADA!   |")
print("| YOU DID IT |")
print("+------------+")""",
            "explanation": "A poster is just text, so four prints are enough - but the spacing is the tricky part. Line 2 needs 12 characters between the bars: a space, `HI, ADA!` (8 chars), then 3 spaces. The top and bottom borders are identical `+` + 12 dashes + `+`.\n\nWhat you learned: exact output means exact characters - spaces count too.",
            "tests": [
                {"kind": "program",
                 "expected": "+------------+\n| HI, ADA!   |\n| YOU DID IT |\n+------------+",
                 "match": "exact"},
            ],
        },
    ],
}
