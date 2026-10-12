"""Kapitel 15 - Exceptions, Deep Dive."""

CHAPTER = {
    "id": "ch15",
    "number": 15,
    "title": "Exceptions: Deep Dive",
    "summary": "Building your own error types, exception objects with luggage, and re-raising.",
    "items": [
        {
            "id": "ch15-lesson",
            "type": "lesson",
            "title": "Errors as objects with luggage",
            "body": r"""
You already know `try`/`except` - now for the deeper trick: a raised
error is an **object**, a real thing you can catch, read, and even
build yourself. Named error types let a program say *which* thing went
wrong, not just *something* went wrong.

## An exception is an object with luggage

Catch it with `as` to look inside - `args` is a tuple holding the
arguments the error was created with:

```python
try:
    raise Exception("my exception")
except Exception as e:
    print(e, e.args)          # my exception ('my exception',)

try:
    raise Exception("my", "exception")
except Exception as e:
    print(e.args)             # ('my', 'exception')
```

> **What happens here**
>
> - line 2: `raise` throws an Exception object carrying one argument
> - line 3: `as e` names the caught parcel so we can open it
> - line 4: printing `e` shows the message; `e.args` is the tuple of
>   all arguments - `('my exception',)`
> - line 9: two arguments land in args as `('my', 'exception')`

> **Think of it like...** an exception is a thrown parcel - `as e` lets
> you open it and read the note inside.

## Your own error types

`class PizzaError(Exception)` creates a named error kind - your own
flag in the zoo. Store extra facts on it; hand the message upward with
`super().__init__()`:

```python
class PizzaError(Exception):
    def __init__(self, pizza, message):
        super().__init__(message)
        self.pizza = pizza

class TooMuchCheeseError(PizzaError):
    def __init__(self, pizza, cheese, message):
        super().__init__(pizza, message)
        self.cheese = cheese

def make_pizza(pizza, cheese):
    if pizza not in ['margherita', 'capricciosa', 'calzone']:
        raise PizzaError(pizza, "no such pizza on the menu")
    if cheese > 100:
        raise TooMuchCheeseError(pizza, cheese, "too much cheese")
    print("Pizza ready!")

for pz, ch in [('calzone', 0), ('margherita', 110), ('mafia', 20)]:
    try:
        make_pizza(pz, ch)
    except TooMuchCheeseError as tmce:
        print(tmce, ':', tmce.cheese)
    except PizzaError as pe:
        print(pe, ':', pe.pizza)
```

> **What happens here**
>
> - line 1: PizzaError **inherits** from Exception - a child that gets
>   everything Exception has
> - line 3: `super().__init__(message)` stores the message the normal
>   Exception way; line 4 keeps `pizza` as extra luggage
> - line 6: TooMuchCheeseError is a PizzaError child - an even more
>   specific flag - and adds a `cheese` field
> - line 13/15: make_pizza raises the matching error for each problem
> - line 21: the specific cheese error is caught first, line 23: the
>   general PizzaError catches the rest

> **Watch out** - branch order matters! `except TooMuchCheeseError`
> must come **before** `except PizzaError`, because the parent branch
> matches its children too and the first match wins.

## Try it yourself

- Catch only `PizzaError` - does it still catch the cheese error?
- Add a third pizza rule: `size > 40` -> a `TooBigError`.

## Key words

| Word | Meaning |
|---|---|
| exception object | a thrown error you can catch and inspect |
| args | tuple of the exception's constructor arguments |
| `as e` | names the caught object |
| custom exception | your own `class X(Exception)` |
| exception hierarchy | error family - parent + specific children |
""",
        },
        {
            "id": "ch15-lesson-2",
            "type": "lesson",
            "title": "Riding along, re-raising, else/finally",
            "body": r"""
Your custom errors don't have to start from `Exception` - they can
inherit from a built-in error and ride along with the handlers other
code already has. Plus: two finishing moves, `else`/`finally`, and
re-throwing.

## Piggyback on a built-in error

Subclass `ZeroDivisionError` and your error IS one - anything catching
the parent catches yours:

```python
class MyZeroDivisionError(ZeroDivisionError):
    pass

for mode in [False, True]:
    try:
        if mode:
            raise MyZeroDivisionError("worse news")
        raise ZeroDivisionError("bad news")
    except MyZeroDivisionError:
        print('My division by zero')
    except ZeroDivisionError:
        print('Original division by zero')
```

> **What happens here**
>
> - line 1: the child inherits - a MyZeroDivisionError IS a
>   ZeroDivisionError
> - line 6-8: mode False throws the plain parent error; mode True
>   throws the child
> - line 9: the specific child branch is listed first - and it must
>   be, or the parent branch would grab it first

> **Think of it like...** an error family tree: catching the parent type
> is like saying "anyone from this family" - children count as members.

## else, finally, and re-raise

```python
try:
    value = int("42")
except ValueError:
    print("not a number")
else:
    print("parsed:", value)    # runs only if NO exception
finally:
    print("always runs")       # cleanup, error or not
```

> **What happens here**
>
> - line 2: `int("42")` succeeds - no flag thrown
> - line 3-4: the except branch is skipped this time
> - line 5-6: `else` runs because the try succeeded
> - line 7-8: `finally` runs no matter which way it went - the cleanup
>   crew

And a bare `raise` inside an except block throws the **same** error
onward - useful for logging a problem and then letting the caller deal
with it (**propagation**).

> **Watch out** - `raise ValueError(...)` creates a NEW error; bare
> `raise` re-throws the current one. They look similar, act different.

## Try it yourself

- Replace `"42"` with `"abc"` - which branches run now?
- Add a bare `raise` inside the except and watch it escape.

## Key words

| Word | Meaning |
|---|---|
| else | runs only when the try succeeded |
| finally | runs no matter what - for cleanup |
| re-raise | bare `raise` throws the same error onward |
| propagation | an uncaught error travels up to the caller |
| inheriting a built-in | your error counts as that error type |
""",
        },
        {
            "id": "ch15-quiz-1",
            "type": "quiz",
            "title": "Exception args",
            "question": "`raise Exception('a', 'b')` caught as `e` - what is `e.args`?",
            "options": ["'a'", "('a', 'b')", "'a b'", "['a', 'b']"],
            "answer": 1,
            "explanation": "args is a TUPLE holding every constructor argument - ('a', 'b'), not joined into a string.",
        },
        {
            "id": "ch15-quiz-2",
            "type": "quiz",
            "title": "Hierarchy",
            "question": "`class E1(Exception)`, `class E2(E1)`. Raising E2 - which branch catches it?",
            "options": ["except E1", "except E2", "whichever comes first", "except Exception only"],
            "answer": 2,
            "explanation": "E2 matches BOTH branches (it's an E1 too) - so the one written first wins. That's why children go first.",
        },
        {
            "id": "ch15-quiz-3",
            "type": "quiz",
            "title": "raise",
            "question": "A bare `raise` inside an `except` block...",
            "options": ["raises a new generic Exception", "re-raises the currently handled exception", "is a syntax error", "exits the program"],
            "answer": 1,
            "explanation": "No argument means 'throw the same parcel again' - handy for logging then letting the caller handle it.",
        },
        {
            "id": "ch15-quiz-4",
            "type": "quiz",
            "title": "finally",
            "question": "When does a `finally` block run?",
            "options": ["only on success", "only on error", "always", "never"],
            "answer": 2,
            "explanation": "finally is the cleanup crew - it runs on success, on error, even when the except re-raises.",
        },
        {
            "id": "ch15-warm-1",
            "type": "task",
            "title": "Your first error type",
            "difficulty": 1,
            "plain": "Invent an error called TooHotError and raise it.",
            "instructions": r"""
Define `TooHotError(Exception)` - an empty subclass is fine - then
raise it inside the `try` and catch it, printing `"cooled down"`.

Expected output: `cooled down`
""",
            "starter": """# TODO: class TooHotError(Exception)

try:
    # TODO: raise TooHotError
    pass
except TooHotError:
    print("cooled down")
""",
            "hints": [
                "`class TooHotError(Exception): pass`.",
                "Throw it with `raise TooHotError` (or `TooHotError('hot')`).",
                "The except already prints - just trigger it.",
            ],
            "solution": """class TooHotError(Exception):
    pass

try:
    raise TooHotError("overheated")
except TooHotError:
    print("cooled down")""",
            "explanation": "An empty subclass already is a fully working error type - it inherits everything from Exception. `raise` throws it, the matching `except` catches it, and the program prints instead of crashing.\n\nWhat you learned: your own exception = `class X(Exception)`.",
            "tests": [
                {"kind": "program", "expected": "cooled down", "match": "exact"},
            ],
        },
        {
            "id": "ch15-warm-2",
            "type": "task",
            "title": "Read the parcel",
            "difficulty": 1,
            "plain": "Catch an exception and print what it carried.",
            "instructions": r"""
Raise `ValueError("bad input")` inside the `try`, catch it as `e`,
and print `e.args[0]`.

Expected output: `bad input`
""",
            "starter": """try:
    # TODO: raise ValueError("bad input")
    pass
except ValueError as e:
    # TODO: print the first constructor argument
    pass
""",
            "hints": [
                "`raise ValueError('bad input')`.",
                "`e.args` is a tuple - index 0 is the message.",
                "`print(e.args[0])` (printing `e` itself also shows it).",
            ],
            "solution": """try:
    raise ValueError("bad input")
except ValueError as e:
    print(e.args[0])""",
            "explanation": "The exception object keeps every argument you handed its constructor in `args` - `args[0]` is the message string. `as e` gives you the caught parcel to inspect.\n\nWhat you learned: exceptions carry data you can read back.",
            "tests": [
                {"kind": "program", "expected": "bad input", "match": "exact"},
            ],
        },
        {
            "id": "ch15-task-1",
            "type": "task",
            "title": "SalaryNotInRangeError",
            "difficulty": 1,
            "plain": "A custom error that complains about a salary outside the band.",
            "instructions": r"""
Define `SalaryNotInRangeError(Exception)`:

- `__init__(self, salary, message="Salary is not in (5000, 15000) range")`
  - stores `salary`, passes `message` to the superclass
- `__str__` -> `'<salary> -> <message>'`

Then `check_salary(salary)` raising it unless `5000 < salary < 15000`.

```python
check_salary(3000)
# SalaryNotInRangeError: 3000 -> Salary is not in (5000, 15000) range
```
""",
            "starter": """class SalaryNotInRangeError(Exception):
    # TODO: __init__(salary, message=...) and __str__
    pass


def check_salary(salary):
    # TODO: raise unless 5000 < salary < 15000
    pass
""",
            "hints": [
                "`super().__init__(message)` hands the text to Exception.",
                "`__str__`: `return f'{self.salary} -> {self.args[0]}'`.",
                "`if not 5000 < salary < 15000: raise SalaryNotInRangeError(salary)`.",
            ],
            "solution": """class SalaryNotInRangeError(Exception):
    def __init__(self, salary, message="Salary is not in (5000, 15000) range"):
        self.salary = salary
        super().__init__(message)

    def __str__(self):
        return f'{self.salary} -> {self.args[0]}'


def check_salary(salary):
    if not 5000 < salary < 15000:
        raise SalaryNotInRangeError(salary)
""",
            "explanation": "The class stores `salary` as luggage and forwards the message to Exception, which puts it in `args[0]` - so `__str__` reads it back from there. `check_salary` guards with one combined comparison and raises early.\n\nWhat you learned: custom errors carry their own fields alongside the message.",
            "tests": [
                {"kind": "assert",
                 "code": "try:\n    check_salary(3000)\n    assert False\nexcept SalaryNotInRangeError as e:\n    assert str(e) == '3000 -> Salary is not in (5000, 15000) range'\n    assert e.salary == 3000",
                 "desc": "3000 raises with formatted message"},
                {"kind": "assert", "code": "check_salary(10000)",
                 "desc": "10000 is accepted"},
                {"kind": "assert",
                 "code": "try:\n    check_salary(15000)\n    assert False\nexcept SalaryNotInRangeError:\n    pass",
                 "desc": "15000 (boundary) raises"},
            ],
        },
        {
            "id": "ch15-task-2",
            "type": "task",
            "title": "Validating Shirt constructor",
            "difficulty": 1,
            "plain": "A shirt that refuses nonsense colors and patterns.",
            "instructions": r"""
`Shirt(color, pattern)` must validate before storing:

- colors: `'BLUE'`, `'RED'`, `'GREEN'` - else
  `ValueError('Invalid color: <color>')`
- patterns: `'PLAIN'`, `'CHECKED'`, `'STRIPED'` - else
  `ValueError('Invalid pattern: <pattern>')`

`__str__` -> `'Shirt color: <color> pattern: <pattern>'` (already
given via `self.__class__.__name__`).
""",
            "starter": """class Shirt:
    def __init__(self, color, pattern):
        # TODO: validate, then store
        self.color = color
        self.pattern = pattern

    def __str__(self):
        return self.__class__.__name__ + " color: " + self.color + " pattern: " + self.pattern

try:
    shirt = Shirt("RED", "CHECKED")
    print(shirt)
except ValueError as ve:
    print(ve)
""",
            "hints": [
                "`if color not in ['BLUE', 'RED', 'GREEN']: raise ValueError(...)`.",
                "Check color first, then pattern, THEN assign.",
                "The raise must happen before `self.color = ...`.",
            ],
            "solution": """class Shirt:
    def __init__(self, color, pattern):
        if color not in ["BLUE", "RED", "GREEN"]:
            raise ValueError("Invalid color: " + color)
        if pattern not in ["PLAIN", "CHECKED", "STRIPED"]:
            raise ValueError("Invalid pattern: " + pattern)
        self.color = color
        self.pattern = pattern

    def __str__(self):
        return self.__class__.__name__ + " color: " + self.color + " pattern: " + self.pattern

try:
    shirt = Shirt("RED", "CHECKED")
    print(shirt)
except ValueError as ve:
    print(ve)
""",
            "explanation": "Two guard clauses run before any assignment - an invalid Shirt can never be half-built. `self.__class__.__name__` in `__str__` reads the class name automatically ('Shirt'), so subclasses print their own name for free.\n\nWhat you learned: validate inputs before touching attributes.",
            "tests": [
                {"kind": "expr", "expr": "str(Shirt('RED', 'CHECKED'))",
                 "expected": "'Shirt color: RED pattern: CHECKED'"},
                {"kind": "assert",
                 "code": "try:\n    Shirt('YELLOW', 'PLAIN')\n    assert False\nexcept ValueError as e:\n    assert str(e) == 'Invalid color: YELLOW'",
                 "desc": "invalid color raises ValueError"},
                {"kind": "assert",
                 "code": "try:\n    Shirt('RED', 'DOTTED')\n    assert False\nexcept ValueError as e:\n    assert str(e) == 'Invalid pattern: DOTTED'",
                 "desc": "invalid pattern raises ValueError"},
            ],
        },
        {
            "id": "ch15-task-3",
            "type": "task",
            "title": "Friends manager with custom exceptions",
            "difficulty": 2,
            "plain": "A friend list that raises its own named errors when rules break.",
            "instructions": r"""
Three custom exceptions (each `Exception` subclass with a default
message):

- `ListFullException` - `'The list is full.'`
- `EmptyElementException` - `'The element does not exist in the list.'`
- `ListEmptyException` - `'The list contains no elements.'`

Then `FriendsManager(max_friends=3)` with list `self.friends`:

- `add_friend(name)` - `ListFullException` when full, else append
- `clean_list()` - `ListEmptyException` when already empty, else clear
- `get_friend(index)` - `EmptyElementException` for a bad index, else
  the entry
""",
            "starter": """class ListFullException(Exception):
    # TODO: default message 'The list is full.'
    pass

class EmptyElementException(Exception):
    # TODO: default message 'The element does not exist in the list.'
    pass

class ListEmptyException(Exception):
    # TODO: default message 'The list contains no elements.'
    pass


class FriendsManager:
    def __init__(self, max_friends=3):
        self.friends = []
        self.max_friends = max_friends

    def add_friend(self, name):
        # TODO
        pass

    def clean_list(self):
        # TODO
        pass

    def get_friend(self, index):
        # TODO
        pass
""",
            "hints": [
                "Each class: `def __init__(self, message='...'): super().__init__(message)`.",
                "add_friend guard: `len(self.friends) >= self.max_friends`.",
                "Bad index: `index < 0 or index >= len(self.friends)`.",
            ],
            "solution": """class ListFullException(Exception):
    def __init__(self, message='The list is full.'):
        super().__init__(message)

class EmptyElementException(Exception):
    def __init__(self, message='The element does not exist in the list.'):
        super().__init__(message)

class ListEmptyException(Exception):
    def __init__(self, message='The list contains no elements.'):
        super().__init__(message)


class FriendsManager:
    def __init__(self, max_friends=3):
        self.friends = []
        self.max_friends = max_friends

    def add_friend(self, name):
        if len(self.friends) >= self.max_friends:
            raise ListFullException
        self.friends.append(name)

    def clean_list(self):
        if len(self.friends) == 0:
            raise ListEmptyException
        self.friends = []

    def get_friend(self, index):
        if index < 0 or index >= len(self.friends):
            raise EmptyElementException
        return self.friends[index]
""",
            "explanation": "Each error class bakes its default message into `__init__`, so raising the bare class name (no parentheses needed!) still produces a readable message. The manager checks each rule first - full, empty, out-of-range - then acts.\n\nWhat you learned: default messages make `raise MyError` self-documenting.",
            "tests": [
                {"kind": "assert",
                 "code": "fv = FriendsManager()\nfor n in ['Michael', 'Andrea', 'Juergen']:\n    fv.add_friend(n)\nassert fv.get_friend(2) == 'Juergen'\ntry:\n    fv.add_friend('Wolfgang')\n    assert False\nexcept ListFullException as e:\n    assert str(e) == 'The list is full.'",
                 "desc": "4th friend raises ListFullException"},
                {"kind": "assert",
                 "code": "fv = FriendsManager()\ntry:\n    fv.clean_list()\n    assert False\nexcept ListEmptyException:\n    pass",
                 "desc": "clean_list on empty raises ListEmptyException"},
                {"kind": "assert",
                 "code": "fv = FriendsManager()\nfv.add_friend('A')\ntry:\n    fv.get_friend(5)\n    assert False\nexcept EmptyElementException:\n    pass",
                 "desc": "get_friend(5) raises EmptyElementException"},
            ],
        },
        {
            "id": "ch15-task-4",
            "type": "task",
            "title": "Conveyor belt temperature check",
            "difficulty": 2,
            "plain": "A sensor that raises different errors for too-hot and too-cold.",
            "instructions": r"""
Build the error family and the checker:

- `TemperatureException(Exception)` - `__init__(self, msg)` passing
  `msg` up
- `TemperatureTooHighException(TemperatureException)` - default
  `'The temperature is too high'`
- `TemperatureTooLowException(TemperatureException)` - default
  `'The temperature is too low'`

`check_temperature(temperature)` with `MIN_TEMP = -15.0`,
`MAX_TEMP = -5.0`:

- below MIN -> `TemperatureTooLowException(f'The minimum temperature of {MIN_TEMP} was undershot.')`
- above MAX -> `TemperatureTooHighException(f'The maximum temperature of {MAX_TEMP} was exceeded.')`
""",
            "starter": """class TemperatureException(Exception):
    # TODO
    pass

class TemperatureTooHighException(TemperatureException):
    # TODO
    pass

class TemperatureTooLowException(TemperatureException):
    # TODO
    pass


MIN_TEMP = -15.0
MAX_TEMP = -5.0

def check_temperature(temperature):
    # TODO
    pass
""",
            "hints": [
                "Base: `def __init__(self, msg): super().__init__(msg)`; children only change the default text.",
                "check_temperature has two guards - low first, then high.",
                "The f-strings interpolate MIN_TEMP/MAX_TEMP into the message.",
            ],
            "solution": """class TemperatureException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class TemperatureTooHighException(TemperatureException):
    def __init__(self, msg="The temperature is too high"):
        super().__init__(msg)

class TemperatureTooLowException(TemperatureException):
    def __init__(self, msg="The temperature is too low"):
        super().__init__(msg)


MIN_TEMP = -15.0
MAX_TEMP = -5.0

def check_temperature(temperature):
    if temperature < MIN_TEMP:
        raise TemperatureTooLowException(
            f"The minimum temperature of {MIN_TEMP} was undershot.")
    if temperature > MAX_TEMP:
        raise TemperatureTooHighException(
            f"The maximum temperature of {MAX_TEMP} was exceeded.")
""",
            "explanation": "Both children inherit the pass-the-message-up machinery from TemperatureException and only swap the default text - one line of real difference each. Because they share the parent, a caller can catch `TemperatureException` and get BOTH kinds.\n\nWhat you learned: exception families let catchers choose how specific to be.",
            "tests": [
                {"kind": "assert",
                 "code": "try:\n    check_temperature(-20.0)\n    assert False\nexcept TemperatureTooLowException as e:\n    assert 'undershot' in str(e)",
                 "desc": "-20 raises TooLow"},
                {"kind": "assert",
                 "code": "try:\n    check_temperature(0.0)\n    assert False\nexcept TemperatureTooHighException as e:\n    assert 'exceeded' in str(e)",
                 "desc": "0 raises TooHigh"},
                {"kind": "assert", "code": "check_temperature(-10.0)",
                 "desc": "-10 passes"},
                {"kind": "assert",
                 "code": "try:\n    check_temperature(-30)\n    assert False\nexcept TemperatureException:\n    pass",
                 "desc": "base class catches subclass exceptions"},
            ],
        },
        {
            "id": "ch15-task-5",
            "type": "task",
            "title": "Pizza errors (exception hierarchy)",
            "difficulty": 2,
            "plain": "The pizza kitchen reports which rule a pizza broke.",
            "instructions": r"""
The pizza hierarchy from the lesson:

- `PizzaError(Exception)`: `__init__(self, pizza, message)` - message
  up, `pizza` stored
- `TooMuchCheeseError(PizzaError)`: `__init__(self, pizza, cheese,
  message)` - parent constructor, then store `cheese`

`make_pizza(pizza, cheese)`:

- unknown pizza -> `PizzaError(pizza, 'no such pizza on the menu')`
- `cheese > 100` -> `TooMuchCheeseError(pizza, cheese, 'too much cheese')`
- otherwise prints `'Pizza ready!'`
""",
            "starter": """class PizzaError(Exception):
    # TODO
    pass


class TooMuchCheeseError(PizzaError):
    # TODO
    pass


def make_pizza(pizza, cheese):
    # TODO
    pass
""",
            "hints": [
                "PizzaError: `super().__init__(message)` + `self.pizza = pizza`.",
                "TooMuchCheeseError: `super().__init__(pizza, message)` + `self.cheese`.",
                "Check the menu first, then the cheese limit.",
            ],
            "solution": """class PizzaError(Exception):
    def __init__(self, pizza, message):
        super().__init__(message)
        self.pizza = pizza


class TooMuchCheeseError(PizzaError):
    def __init__(self, pizza, cheese, message):
        super().__init__(pizza, message)
        self.cheese = cheese


def make_pizza(pizza, cheese):
    if pizza not in ['margherita', 'capricciosa', 'calzone']:
        raise PizzaError(pizza, "no such pizza on the menu")
    if cheese > 100:
        raise TooMuchCheeseError(pizza, cheese, "too much cheese")
    print("Pizza ready!")
""",
            "explanation": "TooMuchCheeseError inherits pizza-storing from PizzaError and adds a cheese field - the subclass enriches the parcel. In make_pizza the menu check runs before the cheese check, so 'mafia' pizzas fail on name even if the cheese is fine.\n\nWhat you learned: error subclasses can add fields while reusing the parent's storage.",
            "tests": [
                {"kind": "assert",
                 "code": "try:\n    make_pizza('mafia', 20)\n    assert False\nexcept TooMuchCheeseError:\n    assert False\nexcept PizzaError as pe:\n    assert pe.pizza == 'mafia'",
                 "desc": "mafia raises PizzaError with .pizza"},
                {"kind": "assert",
                 "code": "try:\n    make_pizza('margherita', 110)\n    assert False\nexcept TooMuchCheeseError as e:\n    assert e.cheese == 110 and e.pizza == 'margherita'",
                 "desc": "too much cheese raises TooMuchCheeseError"},
                {"kind": "stdout", "code": "make_pizza('calzone', 0)",
                 "expected": "Pizza ready!", "match": "exact"},
            ],
        },
        {
            "id": "ch15-boss",
            "type": "task",
            "title": "Rocket launch checklist",
            "difficulty": 3,
            "boss": True,
            "plain": "A launch computer that names the exact check that failed.",
            "instructions": r"""
**BOSS MISSION - mission control.**

Build this exception family (all messages via `super().__init__`):

- `LaunchError(Exception)` - base, takes `msg`
- `FuelError(LaunchError)` - default `"Fuel below 80 percent"`
- `WeatherError(LaunchError)` - default `"Weather is not clear"`
- `CrewError(LaunchError)` - default `"Fewer than 3 crew members"`

`check_launch(fuel, weather_ok, crew)` raises, **in this order**:

- `FuelError` when `fuel < 80`
- `WeatherError` when `weather_ok` is False
- `CrewError` when `crew < 3`
- otherwise returns `"Liftoff!"`

A caller catching only `LaunchError` must catch all three.
""",
            "starter": """class LaunchError(Exception):
    # TODO
    pass


class FuelError(LaunchError):
    # TODO
    pass


class WeatherError(LaunchError):
    # TODO
    pass


class CrewError(LaunchError):
    # TODO
    pass


def check_launch(fuel, weather_ok, crew):
    # TODO
    pass
""",
            "example": """Raising your own error type:

```python
class RecipeError(Exception):
    pass

try:
    raise RecipeError("burned the pasta")
except RecipeError as e:
    print("kitchen report:", e)
```
""",

            "hints": [
                "Same pattern as the temperature family: base takes msg, children set defaults.",
                "Three `if`s in order - fuel, weather, crew - each raising its type.",
                "Return 'Liftoff!' only after all guards pass.",
            ],
            "solution": """class LaunchError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class FuelError(LaunchError):
    def __init__(self, msg="Fuel below 80 percent"):
        super().__init__(msg)


class WeatherError(LaunchError):
    def __init__(self, msg="Weather is not clear"):
        super().__init__(msg)


class CrewError(LaunchError):
    def __init__(self, msg="Fewer than 3 crew members"):
        super().__init__(msg)


def check_launch(fuel, weather_ok, crew):
    if fuel < 80:
        raise FuelError()
    if not weather_ok:
        raise WeatherError()
    if crew < 3:
        raise CrewError()
    return "Liftoff!"
""",
            "explanation": "Four small classes form one family: LaunchError holds the message machinery, the three children just preset their texts. check_launch is a checklist in order - the first failed check aborts the launch with a precise error, and `except LaunchError` catches every child because they all ARE LaunchErrors.\n\nWhat you learned: an exception hierarchy gives you precise AND catch-all handling at once.",
            "tests": [
                {"kind": "expr", "expr": "check_launch(90, True, 4)", "expected": "'Liftoff!'"},
                {"kind": "assert",
                 "code": "try:\n    check_launch(50, True, 4)\n    assert False\nexcept FuelError:\n    pass",
                 "desc": "low fuel -> FuelError"},
                {"kind": "assert",
                 "code": "try:\n    check_launch(90, False, 4)\n    assert False\nexcept WeatherError:\n    pass\ntry:\n    check_launch(90, True, 2)\n    assert False\nexcept CrewError:\n    pass",
                 "desc": "weather and crew errors"},
                {"kind": "assert",
                 "code": "try:\n    check_launch(10, False, 0)\n    assert False\nexcept LaunchError as e:\n    assert isinstance(e, FuelError)",
                 "desc": "first failing check wins; base catches it"},
            ],
        },
    ],
}
