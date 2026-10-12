"""Kapitel 11 - String-Verarbeitung."""

CHAPTER = {
    "id": "ch11",
    "number": 11,
    "title": "String Processing",
    "summary": "Letters are numbers inside - code points, searching, splitting and secret codes.",
    "items": [
        {
            "id": "ch11-lesson",
            "type": "lesson",
            "title": "Characters, code points and string methods",
            "body": r"""
Strings aren't just text to print - you can search them, cut them,
weigh them and rebuild them. This chapter is about the tools that turn
a string into data you can process.

## Letters are secretly numbers

Inside the computer, every letter is stored as a number - its
**code point**. `ord()` reveals the number, `chr()` turns a number
back into a letter:

```python
print(ord('z'))               # 122
print(chr(122))               # 'z'
print(ord('A'), ord('a'))     # 65 97
```

> **What happens here**
>
> - line 1: `ord` asks "what number is 'z'?" -> 122
> - line 2: `chr` goes the other way - 122 -> 'z'
> - line 3: capitals live in a different number range (A=65, a=97)

> **Think of it like...** every letter wears a secret jersey number.
> Shifting the number shifts the letter - that's the whole trick
> behind the Caesar cipher.

Two more spells: `+` glues strings together, `*` repeats them:

```python
print('a' + 'b', 'a' * 5)     # ab aaaaa
```

> **What happens here**
>
> - `'a' + 'b'` glues the strings end to end -> `'ab'`
> - `'a' * 5` repeats the string five times -> `'aaaaa'`
> - the comma in `print` puts a space between the two results

## Strings are letter-chains

Everything you know from lists works on strings - indexing, slicing,
`in` membership checks:

```python
alphabet = "abcdefghijklmnopqrstuvwxyz"
print(alphabet[:10])       # first 10 letters
print(alphabet[::-1])      # backwards
print('q' in alphabet, 'ghi' not in alphabet)
print(min("abcABC"), max("abcABC"))              # 'A' and 'c'
print("abcABC".index("A"), "abcABCA".count("A")) # 3, 2
```

> **What happens here**
>
> - line 2: a slice - index 0 up to (not including) 10
> - line 3: step -1 walks backwards through the whole string
> - line 4: `in` / `not in` test whether a piece lives inside
> - line 5: min/max pick by code point - capital 'A' (65) beats 'c' (99)
> - line 6: `index` finds the first 'A' at position 3; `count` counts
>   all 'A's

## The method toolbox

```python
s = "heLLo how are you"
print(s.upper(), s.lower(), s.title())
print("Good morning".startswith("Goo"), "Good morning".endswith("ing"))
print("Good morning".find("x"))
print("Hallo".isalpha(), "123".isdigit(), "Hallo3".isalnum())
print(":".join(["a", "b", "c"]))
print("a:b:c".split(":"))
print("Narri Narro".replace("a", "aa", 1))
```

> **What happens here**
>
> - line 2: upper/lower/title change the casing
> - line 3: startswith/endswith check the edges -> True, True
> - line 4: `find` returns -1 for "not found" - `index()` would crash!
> - line 5: is-alpha / is-digit / is-alnum answer yes/no questions
> - line 6-7: `join` glues a list with a separator; `split` cuts a
>   string into a list
> - line 8: `replace(old, new, 1)` swaps at most 1 occurrence

> **Watch out** - `find` returns -1 when it fails, but `index` raises
> an error. Know which one you're using!

## Comparing words

Strings compare letter by letter by code point - `'Abcde' > 'b'` is
`False` because A=65 < b=98. If one string is a prefix of the other,
the longer one wins: `'abc' > 'ab'`.

## Try it yourself

- Print `chr(ord('k') + 1)` - which letter comes out?
- Check `'7up'.isalnum()` - letters AND digits only?
- Find `"'hello world'.find('o')"` - which position?

## Key words

| Word | Meaning |
|---|---|
| code point | a letter's secret number |
| ord / chr | letter -> number / number -> letter |
| `in` | 'is this piece inside?' test |
| find / index | position or -1 / position or crash |
| isalpha / isdigit / isalnum | 'only letters / digits / both' |
| startswith / endswith | check the edges of a string |
| join / split | glue a list / cut a string into a list |
| replace(old, new, n) | swap text, at most n times |
| upper/lower/title | change the casing |
""",
        },
        {
            "id": "ch11-quiz-1",
            "type": "quiz",
            "title": "ord and chr",
            "question": "What is `chr(ord('a') + 3)`?",
            "options": ["'a'", "'c'", "'d'", "Error"],
            "answer": 2,
            "explanation": "ord('a') is 97, plus 3 makes 100 - and chr(100) is 'd'. Number-shifting letters is the Caesar cipher's whole trick.",
        },
        {
            "id": "ch11-quiz-2",
            "type": "quiz",
            "title": "find vs index",
            "question": "'hello'.find('x') returns...",
            "options": ["None", "-1", "0", "raises ValueError"],
            "answer": 1,
            "explanation": "find() answers 'not there' politely with -1. index() asks the same question but raises ValueError - pick your style.",
        },
        {
            "id": "ch11-quiz-3",
            "type": "quiz",
            "title": "Validation methods",
            "question": "Which expression is True?",
            "options": ["'Hallo'.isdigit()", "'123'.isalpha()", "'Hallo3'.isalnum()", "''.isalnum()"],
            "answer": 2,
            "explanation": "isalnum() wants only letters and digits, non-empty - 'Hallo3' passes. The empty string fails it; '123' fails isalpha; 'Hallo' fails isdigit.",
        },
        {
            "id": "ch11-quiz-4",
            "type": "quiz",
            "title": "String comparison",
            "question": "Is `'Abc' > 'b'`?",
            "options": ["True", "False", "Error", "Only if same length"],
            "answer": 1,
            "explanation": "Comparison goes by code point of the first letters: 'A' (65) is smaller than 'b' (98) - so False. Length only breaks ties.",
        },
        {
            "id": "ch11-warm-1",
            "type": "task",
            "title": "Next letter",
            "difficulty": 1,
            "plain": "Turn a letter into the next letter with ord and chr.",
            "instructions": r"""
Print the letter that comes **after** `c = 'h'` in the alphabet.

Expected output: `i`
""",
            "starter": """c = "h"
# TODO: print the next letter
""",
            "hints": [
                "`ord(c)` gives c's number; +1 is the next letter's number.",
                "`chr(...)` turns the number back into a letter.",
                "One line: `print(chr(ord(c) + 1))`.",
            ],
            "solution": """c = "h"
print(chr(ord(c) + 1))""",
            "explanation": "`ord('h')` is 104, plus 1 makes 105, and `chr(105)` is 'i'. Letter arithmetic: out through ord, back through chr.\n\nWhat you learned: `ord` and `chr` are a pair - one packs, one unpacks.",
            "tests": [
                {"kind": "program", "expected": "i", "match": "exact"},
            ],
        },
        {
            "id": "ch11-warm-2",
            "type": "task",
            "title": "Glue the words",
            "difficulty": 1,
            "plain": "Join a word list into one dashed string.",
            "instructions": r"""
Join `words` into one string separated by `-` and print it.

Expected output: `one-two-three`
""",
            "starter": """words = ["one", "two", "three"]
# TODO: join with '-' and print
""",
            "hints": [
                "join lives on the *separator*: `\"-\".join(words)`.",
                "It feels backwards - the string provides the glue.",
                "`print(\"-\".join(words))`.",
            ],
            "solution": """words = ["one", "two", "three"]
print("-".join(words))""",
            "explanation": "`\"-\".join(words)` asks the dash to glue the list's pieces together - the separator is the object doing the joining, which surprises everyone at first.\n\nWhat you learned: `sep.join(list)` - the separator is the boss.",
            "tests": [
                {"kind": "program", "expected": "one-two-three", "match": "exact"},
            ],
        },
        {
            "id": "ch11-task-1",
            "type": "task",
            "title": "Hidden word by index",
            "difficulty": 2,
            "plain": "Every 31st letter spells a secret word - pick them out.",
            "instructions": r"""
A word hides in the text: print only the characters whose **index is
divisible by 31** (index 0 excluded). Use a loop.

Expected output (one word): `python`
""",
            "starter": """s = "Lorem ipsum dolor sit amet, conpectetur adipisici elit," \\
    "lapsed yusmod tempor incidunt ut laborte et dolore magna" \\
    "aliquasum. Uthenim ad minim veniam, quis nosorud exercihation" \\
    "ullamco laborin nisi ut aliquid ex consequat."

# TODO: print the characters at indices 31, 62, 93, ...
""",
            "hints": [
                "Loop `i` over `range(1, len(s))`, keep `s[i]` when `i % 31 == 0`.",
                "Collect into `hidden = ""` with `+=`, print at the end.",
                "Slice shortcut: `s[31::31]` - same answer, no loop.",
            ],
            "solution": """s = "Lorem ipsum dolor sit amet, conpectetur adipisici elit," \\
    "lapsed yusmod tempor incidunt ut laborte et dolore magna" \\
    "aliquasum. Uthenim ad minim veniam, quis nosorud exercihation" \\
    "ullamco laborin nisi ut aliquid ex consequat."

hidden = ""
for i in range(1, len(s)):
    if i % 31 == 0:
        hidden += s[i]
print(hidden)
""",
            "explanation": "Every position divisible by 31 contributes one letter - 31, 62, 93, ... - and `hidden += s[i]` stitches them together. The modulo test picks them out; the range starts at 1 because index 0 is excluded.\n\nWhat you learned: `i % n == 0` is the 'every n-th' pattern.",
            "tests": [
                {"kind": "program", "expected": "python", "match": "exact"},
            ],
        },
        {
            "id": "ch11-task-2",
            "type": "task",
            "title": "Measuring resistance",
            "difficulty": 2,
            "plain": "Dig two numbers out of a sensor string and divide them.",
            "instructions": r"""
A device sends a string with voltage (`V`) and current (`mA` -
milliamps; 'Messwerte' means 'measurements', it stays as device
output):

```python
s = "Messwerte=12,54V-17,53mA"
```

Extract both numbers (decimal commas -> `12.54`, `17.53`), convert mA
to A (÷1000) and compute `R = U / I`.

Print exactly: `R = 715.35 Ohm` (2 decimals).
""",
            "starter": """s = "Messwerte=12,54V-17,53mA"

# TODO: extract U and I, compute R = U / I, print "R = 715.35 Ohm"
""",
            "hints": [
                "Split twice: `s.split('=')[1]` then on `'-'` -> the two raw values.",
                "Strip units (`replace('V','')`, `replace('mA','')`), then `replace(',', '.')` and `float()`.",
                "Don't forget ÷1000 for mA->A. `f'R = {u / i:.2f} Ohm'`.",
            ],
            "solution": """s = "Messwerte=12,54V-17,53mA"

values = s.split("=")[1].split("-")
u = float(values[0].replace("V", "").replace(",", "."))
i = float(values[1].replace("mA", "").replace(",", ".")) / 1000
print(f"R = {u / i:.2f} Ohm")
""",
            "explanation": "Two splits peel the numbers out: '=' separates the label, '-' separates the values. `replace` chains remove the units and swap decimal commas for dots so `float` can parse them. Dividing mA by 1000 gives amps - the step that makes the result 715.35 instead of 0.72.\n\nWhat you learned: split + replace + float is the recipe for reading machine text.",
            "tests": [
                {"kind": "program", "expected": "R = 715.35 Ohm", "match": "exact"},
            ],
        },
        {
            "id": "ch11-task-3",
            "type": "task",
            "title": "Secret message after 'nad'",
            "difficulty": 2,
            "plain": "Each 'nad' in the text hides one letter of a secret word.",
            "instructions": r"""
The text contains `nad` several times - each letter **immediately
after** a `nad` belongs to the secret word. Example: `'Wnadxelt'`
yields `'x'`.

Collect all such letters into `secret` and print it. (Expected: a
six-letter German word starting with 'g'.)
""",
            "starter": """s = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit," \\
    "sed diamnadg nonummy nibh euismod tincidunt ut laoreet dolore" \\
    "magna aliquam eratnade volutpat. Ut wisi enim ad minim veniam," \\
    "quis nostrud exerci tation ullamcorper suscipit lobortis" \\
    "nisl ut aliquip ex ea commodo consequat. Duis autem vel eum" \\
    "iriure dolor in hendrerit in vulputate velit esse molestie" \\
    "consequat, vel illum dolore eu feugiat nulla facilisis at" \\
    "vero et accumsan et iusto odio dignissim qui blandit" \\
    "praesent luptatum zzril delenit augue duis dolore te feugait" \\
    "nulla facilisi. Lorem ipsum dolornadh sit amet, consectetuer" \\
    "adipiscing elit, sed diam nonummy nibh euismod tincidunt ut" \\
    "laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad" \\
    "minim veniam, quis nostrud exercinade tation ullamcorper" \\
    "suscipit lobortisnadi nisl ut aliquip ex ea commodo consequat." \\
    "Duis autem vel eum iriure dolor in hendrerit in vulputate" \\
    "velit esse molestie consequat, vel illum dolore eu feugiat" \\
    "nulla facilisis at veronadm et accumsan et iusto odio dignissim" \\
    "qui blandit praesent luptatum zzril delenit augue duis" \\
    "dolore te feugait nulla facilisi. Nam liber tempor cum soluta" \\
    "nobis eleifend option congue nihil imperdiet doming id quod" \\
    "mazim placerat facer possim assum."

secret = ""
# TODO: collect the letters after each 'nad' and print secret
""",
            "hints": [
                "`s.find('nad', start)` searches from position `start` - returns -1 when done.",
                "The wanted letter is `s[i + 3]`; continue searching from `i + 3`.",
                "`secret += s[i + 3]` inside the loop; print after.",
            ],
            "solution": """s = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit," \\
    "sed diamnadg nonummy nibh euismod tincidunt ut laoreet dolore" \\
    "magna aliquam eratnade volutpat. Ut wisi enim ad minim veniam," \\
    "quis nostrud exerci tation ullamcorper suscipit lobortis" \\
    "nisl ut aliquip ex ea commodo consequat. Duis autem vel eum" \\
    "iriure dolor in hendrerit in vulputate velit esse molestie" \\
    "consequat, vel illum dolore eu feugiat nulla facilisis at" \\
    "vero et accumsan et iusto odio dignissim qui blandit" \\
    "praesent luptatum zzril delenit augue duis dolore te feugait" \\
    "nulla facilisi. Lorem ipsum dolornadh sit amet, consectetuer" \\
    "adipiscing elit, sed diam nonummy nibh euismod tincidunt ut" \\
    "laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad" \\
    "minim veniam, quis nostrud exercinade tation ullamcorper" \\
    "suscipit lobortisnadi nisl ut aliquip ex ea commodo consequat." \\
    "Duis autem vel eum iriure dolor in hendrerit in vulputate" \\
    "velit esse molestie consequat, vel illum dolore eu feugiat" \\
    "nulla facilisis at veronadm et accumsan et iusto odio dignissim" \\
    "qui blandit praesent luptatum zzril delenit augue duis" \\
    "dolore te feugait nulla facilisi. Nam liber tempor cum soluta" \\
    "nobis eleifend option congue nihil imperdiet doming id quod" \\
    "mazim placerat facer possim assum."

secret = ""
i = 0
while True:
    i = s.find("nad", i)
    if i == -1:
        break
    if i + 3 < len(s):
        secret += s[i + 3]
    i += 3
print(secret)
""",
            "explanation": "`find('nad', i)` jumps to the next marker and remembers where - `-1` ends the loop via break. `i + 3` is the letter right after the marker, and `i += 3` moves past it so it can't be found twice. Six markers spell 'geheim' (German for 'secret' - fitting!).\n\nWhat you learned: `find` with a start position walks a string marker by marker.",
            "tests": [
                {"kind": "program", "expected": "geheim", "match": "exact"},
                {"kind": "expr", "expr": "secret", "expected": "'geheim'"},
            ],
        },
        {
            "id": "ch11-task-4",
            "type": "task",
            "title": "EAN check digit",
            "difficulty": 2,
            "plain": "The last digit of a barcode is math on the first twelve.",
            "instructions": r"""
An EAN-13 barcode's last digit is a check digit computed from the
first 12: multiply them alternately by 1 and 3, sum, and the check
digit is the distance to the next multiple of 10 (0 when already
divisible).

Example `978381582086?`: the weighted sum is 115 -> check digit **5**.

Write:

- `check_digit(ean12)` -> the check digit (int) for a 12-digit string.
  `check_digit("978381582086")` -> `5`
- `is_valid(ean13)` -> `True` if the last digit equals the computed one.
""",
            "starter": """def check_digit(ean12):
    # TODO: alternating weights 1,3,1,3,... starting with 1
    pass

def is_valid(ean13):
    # TODO
    pass
""",
            "hints": [
                "Weight is 1 at even index, 3 at odd - `enumerate` helps.",
                "Check digit: `(10 - total % 10) % 10` (the outer %10 handles sum divisible by 10).",
                "`is_valid`: `int(ean13[-1]) == check_digit(ean13[:12])`.",
            ],
            "solution": """def check_digit(ean12):
    total = 0
    for i, ch in enumerate(ean12):
        total += int(ch) * (1 if i % 2 == 0 else 3)
    return (10 - total % 10) % 10

def is_valid(ean13):
    return int(ean13[-1]) == check_digit(ean13[:12])
""",
            "explanation": "`enumerate` gives each digit its position; even positions get weight 1, odd get 3 - matching the barcode rule. `(10 - total % 10) % 10` computes the distance to the next ten, and the trailing `% 10` turns '10' into 0. `is_valid` just compares the last printed digit with a fresh computation.\n\nWhat you learned: check digits catch typos - a real-world use of % and weighted sums.",
            "tests": [
                {"kind": "expr", "expr": "check_digit('978381582086')", "expected": "5"},
                {"kind": "expr", "expr": "is_valid('9783815820865')", "expected": "True"},
                {"kind": "expr", "expr": "is_valid('9783815820860')", "expected": "False"},
                {"kind": "expr", "expr": "is_valid('4006381333931')", "expected": "True"},
            ],
        },
        {
            "id": "ch11-task-5",
            "type": "task",
            "title": "Caesar cipher",
            "difficulty": 2,
            "plain": "Shift every letter by a secret key - z wraps around to a.",
            "instructions": r"""
Write `caesar(text, key)` shifting every letter by `key` positions -
circular, so `Z` + 1 -> `A`. Keep upper/lowercase; leave non-letters
unchanged.

```python
caesar("Volkswagen", 10)   # 'Fyvucgkqox'
caesar("abc", 1)           # 'bcd'
caesar("Zz!", 1)           # 'Aa!'
```
""",
            "starter": """def caesar(text, key):
    # TODO: shift letters circularly by key
    pass
""",
            "hints": [
                "Per letter: move into 0-25 space (`ord(c) - ord('a')`), add key, wrap with `% 26`, move back.",
                "Lowercase and uppercase each need their own branch ('a' vs 'A' as base).",
                "Everything else appends unchanged; build `result` with `+=`.",
            ],
            "solution": """def caesar(text, key):
    result = ""
    for c in text:
        if 'a' <= c <= 'z':
            result += chr((ord(c) - ord('a') + key) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            result += chr((ord(c) - ord('A') + key) % 26 + ord('A'))
        else:
            result += c
    return result
""",
            "explanation": "Each letter is shifted inside 0-25 space: subtract the base ('a' or 'A'), add the key, `% 26` wraps Z->A, add the base back. Two branches handle the two cases; everything else passes through untouched. Shifting by 26 - key decodes, which is why `caesar(caesar(s, 7), 19)` returns the original.\n\nWhat you learned: `(x + k) % n` is wrap-around arithmetic.",
            "tests": [
                {"kind": "expr", "expr": "caesar('Volkswagen', 10)", "expected": "'Fyvucgkqox'"},
                {"kind": "expr", "expr": "caesar('abc', 1)", "expected": "'bcd'"},
                {"kind": "expr", "expr": "caesar('Zz!', 1)", "expected": "'Aa!'"},
                {"kind": "expr", "expr": "caesar(caesar('Secret-Text', 7), 19)", "expected": "'Secret-Text'"},
            ],
        },
        {
            "id": "ch11-task-6",
            "type": "task",
            "title": "Wind turbine record",
            "difficulty": 2,
            "plain": "Split a turbine's status line and flip the date around.",
            "instructions": r"""
A wind turbine reports hourly data `;`-separated:

```python
wkr = "2020-12-16,08:00;8ms;2,3MW"
#       datetime        ;wind;power
```

Print the fields, then reformat the date to DD.MM.YYYY - exactly:

```
Datetime: 2020-12-16,08:00
Wind: 8ms
Power: 2,3MW
Datetime: 16.12.2020,08:00
```
""",
            "starter": """wkr = "2020-12-16,08:00;8ms;2,3MW"

# TODO: split, print the fields, reformat the date
""",
            "hints": [
                "`wkr.split(';')` gives `[datetime, wind, power]` - unpack into three variables.",
                "Split the datetime on `','`, then the date on `'-'` into y, m, d.",
                "Reassemble as `f'{d}.{m}.{y},{time}'`.",
            ],
            "solution": """wkr = "2020-12-16,08:00;8ms;2,3MW"

dt, wind, power = wkr.split(";")
print("Datetime:", dt)
print("Wind:", wind)
print("Power:", power)

date_part, time_part = dt.split(",")
y, m, d = date_part.split("-")
print(f"Datetime: {d}.{m}.{y},{time_part}")
""",
            "explanation": "Nested splits dissect the line: ';' for the three fields, ',' for date vs time, '-' for year/month/day. Unpacking into named variables keeps it readable, and the f-string reorders them into German date format.\n\nWhat you learned: splitting by different separators peels a record layer by layer.",
            "tests": [
                {"kind": "program",
                 "expected": "Datetime: 2020-12-16,08:00\nWind: 8ms\nPower: 2,3MW\nDatetime: 16.12.2020,08:00",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch11-boss",
            "type": "task",
            "title": "Secret message decoder",
            "difficulty": 3,
            "boss": True,
            "plain": "Decode a scrambled message - every letter was shifted by 3.",
            "instructions": r"""
**BOSS MISSION - decode the intercepted message.**

A spy shifted every letter **forward by 3** (Caesar key 3, circular).
Write `decode(text)` that shifts letters **back** by 3 - wrap-around
and case preserved, non-letters unchanged:

```python
decode("Sbwkrq urfnv!")    # 'Python rocks!'
decode("Deefgh")          # 'Abbcde'  (D wraps to A)
```
""",
            "starter": """def decode(text):
    # TODO: shift every letter back by 3 (circular)
    pass
""",
            "example": """A Caesar shift on three letters:

```python
def shift(c, k):
    if "a" <= c <= "z":
        return chr((ord(c) - ord("a") + k) % 26 + ord("a"))
    return c

print("".join(shift(c, 1) for c in "hi!"))
```
""",

            "hints": [
                "Same trick as the Caesar task - but `key = -3`, or subtract 3.",
                "`(ord(c) - ord('a') - 3) % 26` handles the wrap for you.",
                "Two branches: lowercase base 'a', uppercase base 'A'; others pass through.",
            ],
            "solution": """def decode(text):
    result = ""
    for c in text:
        if 'a' <= c <= 'z':
            result += chr((ord(c) - ord('a') - 3) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            result += chr((ord(c) - ord('A') - 3) % 26 + ord('A'))
        else:
            result += c
    return result
""",
            "explanation": "Decoding is just shifting the other way - subtracting 3 instead of adding the key. `% 26` rescues letters that dip below 'a' (D becomes 0-something, wraps to A). Punctuation never enters the branches and passes through.\n\nWhat you learned: encrypting and decrypting are the same code with opposite signs.",
            "tests": [
                {"kind": "expr", "expr": "decode('Sbwkrq urfnv!')", "expected": "'Python rocks!'"},
                {"kind": "expr", "expr": "decode('Deefgh')", "expected": "'Abbcde'"},
                {"kind": "expr", "expr": "decode('D')", "expected": "'A'"},
            ],
        },
    ],
}
