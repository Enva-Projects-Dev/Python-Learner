"""Kapitel 13 - OOP Vertiefung."""

CHAPTER = {
    "id": "ch13",
    "number": 13,
    "title": "OOP Deep Dive",
    "summary": "Shared chalkboards (class variables), helper methods without self, and peeking inside objects.",
    "items": [
        {
            "id": "ch13-lesson",
            "type": "lesson",
            "title": "Class variables and methods without self",
            "body": r"""
Objects each keep their own `self.` attributes - but sometimes all
objects of a kind should share ONE value: a counter, a setting, a list
of valid choices. A variable written in the class body (not inside a
method) is a **class variable** - one shared chalkboard every object
reads and writes.

> **Think of it like...** a chalkboard pinned next to the cookie cutter.
> Each cookie has its own sprinkles (`self.` attributes), but there's
> only ONE chalkboard - and every new cookie bumps the count on it.

```python
class Person:
    __counter = 0                       # shared by ALL objects
    def __init__(self, name):
        self.__name = name
        Person.__counter += 1
        self.__id = 1000 + Person.__counter
    def __str__(self):
        return f"Person Name: {self.__name} ID: {self.__id}"
    @staticmethod
    def count():
        return Person.__counter

print(Person.count())
maxi = Person("Max")
tom = Person("Tom")
print(maxi, maxi.count(), sep=" | ")
```

> **What happens here**
>
> - line 2: `__counter` lives on the class - created once, shared by
>   everyone
> - line 5: `Person.__counter += 1` bumps the chalkboard each time a
>   person is built
> - line 6: the id is `1000 + counter`, so the first person gets 1001
> - line 9: `@staticmethod` marks a method that needs **no self** -
>   you can call it on the class (`Person.count()`) or an object
> - line 13: the count is 0 before any Person exists

> **Watch out** - `self.__counter += 1` would look like it bumps the
> counter, but it secretly creates a *private copy* on that object!
> Always write `Person.__counter` (ClassName.attribute) for shared
> values.

## @classmethod - named recipes for building objects

A **class method** receives the class itself as `cls` - handy for
factory recipes like "make me a margherita":

```python
class Pizza:
    def __init__(self, ingredients):
        self.ingredients = ingredients
    def __str__(self):
        return f"Pizza with {self.ingredients}"
    @classmethod
    def margherita(cls):
        return cls(['mozzarella', 'tomatoes'])

print(Pizza.margherita())
```

> **What happens here**
>
> - line 6: `@classmethod` means the method gets `cls` - the class -
>   not an object
> - line 8: `cls(...)` calls the constructor, so `cls` in
>   `Pizza.margherita()` is `Pizza`
> - line 10: no pizza object needed - the class itself does the cooking

**Rule of thumb:** instance methods get `self`, class methods get
`cls`, static methods get neither.

A taste of what's coming: `class WeekDayError(Exception)` creates your
own error type - a full lesson on that waits in chapter 15.

## Try it yourself

- Add `@classmethod prosciutto` returning a pizza with ham.
- Build two Persons and print `Person.count()` before and after.

## Key words

| Word | Meaning |
|---|---|
| class variable | one value shared by all objects of a class |
| @staticmethod | a method needing no self - call it on the class |
| @classmethod | gets `cls` - a factory recipe |
| factory method | a named recipe that builds objects |
| self vs cls | "this object" vs "the class" |
""",
        },
        {
            "id": "ch13-lesson-2",
            "type": "lesson",
            "title": "Peeking inside: introspection",
            "body": r"""
Python objects can answer questions about themselves while the program
runs - "what attributes do you have?", "which class made you?". That
trick is called **introspection**: code looking at objects from the
inside.

> **Think of it like...** an x-ray for objects - you can peek at the
> insides without opening anything up.

```python
class Example:
    def __init__(self, val):
        if val % 2:
            self.a = 1
        else:
            self.b = 1

obj = Example(0)
print(hasattr(obj, 'a'), hasattr(obj, 'b'))   # False True
print(obj.__dict__)                            # {'b': 1}
```

> **What happens here**
>
> - line 8: `Example(0)` - 0 is even, so only `self.b` is created
> - line 9: `hasattr(obj, 'a')` asks "does this object have attribute
>   a?" - False, safely, no crash; `b` exists -> True
> - line 10: `__dict__` is the object's attribute drawer - literally
>   the dict holding all its attributes

Classes have their own mirrors: `__name__` (the class's name as a
string) and `__bases__` (its parent classes - only classes have
parents, objects don't):

```python
class Example:
    pass

print(Example.__name__)        # 'Example'
print(object.__bases__)        # ()
```

> **What happens here**
>
> - line 1: `__name__` is the class's own name as a string
> - line 2: `__bases__` is the tuple of parent classes - `object` is
>   the root of everything, so it has no parents -> `()`

> **Watch out** - `hasattr` is your safe 'does it exist?' test. Direct
> `obj.a` on a missing attribute crashes with AttributeError - this is
> exactly the difference between a polite knock and kicking the door.

Side note from the last lesson: `==` compares *contents*, `is` compares
*identity* - two different object questions:

```python
a = [1, 2]
b = [1, 2]
print(a == b, a is b)   # True False - equal lists, different objects
```

> **What happens here** - `a` and `b` hold the same values but are two
> separate list objects, so `==` says True while `is` says False.

## Try it yourself

- Print `Example(1).__dict__` - what changes with an odd number?
- Check `hasattr(obj, '__class__')` - does the object know its class?

## Key words

| Word | Meaning |
|---|---|
| introspection | code inspecting objects while running |
| `__dict__` | an object's attribute drawer |
| `__name__` | a class's own name |
| `__bases__` | a class's parent classes (classes only!) |
| hasattr | safe 'does this attribute exist?' check |
| `is` vs `==` | same object vs same contents |
""",
        },
        {
            "id": "ch13-quiz-1",
            "type": "quiz",
            "title": "Class variable",
            "question": "A class variable `x` is incremented in `__init__`. Two objects are created. What are `a.x` and `b.x`?",
            "options": ["both 1", "both 2", "1 and 2", "independent values"],
            "answer": 1,
            "explanation": "It's ONE shared counter - two constructions pushed it to 2, and both objects read the same chalkboard.",
        },
        {
            "id": "ch13-quiz-2",
            "type": "quiz",
            "title": "@classmethod",
            "question": "What does a `@classmethod` get as its first parameter?",
            "options": ["self - the instance", "cls - the class", "nothing", "the module"],
            "answer": 1,
            "explanation": "cls is the class itself - that's why `cls(...)` inside it builds a new object (a factory).",
        },
        {
            "id": "ch13-quiz-3",
            "type": "quiz",
            "title": "Introspection",
            "question": "Which attribute exists only on classes, not on objects?",
            "options": ["__dict__", "__name__", "__bases__", "__module__"],
            "answer": 2,
            "explanation": "__bases__ lists a class's parent classes - an object isn't a blueprint, so it has no parents to list.",
        },
        {
            "id": "ch13-quiz-4",
            "type": "quiz",
            "title": "@staticmethod",
            "question": "Can `Robot.count()` (a @staticmethod) be called on the class without an object?",
            "options": ["No - needs an instance", "Yes - it needs no self", "Only inside __init__", "Only once"],
            "answer": 1,
            "explanation": "Static methods take no self, so the class itself can call them - like a tool hanging on the blueprint's wall.",
        },
        {
            "id": "ch13-warm-1",
            "type": "task",
            "title": "Shared counter",
            "difficulty": 1,
            "plain": "One class variable counts how many objects were built.",
            "instructions": r"""
The class `Balloon` has a class variable `count`. Make `__init__`
increment it, then print `Balloon.count` after building two balloons.

Expected output: `2`
""",
            "starter": """class Balloon:
    count = 0
    def __init__(self, color):
        self.color = color
        # TODO: bump the shared counter

Balloon("red")
Balloon("blue")
# TODO: print Balloon.count
""",
            "hints": [
                "Inside __init__ the class name is `Balloon` - `Balloon.count += 1`.",
                "The counter lives on the class, not self.",
                "Print `Balloon.count` at the end.",
            ],
            "solution": """class Balloon:
    count = 0
    def __init__(self, color):
        self.color = color
        Balloon.count += 1

Balloon("red")
Balloon("blue")
print(Balloon.count)""",
            "explanation": "`count` sits on the class - `Balloon.count += 1` bumps the shared chalkboard every time a balloon is built, while `self.color` stays per-balloon. Two constructions -> 2.\n\nWhat you learned: `Class.var` is shared; `self.var` is personal.",
            "tests": [
                {"kind": "program", "expected": "2", "match": "exact"},
            ],
        },
        {
            "id": "ch13-warm-2",
            "type": "task",
            "title": "A static greeter",
            "difficulty": 1,
            "plain": "A method on the class that needs no object at all.",
            "instructions": r"""
Add a `@staticmethod` `motto()` to `Robot` returning
`"Beep boop!"`, then print `Robot.motto()`.

Expected output: `Beep boop!`
""",
            "starter": """class Robot:
    # TODO: @staticmethod def motto()
    pass

print(Robot.motto())
""",
            "hints": [
                "`@staticmethod` on the line above `def motto():`.",
                "No `self` parameter - it takes nothing.",
                "`return \"Beep boop!\"`.",
            ],
            "solution": """class Robot:
    @staticmethod
    def motto():
        return "Beep boop!"

print(Robot.motto())""",
            "explanation": "The @staticmethod marker tells Python 'no self needed' - so `Robot.motto()` works without ever building a robot. It lives in the class for organisation, like a note pinned to the blueprint.\n\nWhat you learned: @staticmethod = a class-owned function.",
            "tests": [
                {"kind": "program", "expected": "Beep boop!", "match": "exact"},
            ],
        },
        {
            "id": "ch13-task-1",
            "type": "task",
            "title": "The Timer class",
            "difficulty": 2,
            "plain": "A digital clock object that ticks forward and backward.",
            "instructions": r"""
Write `Timer` counting seconds with military time:

- `Timer(hours=0, minutes=0, seconds=0)` - all private, no validation
- `__str__` -> `"hh:mm:ss"` with leading zeros
- `next_second()` / `prev_second()` shift the time by one second,
  wrapping at 24:00:00 / 00:00:00

```python
timer = Timer(23, 59, 59)
timer.next_second(); print(timer)   # 00:00:00
timer.prev_second(); print(timer)   # 23:59:59
```
""",
            "starter": """class Timer:
    def __init__(self, hours=0, minutes=0, seconds=0):
        # TODO
        pass

    def __str__(self):
        # TODO: "hh:mm:ss"
        pass

    def next_second(self):
        # TODO
        pass

    def prev_second(self):
        # TODO
        pass


timer = Timer(23, 59, 59)
print(timer)
timer.next_second()
print(timer)
timer.prev_second()
print(timer)
""",
            "hints": [
                "Store `__hours/__minutes/__seconds`; format `f'{h:02}:{m:02}:{s:02}'`.",
                "next_second cascades: seconds 60->0 bumps minutes, minutes 60->0 bumps hours `% 24`.",
                "prev_second mirrors it: -1 becomes 59 (or 23 for hours).",
            ],
            "solution": """class Timer:
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.__hours = hours
        self.__minutes = minutes
        self.__seconds = seconds

    def __str__(self):
        return f"{self.__hours:02}:{self.__minutes:02}:{self.__seconds:02}"

    def next_second(self):
        self.__seconds += 1
        if self.__seconds == 60:
            self.__seconds = 0
            self.__minutes += 1
            if self.__minutes == 60:
                self.__minutes = 0
                self.__hours = (self.__hours + 1) % 24

    def prev_second(self):
        self.__seconds -= 1
        if self.__seconds == -1:
            self.__seconds = 59
            self.__minutes -= 1
            if self.__minutes == -1:
                self.__minutes = 59
                self.__hours -= 1
                if self.__hours == -1:
                    self.__hours = 23


timer = Timer(23, 59, 59)
print(timer)
timer.next_second()
print(timer)
timer.prev_second()
print(timer)
""",
            "explanation": "The carry logic cascades like a real clock: seconds overflow resets to 0 and ticks minutes, which may overflow into hours, which wraps with `% 24`. `prev_second` is the mirror - underflow (-1) borrows from the bigger unit. `:02` pads the numbers in `__str__`.\n\nWhat you learned: carry/borrow logic is just 'on overflow, reset and bump the next unit'.",
            "tests": [
                {"kind": "program",
                 "expected": "23:59:59\n00:00:00\n23:59:59",
                 "match": "exact"},
                {"kind": "expr", "expr": "str(Timer(1, 2, 3))", "expected": "'01:02:03'"},
                {"kind": "assert",
                 "code": "t = Timer(0, 0, 0)\nt.prev_second()\nassert str(t) == '23:59:59'",
                 "desc": "prev_second wraps 00:00:00 to 23:59:59"},
            ],
        },
        {
            "id": "ch13-task-2",
            "type": "task",
            "title": "The Weeker class",
            "difficulty": 2,
            "plain": "A weekday object - and your very own error type for bad days.",
            "instructions": r"""
Implement `Weeker`:

- `Weeker(day)` accepts only `'Mon' 'Tue' 'Wed' 'Thu' 'Fri' 'Sat'
  'Sun'` - anything else raises `WeekDayError` (define it yourself: a
  subclass of `Exception` with a message).
- `__str__` returns the day.
- `add_days(n)` / `subtract_days(n)` shift the day, wrapping around.

```python
w = Weeker('Mon')
w.add_days(15);  print(w)   # Tue
w.subtract_days(23); print(w) # Sun
Weeker('Monday')             # raises WeekDayError
```
""",
            "starter": """class WeekDayError(Exception):
    # TODO
    pass


class Weeker:
    __weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def __init__(self, day):
        # TODO: store day or raise WeekDayError
        pass

    def __str__(self):
        # TODO
        pass

    def add_days(self, n):
        # TODO
        pass

    def subtract_days(self, n):
        # TODO
        pass
""",
            "hints": [
                "`raise WeekDayError('Wrong day of the week')` for bad input.",
                "Day arithmetic: `(__weekdays.index(self.__day) + n) % 7`.",
                "subtract uses `-n` - Python's `%` wraps negatives correctly.",
            ],
            "solution": """class WeekDayError(Exception):
    def __init__(self, message="Wrong day of the week"):
        super().__init__(message)


class Weeker:
    __weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def __init__(self, day):
        if day not in Weeker.__weekdays:
            raise WeekDayError("Wrong day of the week")
        self.__day = day

    def __str__(self):
        return self.__day

    def add_days(self, n):
        pos = (Weeker.__weekdays.index(self.__day) + n) % 7
        self.__day = Weeker.__weekdays[pos]

    def subtract_days(self, n):
        pos = (Weeker.__weekdays.index(self.__day) - n) % 7
        self.__day = Weeker.__weekdays[pos]
""",
            "explanation": "`WeekDayError` inherits from Exception - `super().__init__(message)` stores the text the normal way. `Weeker` keeps the weekday list on the class (shared, like a chalkboard); the index+`% 7` math wraps around the week, even for negative shifts.\n\nWhat you learned: `class MyError(Exception)` creates a named error type you can raise and catch precisely.",
            "tests": [
                {"kind": "assert",
                 "code": "w = Weeker('Mon')\nw.add_days(15)\nassert str(w) == 'Tue'\nw.subtract_days(23)\nassert str(w) == 'Sun'",
                 "desc": "Mon +15 -> Tue, -23 -> Sun"},
                {"kind": "assert",
                 "code": "try:\n    Weeker('Monday')\n    assert False\nexcept WeekDayError:\n    pass",
                 "desc": "Weeker('Monday') raises WeekDayError"},
                {"kind": "assert",
                 "code": "w = Weeker('Fri')\nw.add_days(3)\nassert str(w) == 'Mon'",
                 "desc": "Fri + 3 wraps to Mon"},
            ],
        },
        {
            "id": "ch13-task-3",
            "type": "task",
            "title": "Point on a plane",
            "difficulty": 2,
            "plain": "A point that knows where it is and how far away others are.",
            "instructions": r"""
Implement `Point` for a coordinate plane:

- `__init__(self, x=0.0, y=0.0)` - private coordinates
- `getx()`, `gety()` return them
- `distance_from_xy(x, y)` - distance to a point given as coordinates
  (`math.hypot`)
- `distance_from_point(point)` - same, but the other is a `Point`

```python
Point(0, 0).distance_from_point(Point(1, 1))   # 1.4142135623730951
```
""",
            "starter": """import math

class Point:
    def __init__(self, x=0.0, y=0.0):
        # TODO
        pass

    def getx(self):
        # TODO
        pass

    def gety(self):
        # TODO
        pass

    def distance_from_xy(self, x, y):
        # TODO
        pass

    def distance_from_point(self, point):
        # TODO
        pass
""",
            "hints": [
                "`math.hypot(dx, dy)` gives the straight-line distance.",
                "distance_from_point calls distance_from_xy with `point.getx()`, `point.gety()`.",
                "Private storage: `self.__x`, `self.__y`.",
            ],
            "solution": """import math

class Point:
    def __init__(self, x=0.0, y=0.0):
        self.__x = x
        self.__y = y

    def getx(self):
        return self.__x

    def gety(self):
        return self.__y

    def distance_from_xy(self, x, y):
        return math.hypot(self.__x - x, self.__y - y)

    def distance_from_point(self, point):
        return self.distance_from_xy(point.getx(), point.gety())
""",
            "explanation": "The two distance methods share one implementation - the Point version unpacks the other object through its getters, then delegates. `math.hypot` is the hypotenuse formula: √((dx)²+(dy)²).\n\nWhat you learned: one method can reuse another instead of duplicating it.",
            "tests": [
                {"kind": "expr", "expr": "Point(0, 0).distance_from_point(Point(1, 1))",
                 "expected": "1.4142135623730951"},
                {"kind": "expr", "expr": "Point(1, 1).distance_from_xy(2, 0)",
                 "expected": "1.4142135623730951"},
                {"kind": "expr", "expr": "Point(0, 0).distance_from_xy(3, 4)", "expected": "5.0"},
                {"kind": "expr", "expr": "Point().getx()", "expected": "0.0"},
            ],
        },
        {
            "id": "ch13-task-4",
            "type": "task",
            "title": "Triangle (composition)",
            "difficulty": 2,
            "plain": "A triangle is just three points - build it from Point objects.",
            "instructions": r"""
The starter includes the finished `Point` class. Add `Triangle` -
objects containing other objects (**composition**):

- `Triangle(v1, v2, v3)` - three `Point` objects in a private list
- `perimeter()` - sum of the three edge lengths

```python
Triangle(Point(0, 0), Point(1, 0), Point(0, 1)).perimeter()
# 3.414213562373095
```
""",
            "starter": """import math

class Point:
    def __init__(self, x=0.0, y=0.0):
        self.__x = x
        self.__y = y

    def getx(self):
        return self.__x

    def gety(self):
        return self.__y

    def distance_from_xy(self, x, y):
        return math.hypot(self.__x - x, self.__y - y)

    def distance_from_point(self, point):
        return self.distance_from_xy(point.getx(), point.gety())


class Triangle:
    def __init__(self, vertice1, vertice2, vertice3):
        # TODO
        pass

    def perimeter(self):
        # TODO
        pass
""",
            "hints": [
                "Store `self.__points = [vertice1, vertice2, vertice3]`.",
                "Edge i connects point i to point `(i+1) % 3` - the modulo wraps the last edge back to the first.",
                "Sum `points[i].distance_from_point(points[(i+1) % 3])`.",
            ],
            "solution": """import math

class Point:
    def __init__(self, x=0.0, y=0.0):
        self.__x = x
        self.__y = y

    def getx(self):
        return self.__x

    def gety(self):
        return self.__y

    def distance_from_xy(self, x, y):
        return math.hypot(self.__x - x, self.__y - y)

    def distance_from_point(self, point):
        return self.distance_from_xy(point.getx(), point.gety())


class Triangle:
    def __init__(self, vertice1, vertice2, vertice3):
        self.__points = [vertice1, vertice2, vertice3]

    def perimeter(self):
        total = 0
        for i in range(len(self.__points)):
            total += self.__points[i].distance_from_point(
                self.__points[(i + 1) % len(self.__points)])
        return total
""",
            "explanation": "The Triangle doesn't know coordinate math at all - it asks its Point objects for distances: `distance_from_point` between corner i and corner (i+1)%3 covers all three edges, including the closing edge back to corner 0. Objects inside objects, each doing its own job.\n\nWhat you learned: composition - build complex objects from simpler ones.",
            "tests": [
                {"kind": "expr",
                 "expr": "Triangle(Point(0, 0), Point(1, 0), Point(0, 1)).perimeter()",
                 "expected": "3.414213562373095"},
                {"kind": "expr",
                 "expr": "Triangle(Point(0, 0), Point(3, 0), Point(0, 4)).perimeter()",
                 "expected": "12.0"},
            ],
        },
        {
            "id": "ch13-task-5",
            "type": "task",
            "title": "Person counter (class variable)",
            "difficulty": 2,
            "plain": "Every new person gets the next id - the class keeps count.",
            "instructions": r"""
Implement `Person` with private class variable `__counter`:

- `__init__(self, name)` stores the name privately, increments the
  counter, assigns `__id = 1000 + Person.__counter` (first id: 1001)
- `__str__` -> `'Person Name: <name> ID: <id>'`
- `@staticmethod count()` returns the counter

```python
a = Person("Max"); b = Person("Tom")
print(a)               # Person Name: Max ID: 1001  (fresh program)
print(Person.count())  # 2
```
""",
            "starter": """class Person:
    __counter = 0   # class variable

    def __init__(self, name):
        # TODO
        pass

    def __str__(self):
        # TODO
        pass

    @staticmethod
    def count():
        # TODO
        pass
""",
            "hints": [
                "Reach the private class variable as `Person._Person__counter` from outside - but inside the class plain `Person.__counter` works (Python auto-renames).",
                "Increment first, then `self.__id = 1000 + Person.__counter`.",
                "`count` is a staticmethod returning `Person.__counter`.",
            ],
            "solution": """class Person:
    __counter = 0

    def __init__(self, name):
        self.__name = name
        Person.__counter += 1
        self.__id = 1000 + Person.__counter

    def __str__(self):
        return f"Person Name: {self.__name} ID: {self.__id}"

    @staticmethod
    def count():
        return Person.__counter
""",
            "explanation": "The counter lives on the blueprint, so it survives between constructions - each `__init__` bumps it and snapshots `1000 + counter` as the id. `count` needs no object, hence @staticmethod. Inside the class, `Person.__counter` just works because Python rewrites `__counter` the same way on both sides.\n\nWhat you learned: class variables + static methods model 'shared' data cleanly.",
            "tests": [
                {"kind": "assert",
                 "code": "base = Person.count()\na = Person('Max')\nb = Person('Tom')\nassert Person.count() == base + 2\nassert 'ID: ' + str(base + 1001) in str(a)\nassert 'ID: ' + str(base + 1002) in str(b)",
                 "desc": "counter increments, ids 1001-based"},
                {"kind": "assert",
                 "code": "p = Person('X')\nassert str(p).startswith('Person Name: X ID: ')",
                 "desc": "__str__ format"},
            ],
        },
        {
            "id": "ch13-boss",
            "type": "task",
            "title": "Bank account with history",
            "difficulty": 3,
            "boss": True,
            "plain": "An account that remembers every move and refuses overdrafts.",
            "instructions": r"""
**BOSS MISSION - build a bank account.**

Write `BankAccount(owner)`:

- starts with balance 0, a private `__balance`, and an empty
  `history` list
- `deposit(amount)` - adds, appends `"deposit X"` to history, returns
  the new balance; raises `ValueError` for amount <= 0
- `withdraw(amount)` - subtracts, appends `"withdraw X"`, returns the
  balance; raises `ValueError` when amount > balance or <= 0
- `__str__` -> `"<owner>: <balance> EUR"`
- `history` must be a list of the transaction strings in order

```python
a = BankAccount("Ada")
a.deposit(100); a.withdraw(30)
print(a)            # Ada: 70 EUR
print(a.history)    # ['deposit 100', 'withdraw 30']
```
""",
            "starter": """class BankAccount:
    def __init__(self, owner):
        # TODO
        pass

    def deposit(self, amount):
        # TODO
        pass

    def withdraw(self, amount):
        # TODO
        pass

    def __str__(self):
        # TODO
        pass
""",
            "example": """A class that keeps a history list:

```python
class Wallet:
    def __init__(self):
        self.history = []

    def pay(self, amount):
        self.history.append(-amount)

w = Wallet()
w.pay(5)
print(w.history)
```
""",

            "hints": [
                "`self.__balance = 0` and `self.history = []` in `__init__`.",
                "Guard clauses first: `if amount <= 0: raise ValueError(...)`.",
                "withdraw needs a second guard: `amount > self.__balance`.",
            ],
            "solution": """class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self.__balance = 0
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.__balance += amount
        self.history.append(f"deposit {amount}")
        return self.__balance

    def withdraw(self, amount):
        if amount <= 0 or amount > self.__balance:
            raise ValueError("invalid amount")
        self.__balance -= amount
        self.history.append(f"withdraw {amount}")
        return self.__balance

    def __str__(self):
        return f"{self.owner}: {self.__balance} EUR"
""",
            "explanation": "Every public method guards first (raise ValueError) and only then mutates - so a bad call can never corrupt the balance. `history` records a human-readable line per move; `__balance` stays private so nobody bypasses the rules by assigning directly.\n\nWhat you learned: validate at the door, then act - object state stays consistent.",
            "tests": [
                {"kind": "assert",
                 "code": "a = BankAccount('Ada')\na.deposit(100)\nassert a.withdraw(30) == 70\nassert str(a) == 'Ada: 70 EUR'\nassert a.history == ['deposit 100', 'withdraw 30']",
                 "desc": "deposit/withdraw, balance and history"},
                {"kind": "assert",
                 "code": "a = BankAccount('X')\ntry:\n    a.withdraw(1)\n    assert False\nexcept ValueError:\n    pass\ntry:\n    a.deposit(0)\n    assert False\nexcept ValueError:\n    pass",
                 "desc": "overdraft and zero deposit raise ValueError"},
            ],
        },
    ],
}
