"""Kapitel 12 - Vier kleine Programme."""

CHAPTER = {
    "id": "ch12",
    "number": 12,
    "title": "Four Simple Programs",
    "summary": "Small complete programs: anagrams, digit of life, hidden words and Sudoku checks.",
    "items": [
        {
            "id": "ch12-lesson",
            "type": "lesson",
            "title": "From building blocks to programs",
            "body": r"""
Time to combine everything - strings, lists, sets, loops - into small
complete programs. Three patterns show up again and again in this
chapter's missions.

### Pattern 1: normalise before comparing

To compare two texts "fairly", first clean them the same way - spaces
out, all lowercase:

```python
text1 = "Schach spielen"
text2 = "Schnapsleiche"
a = sorted(text1.replace(" ", "").lower())
b = sorted(text2.replace(" ", "").lower())
print(a == b)    # True - same letters, same counts
```

> **What happens here**
>
> - line 3: `replace(" ", "")` deletes every space, `lower()` flattens
>   the case, `sorted` alphabetises the letters into a list
> - line 4: the same cleaning for the second text
> - line 5: two texts with identical letters produce identical sorted
>   lists - that's the whole **anagram** test (same letters, different
>   order)

> **Think of it like...** dumping two Scrabble bags on the table and
> sorting the tiles - if the piles match, the words are anagrams.

### Pattern 2: walking a grid

A grid (like a Sudoku board) is a list of strings - `board[row][col]`
digs in two steps, first the row, then the character:

```python
board = ["295743861", "431865927", "876192543"]
print(board[0])        # first row
print(board[0][1])     # row 0, column 1
col = "".join(board[r][0] for r in range(3))   # first column
print(col)
```

> **What happens here**
>
> - line 2: `board[0]` is the whole first row string
> - line 3: `board[0]` gives row 0, then `[1]` picks its character -
>   '9'
> - line 4: a generator grabs `board[r][0]` for each row r, `join`
>   glues them into the column string '248'

> **Watch out** - `board[0][1]` is row-first, column-second - the
> opposite of x/y coordinates!

### Pattern 3: repeat until done

Some questions need a loop that keeps shrinking the answer until only
one digit is left - the "digit sum":

```python
digits = "19911228"
while len(digits) > 1:
    digits = str(sum(int(c) for c in digits))
print(digits)
```

> **What happens here**
>
> - line 2: while more than one character remains...
> - line 3: `int(c)` turns each character into a number, `sum` adds
>   them, `str` makes it a string again for the next round -
>   '19911228' -> '40' -> '4'
> - line 4: the loop ends when one digit survives -> prints 4

## Try it yourself

- Check if `'abc'` and `'cab '` are "equal" after normalising.
- Hand-compute the digit sum of `'9999'`, then let Python do it.
- Print `board[1][2]` from the grid - which digit?

## Key words

| Word | Meaning |
|---|---|
| anagram | same letters, different order |
| normalise | clean data before comparing (spaces, case) |
| sorted(word) | a word's letters as a sorted list |
| grid | a list of strings - `board[row][col]` |
| generator + join | collect characters into a string |
| digit sum | add all digits, repeat until one remains |
""",
        },
        {
            "id": "ch12-quiz-1",
            "type": "quiz",
            "title": "Anagrams",
            "question": "Which pair is an anagram (case- and space-insensitive)?",
            "options": ["'Auto' / 'Haus'", "'Bier' / 'Brei'", "'Haus' / 'Maus'", "'Tag' / 'Tor'"],
            "answer": 1,
            "explanation": "Bier and Brei hold exactly the same letters - sorted they're identical. Haus/Maus look tempting (rhyme!) but swap h->m.",
        },
        {
            "id": "ch12-quiz-2",
            "type": "quiz",
            "title": "find()",
            "question": "'abcabc'.find('c', 3) returns...",
            "options": ["2", "5", "-1", "3"],
            "answer": 1,
            "explanation": "The second argument says 'start looking at index 3' - the c at index 2 is skipped, the next is at 5.",
        },
        {
            "id": "ch12-quiz-3",
            "type": "quiz",
            "title": "Sudoku rule",
            "question": "A solved Sudoku requires each row, column and 3x3 box to contain...",
            "options": ["digits sorted ascending", "each digit 1-9 exactly once", "an even sum", "no repeats anywhere on the board"],
            "answer": 1,
            "explanation": "Every unit needs all of 1-9 exactly once - order irrelevant. 'No repeats on the whole board' would be impossible (81 squares, 9 digits).",
        },
        {
            "id": "ch12-quiz-4",
            "type": "quiz",
            "title": "Digit sum",
            "question": "The digit of life of '99' is...",
            "options": ["18", "9", "1", "99"],
            "answer": 1,
            "explanation": "9+9=18, still two digits, so again: 1+8=9. Repeating until one digit is the whole rule.",
        },
        {
            "id": "ch12-warm-1",
            "type": "task",
            "title": "Same letters?",
            "difficulty": 1,
            "plain": "Check if two words contain the same letters - the mini version of anagrams.",
            "instructions": r"""
Print `True` if `a` and `b` contain the same letters (case ignored),
else `False`.

```python
a = "Listen"; b = "Silent"   # -> True
```

Expected output: `True`
""",
            "starter": """a = "Listen"
b = "Silent"
# TODO: print whether a and b have the same letters
""",
            "hints": [
                "Lowercase both, then compare `sorted(...)`.",
                "`sorted` on a string gives a sorted letter list.",
                "One print: `print(sorted(a.lower()) == sorted(b.lower()))`.",
            ],
            "solution": """a = "Listen"
b = "Silent"
print(sorted(a.lower()) == sorted(b.lower()))""",
            "explanation": "`sorted` alphabetises each word's letters - equal letter bags give equal lists. `lower()` makes the capital L fair. The comparison itself is the True/False answer.\n\nWhat you learned: `sorted(word)` is the fingerprint of its letters.",
            "tests": [
                {"kind": "program", "expected": "True", "match": "exact"},
            ],
        },
        {
            "id": "ch12-warm-2",
            "type": "task",
            "title": "Sum the digits",
            "difficulty": 1,
            "plain": "Add up all the digits in a number string - once.",
            "instructions": r"""
Print the sum of all digits in `digits = "12345"`.

Expected output: `15`
""",
            "starter": """digits = "12345"
# TODO: print the sum of the digits
""",
            "hints": [
                "Each character must become a number: `int(c)`.",
                "`sum(int(c) for c in digits)` does it in one line.",
                "A generator inside `sum` needs no list brackets.",
            ],
            "solution": """digits = "12345"
print(sum(int(c) for c in digits))""",
            "explanation": "The generator `int(c) for c in digits` feeds each digit - converted from character to number - into `sum`. 1+2+3+4+5 = 15.\n\nWhat you learned: `sum(int(c) for c in s)` totals a digit string.",
            "tests": [
                {"kind": "program", "expected": "15", "match": "exact"},
            ],
        },
        {
            "id": "ch12-task-1",
            "type": "task",
            "title": "Anagrams",
            "difficulty": 1,
            "plain": "Ask for two words and say whether they're letter-twins.",
            "instructions": r"""
Read two texts and print whether they are **anagrams** - same letters,
ignoring case and spaces.

Rules:

- case ignored; spaces ignored entirely
- two empty strings are NOT anagrams
- print exactly `anagrams` or `no anagrams`

`Bundestag`/`Angstbude` -> anagrams (and the tricky pair `Achse`/
`Sache` - same letters!); `Haus`/`Maus` -> no anagrams.
""",
            "starter": """word1 = input("Word 1: ")
word2 = input("Word 2: ")

# TODO: check whether word1 and word2 are anagrams
""",
            "hints": [
                "Normalise both: `replace(' ', '').lower()`.",
                "Letter-twins check: `sorted(a) == sorted(b)`.",
                "Guard against empty: `if a and b and sorted(a) == sorted(b)`.",
            ],
            "solution": """word1 = input("Word 1: ")
word2 = input("Word 2: ")

a = word1.replace(" ", "").lower()
b = word2.replace(" ", "").lower()

if a and b and sorted(a) == sorted(b):
    print("anagrams")
else:
    print("no anagrams")
""",
            "explanation": "Both texts get cleaned the same way - spaces out, case down - then `sorted` compares their letter fingerprints. The `a and b` guard rejects the empty-empty case, which would otherwise sneak through as a false match.\n\nWhat you learned: normalise first, then compare fingerprints.",
            "tests": [
                {"kind": "program", "stdin": "Bundestag\nAngstbude\n",
                 "expected": "anagrams", "match": "lines"},
                {"kind": "program", "stdin": "Schach spielen\nSchnapsleiche\n",
                 "expected": "anagrams", "match": "lines"},
                {"kind": "program", "stdin": "Achse\nSache\n",
                 "expected": "anagrams", "match": "lines"},
                {"kind": "program", "stdin": "Haus\nMaus\n",
                 "expected": "no anagrams", "match": "lines"},
            ],
        },
        {
            "id": "ch12-task-2",
            "type": "task",
            "title": "The digit of life",
            "difficulty": 1,
            "plain": "Shrink a birthday to one digit by adding digits again and again.",
            "instructions": r"""
The "digit of life" of a birthday: add all digits; if the result still
has more than one digit, repeat until one remains.

`20170101` -> `2+0+1+7+0+1+0+1 = 12` -> `1+2 = 3` -> `3`.

Read a digit string, accept length 6 or 8 only (else print
`invalid input`), then print the single digit.
""",
            "starter": """digits = input("Your birthday: ")

# TODO: validate length (6 or 8 digits), then reduce to one digit
""",
            "hints": [
                "Check `len(digits) in (6, 8)` and `digits.isdigit()` first.",
                "The shrinking loop: `while len(digits) > 1: digits = str(sum(int(c) for c in digits))`.",
                "After the loop, digits holds one character - print it.",
            ],
            "solution": """digits = input("Your birthday: ")
if len(digits) not in (6, 8) or not digits.isdigit():
    print("invalid input")
else:
    while len(digits) > 1:
        digits = str(sum(int(c) for c in digits))
    print(digits)
""",
            "explanation": "Each loop round converts the digit string into its sum and back - '19911228' -> '40' -> '4'. The while stops when a single character remains. `isdigit` plus the length check guard the entrance.\n\nWhat you learned: `while` + reassigning the variable = 'repeat until done'.",
            "tests": [
                {"kind": "program", "stdin": "19911228\n", "expected": "6", "match": "lines"},
                {"kind": "program", "stdin": "20000101\n", "expected": "4", "match": "lines"},
                {"kind": "program", "stdin": "20170101\n", "expected": "3", "match": "lines"},
            ],
        },
        {
            "id": "ch12-task-3",
            "type": "task",
            "title": "Find a word",
            "difficulty": 2,
            "plain": "Do the word's letters hide inside the text - in order?",
            "instructions": r"""
Are the word's characters hidden inside the text **in order** (not
necessarily next to each other)?

Examples: `Nabu` in `Nabucodonosor` -> `yes`; `Bund` in
`Nabucodonosor` -> `no` (its only `d` sits before the second `n`).

Read word and text (two input lines), ignore case, print `yes` or
`no`. Use `find()` with a start position.
""",
            "starter": """word = input("Your word: ").strip().lower()
hideout = input("Your hideout: ").strip().lower()

# TODO: check whether word's letters appear in order inside hideout
""",
            "hints": [
                "Track `pos = 0`; for each letter `c`, `i = hideout.find(c, pos)`.",
                "`i == -1` -> letter not found -> `no`, break.",
                "Otherwise move forward: `pos = i + 1` - letters must come in order.",
            ],
            "solution": """word = input("Your word: ").strip().lower()
hideout = input("Your hideout: ").strip().lower()

pos = 0
found = True
for c in word:
    i = hideout.find(c, pos)
    if i == -1:
        found = False
        break
    pos = i + 1
print("yes" if found else "no")
""",
            "explanation": "`find(c, pos)` searches only from `pos` onward - so each new letter must appear *after* the previous hit, which enforces the order. `pos = i + 1` steps past the found letter; a `-1` flips `found` to False and breaks.\n\nWhat you learned: a moving start position makes find() an order-checker.",
            "tests": [
                {"kind": "program", "stdin": "Nabu\nNabucodonosor\n",
                 "expected": "yes", "match": "lines"},
                {"kind": "program", "stdin": "Bund\nNabucodonosor\n",
                 "expected": "no", "match": "lines"},
                {"kind": "program", "stdin": "Hund\nhxxuxxnd\n",
                 "expected": "yes", "match": "lines"},
                {"kind": "program", "stdin": "Hund\nvcxzlxduybfdsobymwefgas\n",
                 "expected": "no", "match": "lines"},
            ],
        },
        {
            "id": "ch12-task-4",
            "type": "task",
            "title": "Sudoku validation",
            "difficulty": 3,
            "instructions": r"""
Write `is_valid_sudoku(rows)` - takes a list of 9 strings (9 digits
each) and returns `True` for a correctly solved Sudoku:

- every row contains digits 1-9 exactly once
- every column too
- every 3x3 box too

Return `False` for malformed input (non-digits, wrong length).
""",
            "starter": """def is_valid_sudoku(rows):
    # TODO: check rows, columns and 3x3 boxes
    pass


# quick check:
# valid = ["295743861","431865927","876192543",
#          "387459216","612387495","549216738",
#          "763524189","928671354","154938672"]
# print(is_valid_sudoku(valid))   # True
""",
            "plain": "Check a finished Sudoku: every row, column and box must have 1-9 exactly once.",
            "hints": [
                "One helper does all the work: `sorted(unit) == list('123456789')`.",
                "Column c: `''.join(rows[r][c] for r in range(9))`.",
                "Box at corner (z, s): `rows[z+i][s:s+3]` for i in 0..2, with z,s stepping 0,3,6.",
            ],
            "solution": """def is_valid_sudoku(rows):
    def all_digits(chars):
        return sorted(chars) == list("123456789")

    if len(rows) != 9:
        return False
    for row in rows:
        if not row.isdecimal() or len(row) != 9:
            return False
        if not all_digits(row):
            return False
    for c in range(9):
        if not all_digits("".join(rows[r][c] for r in range(9))):
            return False
    for z in range(0, 9, 3):
        for s in range(0, 9, 3):
            box = rows[z][s:s+3] + rows[z+1][s:s+3] + rows[z+2][s:s+3]
            if not all_digits(box):
                return False
    return True
""",
            "explanation": "The helper `all_digits` turns 'contains 1-9 once each' into `sorted(x) == '123456789'` - one check used for all three unit types. Rows come straight from the list, columns are gathered with a generator over r, and boxes collect three row-slices starting at corner (z, s). Malformed input exits early with False.\n\nWhat you learned: write the rule once as a helper, then apply it to every kind of unit.",
            "tests": [
                {"kind": "expr",
                 "expr": "is_valid_sudoku(['295743861','431865927','876192543','387459216','612387495','549216738','763524189','928671354','154938672'])",
                 "expected": "True"},
                {"kind": "expr",
                 "expr": "is_valid_sudoku(['195743862','431865927','876192543','387459216','612387495','549216738','763524189','928671354','254938671'])",
                 "expected": "False"},
                {"kind": "expr",
                 "expr": "is_valid_sudoku(['29574386x','431865927','876192543','387459216','612387495','549216738','763524189','928671354','154938672'])",
                 "expected": "False"},
            ],
        },
        {
            "id": "ch12-boss",
            "type": "task",
            "title": "Mini Sudoku checker",
            "difficulty": 3,
            "boss": True,
            "plain": "The same Sudoku rules - but on a cute 4x4 board.",
            "instructions": r"""
**BOSS MISSION - Mini Sudoku.**

A 4x4 mini-Sudoku uses digits 1-4. Write `is_valid_mini(rows)` -
4 strings of 4 digits, `True` when every row, column and **2x2 box**
contains 1-4 exactly once (False for anything malformed too).

```python
is_valid_mini(['1234','3412','2143','4321'])   # True
is_valid_mini(['1134','3412','2143','4321'])   # False - row 0 broken
```
""",
            "starter": """def is_valid_mini(rows):
    # TODO: rows, columns and 2x2 boxes must each hold 1-4 once
    pass
""",
            "example": """Is a row a valid 1-4 row?

```python
print(sorted("2413") == list("1234"))
print(sorted("1123") == list("1234"))
```
""",

            "hints": [
                "Same pattern as the big task - helper `sorted(u) == list('1234')`.",
                "Boxes step 2: corners (0,0), (0,2), (2,0), (2,2); each box is two row-slices of 2.",
                "Guard first: 4 rows, all digits, length 4.",
            ],
            "solution": """def is_valid_mini(rows):
    def all_digits(chars):
        return sorted(chars) == list("1234")

    if len(rows) != 4:
        return False
    for row in rows:
        if not row.isdecimal() or len(row) != 4:
            return False
        if not all_digits(row):
            return False
    for c in range(4):
        if not all_digits("".join(rows[r][c] for r in range(4))):
            return False
    for z in range(0, 4, 2):
        for s in range(0, 4, 2):
            box = rows[z][s:s+2] + rows[z+1][s:s+2]
            if not all_digits(box):
                return False
    return True
""",
            "explanation": "Identical machinery, smaller board: the helper checks sorted content is '1234', rows and columns loop as before, and the four 2x2 boxes sit at corners stepping by 2. Each box is two 2-character row-slices glued together.\n\nWhat you learned: a solution that generalises is worth twice as much - sizes became parameters.",
            "tests": [
                {"kind": "expr",
                 "expr": "is_valid_mini(['1234','3412','2143','4321'])", "expected": "True"},
                {"kind": "expr",
                 "expr": "is_valid_mini(['1134','3412','2143','4321'])", "expected": "False"},
                {"kind": "expr",
                 "expr": "is_valid_mini(['1234','3412','2143','1423'])", "expected": "False"},
                {"kind": "expr", "expr": "is_valid_mini(['1234','34x2','2143','4321'])", "expected": "False"},
            ],
        },
    ],
}
