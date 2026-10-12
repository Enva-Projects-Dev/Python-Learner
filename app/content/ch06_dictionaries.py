"""Kapitel 6 - Dictionaries & JSON."""

CHAPTER = {
    "id": "ch06",
    "number": 6,
    "title": "Dictionaries & JSON",
    "summary": "The phone book: look things up by name instead of by number.",
    "items": [
        {
            "id": "ch06-lesson",
            "type": "lesson",
            "title": "Dictionaries: the phone book",
            "body": r"""
## Look it up by name

In a list you find things by locker **number**. A **dictionary** finds
things by **name** - like a phone book: look up "Klose", get "11".

```python
team = {"Neuer": 1, "Kroos": 18, "Mueller": 13, "Klose": 11}
print(team["Klose"])          # 11 - instant!
```

The word you look up (`"Klose"`) is the **key**, what you get back is
the **value**: `key -> value` pairs.

## Writing in the phone book

```python
names = {}                          # empty book
names["Potter"] = "Harry"           # add a line
names["Weasley"] = "Ron"
names["Weasley"] = "Percy"          # same key = overwrite!
del names["Weasley"]                # tear the page out

print(names.get("Meier"))                       # None - no crash
print(names.get("Meier", "unknown person"))     # with a fallback
print("Potter" in names)                        # True
```

> **Watch out** - `names["Meier"]` on a missing key crashes with a
> `KeyError`. `.get(name)` answers politely with `None` instead.

## Walking the whole book

```python
names = {"Potter": "Harry", "Granger": "Hermione"}   # our phone book
for last in names:                    # loops over the KEYS
    print(last)
for first in names.values():          # the values
    print(first)
for last, first in names.items():     # both at once
    print(last, "->", first)
```

> **What happens here**
>
> - line 1: rebuild the phone book - Potter->Harry, Granger->Hermione
> - line 2: looping a dict visits the keys (the last names)
> - line 4: `.values()` visits only the right-hand sides
> - line 6: `.items()` hands out both at once, as pairs

## JSON: dicts as text

**JSON** is a text format that looks exactly like a Python dict - every
program on the planet can read it. `json.dumps` packs a dict into text,
`json.loads` unpacks it back:

```python
import json

sensor = {"sensor": "DHT12", "reading": {"temp": {"value": 27.5, "unit": "C"}}}
text = json.dumps(sensor)        # -> one long string
data = json.loads(text)          # -> the dict again
print(data["reading"]["temp"]["value"])   # 27.5
```

## Try it yourself

- Make a dict of 3 friends -> their favourite food, then print one.
- Add `["Bob"]` to it, then loop `.items()` and print each line.

## Key words

| Word | Meaning |
|---|---|
| dictionary / dict | key -> value pairs in `{ }` |
| key / value | the name you look up / what you get back |
| `.get(key, default)` | safe lookup with a fallback |
| `.keys() / .values() / .items()` | ways to walk the book |
| JSON / dumps / loads | dicts as text / pack / unpack |
""",
        },
        {
            "id": "ch06-quiz-1",
            "type": "quiz",
            "title": "get() with default",
            "question": "For `d = {'a': 1}`, what does `d.get('b', 99)` return?",
            "options": ["None", "KeyError", "99", "1"],
            "answer": 2,
            "explanation": "get() falls back to the default when the key isn't there - 'b' is missing, so you get 99 instead of a crash.",
        },
        {
            "id": "ch06-quiz-2",
            "type": "quiz",
            "title": "Iteration",
            "question": "`for k in {'x': 1, 'y': 2}: print(k)` prints what?",
            "options": ["1 then 2", "x then y", "('x',1) then ('y',2)", "Error"],
            "answer": 1,
            "explanation": "Looping over a dict walks its KEYS - x, then y. For the pairs you need `.items()`.",
        },
        {
            "id": "ch06-quiz-3",
            "type": "quiz",
            "title": "JSON",
            "question": "`json.loads('{\"a\": [1, 2]}')['a'][1]` is...",
            "options": ["'1'", "2", "[1, 2]", "Error"],
            "answer": 1,
            "explanation": "loads() rebuilds real Python objects - a dict containing a list - so ['a'] gives the list and [1] picks out 2.",
        },
        {
            "id": "ch06-quiz-4",
            "type": "quiz",
            "title": "Overwriting keys",
            "question": "After `d = {}; d['a'] = 1; d['a'] = 2`, what is `d`?",
            "options": ["{'a': 1}", "{'a': 2}", "{'a': [1, 2]}", "Error - key used twice"],
            "answer": 1,
            "explanation": "A key is one line in the book - assigning again overwrites it: {'a': 2}. No error, no list.",
        },
        {
            "id": "ch06-warm-1",
            "type": "task",
            "title": "First phone book",
            "difficulty": 1,
            "plain": "Put one friend in the book and look them up.",
            "instructions": r"""
1. Add `"Tick" -> "12345"` to the phone book.
2. Print the number stored under `"Tick"`.

Expected output: `12345`
""",
            "starter": """phonebook = {}
# TODO: add "Tick" -> "12345", then print it
""",
            "hints": [
                "Write a line into the book: `phonebook['Tick'] = '12345'`.",
                "Read it back the same way: `phonebook['Tick']`.",
                "One assignment, one print.",
            ],
            "solution": """phonebook = {}
phonebook["Tick"] = "12345"
print(phonebook["Tick"])""",
            "explanation": "`phonebook[\"Tick\"] = \"12345\"` writes a key->value line; reading `phonebook[\"Tick\"]` looks the name up - number out, just like a real phone book.\n\nWhat you learned: `d[key] = value` writes, `d[key]` reads.",
            "tests": [
                {"kind": "program", "expected": "12345", "match": "exact"},
            ],
        },
        {
            "id": "ch06-warm-2",
            "type": "task",
            "title": "Safe lookup",
            "difficulty": 1,
            "plain": "Ask for a name that is not in the book - without crashing.",
            "instructions": r"""
The book below has no `"Max"`. Print the lookup result for `"Max"`
using `.get()` with the default `"not found"`.

Expected output: `not found`
""",
            "starter": """phonebook = {"Tick": "12345", "Trick": "23456"}
# TODO: print a safe lookup for "Max"
""",
            "hints": [
                "`phonebook['Max']` would crash - use `.get` instead.",
                "Second argument is the fallback: `.get('Max', 'not found')`.",
                "`print(phonebook.get(...))`.",
            ],
            "solution": """phonebook = {"Tick": "12345", "Trick": "23456"}
print(phonebook.get("Max", "not found"))""",
            "explanation": "`.get` never crashes on a missing key - it quietly returns the second argument instead. `phonebook['Max']` would have raised a KeyError.\n\nWhat you learned: `.get(key, fallback)` is the polite way to look things up.",
            "tests": [
                {"kind": "program", "expected": "not found", "match": "exact"},
            ],
        },
        {
            "id": "ch06-task-1",
            "type": "task",
            "title": "Phone book lookup",
            "difficulty": 1,
            "plain": "Let the user type a name and get the number back.",
            "instructions": r"""
Extend the phone book with at least one more entry, then read a name
from input and print its number - or `unknown person` when it isn't
in the book.

Example runs:

```
input:  Trick   -> output: 23456
input:  Donald  -> output: unknown person
```
""",
            "starter": """phonebook = {}
phonebook["Tick"] = "12345"
phonebook["Trick"] = "23456"
# TODO: add at least one more person

name = input("Name: ")
# TODO: print the number or "unknown person"
""",
            "hints": [
                "`phonebook['Track'] = '34567'` adds another line.",
                "One `.get` call handles both cases - with `'unknown person'` as fallback.",
                "Print whatever `.get` returns.",
            ],
            "solution": """phonebook = {}
phonebook["Tick"] = "12345"
phonebook["Trick"] = "23456"
phonebook["Track"] = "34567"

name = input("Name: ")
print(phonebook.get(name, "unknown person"))
""",
            "explanation": "The book gets a third entry, then `input` reads the name to search. `.get(name, 'unknown person')` answers with the number when the name exists and the fallback when it doesn't - one line covers both cases.\n\nWhat you learned: `input` + `.get` = a tiny interactive lookup program.",
            "tests": [
                {"kind": "program", "stdin": "Trick\n", "expected": "23456", "match": "lines"},
                {"kind": "program", "stdin": "Donald\n", "expected": "unknown person", "match": "lines"},
            ],
        },
        {
            "id": "ch06-task-2",
            "type": "task",
            "title": "Maternal ancestors",
            "difficulty": 2,
            "plain": "Follow the mother-links until the trail ends.",
            "instructions": r"""
`daughter_to_mother` maps each woman to her mother. Starting from
`wanted = "Lilli"`, print the whole maternal line exactly like this:

```
Lilli is the daughter of Anne.
Anne is the daughter of Ursula.
Ursula is the daughter of Lydia.
The mother of Lydia is not known.
```

Stop when a woman has no entry in the dict.
""",
            "starter": """daughter_to_mother = dict(Nicole="Gabi", Anne="Ursula", Margret="Anneliese",
                          Matilda="Anne", Lilli="Anne", Cornelia="Margret",
                          Marlene="Nicole", Ursula="Lydia")
wanted = "Lilli"

# TODO: print the ancestor lines
""",
            "hints": [
                "Keep going while `wanted in daughter_to_mother`.",
                "Inside the loop: look up the mother, print the line, then `wanted = mother` to move one generation up.",
                "After the loop, `wanted` is the woman without an entry - print the 'not known' line.",
            ],
            "solution": """daughter_to_mother = dict(Nicole="Gabi", Anne="Ursula", Margret="Anneliese",
                          Matilda="Anne", Lilli="Anne", Cornelia="Margret",
                          Marlene="Nicole", Ursula="Lydia")
wanted = "Lilli"

while wanted in daughter_to_mother:
    mother = daughter_to_mother[wanted]
    print(f"{wanted} is the daughter of {mother}.")
    wanted = mother
print(f"The mother of {wanted} is not known.")
""",
            "explanation": "The while loop is a chain-climber: each round looks up the current woman's mother and steps onto her. `in` checks whether the book has a next link - when it doesn't, `wanted` still holds the last woman and the loop ends. The final print reports her as the end of the known line.\n\nWhat you learned: a dict plus a while loop can follow chains of any length.",
            "tests": [
                {"kind": "program",
                 "expected": "Lilli is the daughter of Anne.\nAnne is the daughter of Ursula.\nUrsula is the daughter of Lydia.\nThe mother of Lydia is not known.",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch06-task-3",
            "type": "task",
            "title": "Word frequencies in Faust",
            "difficulty": 2,
            "plain": "Count how often every word appears in a whole book.",
            "instructions": r"""
`Goethe--Faust.txt` is in your folder. Count each word:

1. The starter already reads the file and builds `words` (punctuation
   stripped - same trick as chapter 3).
2. Count occurrences into a dict `counter` (word -> count). Skip empty
   words (`if w`).
3. Build `top10`: the ten most frequent words as `(count, word)`
   tuples, most frequent first.

Expected `top10`:

```python
[(507, 'und'), (474, 'Faust'), (465, 'die'), (461, 'ich'),
 (454, 'der'), (412, 'Und'), (395, 'nicht'), (368, 'zu'),
 (312, 'ist'), (296, 'ein')]
```
""",
            "starter": """import string

with open("Goethe--Faust.txt", encoding="utf-8") as f:
    lines = f.readlines()

words = [w.strip(string.punctuation) for line in lines for w in line.split()]

counter = {}
# TODO: count words into counter

top10 = []
# TODO: ten most frequent as (count, word) tuples

print(top10)
""",
            "hints": [
                "The counting line: `counter[w] = counter.get(w, 0) + 1`.",
                "Swap to `(count, word)` so sorting ranks by count: `[(c, w) for w, c in counter.items()]`.",
                "`sorted(pairs, reverse=True)[:10]` gives the top ten.",
            ],
            "solution": """import string

with open("Goethe--Faust.txt", encoding="utf-8") as f:
    lines = f.readlines()

words = [w.strip(string.punctuation) for line in lines for w in line.split()]

counter = {}
for w in words:
    if w:
        counter[w] = counter.get(w, 0) + 1

pairs = [(c, w) for w, c in counter.items()]
top10 = sorted(pairs, reverse=True)[:10]
print(top10)
""",
            "explanation": "`counter.get(w, 0) + 1` is the classic counting trick - a word we've never seen counts as 0, then gets +1. Sorting needs numbers first, so the comprehension swaps each pair to `(count, word)`; `sorted(..., reverse=True)` puts the biggest counts on top, and `[:10]` keeps the ten leaders.\n\nWhat you learned: dict + get-with-default turns counting into one line.",
            "tests": [
                {"kind": "expr", "expr": "counter['und']", "expected": "507"},
                {"kind": "expr", "expr": "counter['Faust']", "expected": "474"},
                {"kind": "expr", "expr": "top10",
                 "expected": "[(507, 'und'), (474, 'Faust'), (465, 'die'), (461, 'ich'), (454, 'der'), (412, 'Und'), (395, 'nicht'), (368, 'zu'), (312, 'ist'), (296, 'ein')]"},
            ],
        },
        {
            "id": "ch06-task-4",
            "type": "task",
            "title": "Invert the family tree",
            "difficulty": 3,
            "plain": "Flip the mother-dict around: from each mother to her daughters.",
            "instructions": r"""
Build `mother_to_daughters` from `daughter_to_mother`: each mother
maps to a **list** of her daughters (a mother can have several!).

Then compute `descendants`: all female descendants of `"Lydia"`,
sorted alphabetically.

Expected: `['Anne', 'Lilli', 'Matilda', 'Ursula']`

(Lydia -> Ursula -> Anne -> Lilli and Matilda.)
""",
            "starter": """daughter_to_mother = dict(Nicole="Gabi", Anne="Ursula", Margret="Anneliese",
                          Matilda="Anne", Lilli="Anne", Cornelia="Margret",
                          Marlene="Nicole", Ursula="Lydia")

mother_to_daughters = {}
# TODO: build the inverted dict (mother -> list of daughters)

descendants = []
# TODO: collect all descendants of "Lydia", then sort
""",
            "hints": [
                "Loop `daughter_to_mother.items()` and append each daughter to her mother's list: `setdefault(mother, []).append(daughter)`.",
                "Use a worklist: start with `['Lydia']`, pop a name, add her daughters to descendants AND the worklist.",
                "Sort `descendants` at the end.",
            ],
            "solution": """daughter_to_mother = dict(Nicole="Gabi", Anne="Ursula", Margret="Anneliese",
                          Matilda="Anne", Lilli="Anne", Cornelia="Margret",
                          Marlene="Nicole", Ursula="Lydia")

mother_to_daughters = {}
for daughter, mother in daughter_to_mother.items():
    mother_to_daughters.setdefault(mother, []).append(daughter)

descendants = []
worklist = ["Lydia"]
while worklist:
    name = worklist.pop()
    for child in mother_to_daughters.get(name, []):
        descendants.append(child)
        worklist.append(child)
descendants = sorted(descendants)
""",
            "explanation": "Inverting means walking every pair and appending the daughter to the mother's list - `setdefault` creates the list on first sight. The worklist then explores like a flood: pop a woman, record her daughters, push them so THEIR daughters get visited too. Sorting at the end gives alphabetical order.\n\nWhat you learned: `setdefault` fills dicts of lists, and a worklist walks a whole tree.",
            "tests": [
                {"kind": "expr", "expr": "sorted(mother_to_daughters['Anne'])",
                 "expected": "['Lilli', 'Matilda']"},
                {"kind": "expr", "expr": "mother_to_daughters['Ursula']", "expected": "['Anne']"},
                {"kind": "expr", "expr": "descendants",
                 "expected": "['Anne', 'Lilli', 'Matilda', 'Ursula']"},
            ],
        },
        {
            "id": "ch06-task-5",
            "type": "task",
            "title": "Sensor JSON round-trip",
            "difficulty": 2,
            "plain": "Build a nested dict, pack it into JSON text, unpack it back.",
            "instructions": r"""
Build this nested dict in `sensor` (exact structure - it comes from a
real weather-station project, so the German field names stay):

```python
{'Sensor': 'DHT12',
 'Messwert': {'Temperatur': {'Wert': 27.5, 'Einheit': 'Grad'},
              'Feuchtigkeit': {'Wert': 65.5, 'Einheit': '%'}}}
```

Then:

- `json_text` - `json.dumps(sensor)` (a string)
- `restored` - `json.loads(json_text)`, equal to the original
""",
            "starter": """import json

sensor = {}        # TODO: build the nested dict
json_text = ""     # TODO: serialise with json.dumps
restored = {}      # TODO: parse back with json.loads
""",
            "hints": [
                "Write the literal exactly as shown - dicts inside dicts.",
                "`json_text = json.dumps(sensor)` packs it.",
                "`restored = json.loads(json_text)` unpacks it.",
            ],
            "solution": """import json

sensor = {'Sensor': 'DHT12',
          'Messwert': {'Temperatur': {'Wert': 27.5, 'Einheit': 'Grad'},
                       'Feuchtigkeit': {'Wert': 65.5, 'Einheit': '%'}}}
json_text = json.dumps(sensor)
restored = json.loads(json_text)
""",
            "explanation": "The dict nests three levels deep - Sensor -> Messwert -> two readings with value and unit each. `dumps` flattens it into one portable string; `loads` rebuilds the identical structure, which the test proves with `restored == sensor`.\n\nWhat you learned: JSON round-trips preserve nested structures exactly.",
            "tests": [
                {"kind": "expr", "expr": "sensor['Messwert']['Temperatur']['Wert']", "expected": "27.5"},
                {"kind": "expr", "expr": "sensor['Messwert']['Feuchtigkeit']['Einheit']", "expected": "'%'"},
                {"kind": "assert", "code": "assert restored == sensor", "desc": "restored equals the original dict"},
                {"kind": "expr", "expr": "json.loads(json_text)['Sensor']", "expected": "'DHT12'"},
            ],
        },
        {
            "id": "ch06-task-6",
            "type": "task",
            "title": "IoT weather message",
            "difficulty": 2,
            "plain": "Dig six numbers out of a real sensor's JSON message.",
            "instructions": r"""
A weather station sent this JSON (already parsed in the starter).
Extract:

- `illuminance` - BH1750 value -> `190`
- `avg_temp` - mean of BMP180 and SHT3X temperatures -> `(30.7 + 29.1) / 2`
- `pressure` - BMP180 pressure -> `1005.0`
- `humidity` - SHT3X humidity -> `46.3`
- `dewpoint` - SHT3X dew point + the message's `TempUnit` -> `'16.4 C'`
- `timestamp` - the `Time` string

Variables must have exactly these names.
""",
            "starter": """import json

json_string = '''{"Time":"2021-09-02T16:04:21",
       "BMP180":{"Temperature":30.7,"Pressure":1005.0},
       "BH1750":{"Illuminance":190},
       "SHT3X":{"Temperature":29.1,"Humidity":46.3,"DewPoint":16.4},
       "PressureUnit":"hPa",
       "TempUnit":"C"}'''

data = json.loads(json_string)

# TODO: extract the six values into the variables below
illuminance = None
avg_temp = None
pressure = None
humidity = None
dewpoint = None
timestamp = None
""",
            "hints": [
                "Nested lookup: `data['BH1750']['Illuminance']`.",
                "Average of two lookups: `(bmp_temp + sht_temp) / 2`.",
                "Dew point combines a number and the unit string in an f-string.",
            ],
            "solution": """import json

json_string = '''{"Time":"2021-09-02T16:04:21",
       "BMP180":{"Temperature":30.7,"Pressure":1005.0},
       "BH1750":{"Illuminance":190},
       "SHT3X":{"Temperature":29.1,"Humidity":46.3,"DewPoint":16.4},
       "PressureUnit":"hPa",
       "TempUnit":"C"}'''

data = json.loads(json_string)

illuminance = data["BH1750"]["Illuminance"]
avg_temp = (data["BMP180"]["Temperature"] + data["SHT3X"]["Temperature"]) / 2
pressure = data["BMP180"]["Pressure"]
humidity = data["SHT3X"]["Humidity"]
dewpoint = f"{data['SHT3X']['DewPoint']} {data['TempUnit']}"
timestamp = data["Time"]
""",
            "explanation": "Each reading is a nested lookup - `data['SHT3X']['Humidity']` digs two levels. The average adds two temperature lookups and halves the sum, and the dew point f-string pairs the value with the unit the message itself declares.\n\nWhat you learned: chained `['a']['b']` lookups navigate nested JSON.",
            "tests": [
                {"kind": "expr", "expr": "illuminance", "expected": "190"},
                {"kind": "expr", "expr": "avg_temp", "expected": "29.9"},
                {"kind": "expr", "expr": "pressure", "expected": "1005.0"},
                {"kind": "expr", "expr": "humidity", "expected": "46.3"},
                {"kind": "expr", "expr": "dewpoint", "expected": "'16.4 C'"},
                {"kind": "expr", "expr": "timestamp", "expected": "'2021-09-02T16:04:21'"},
            ],
        },
        {
            "id": "ch06-boss",
            "type": "task",
            "title": "The pantry inventory",
            "difficulty": 3,
            "boss": True,
            "plain": "Read a JSON pantry, print a sorted stock report.",
            "instructions": r"""
**BOSS MISSION - the pantry report.**

The kitchen's stock arrives as JSON (in the starter). Parse it, then
print this exact report - items in **alphabetical** order:

```
apple: 3
bread: 1
cola: 6
Total items: 10
Most: cola (6)
```

- one `name: count` line per item, sorted by name
- `Total items:` the sum of all counts
- `Most:` the item with the biggest count - find it in a loop, no
  `max()` on dicts
""",
            "starter": """import json

raw = '{"cola": 6, "apple": 3, "bread": 1}'
stock = json.loads(raw)

# TODO: print the 5-line report
""",
            "example": """Pick the top entry of a dictionary:

```python
scores = {"ada": 4, "tim": 9}
best = max(scores, key=scores.get)
print(best, scores[best])
```
""",

            "hints": [
                "`sorted(stock)` gives the item names in alphabetical order - loop over it.",
                "Sum the counts with a loop (or `sum(stock.values())`).",
                "Champion loop: `if stock[name] > best_count:` remember name + count.",
            ],
            "solution": """import json

raw = '{"cola": 6, "apple": 3, "bread": 1}'
stock = json.loads(raw)

total = 0
best_name, best_count = "", -1
for name, count in stock.items():
    total += count
    if count > best_count:
        best_name, best_count = name, count

for name in sorted(stock):
    print(f"{name}: {stock[name]}")
print(f"Total items: {total}")
print(f"Most: {best_name} ({best_count})")
""",
            "explanation": "The first loop does double duty - adding every count to `total` while keeping the champion `(best_name, best_count)` up to date. `sorted(stock)` then walks the keys alphabetically for the item lines (dicts remember insertion order, but we want alphabetical). The two f-strings close the report.\n\nWhat you learned: `stock.items()` for pairs, `sorted(dict)` for keys in order - the two workhorse dict loops.",
            "tests": [
                {"kind": "program",
                 "expected": "apple: 3\nbread: 1\ncola: 6\nTotal items: 10\nMost: cola (6)",
                 "match": "exact"},
            ],
        },
    ],
}
