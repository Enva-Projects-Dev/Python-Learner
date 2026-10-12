"""Kapitel 18 - Dateiverarbeitung."""

CHAPTER = {
    "id": "ch18",
    "number": 18,
    "title": "File Processing",
    "summary": "Read and write real files - open modes, with-blocks, text vs bytes.",
    "items": [
        {
            "id": "ch18-lesson",
            "type": "lesson",
            "title": "Reading, writing, error handling",
            "body": r"""
Everything so far lived in memory - gone the moment the program ends.
**Files** let a program store data on disk and read it back later.
`open()` is the door; the **mode** letter decides what you may do:

- `'r'` read text (default), `'w'` write (**empties the file first!**),
  `'a'` append at the end, `'x'` create-or-fail
- `'rb'`/`'wb'` binary modes - raw bytes instead of text
- always pass `encoding='utf-8'` for text files

## Reading and writing

```python
with open('adressen.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line.strip())
```

> **What happens here**
>
> - line 1: `with open(...) as f` opens the file and hands it a name -
>   when the block ends, the file closes **automatically**, even on
>   errors
> - line 2: looping over a file yields it line by line
> - line 3: `strip()` removes the invisible `\n` at each line's end

Writing creates (or wipes!) the file:

```python
with open('numbers.txt', 'w') as f:
    for v in [1, 2, 3, 4, 5]:
        f.write(str(v) + ' ')

with open('numbers.txt', 'a') as f:
    f.write('6 7 8 9')

print(open('numbers.txt').read())
```

> **What happens here**
>
> - line 1: `'w'` makes a fresh empty file - old contents are gone
> - line 3: `write` adds exactly what you pass - no newline unless you
>   write `'\n'` yourself
> - line 5: `'a'` continues at the end instead of wiping
> - line 8: `read()` pulls the whole file back as one string

> **Think of it like...** `'w'` is a fresh whiteboard, `'a'` is writing
> under what's already there, and `with` is the polite guest who always
> puts the marker cap back on.

> **Watch out** - opening a file with `'w'` erases it instantly,
> before you write anything. Double-check the mode!

## When files fight back

A missing file raises `FileNotFoundError`; `os.strerror` translates the
error number into a readable message:

```python
from os import strerror
try:
    print(open('does_not_exist.txt').read())
except Exception as exc:
    print("could not open:", strerror(exc.errno))
```

> **What happens here**
>
> - line 3: opening a missing file raises FileNotFoundError
> - line 4-5: the except catches it; `exc.errno` is the error's number
>   and `strerror` translates it into words - "No such file or
>   directory" instead of a crash

## Bytes - what's underneath

Binary mode (`'rb'`) delivers `bytes`/`bytearray` - containers of
integers 0-255, the raw atoms of every file:

```python
data = bytearray(10)
for i in range(len(data)):
    data[i] = 10 + i

with open('file.bin', 'wb') as bf:
    bf.write(data)

with open('file.bin', 'rb') as bf:
    for b in bytearray(bf.read(5)):
        print(hex(b), end=' ')
```

> **What happens here**
>
> - line 1-3: a bytearray of ten zeros, filled with 10..19
> - line 5-6: `'wb'` writes raw bytes
> - line 8-9: `'rb'` + `read(5)` pulls the first 5 bytes back; `hex`
>   shows them in base 16

## Your data files

The working directory always contains `adressen.txt`, `Kunden.txt`,
`Python.txt`, `Jekyll.txt`, `Goethe--Faust.txt` (UTF-8). Task runs get
a fresh copy each time - write freely.

## Try it yourself

- Print the first line of `Python.txt`.
- Write your name to `me.txt` and read it back.
- Open a missing file and print `strerror` on the error.

## Key words

| Word | Meaning |
|---|---|
| open(file, mode) | the door to a file |
| mode | 'r' read, 'w' write, 'a' append, 'x' create-only, 'b' binary |
| with-block | auto-closes the file, even on errors |
| encoding | how text becomes bytes - use 'utf-8' |
| write vs print | write adds exactly what you pass - no newline |
| bytes / bytearray | raw numbers 0-255 |
| strerror | error number -> readable message |
""",
        },
        {
            "id": "ch18-quiz-1",
            "type": "quiz",
            "title": "Open modes",
            "question": "Which mode appends to an existing file without emptying it?",
            "options": ["'w'", "'a'", "'r+'", "'x'"],
            "answer": 1,
            "explanation": "'a' = append at the end. 'w' would wipe it, 'x' would crash if it exists.",
        },
        {
            "id": "ch18-quiz-2",
            "type": "quiz",
            "title": "Binary files",
            "question": "Opening a file with `'rb'` and calling read() returns...",
            "options": ["a string", "bytes-like data", "a list of lines", "an int"],
            "answer": 1,
            "explanation": "No decoding happens in binary mode - you get raw bytes (wrap in bytearray() to edit).",
        },
        {
            "id": "ch18-quiz-3",
            "type": "quiz",
            "title": "with statement",
            "question": "What does `with open(...) as f:` guarantee?",
            "options": ["The file exists", "The file is closed automatically", "UTF-8 encoding", "Read access"],
            "answer": 1,
            "explanation": "The with-block closes the file even when an error jumps out mid-way - that's its whole job.",
        },
        {
            "id": "ch18-quiz-4",
            "type": "quiz",
            "title": "write vs print",
            "question": "`f.write('hi')` vs `print('hi', file=f)` - the difference?",
            "options": ["None", "print adds a newline; write doesn't", "write adds a newline; print doesn't", "write is faster"],
            "answer": 1,
            "explanation": "write is literal - only what you pass lands in the file. print appends '\\n' unless you say end=''.",
        },
        {
            "id": "ch18-warm-1",
            "type": "task",
            "title": "Write one line",
            "difficulty": 1,
            "plain": "Create a file with one word inside.",
            "instructions": r"""
Write `"hello"` into a file called `hello.txt`, then read it back and
print it.

Expected output: `hello`
""",
            "starter": """# TODO: write 'hello' to hello.txt, read it back, print it
""",
            "hints": [
                "`with open('hello.txt', 'w') as f: f.write('hello')`.",
                "Then `print(open('hello.txt').read())`.",
                "Two opens - one for writing, one for reading.",
            ],
            "solution": """with open('hello.txt', 'w') as f:
    f.write('hello')

print(open('hello.txt').read())""",
            "explanation": "'w' creates (or empties) the file and `write` drops the text in - when the with-block ends, the file is safely closed. Reading it back confirms it landed.\n\nWhat you learned: write with 'w', read with default 'r'.",
            "tests": [
                {"kind": "program", "expected": "hello", "match": "exact"},
            ],
        },
        {
            "id": "ch18-warm-2",
            "type": "task",
            "title": "Count the lines",
            "difficulty": 1,
            "plain": "Count how many lines Python.txt has.",
            "instructions": r"""
Print the number of lines in `Python.txt` (the file exists in your
working directory).

Expected output: `13`
""",
            "starter": """# TODO: open Python.txt and print its line count
""",
            "hints": [
                "A file object is iterable - loop and count.",
                "Or `len(f.readlines())`.",
                "`with open('Python.txt', encoding='utf-8') as f:`.",
            ],
            "solution": """with open('Python.txt', encoding='utf-8') as f:
    print(len(f.readlines()))""",
            "explanation": "`readlines()` collects every line into a list - `len` of it is the line count. A for-loop counter would work identically since iterating a file yields lines.\n\nWhat you learned: files are iterable line-by-line.",
            "tests": [
                {"kind": "program", "expected": "13", "match": "exact"},
            ],
        },
        {
            "id": "ch18-task-1",
            "type": "task",
            "title": "Total revenue from Kunden.txt",
            "difficulty": 2,
            "plain": "Add up all the money in a customer file - mind the German commas.",
            "instructions": r"""
`Kunden.txt` (UTF-8) holds customer records separated by `;`:

```
Kunden-Nr;Name;Ort;Straße;Umsatzerlöse;ABC-Klasse
4711;Stoll AG; 70567 Stuttgart ;Finkenweg 12;690.625,00 €;A
```

Revenue uses German formatting: `.` for thousands, `,` for decimals,
then ` €`.

Read the file (skip the header) and print the total:

```
Total revenue: 2732225.00 EUR
```
""",
            "starter": """def euro_to_float(text):
    # TODO: '690.625,00 €' -> 690625.0
    pass

total = 0.0
# TODO: read Kunden.txt (utf-8), skip the header, sum the revenue column

print(f"Total revenue: {total:.2f} EUR")
""",
            "hints": [
                "Drop `' €'`, remove `'.'`, swap `','` for `'.'`, then `float()`.",
                "Fields: `line.strip().split(';')` - revenue is index 4.",
                "Skip line 1 - the header.",
            ],
            "solution": """def euro_to_float(text):
    text = text[:len(text) - 2]      # drop ' €'
    text = text.replace('.', '')
    text = text.replace(',', '.')
    return float(text)

total = 0.0
with open('Kunden.txt', 'r', encoding='utf-8') as customers:
    for i, line in enumerate(customers):
        if i == 0:
            continue
        total += euro_to_float(line.strip().split(';')[4])

print(f"Total revenue: {total:.2f} EUR")
""",
            "explanation": "`euro_to_float` untangles German notation in three steps - strip ' €', delete thousands dots, turn the decimal comma into a dot - then float() parses it. The main loop enumerates lines so `i == 0` skips the header, splits each record on ';' and adds field 4.\n\nWhat you learned: real-world data needs cleaning before parsing.",
            "tests": [
                {"kind": "program", "expected": "Total revenue: 2732225.00 EUR",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch18-task-2",
            "type": "task",
            "title": "ABC customer lists",
            "difficulty": 2,
            "plain": "Sort customers into three files by their ABC class.",
            "instructions": r"""
Write `split_by_class()`:

- reads `Kunden.txt` (header + `;`-separated data)
- writes each data line to `KundenA.txt`, `KundenB.txt` or
  `KundenC.txt` by its ABC class (last field, index 5)
- returns `{'A': n_a, 'B': n_b, 'C': n_c}` - lines written per class

Expected counts: `{'A': 3, 'B': 3, 'C': 10}`.
""",
            "starter": """def split_by_class():
    counts = {'A': 0, 'B': 0, 'C': 0}
    # TODO: read Kunden.txt, write each line to KundenA/B/C.txt
    return counts
""",
            "hints": [
                "Open all three output files inside one `with` (comma-separated).",
                "Class = `line.strip().split(';')[5]`; a `targets` dict maps 'A'->fa etc.",
                "Count `counts[kz] += 1` for every written line.",
            ],
            "solution": """def split_by_class():
    counts = {'A': 0, 'B': 0, 'C': 0}
    with open('Kunden.txt', 'r', encoding='utf-8') as customers:
        with open('KundenA.txt', 'w', encoding='utf-8') as fa, \\
             open('KundenB.txt', 'w', encoding='utf-8') as fb, \\
             open('KundenC.txt', 'w', encoding='utf-8') as fc:
            targets = {'A': fa, 'B': fb, 'C': fc}
            for i, line in enumerate(customers):
                if i == 0:
                    continue
                kz = line.strip().split(';')[5]
                targets[kz].write(line)
                counts[kz] += 1
    return counts
""",
            "explanation": "One `with` opens four files at once - `targets` maps each class letter to its open file, so routing a line is just `targets[kz].write(line)`. The header (i==0) is skipped, and every write bumps the matching counter.\n\nWhat you learned: a dict can route data to different files.",
            "tests": [
                {"kind": "expr", "expr": "split_by_class()",
                 "expected": "{'A': 3, 'B': 3, 'C': 10}"},
                {"kind": "assert",
                 "code": "split_by_class()\nlines = open('KundenA.txt', encoding='utf-8').read().splitlines()\nassert len(lines) == 3\nassert all(l.split(';')[5] == 'A' for l in lines)\nassert 'Stoll AG' in lines[0]",
                 "desc": "KundenA.txt has 3 A-records incl. Stoll AG"},
                {"kind": "assert",
                 "code": "split_by_class()\nassert len(open('KundenC.txt', encoding='utf-8').read().splitlines()) == 10",
                 "desc": "KundenC.txt has 10 records"},
            ],
        },
        {
            "id": "ch18-task-3",
            "type": "task",
            "title": "Read bytes from adressen.txt",
            "difficulty": 1,
            "plain": "Look at the raw bytes of a file - just the first five.",
            "instructions": r"""
Read the **first 5 bytes** of `adressen.txt` in binary mode and print
each as a character, space-separated:

```
F r a n k
```
""",
            "starter": """# TODO: open adressen.txt as 'rb', read 5 bytes, print as chars
""",
            "hints": [
                "`open('adressen.txt', 'rb')` + `f.read(5)`.",
                "Each byte is an int - `chr(b)` turns it into a character.",
                "`print(chr(b), end=' ')` then a final `print()`.",
            ],
            "solution": """with open('adressen.txt', 'rb') as bf:
    data = bytearray(bf.read(5))

for b in data:
    print(chr(b), end=' ')
print()
""",
            "explanation": "Binary read returns byte-numbers; `bytearray` makes a friendly iterable of them and `chr` decodes each to a character - the first name in the file starts 'Frank'. `end=' '` keeps them on one line.\n\nWhat you learned: files are bytes underneath; text mode decodes them for you.",
            "tests": [
                {"kind": "program", "expected": "F r a n k", "match": "exact"},
            ],
        },
        {
            "id": "ch18-task-4",
            "type": "task",
            "title": "Write and append a numbers file",
            "difficulty": 1,
            "plain": "Write five numbers, then append four more.",
            "instructions": r"""
1. Write `1 2 3 4 5` (each followed by a space) to `numbers.txt`
   with mode `'w'`.
2. Append `6 7 8 9` in the same format with `'a'`.
3. Read the file and print its contents.

Expected output: `1 2 3 4 5 6 7 8 9 `
""",
            "starter": """# TODO: write 1-5, append 6-9, read and print the file
""",
            "hints": [
                "`f.write(str(v) + ' ')` inside a loop.",
                "Mode 'a' continues at the end of the file.",
                "Read back with `open('numbers.txt').read()`.",
            ],
            "solution": """with open('numbers.txt', 'w') as f:
    for v in [1, 2, 3, 4, 5]:
        f.write(str(v) + ' ')

with open('numbers.txt', 'a') as f:
    for v in [6, 7, 8, 9]:
        f.write(str(v) + ' ')

with open('numbers.txt') as f:
    print(f.read())
""",
            "explanation": "'w' starts a fresh file with 1-5, 'a' adds 6-9 at the end without touching what exists - the trailing space after each number keeps them separated. Reading the whole file shows the joined result.\n\nWhat you learned: 'w' overwrites, 'a' appends.",
            "tests": [
                {"kind": "program", "expected": "1 2 3 4 5 6 7 8 9", "match": "lines"},
                {"kind": "assert",
                 "code": "assert open('numbers.txt').read() == '1 2 3 4 5 6 7 8 9 '",
                 "desc": "file contents exact"},
            ],
        },
        {
            "id": "ch18-boss",
            "type": "task",
            "title": "Customer report file",
            "difficulty": 3,
            "boss": True,
            "plain": "Read the customer file and write a tidy summary report.",
            "instructions": r"""
**BOSS MISSION - the accountant's report.**

Write `write_report()` reading `Kunden.txt` (header + `;` data) and
writing `report.txt` with **exactly** these 5 lines:

```text
Customers: 16
Class A: 3
Class B: 3
Class C: 10
Total revenue: 2732225.00 EUR
```

Revenue parsing as before (index 4, German format); class is field 5.
Return the report text as well.
""",
            "starter": """def euro_to_float(text):
    text = text[:len(text) - 2]
    return float(text.replace('.', '').replace(',', '.'))


def write_report():
    # TODO: read Kunden.txt, build the 5-line report, write report.txt
    pass
""",
            "example": """German money text into a float:

```python
text = "1.234,50 EUR"
value = float(text[:-4].replace(".", "").replace(",", "."))
print(value)
```
""",

            "hints": [
                "Loop the data lines once: count total, count classes via a dict, sum revenue.",
                "Assemble lines into a list, `'\\n'.join(lines) + '\\n'`.",
                "Write with `open('report.txt', 'w', encoding='utf-8')` and return the same string.",
            ],
            "solution": """def euro_to_float(text):
    text = text[:len(text) - 2]
    return float(text.replace('.', '').replace(',', '.'))


def write_report():
    total = 0.0
    counts = {'A': 0, 'B': 0, 'C': 0}
    n = 0
    with open('Kunden.txt', 'r', encoding='utf-8') as customers:
        for i, line in enumerate(customers):
            if i == 0:
                continue
            fields = line.strip().split(';')
            n += 1
            counts[fields[5]] += 1
            total += euro_to_float(fields[4])
    report = (f"Customers: {n}\\n"
              f"Class A: {counts['A']}\\n"
              f"Class B: {counts['B']}\\n"
              f"Class C: {counts['C']}\\n"
              f"Total revenue: {total:.2f} EUR\\n")
    with open('report.txt', 'w', encoding='utf-8') as out:
        out.write(report)
    return report
""",
            "explanation": "One pass over the data collects everything: total customers, per-class counts (via the dict), and the revenue sum. The five report lines are built with f-strings, written to report.txt, and returned - so the same text is both saved and checkable.\n\nWhat you learned: gather in one pass, format once, write once.",
            "tests": [
                {"kind": "expr",
                 "expr": "write_report()",
                 "expected": "'Customers: 16\\nClass A: 3\\nClass B: 3\\nClass C: 10\\nTotal revenue: 2732225.00 EUR\\n'"},
                {"kind": "assert",
                 "code": "write_report()\nassert open('report.txt', encoding='utf-8').read() == 'Customers: 16\\nClass A: 3\\nClass B: 3\\nClass C: 10\\nTotal revenue: 2732225.00 EUR\\n'",
                 "desc": "report.txt contents exact"},
            ],
        },
    ],
}
