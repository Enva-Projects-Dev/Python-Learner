"""Kapitel 19 - Labs (Abschlussprojekte)."""

CHAPTER = {
    "id": "ch19",
    "number": 19,
    "title": "Labs",
    "summary": "Capstone labs combining files, dicts, lambdas and exceptions - plus Prof. Jekyll's grade book.",
    "items": [
        {
            "id": "ch19-lesson",
            "type": "lesson",
            "title": "Combining files, dicts and lambdas",
            "body": r"""
The labs ahead snap together nearly the whole course - files,
dictionaries, sorting, exceptions. Three moves do most of the work.

## Move 1: counting with a dictionary

Counting things is THE dict job - `get(ch, 0)` starts every unseen key
at zero so the first sighting works:

```python
letters = {}
text = open("Jekyll.txt", encoding="utf-8").read().lower()
for ch in text:
    if ch.isalpha():
        letters[ch] = letters.get(ch, 0) + 1
print(letters)
```

> **What happens here**
>
> - line 2: read the whole file as one string and lowercase it - 'N'
>   and 'n' count together
> - line 4: `isalpha()` keeps only letters - no digits, no punctuation
> - line 5: `get(ch, 0)` says "give me ch's count, or 0 if new" - then
>   +1 bumps it. The classic counting pattern.

> **Think of it like...** a tally board: every time a letter shows up,
> another stroke goes next to its name.

## Move 2: sorting by the count

`dict.items()` hands you `(key, value)` pairs - sort them with a
lambda key:

```python
letters = {"j": 2, "e": 1, "k": 1, "y": 1, "l": 2}   # pretend counts
for ch, cnt in sorted(letters.items(), key=lambda kv: kv[1], reverse=True):
    print(ch, "->", cnt)
```

> **What happens here**
>
> - `items()` turns the dict into pairs like `('n', 9)`
> - `key=lambda kv: kv[1]` says "sort by the count" (index 1 of the
>   pair - index 0 is the letter)
> - `reverse=True` puts the biggest first
> - `ch, cnt` unpacks each pair into two names

> **Watch out** - without `reverse=True` you'd get the RAREST letter
> first. Easy to forget!

## Move 3: defensive file processing

Real files can be missing, empty, or broken. Your own exception family
lets callers catch "anything student-related" or each specific kind:

```python
class StudentsDataException(Exception):
    pass

class BadLine(StudentsDataException):
    pass

class FileEmpty(StudentsDataException):
    pass

try:
    raise BadLine("broken input")
except StudentsDataException as e:
    print(type(e).__name__, "->", e)
```

> **What happens here**
>
> - lines 1-9: three error classes forming a family - BadLine and
>   FileEmpty are children of StudentsDataException
> - line 13: catching the PARENT catches the child - `type(e).__name__`
>   prints the actual type ('BadLine')

The files `Jekyll.txt`, `adressen.txt`, `Kunden.txt`, `Python.txt`
and `Goethe--Faust.txt` sit in your working directory.

## Try it yourself

- Print the 3 most common letters of `Python.txt`.
- Count words (not letters) in `Jekyll.txt` with the same dict trick.

## Key words

| Word | Meaning |
|---|---|
| histogram | a dict counting occurrences |
| get(k, 0) | read with a default for missing keys |
| items() | the dict's (key, value) pairs |
| lambda key | which part of the pair to sort by |
| reverse=True | biggest first |
| exception family | parent error + specific children |
""",
        },
        {
            "id": "ch19-quiz-1",
            "type": "quiz",
            "title": "Histogram sorting",
            "question": "To sort `letters.items()` by count descending, the call is...",
            "options": ["sorted(..., key=lambda kv: kv[0])", "sorted(..., key=lambda kv: kv[1], reverse=True)", "sorted(..., key=kv[1])", "sorted(..., reverse=True) only"],
            "answer": 1,
            "explanation": "kv[1] is the count - reverse=True flips it so the biggest lands first. kv[0] would sort by letter.",
        },
        {
            "id": "ch19-quiz-2",
            "type": "quiz",
            "title": "Counting pattern",
            "question": "`letters[ch] = letters.get(ch, 0) + 1` does what?",
            "options": ["Always sets 1", "Bumps the counter for ch, starting at 0 for new letters", "Deletes ch", "Crashes on new letters"],
            "answer": 1,
            "explanation": "get's default 0 means the first sighting works - no KeyError, just 0+1. That's the counting idiom.",
        },
        {
            "id": "ch19-quiz-3",
            "type": "quiz",
            "title": "Exception family",
            "question": "`except StudentsDataException` catches `BadLine` because...",
            "options": ["BadLine is raised first", "BadLine is a subclass of StudentsDataException", "all exceptions are equal", "it doesn't"],
            "answer": 1,
            "explanation": "A catch branch matches the class AND its children - BadLine IS a StudentsDataException.",
        },
        {
            "id": "ch19-quiz-4",
            "type": "quiz",
            "title": "Comma decimals",
            "question": "`float('4,5')` - what happens?",
            "options": ["4.5", "45.0", "ValueError", "4"],
            "answer": 2,
            "explanation": "float() only understands the dot - '4,5' crashes. Fix first: `'4,5'.replace(',', '.')`.",
        },
        {
            "id": "ch19-warm-1",
            "type": "task",
            "title": "Count the vowels",
            "difficulty": 1,
            "plain": "Count how many vowels live in Jekyll.txt.",
            "instructions": r"""
Count the vowels (a, e, i, o, u - case-insensitive) in `Jekyll.txt`
and print the number.

Expected output: `15`
""",
            "starter": """# TODO: count vowels in Jekyll.txt and print the count
""",
            "hints": [
                "Read with `open('Jekyll.txt', encoding='utf-8').read().lower()`.",
                "`if ch in 'aeiou':` bumps a counter.",
                "Or `sum(1 for ch in text if ch in 'aeiou')`.",
            ],
            "solution": """text = open("Jekyll.txt", encoding="utf-8").read().lower()
print(sum(1 for ch in text if ch in "aeiou"))""",
            "explanation": "The generator yields 1 for every vowel character in the lowercased text; `sum` totals them - 15 vowels in Prof. Jekyll's notes.\n\nWhat you learned: `sum(1 for x in s if cond)` is a compact counter.",
            "tests": [
                {"kind": "program", "expected": "15", "match": "exact"},
            ],
        },
        {
            "id": "ch19-warm-2",
            "type": "task",
            "title": "Comma to dot",
            "difficulty": 1,
            "plain": "Turn the German '4,5' into a real number.",
            "instructions": r"""
`score = "4,5"`. Convert it to a float and print it plus 1.

Expected output: `5.5`
""",
            "starter": """score = "4,5"
# TODO: convert and print score + 1
""",
            "hints": [
                "float() can't read commas - replace first.",
                "`float(score.replace(',', '.'))`.",
                "Then add 1 and print.",
            ],
            "solution": """score = "4,5"
print(float(score.replace(",", ".")) + 1)""",
            "explanation": "`replace` swaps the comma for a dot so float() understands it - 4.5 + 1 = 5.5. This tiny fix is the key to parsing Prof. Jekyll's file.\n\nWhat you learned: normalise text formats before converting.",
            "tests": [
                {"kind": "program", "expected": "5.5", "match": "exact"},
            ],
        },
        {
            "id": "ch19-task-1",
            "type": "task",
            "title": "Character frequency histogram",
            "difficulty": 2,
            "plain": "Count each letter in a file - the classic histogram.",
            "instructions": r"""
Write `letter_counts(filename)`:

- read the file (UTF-8), lowercase it, count letters only
  (`ch.isalpha()`)
- return `{letter: count}` - only letters that occur

```python
letter_counts("Jekyll.txt")['n']   # 9
```
""",
            "starter": """def letter_counts(filename):
    letters = {}
    # TODO: read the file, count letters (case-insensitive)
    return letters
""",
            "hints": [
                "`open(filename, encoding='utf-8').read().lower()` gets the text.",
                "`if ch.isalpha(): letters[ch] = letters.get(ch, 0) + 1`.",
                "Return the dict - no printing.",
            ],
            "solution": """def letter_counts(filename):
    letters = {}
    with open(filename, encoding="utf-8") as f:
        for ch in f.read().lower():
            if ch.isalpha():
                letters[ch] = letters.get(ch, 0) + 1
    return letters
""",
            "explanation": "Lowercasing first merges 'N' and 'n' into one bucket; `isalpha` filters out spaces, digits and punctuation; `get(ch, 0)` starts every new letter at zero so the increment always works.\n\nWhat you learned: clean -> filter -> count is the histogram recipe.",
            "tests": [
                {"kind": "expr", "expr": "letter_counts('Jekyll.txt')['n']", "expected": "9"},
                {"kind": "expr", "expr": "letter_counts('Jekyll.txt')['o']", "expected": "5"},
                {"kind": "expr", "expr": "len(letter_counts('Jekyll.txt'))", "expected": "18"},
                {"kind": "expr", "expr": "letter_counts('Jekyll.txt').get('z', 0)", "expected": "0"},
            ],
        },
        {
            "id": "ch19-task-2",
            "type": "task",
            "title": "Sorted histogram to file",
            "difficulty": 2,
            "plain": "Same counts - but sorted big-to-small and saved to a file.",
            "instructions": r"""
Write `write_sorted_histogram(src, dest)`:

- count letters in `src` (same recipe as before)
- write `'<letter> -> <count>'` lines into `dest`, sorted by count
  **descending**
- return the sorted list of `(letter, count)` tuples

For `Jekyll.txt` the first lines are:

```
n -> 9
o -> 5
```
""",
            "starter": """def write_sorted_histogram(src, dest):
    letters = {}
    # TODO: count letters of src (see previous task)

    # TODO: sort by count descending, write "x -> n" lines to dest
    #       and return the sorted (letter, count) list
    pass
""",
            "hints": [
                "`sorted(letters.items(), key=lambda kv: kv[1], reverse=True)`.",
                "`f.write(f'{ch} -> {cnt}\\n')` per pair.",
                "Return the sorted list - the file and the return share it.",
            ],
            "solution": """def write_sorted_histogram(src, dest):
    letters = {}
    with open(src, encoding="utf-8") as f:
        for ch in f.read().lower():
            if ch.isalpha():
                letters[ch] = letters.get(ch, 0) + 1

    sorted_letters = sorted(letters.items(), key=lambda kv: kv[1],
                            reverse=True)
    with open(dest, "wt", encoding="utf-8") as f:
        for ch, cnt in sorted_letters:
            f.write(f"{ch} -> {cnt}\\n")
    return sorted_letters
""",
            "explanation": "The counting half is the histogram recipe; the new part sorts `letters.items()` with a lambda key on the count (reverse for descending) and writes each pair as a 'x -> n' line. Returning the same sorted list makes it testable.\n\nWhat you learned: items() + key=lambda kv: kv[1] sorts a dict by value.",
            "tests": [
                {"kind": "expr",
                 "expr": "write_sorted_histogram('Jekyll.txt', 'out.hist')[:2]",
                 "expected": "[('n', 9), ('o', 5)]"},
                {"kind": "assert",
                 "code": "write_sorted_histogram('Jekyll.txt', 'out.hist')\nfirst = open('out.hist', encoding='utf-8').read().splitlines()[0]\nassert first == 'n -> 9'",
                 "desc": "first line of out.hist is 'n -> 9'"},
            ],
        },
        {
            "id": "ch19-task-3",
            "type": "task",
            "title": "Evaluating students' results",
            "difficulty": 3,
            "plain": "Sum every student's points and spot bad lines with your own errors.",
            "instructions": r"""
Prof. Jekyll notes scores in `Jekyll.txt` - three fields per line:
first name, last name, points (comma decimals possible):

```
John Smith 5
Anna Boleyn 4,5
```

Write `students_report(filename)` -> sorted list of `'Name total'`
strings:

```python
students_report("Jekyll.txt")
# ['Andrew Cox 1.5', 'Anna Boleyn 15.5', 'John Smith 7.0']
```

Define `StudentsDataException(Exception)` with children `BadLine`
(malformed line) and `FileEmpty` (file exists but is empty).
""",
            "starter": """class StudentsDataException(Exception):
    pass

class BadLine(StudentsDataException):
    # TODO
    pass

class FileEmpty(StudentsDataException):
    # TODO
    pass


def students_report(filename):
    totals = {}
    # TODO: read lines, sum points per student, return sorted
    #       "Name total" strings; raise FileEmpty / BadLine
    pass
""",
            "hints": [
                "`line.split()` -> `[first, last, points]`; name = `' '.join(parts[:2])`.",
                "`float(parts[2].replace(',', '.'))` - wrap in try, raise BadLine on failure.",
                "Empty file check first: `if not lines: raise FileEmpty()`.",
            ],
            "solution": """class StudentsDataException(Exception):
    pass

class BadLine(StudentsDataException):
    def __init__(self, msg="Bad line in the data"):
        super().__init__(msg)

class FileEmpty(StudentsDataException):
    def __init__(self, msg="File contains no data"):
        super().__init__(msg)


def students_report(filename):
    with open(filename, "rt", encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines) == 0:
        raise FileEmpty()

    totals = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            parts = line.split()
            key = " ".join(parts[:2])
            value = float(parts[2].replace(",", "."))
        except Exception:
            raise BadLine("Bad line: " + line.strip())
        totals[key] = totals.get(key, 0) + value

    return [f"{name} {totals[name]}" for name in sorted(totals)]
""",
            "explanation": "The file-empty guard fires first, then each line is parsed inside try - a wrong field count or a non-number raises BadLine instead of crashing. `totals.get(name, 0)` accumulates repeated names (John Smith appears twice: 5+2=7.0), and `sorted(totals)` orders names alphabetically for the output list.\n\nWhat you learned: validate per line, accumulate per key, format at the end.",
            "tests": [
                {"kind": "expr", "expr": "students_report('Jekyll.txt')",
                 "expected": "['Andrew Cox 1.5', 'Anna Boleyn 15.5', 'John Smith 7.0']"},
                {"kind": "assert",
                 "code": "open('empty.txt', 'w').close()\ntry:\n    students_report('empty.txt')\n    assert False\nexcept FileEmpty:\n    pass",
                 "desc": "empty file raises FileEmpty"},
                {"kind": "assert",
                 "code": "open('bad.txt', 'w').write('Only Two\\n')\ntry:\n    students_report('bad.txt')\n    assert False\nexcept BadLine:\n    pass",
                 "desc": "malformed line raises BadLine"},
            ],
        },
        {
            "id": "ch19-task-4",
            "type": "task",
            "title": "Most common letter",
            "difficulty": 1,
            "plain": "Find the single most-used letter in a file.",
            "instructions": r"""
Write `most_common_letter(filename)` returning `(letter, count)` -
the most frequent letter (case-insensitive).

`most_common_letter("Jekyll.txt")` -> `('n', 9)`
""",
            "starter": """def most_common_letter(filename):
    # TODO: return (letter, count) of the most frequent letter
    pass
""",
            "hints": [
                "Count into a dict first (histogram recipe).",
                "`max(letters.items(), key=lambda kv: kv[1])` is a one-liner.",
                "Or `sorted(..., reverse=True)[0]`.",
            ],
            "solution": """def most_common_letter(filename):
    letters = {}
    with open(filename, encoding="utf-8") as f:
        for ch in f.read().lower():
            if ch.isalpha():
                letters[ch] = letters.get(ch, 0) + 1
    return max(letters.items(), key=lambda kv: kv[1])
""",
            "explanation": "Same histogram, different finish: `max` with `key=lambda kv: kv[1]` picks the pair with the biggest count directly - no sorting needed when you only want the winner.\n\nWhat you learned: max/min also accept key=.",
            "tests": [
                {"kind": "expr", "expr": "most_common_letter('Jekyll.txt')",
                 "expected": "('n', 9)"},
                {"kind": "assert",
                 "code": "letter, count = most_common_letter('adressen.txt')\nassert count > 0 and letter.isalpha()",
                 "desc": "works on adressen.txt too"},
            ],
        },
        {
            "id": "ch19-boss",
            "type": "task",
            "title": "Prof. Jekyll's grade book",
            "difficulty": 3,
            "boss": True,
            "plain": "The final exam: read the grade file, rank the students, write the report.",
            "instructions": r"""
**BOSS MISSION - the final grade book.**

Write `write_grade_book(src, dest)`:

- sum each student's points from `src` (same format as task 3 -
  name fields + comma-decimal points)
- write `dest` with one line per student `"<name>: <total>"`, sorted
  by total **descending**, then a final line
  `"Average: <mean of totals, 2 decimals>"`
- return the report text

For `Jekyll.txt` the file must be exactly:

```text
Anna Boleyn: 15.5
John Smith: 7.0
Andrew Cox: 1.5
Average: 8.00
```
""",
            "starter": """def write_grade_book(src, dest):
    totals = {}
    # TODO: accumulate points per student, sort by total desc,
    #       write lines + Average, return the text
    pass
""",
            "example": """Collect scores per name, average them:

```python
grades = {}
for name, note in [("ada", "1"), ("bo", "2"), ("ada", "3")]:
    grades.setdefault(name, []).append(int(note))
print({n: sum(v) / len(v) for n, v in grades.items()})
```
""",

            "hints": [
                "Parse like task 3: `parts = line.split()`, name join, comma->dot float.",
                "Sort `totals.items()` by `key=lambda kv: -kv[1]`.",
                "Lines via f-strings; average = `sum/len` formatted `:.2f`.",
            ],
            "solution": """def write_grade_book(src, dest):
    totals = {}
    with open(src, "rt", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.split()
            key = " ".join(parts[:2])
            totals[key] = totals.get(key, 0) + float(parts[2].replace(",", "."))

    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    lines = [f"{name}: {total}" for name, total in ranked]
    avg = sum(totals.values()) / len(totals)
    lines.append(f"Average: {avg:.2f}")
    report = "\\n".join(lines) + "\\n"
    with open(dest, "wt", encoding="utf-8") as out:
        out.write(report)
    return report
""",
            "explanation": "One pass builds the totals dict (comma->dot conversion included), a lambda sort by `-kv[1]` ranks students best-first, and the average line appends the mean formatted to two decimals. The string is written once and returned for checking.\n\nWhat you learned: parse -> accumulate -> rank -> format - the full data pipeline.",
            "tests": [
                {"kind": "assert",
                 "code": "rep = write_grade_book('Jekyll.txt', 'grades.txt')\nassert rep == 'Anna Boleyn: 15.5\\nJohn Smith: 7.0\\nAndrew Cox: 1.5\\nAverage: 8.00\\n'\nassert open('grades.txt', encoding='utf-8').read() == rep",
                 "desc": "grade book content + file match"},
            ],
        },
    ],
}
