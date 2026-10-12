"""Kapitel 10 - Exceptions, Einstieg."""

CHAPTER = {
    "id": "ch10",
    "number": 10,
    "title": "Exceptions: Introduction",
    "summary": "Catching errors politely: try/except, the exception zoo, else/finally.",
    "items": [
        {
            "id": "ch10-lesson",
            "type": "lesson",
            "title": "try, except, else, finally",
            "body": r"""
Real programs meet bad input, missing files and impossible math all
the time. Without protection, the first problem kills the whole
program. **Exceptions** are Python's alarm system - and `try`/`except`
is how you answer the alarm instead of crashing.

> **Think of it like...** an exception is the program shouting
> "something went wrong!" and throwing a red flag. `except` is the
> catcher who grabs that flag and decides what to do.

```python
x = 0
try:
    print(100 / x)
except ZeroDivisionError:
    print("Division by zero is not allowed.")
```

> **What happens here**
>
> - line 2: `try:` starts the risky zone - "this might blow up"
> - line 3: dividing by zero raises a **ZeroDivisionError**; the print
>   never finishes
> - line 4: `except ZeroDivisionError:` catches exactly that flag
> - line 5: this line runs instead of crashing

## The exception zoo - know your flags

Every error type has a name; you can catch exactly the one you expect:

| Exception | Raised when |
|-----------|-------------|
| `ValueError` | right type, wrong content (`int('abc')`) |
| `TypeError` | wrong type (`'a' + 1`) |
| `ZeroDivisionError` | dividing by zero |
| `IndexError` | list index too big |
| `KeyError` | missing dict key |
| `FileNotFoundError` | opening a file that isn't there |
| `AttributeError` | object doesn't have that attribute |

> **Watch out** - list specific types first! `except Exception` catches
> almost everything, so if it comes before `except ValueError`, the
> ValueError branch never runs - and surprise bugs get silently
> swallowed.

## else and finally

Two optional endings for a try block:

- `else:` runs only when `try` **succeeded**
- `finally:` runs **always** - the tidy-up spot (closing files)

```python
f = open("data.txt", "w")
try:
    f.write("hello")
except IOError as e:
    print("I/O error:", e)
else:
    print("written successfully")
finally:
    f.close()        # runs either way
```

> **What happens here**
>
> - line 3: the risky write happens inside try
> - line 4: `as e` gives the caught exception a name so we can print it
> - line 6: `else` only prints when writing worked
> - line 8: `finally` closes the file no matter what happened

## Raising yourself

`raise` throws a flag on purpose; a **bare** `raise` inside `except`
re-throws the same one upward so the caller can also react:

```python
def demo(x):
    try:
        return 10 / x
    except ZeroDivisionError:
        print("logging the problem")
        raise    # re-throw - the caller still sees it
```

> **What happens here**
>
> - line 3: `return 10 / x` - with `x = 0` this throws
>   ZeroDivisionError and the return never happens
> - line 5: the except catches it and prints a log line first
> - line 6: the bare `raise` throws the SAME flag onward - whoever
>   called `demo(0)` still sees the error

## Try it yourself

- Wrap `print([1, 2][5])` in try/except IndexError and print "oops".
- Try `int("abc")` inside try/except ValueError.

## Key words

| Word | Meaning |
|---|---|
| exception | an error flag Python throws |
| raise | throw a flag yourself |
| try / except | risky code / the catcher |
| `as e` | names the caught exception object |
| else | runs only on success |
| finally | runs always, for cleanup |
| propagate | an uncaught flag travels up to the caller |
""",
        },
        {
            "id": "ch10-quiz-1",
            "type": "quiz",
            "title": "Exception types",
            "question": "`int('3.5')` raises which exception?",
            "options": ["TypeError", "ValueError", "IndexError", "SyntaxError"],
            "answer": 1,
            "explanation": "The input IS a string (right type), but '3.5' isn't valid int content - ValueError. TypeError would be for `int([1])` - a type that can't be a number at all.",
        },
        {
            "id": "ch10-quiz-2",
            "type": "quiz",
            "title": "finally",
            "question": "When does a `finally:` block run?",
            "options": ["Only when an exception occurs", "Only without exceptions", "Always", "Only after else:"],
            "answer": 2,
            "explanation": "finally runs no matter what - exception or clean path. That's why it's the home of close() and cleanup.",
        },
        {
            "id": "ch10-quiz-3",
            "type": "quiz",
            "title": "except order",
            "question": "`try` may raise KeyError; branches are `except Exception` then `except KeyError`. What happens?",
            "options": ["KeyError branch runs", "Exception branch runs", "SyntaxError: invalid order", "Both run"],
            "answer": 1,
            "explanation": "The first matching except wins - and Exception is the parent of almost every error, so it grabs the KeyError and the KeyError branch never runs. Always put specific types first.",
        },
        {
            "id": "ch10-quiz-4",
            "type": "quiz",
            "title": "else",
            "question": "When does the `else:` block after a try run?",
            "options": ["Always", "Only when no exception occurred", "Only on errors", "Never"],
            "answer": 1,
            "explanation": "else = 'try succeeded'. It's the opposite of what many guess - finally is the 'always' one.",
        },
        {
            "id": "ch10-warm-1",
            "type": "task",
            "title": "Catch the bad number",
            "difficulty": 1,
            "plain": "Ask for a number, say 'oops' if the user types letters.",
            "instructions": r"""
Read one input line. If it's a valid integer, print `double: N*2`.
If not, print `oops`.

Example: input `abc` -> `oops`; input `21` -> `double: 42`.
""",
            "starter": """# TODO: try int(input()), print "double: ..." or "oops"
""",
            "hints": [
                "`int('abc')` raises ValueError - that's the one to catch.",
                "Structure: `try: n = int(input()) ... except ValueError: print('oops')`.",
                "Print `f'double: {n * 2}'` inside the try or an else.",
            ],
            "solution": """try:
    n = int(input())
    print(f"double: {n * 2}")
except ValueError:
    print("oops")
""",
            "explanation": "The try block attempts the conversion and the doubling; typing letters throws ValueError and lands in except, which prints 'oops'. Clean input never touches the except branch.\n\nWhat you learned: try/except turns a crash into a friendly message.",
            "tests": [
                {"kind": "program", "stdin": "21\n", "expected": "double: 42", "match": "lines"},
                {"kind": "program", "stdin": "abc\n", "expected": "oops", "match": "lines"},
            ],
        },
        {
            "id": "ch10-warm-2",
            "type": "task",
            "title": "Safe division",
            "difficulty": 1,
            "plain": "Divide two typed-in numbers - survive a zero.",
            "instructions": r"""
Read two integers `a` and `b` from input. Print `a / b`. If `b` is 0,
print `can't divide by zero` instead of crashing.

Examples:

```
input: 10, 2 -> 5.0
input: 1, 0  -> can't divide by zero
```
""",
            "starter": """# TODO: read a and b, print a/b or the zero message
""",
            "hints": [
                "Dividing by 0 raises `ZeroDivisionError`.",
                "`try:` around the division, `except ZeroDivisionError:` for the message.",
                "Read both inputs first, then try the division.",
            ],
            "solution": """a = int(input())
b = int(input())
try:
    print(a / b)
except ZeroDivisionError:
    print("can't divide by zero")
""",
            "explanation": "The division sits inside try - b=0 triggers ZeroDivisionError and the except prints the friendly line. Valid inputs print the float result directly.\n\nWhat you learned: wrap only the risky line, not the whole program.",
            "tests": [
                {"kind": "program", "stdin": "10\n2\n", "expected": "10\n2\n5.0", "match": "exact"},
                {"kind": "program", "stdin": "1\n0\n", "expected": "can't divide by zero", "match": "lines"},
            ],
        },
        {
            "id": "ch10-task-1",
            "type": "task",
            "title": "Robust number input",
            "difficulty": 1,
            "plain": "Collect 10 good numbers from a clumsy user.",
            "instructions": r"""
The program must collect **10 valid integers** from input - the user
may type nonsense, so keep asking until 10 valid numbers were entered.

- For each invalid input print `invalid input`.
- Write every valid number on its own line into `numbers.txt`
  (mode `w`).
- At the end print `10 numbers written.`
""",
            "starter": """# TODO: open numbers.txt for writing, read until 10 valid ints,
#       print "invalid input" for bad entries, close the file
""",
            "hints": [
                "`while i < 10:` with inner `try: int(input())` / `except ValueError: print('invalid input')`.",
                "Only increment i (and write the line) after a successful conversion.",
                "`with open(...)` or try/finally makes sure the file closes.",
            ],
            "solution": """try:
    file = open("numbers.txt", mode="w")
    i = 0
    while i < 10:
        try:
            number = int(input("Number: "))
            file.write(str(number) + "\\n")
            i += 1
        except ValueError:
            print("invalid input")
except PermissionError as pe:
    print(pe)
finally:
    file.close()
print("10 numbers written.")
""",
            "explanation": "The outer try/finally guarantees `close()` runs even if something explodes. Inside, the while loop only counts successful conversions - a ValueError prints 'invalid input' and loops again without incrementing. That way exactly 10 valid numbers land in the file no matter how clumsy the typing.\n\nWhat you learned: an inner try inside a counting loop skips bad input gracefully.",
            "tests": [
                {"kind": "program",
                 "stdin": "1\ntwo\n2\n3\n4\n5\n6\n7\n8\n9\n10\n",
                 "expected": "invalid input\n10 numbers written.",
                 "match": "lines"},
                {"kind": "program",
                 "stdin": "0\n-5\nabc\n42\n7\nx\n8\n9\n10\n11\n12\n13\n",
                 "expected": "invalid input\ninvalid input\n10 numbers written.",
                 "match": "lines"},
            ],
        },
        {
            "id": "ch10-task-2",
            "type": "task",
            "title": "reverse_string with TypeError",
            "difficulty": 1,
            "plain": "Reverse a string - but complain politely if it isn't a string.",
            "instructions": r"""
Implement `reverse_string(s)` returning `s` reversed. If `s` isn't a
string (e.g. `None`), raise `TypeError` with message `"invalid text"`.

```python
reverse_string("turn me around")   # 'dnuora em nrut'
reverse_string(None)               # TypeError: invalid text
```
""",
            "starter": """def reverse_string(s):
    # TODO: return s reversed; raise TypeError('invalid text') for non-strings
    pass

try:
    print(reverse_string("turn me around"))
    print(reverse_string(None))
except TypeError as te:
    print("Error:", te)
""",
            "hints": [
                "`s[::-1]` on None already raises TypeError - catch it and raise your own with the message.",
                "Or `raise TypeError('invalid text')` when `not isinstance(s, str)`.",
                "`raise` creates the flag: `raise TypeError('invalid text')`.",
            ],
            "solution": """def reverse_string(s):
    try:
        return s[::-1]
    except TypeError:
        raise TypeError("invalid text")

try:
    print(reverse_string("turn me around"))
    print(reverse_string(None))
except TypeError as te:
    print("Error:", te)
""",
            "explanation": "Slicing None raises TypeError - the except catches it and re-raises a *new* TypeError carrying a clearer message. Callers see one clean error instead of a cryptic slicing complaint.\n\nWhat you learned: raising your own exception with a clear message makes errors readable.",
            "tests": [
                {"kind": "expr", "expr": "reverse_string('turn me around')",
                 "expected": "'dnuora em nrut'"},
                {"kind": "assert",
                 "code": "try:\n    reverse_string(None)\n    assert False\nexcept TypeError as e:\n    assert str(e) == 'invalid text'",
                 "desc": "reverse_string(None) raises TypeError('invalid text')"},
                {"kind": "program",
                 "expected": "dnuora em nrut\nError: invalid text",
                 "match": "exact"},
            ],
        },
        {
            "id": "ch10-task-3",
            "type": "task",
            "title": "list_output with propagation",
            "difficulty": 2,
            "plain": "Write numbers to a file - and pass any error up to the caller.",
            "instructions": r"""
Complete `list_output(filename="test.txt", max_value=10)` so it writes
the numbers `0` ... `max_value - 1`, one per line, into `filename`.

Any exception inside the function must be **propagated** to the
caller: catch it, then re-raise with a bare `raise` (real code would
log or clean up there).
""",
            "starter": """def list_output(filename="test.txt", max_value=10):
    # TODO: write 0..max_value-1 into the file; re-raise errors
    pass

try:
    list_output()
except Exception as e:
    print(e)
""",
            "hints": [
                "Wrap the file block in `try: ... except: raise`.",
                "`open(filename, 'w')`, loop `range(max_value)`, `file.write(str(i) + '\\n')`, close.",
                "A bare `raise` inside `except` re-throws the current exception unchanged.",
            ],
            "solution": """def list_output(filename="test.txt", max_value=10):
    try:
        file = open(filename, mode="w")
        for i in range(max_value):
            file.write(str(i) + "\\n")
        file.close()
    except:
        raise

try:
    list_output()
except Exception as e:
    print(e)
""",
            "explanation": "The function does its file work inside try; the bare `except:` catches anything and bare `raise` throws the same flag upward - the caller's `except Exception` is what finally deals with it. The except block is where logging or cleanup would live.\n\nWhat you learned: catch-raise lets a function notice errors without hiding them.",
            "tests": [
                {"kind": "assert",
                 "code": "list_output('test.txt', 10)\nwith open('test.txt') as f:\n    assert f.read().split() == [str(i) for i in range(10)]",
                 "desc": "test.txt contains 0..9"},
                {"kind": "assert",
                 "code": "list_output('short.txt', 3)\nwith open('short.txt') as f:\n    assert f.read().split() == ['0', '1', '2']",
                 "desc": "max_value=3 writes 0..2"},
            ],
        },
        {
            "id": "ch10-task-4",
            "type": "task",
            "title": "Differentiated error handling",
            "difficulty": 2,
            "plain": "Same program, different troubles - print each error's type and message.",
            "instructions": r"""
The program opens `number.txt` in exclusive mode (`'x'` - fails if it
already exists), reads one integer `z`, computes `1 / z` and writes
`z` to the file.

Catch the possible errors **as differentiated as possible** - for each
type print two lines, the exception class and its message:

```
<class 'ZeroDivisionError'>
division by zero
```

Handle at least `ZeroDivisionError`, `TypeError`, `FileExistsError`,
`ValueError`. The test feeds `0` (zero division) and `abc`
(ValueError).
""",
            "starter": """# TODO: wrap the block below in try/except branches printing
#       type(e) and e for each distinct exception type
try:
    file = open("number.txt", mode="x")
    z = int(input("Number: "))
    kw = 1 / z
    file.write(str(z))
    file.close()
    print("reciprocal:", kw)
except Exception:
    pass    # TODO: replace this catch-all with one except branch per
            # error type, each printing type(e) and e
""",
            "hints": [
                "One branch per type: `except ZeroDivisionError as e: print(type(e)); print(e)`.",
                "`int(input())` raises ValueError on letters; `1/z` raises ZeroDivisionError on 0.",
                "Four except branches in any order - they're all siblings.",
            ],
            "solution": """try:
    file = open("number.txt", mode="x")
    z = int(input("Number: "))
    kw = 1 / z
    file.write(str(z))
    file.close()
    print("reciprocal:", kw)
except ZeroDivisionError as e:
    print(type(e))
    print(e)
except TypeError as e:
    print(type(e))
    print(e)
except FileExistsError as e:
    print(type(e))
    print(e)
except ValueError as e:
    print(type(e))
    print(e)
""",
            "explanation": "Each `except X as e` names one trouble type; `e` is the exception object - `type(e)` prints its class, `print(e)` its message. `mode='x'` fails when the file exists (FileExistsError), `int` fails on letters, `1/0` divides by zero - four distinct nets for four distinct falls.\n\nWhat you learned: `as e` captures the error so you can inspect it.",
            "tests": [
                {"kind": "program", "stdin": "0\n",
                 "expected": "<class 'ZeroDivisionError'>\ndivision by zero",
                 "match": "lines"},
                {"kind": "program", "stdin": "abc\n",
                 "expected": "<class 'ValueError'>",
                 "match": "lines"},
                {"kind": "program", "stdin": "4\n",
                 "expected": "reciprocal: 0.25", "match": "lines"},
            ],
        },
        {
            "id": "ch10-boss",
            "type": "task",
            "title": "Vending machine that never crashes",
            "difficulty": 3,
            "boss": True,
            "plain": "A vending machine that survives every silly input.",
            "instructions": r"""
**BOSS MISSION - build an uncrashable vending machine.**

Prices (cents): `{"cola": 120, "chips": 150, "water": 100}`.

Read two inputs: product name, then the payment in cents. Output
exactly:

- product not in the dict -> `unknown product`
- payment not a number -> `not a number` (catch `ValueError`!)
- payment < price -> `missing <X> cents` (X = shortfall)
- otherwise -> `sold: <name>, change: <X> cents`

Examples:

```
input: cola / 200 -> sold: cola, change: 80 cents
input: chips / 50 -> missing 100 cents
```

The program must never crash - whatever the input.
""",
            "starter": """prices = {"cola": 120, "chips": 150, "water": 100}

# TODO: read product + cents, answer per the rules above
""",
            "example": """Guarded price parsing:

```python
raw = "1.50"
try:
    cents = int(float(raw) * 100)
except ValueError:
    print("bad input")
else:
    print(cents, "cents")
```
""",

            "hints": [
                "Check `name in prices` before anything else - a dict lookup with a bad key would raise KeyError.",
                "Wrap `int(input())` in try/except ValueError for 'not a number'.",
                "Shortfall is `price - cents`; change is `cents - price`.",
            ],
            "solution": """prices = {"cola": 120, "chips": 150, "water": 100}

name = input()
if name not in prices:
    print("unknown product")
else:
    try:
        cents = int(input())
    except ValueError:
        print("not a number")
    else:
        price = prices[name]
        if cents < price:
            print(f"missing {price - cents} cents")
        else:
            print(f"sold: {name}, change: {cents - price} cents")
""",
            "explanation": "Three safety nets in a row: the `in` check guards the dict lookup, try/except ValueError guards the int conversion, and the if splits 'too little' from 'sold'. The `else` after try runs only when the conversion worked - perfect place for the money math.\n\nWhat you learned: layer checks from 'can't proceed' to 'compute the answer'.",
            "tests": [
                {"kind": "program", "stdin": "cola\n200\n",
                 "expected": "cola\n200\nsold: cola, change: 80 cents", "match": "exact"},
                {"kind": "program", "stdin": "chips\n50\n",
                 "expected": "chips\n50\nmissing 100 cents", "match": "exact"},
                {"kind": "program", "stdin": "choc\n100\n",
                 "expected": "choc\nunknown product", "match": "exact"},
                {"kind": "program", "stdin": "water\nabc\n",
                 "expected": "water\nabc\nnot a number", "match": "exact"},
                {"kind": "program", "stdin": "water\n100\n",
                 "expected": "water\n100\nsold: water, change: 0 cents", "match": "exact"},
            ],
        },
    ],
}
