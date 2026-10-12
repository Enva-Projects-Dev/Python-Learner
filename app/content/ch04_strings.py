"""Kapitel 4 - Strings."""

CHAPTER = {
    "id": "ch04",
    "number": 4,
    "title": "Strings",
    "summary": "Text is a row of letters - read it, slice it, clean it and rebuild it.",
    "items": [
        {
            "id": "ch04-lesson",
            "type": "lesson",
            "title": "Working with strings",
            "body": r"""
## A string is a bead chain of letters

A **string** is text: a chain of single letters in order - like beads on
a string. You write it in quotes (single, double, or triple for
multi-line):

```python
s1 = 'A string in single quotes'
s2 = "The neighbour's dog is called Waldi"
print(s1)
print(s2)
```

Strings are **immutable** - you can't change a bead, only build a new
chain. All string methods return a **new** string:

```python
a = " Hello," + " World! "   # + glues strings together
b = a.strip()                # 'Hello, World!' - shaves edge spaces
print(b.lower())             # 'hello, world!'
print(b.upper())             # 'HELLO, WORLD!'
print("," in b)              # True - is it inside?
print(b.replace(",", ""))    # 'Hello World!'
print(b.split(" "))          # ['Hello,', 'World!'] - cut into a list
```

> **What happens here**
>
> - `strip` removes whitespace at both ends
> - `lower`/`upper` change every letter's case
> - `in` asks "is this inside?" -> True/False
> - `split` cuts at every space -> a list

Text and numbers can't be glued directly - convert with `str()` or use
an f-string:

```python
age = 17
print(f"I am {age}")          # best way
```

Two more string tricks: `*` repeats a string, `join` glues a list
back into one string:

```python
print("ab" * 3)                    # ababab
print("-" * 10)                    # a divider line
names = ["Ada", "Tom", "Zoe"]
print(", ".join(names))            # Ada, Tom, Zoe
```

## Lockers again: indexing and slicing

Letters have numbers just like list lockers - everything from chapter 3
works:

```python
s = "Hello World!"
print(s[0])       # 'H'
print(s[-1])      # '!'
print(s[6:])      # 'World!'
print(s[6:-1])    # 'World'
for c in s:
    print(c, end="-")   # walks letter by letter
print()
```

## Backwards: [::-1]

`s[::-1]` is the string backwards - perfect for palindromes (words that
read the same both ways):

```python
word = "Racecar"
print(word.lower() == word.lower()[::-1])   # True
```

## A first peek at functions

The last tasks of this chapter ask for tiny **functions**. A function
packs code under a name; `return` hands the answer back to the caller:

```python
def shout(word):
    return word.upper() + "!"

print(shout("hello"))     # HELLO!
print(shout("python"))    # PYTHON!
```

> **What happens here**
>
> - `def shout(word):` declares the recipe - `word` is its input
> - `return` sends the result back; `print` shows it
> - calling `shout("hello")` runs the recipe with `word = "hello"`

Chapter 5 goes much deeper - for now: `def` makes it, `return`
answers it.

## Try it yourself

- Print your name backwards with one slice.
- Take `"  spaces  "` and print it clean - then SHOUT it.

## Key words

| Word | Meaning |
|---|---|
| string | text - a chain of letters |
| immutable | can't be changed, only rebuilt |
| strip / lower / upper / replace / split | string methods (return new strings) |
| `[::-1]` | the backwards slice |
| palindrome | reads the same forwards and backwards |
""",
        },
        {
            "id": "ch04-quiz-1",
            "type": "quiz",
            "title": "Method chain",
            "question": "What does `'  Hello World  '.strip().upper()` produce?",
            "options": ["'  HELLO WORLD  '", "'HELLO WORLD'", "'hello world'", "'HELLO WORLD  '"],
            "answer": 1,
            "explanation": "strip() shaves the edge spaces first, then upper() shouts - 'HELLO WORLD'. The spaces survive only in the first and last options, but strip removes them before upper runs.",
        },
        {
            "id": "ch04-quiz-2",
            "type": "quiz",
            "title": "Slicing strings",
            "question": "For `s = 'Hello World!'`, what is `s[6:-1]`?",
            "options": ["'World!'", "'World'", "' World'", "'orld!'"],
            "answer": 1,
            "explanation": "Index 6 is 'W', and -1 cuts *before* the last character - so the '!' stays out: 'World'. 'World!' would be `s[6:]`.",
        },
        {
            "id": "ch04-quiz-3",
            "type": "quiz",
            "title": "Immutability",
            "question": "What happens on `s = 'abc'; s[0] = 'x'`?",
            "options": ["s becomes 'xbc'", "s becomes 'abc'", "A TypeError is raised", "A ValueError is raised"],
            "answer": 2,
            "explanation": "Strings are sealed - single letters can't be swapped out like list elements. `s[0] = 'x'` raises TypeError; to change text you build a new string.",
        },
        {
            "id": "ch04-quiz-4",
            "type": "quiz",
            "title": "Split",
            "question": "What does `'a-b-c'.split('-')` give?",
            "options": ["'abc'", "['a', 'b', 'c']", "['a-b', 'c']", "'a-b-c'"],
            "answer": 1,
            "explanation": "split cuts the string at every '-' and collects the pieces in a list: ['a', 'b', 'c']. The separator itself disappears.",
        },
        {
            "id": "ch04-warm-1",
            "type": "task",
            "title": "Shout it",
            "difficulty": 1,
            "plain": "Turn a quiet word into a loud one.",
            "instructions": r"""
Given `word = "python"`, print it in ALL CAPS.

Expected output: `PYTHON`
""",
            "starter": """word = "python"
# TODO: print the word in all caps
""",
            "example": """Try the same trick on a different problem:

```python
name = "ada"
print(name.upper())
print(name.title())
```
""",

            "hints": [
                "There's a string method that shouts: `.upper()`.",
                "`print(word.upper())`.",
                "The original variable stays lowercase - methods make new strings.",
            ],
            "solution": """word = "python"
print(word.upper())""",
            "explanation": "`.upper()` returns a new string with every letter capitalised - the original word is untouched (strings are immutable). The same idea gives `.lower()` and `.title()`.\n\nWhat you learned: `word.upper()` shouts the whole string.",
            "tests": [
                {"kind": "program", "expected": "PYTHON", "match": "exact"},
            ],
        },
        {
            "id": "ch04-warm-2",
            "type": "task",
            "title": "First and last letter",
            "difficulty": 1,
            "plain": "Print the first and the last letter of a word.",
            "instructions": r"""
Given `word = "banana"`, print two lines: the first letter, then the
last letter - using negative indexing for the last one.

Expected output:

```
b
a
```
""",
            "starter": """word = "banana"
# TODO: print word[0] and word[-1]
""",
            "example": """Try the same trick on a different problem:

```python
code = "a-b-c"
print(code[0], code[-1])
print(code[2:4])
```
""",

            "hints": [
                "Letters are numbered like list lockers: `word[0]` is first.",
                "`word[-1]` is the last letter.",
                "Two prints, one per line.",
            ],
            "solution": """word = "banana"
print(word[0])
print(word[-1])""",
            "explanation": "Strings are letter-chains with numbered positions - `word[0]` grabs the first bead, `word[-1]` the last without counting length. Exactly like lists.\n\nWhat you learned: `s[0]` and `s[-1]` pick edge letters.",
            "tests": [
                {"kind": "program", "expected": "b\na", "match": "exact"},
            ],
        },
        {
            "id": "ch04-warm-3",
            "type": "task",
            "title": "Split a line",
            "difficulty": 1,
            "plain": "Cut a record into fields and pick one out.",
            "instructions": "Given `line = \"Ada;Meyer;Berlin\"`, split it at the semicolons and print only the city. Output: `Berlin`",
            "starter": """line = "Ada;Meyer;Berlin"
parts = line.split(";")
# TODO: print the third field - index 2
""",
            "example": """A shorter record splits the same way:

```python
row = "Tom;Weber;Ulm"
print(row.split(";")[2])
```
""",
            "hints": [
                "`.split(\";\")` turns the string into a list of three pieces.",
                "Indexes count from 0 - the city is `parts[2]`.",
                "`print(parts[2])` gives `Berlin`.",
            ],
            "solution": """line = "Ada;Meyer;Berlin"
parts = line.split(";")
print(parts[2])""",
            "explanation": "Semicolon-separated records are everywhere - one split turns the line into ['Ada', 'Meyer', 'Berlin']. Index 2 then picks the city. This exact move powers the address-file tasks that follow.",
            "tests": [
                {"kind": "program", "expected": "Berlin"},
            ],
        },
        {
            "id": "ch04-task-1",
            "type": "task",
            "title": "Shortened address list",
            "difficulty": 2,
            "plain": "Turn a phone-book file into a tidy short list.",
            "instructions": r"""
The file `adressen.txt` (UTF-8, in your folder) holds friend addresses,
one per line:

```
FirstName;LastName;City;Phone
```

Print a shortened list in the form `F.Last - Tel: number` - the first
name's initial, the last name, then the phone number:

```
F.Meyer - Tel: 07732/43452
P.Rabe - Tel: 07531/70021
...
```
""",
            "starter": """fh = open("adressen.txt", encoding="utf-8")
for address in fh:
    address = address.strip()
    parts = address.split(";")
    # TODO: print f"{parts[0][0]}.{parts[1]} - Tel: {parts[3]}"
fh.close()
""",
            "example": """Same format, one hard-coded record:

```python
record = "Tom;Weber;Ulm;555"
p = record.split(";")
print(f"{p[0][0]}.{p[1]} - Tel: {p[3]}")
```
""",

            "hints": [
                "`address.split(';')` cuts each line into `[first, last, city, phone]`.",
                "The initial is `parts[0][0]` - first letter of the first name.",
                "One f-string: `f\"{parts[0][0]}.{parts[1]} - Tel: {parts[3]}\"`.",
            ],
            "solution": """fh = open("adressen.txt", encoding="utf-8")
for address in fh:
    address = address.strip()
    parts = address.split(";")
    print(f"{parts[0][0]}.{parts[1]} - Tel: {parts[3]}")
fh.close()
""",
            "explanation": "Each file line is chopped at the semicolons into four pieces. `parts[0][0]` digs one level deeper - first letter of the first name. The f-string then reassembles initial, last name and phone into the required shape.\n\nWhat you learned: `split(';')` turns flat text into fields you can index.",
            "tests": [
                {"kind": "program",
                 "expected": "F.Meyer - Tel: 07732/43452\nP.Rabe - Tel: 07531/70021\nO.Huber - Tel: 08031/7877-0\nA.Rabe - Tel: 07732/2343\nO.Lindner - Tel: 07531/890\nA.List - Tel: 089/3434544\nF.Huber - Tel: 08031/787878\nS.Rabe - Tel: 07531/343454",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch04-task-2",
            "type": "task",
            "title": "Friends from Konstanz",
            "difficulty": 2,
            "plain": "Filter the address list: only friends living in Konstanz.",
            "instructions": r"""
Same `adressen.txt` file (`FirstName;LastName;City;Phone` per line).
Print `First Last` for every friend living in **Konstanz**:

```
Peter Rabe
Oskar Lindner
Sarah Rabe
```
""",
            "starter": """with open("adressen.txt", encoding="utf-8") as fh:
    for address in fh:
        parts = address.strip().split(";")
        if parts[2] == "Konstanz":
            pass    # TODO: print first and last name: parts[0], parts[1]
""",
            "example": """Filter one record by its city field:

```python
line = "Ada;Meyer;Konstanz;123"
parts = line.split(";")
if parts[2] == "Konstanz":
    print(parts[0], parts[1])
```
""",

            "hints": [
                "Split each line on `';'` - the city is element 2.",
                "Only print when `parts[2] == 'Konstanz'`.",
                "`print(parts[0], parts[1])` puts a space between them automatically.",
            ],
            "solution": """with open("adressen.txt", encoding="utf-8") as fh:
    for address in fh:
        parts = address.strip().split(";")
        if parts[2] == "Konstanz":
            print(parts[0], parts[1])
""",
            "explanation": "The if filters every line: only rows whose city field equals 'Konstanz' pass through. `with open(...)` closes the file for us at the end. `print(a, b)` inserts the space between first and last name for free.\n\nWhat you learned: loop + if is the universal 'search and filter' pattern.",
            "tests": [
                {"kind": "program",
                 "expected": "Peter Rabe\nOskar Lindner\nSarah Rabe",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch04-task-3",
            "type": "task",
            "title": "Palindromes in a list",
            "difficulty": 1,
            "plain": "Find the words that read the same backwards.",
            "instructions": r"""
Print every word palindrome in the list, one per line - checking
**case-insensitively** (`Otto` counts as a palindrome).

Expected output:

```
Otto
Lagerregal
Egge
Hannah
Kajak
Radar
Rentner
```
""",
            "starter": """for w in words:
    if w.lower() == w.lower()[::-1]:
        pass    # TODO: print the palindrome w
""",
            "example": """One word against its mirror:

```python
w = "wow"
print(w == w[::-1])
```
""",

            "hints": [
                "`w[::-1]` flips a word around.",
                "Compare `w.lower()` with `w.lower()[::-1]` so 'Otto' matches 'ottO'.",
                "Print `w` (the original spelling) when the check passes.",
            ],
            "solution": """words = ["Otto", "Hallo", "Test", "Lagerregal", "Egge", "Hannah",
         "Kajak", "Warum", "also", "Radar", "Rentner"]

for w in words:
    if w.lower() == w.lower()[::-1]:
        print(w)
""",
            "explanation": "The check lowercases the word first - that way the capital O in Otto doesn't break the comparison - then compares it to its backwards slice. Seven of the eleven words survive.\n\nWhat you learned: `s.lower() == s.lower()[::-1]` is the one-line palindrome test.",
            "tests": [
                {"kind": "program",
                 "expected": "Otto\nLagerregal\nEgge\nHannah\nKajak\nRadar\nRentner",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch04-task-4",
            "type": "task",
            "title": "Function: is_palindrome",
            "difficulty": 1,
            "plain": "Pack the palindrome check into a reusable function.",
            "instructions": r"""
Write `is_palindrome(text)` returning `True` when the string is a
palindrome (case-insensitive), else `False`.

```python
is_palindrome("Anna")     # True
is_palindrome("Python")   # False
```
""",
            "starter": """def is_palindrome(text):
    low = text.lower()        # compare without case
    backwards = low[::-1]     # the backwards trick from the lesson
    # TODO: return whether low equals backwards
""",
            "example": """A tiny function with return:

```python
def shout(word):
    return word.upper() + "!"

print(shout("hi"))
```
""",

            "hints": [
                "Lowercase the text first - same trick as the previous task.",
                "Compare it with its `[::-1]` reverse.",
                "The comparison already gives True/False - return it directly.",
            ],
            "solution": """def is_palindrome(text):
    return text.lower() == text.lower()[::-1]
""",
            "explanation": "A function is a named recipe: `text` is the ingredient, `return` hands back the answer. The comparison `lower() == lower()[::-1]` already evaluates to True or False - exactly what the function should return, no if needed.\n\nWhat you learned: `return` sends a value back to whoever called the function.",
            "tests": [
                {"kind": "expr", "expr": "is_palindrome('Anna')", "expected": "True"},
                {"kind": "expr", "expr": "is_palindrome('Rentner')", "expected": "True"},
                {"kind": "expr", "expr": "is_palindrome('Python')", "expected": "False"},
                {"kind": "expr", "expr": "is_palindrome('')", "expected": "True"},
            ],
        },
        {
            "id": "ch04-task-5",
            "type": "task",
            "title": "Formatted contact card",
            "difficulty": 1,
            "plain": "Assemble a one-line contact card from four pieces.",
            "instructions": r"""
Write `contact_card(first, last, city, phone)` returning a string in
exactly this format:

```
Last, First (City) - Phone
```

Example: `contact_card('Frank', 'Meyer', 'Radolfzell', '07732/43452')`
-> `'Meyer, Frank (Radolfzell) - 07732/43452'`.
""",
            "starter": """def contact_card(first, last, city, phone):
    return f"{last}, {first} ({city})"    # TODO: add " - {phone}" at the end
""",
            "example": """One f-string packs the fields:

```python
def label(name, room):
    return f"{name} ({room})"

print(label("Ada", "Lab"))
```
""",

            "hints": [
                "One f-string with four holes does it.",
                "`f'{last}, {first} ({city}) - {phone}'`.",
                "`return` the string - printing won't pass the test.",
            ],
            "solution": """def contact_card(first, last, city, phone):
    return f"{last}, {first} ({city}) - {phone}"
""",
            "explanation": "The f-string fills four holes in a fixed shape - last name first, first name after the comma, city in brackets, phone after the dash. `return` hands the finished string back; the tests call the function and compare what comes out.\n\nWhat you learned: f-strings assemble fixed-format text from values.",
            "tests": [
                {"kind": "expr", "expr": "contact_card('Frank', 'Meyer', 'Radolfzell', '07732/43452')",
                 "expected": "'Meyer, Frank (Radolfzell) - 07732/43452'"},
                {"kind": "expr", "expr": "contact_card('Anna', 'List', 'München', '089/3434544')",
                 "expected": "'List, Anna (München) - 089/3434544'"},
            ],
        },
        {
            "id": "ch04-boss",
            "type": "task",
            "title": "Login generator",
            "difficulty": 3,
            "boss": True,
            "plain": "Build a login name for every friend from the address file.",
            "instructions": r"""
**BOSS MISSION - generate logins.**

For every line in `adressen.txt` (`FirstName;LastName;City;Phone`),
print a login in this form:

```
meyerf@07732
rabep@07531
hubero@08031
...
```

- the part before `@`: last name **lowercase** + first letter of the
  first name, lowercase -> `meyer` + `f`
- the part after `@`: the phone's **area code** = everything before
  the `/`
- `strip()` each line first, split on `;`, and split the phone on `/`
""",
            "starter": """# BOSS: one login per address line
""",
            "example": """One login from two fields:

```python
first, last = "Ada", "Meyer"
login = (first[0] + last).lower()
print(login)
```
""",

            "hints": [
                "Same splitting as the earlier tasks - phone needs a second `split('/')`.",
                "Lowercase the whole last name with `.lower()`, initial is `parts[0][0].lower()`.",
                "f-string: `f\"{parts[1].lower()}{parts[0][0].lower()}@{parts[3].split('/')[0]}\"`.",
            ],
            "solution": """with open("adressen.txt", encoding="utf-8") as fh:
    for line in fh:
        parts = line.strip().split(";")
        area = parts[3].split("/")[0]
        print(f"{parts[1].lower()}{parts[0][0].lower()}@{area}")
""",
            "explanation": "The line splits into four fields; the phone splits a second time on `/` to keep only the area code. `.lower()` normalises the last name and the initial so 'Meyer, Frank' becomes 'meyerf'. One f-string glues the pieces with the `@` in the middle.\n\nWhat you learned: chained splits let you carve nested fields out of flat text.",
            "tests": [
                {"kind": "program",
                 "expected": "meyerf@07732\nrabep@07531\nhubero@08031\nrabea@07732\nlindnero@07531\nlista@089\nhuberf@08031\nrabes@07531",
                 "match": "exact"},
            ],
        },
    ],
}
