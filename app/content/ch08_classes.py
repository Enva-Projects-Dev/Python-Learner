"""Kapitel 8 - Klassen."""

CHAPTER = {
    "id": "ch08",
    "number": 8,
    "title": "Classes",
    "summary": "Blueprints for your own things: attributes, methods and tidy doors called properties.",
    "items": [
        {
            "id": "ch08-lesson",
            "type": "lesson",
            "title": "Classes and objects",
            "body": r"""
So far every value was a loose thing in a variable. Real programs group
data *and* the actions that use it into one tidy package. A **class**
is the blueprint for such a package; an **object** is one thing built
from that blueprint.

> **Think of it like...** a cookie cutter. The cutter (class) is just a
> shape - the cookies (objects) are the real things you can eat. Every
> cookie shares the cutter's shape but gets its own sprinkles.

```python
class Robot:
    def say_hello(self):
        print("Hello, I am a " + self.kind)
    def set_kind(self, kind):
        self.kind = kind

robby = Robot()               # build one robot from the blueprint
robby.set_kind("mobile robot")
robby.say_hello()
```

> **What happens here**
>
> - line 1: `class Robot:` defines the blueprint (a recipe card, not a
>   robot yet)
> - line 2: `say_hello` is a **method** - a function that lives inside
>   the class; its first input `self` means "the object we're called on"
> - line 4: `self.kind = kind` stores a value **inside this one robot**
>   - that's an *attribute*, a variable owned by an object
> - line 7: `Robot()` builds a real object - this is called
>   *constructing* or *instantiating*
> - line 9: `robby.say_hello()` runs the method on robby, so `self` is
>   robby

> **Think of it like...** `self` is "this particular cookie". Two robots
> share the blueprint but each keeps its own `kind`.

## __init__ and __str__ - the automatic methods

Two special names Python calls by itself:

- `__init__` - the **constructor**: runs the moment an object is built,
>  fills the fresh object with starting values.
- `__str__` - decides what `print(obj)` shows.

```python
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius ** 2
    def circumference(self):
        return 2.0 * math.pi * self.radius
    def __str__(self):
        return f"Circle r={self.radius} a={self.area()} u={self.circumference()}"

k = Circle(10.0)
print(k.area())
print(k)
```

> **What happens here**
>
> - line 4: `__init__` runs when `Circle(10.0)` is called; `self` is the
>   newborn circle, `radius` is stored in it
> - line 6: `area` uses the stored radius - objects remember their data
> - line 10: `__str__` returns the text that `print(k)` will show
> - line 14: `print(k)` secretly calls `k.__str__()`

> **Watch out** - forgetting `self` as the first parameter is the most
> common class bug: `def area()` breaks with a confusing TypeError.

## Try it yourself

- Build a second robot, give it a different `kind`, call `say_hello`.
- Change `Circle(10.0)` to `Circle(5.0)` and compare the outputs.

## Key words

| Word | Meaning |
|---|---|
| class | a blueprint for objects |
| object / instance | one thing built from the blueprint |
| construct / instantiate | building an object with `Class()` |
| method | a function inside a class |
| self | the object the method is running on |
| attribute | a variable stored inside an object |
| `__init__` | constructor - runs automatically on creation |
| `__str__` | decides what `print(obj)` shows |
""",
        },
        {
            "id": "ch08-lesson-2",
            "type": "lesson",
            "title": "Locked doors: private attributes and properties",
            "body": r"""
## Keep fingers out: private attributes

Attributes are public by default - anyone can poke `obj.radius = -99`
and break your object. To mark an attribute as "hands off", start its
name with `__` - Python secretly renames `__a` to `_ClassName__a`, so
`obj.__a` fails from outside. Inside the class it's used normally.

> **Think of it like...** a locked diary. The diary owner (the class)
> writes freely; strangers can't even find the right keyhole.

```python
class Safe:
    def __init__(self):
        self.__secret = 42

s = Safe()
# print(s.__secret)   # AttributeError!
print(s._Safe__secret)  # 42 - renamed, not truly locked
```

> **What happens here**
>
> - line 3: `__secret` is stored under the hidden name `_Safe__secret`
> - line 7 (commented): `s.__secret` crashes with AttributeError -
>   outside code can't see the name
> - line 8: the mangled name still works - it's privacy by convention,
>   not a vault

> **Watch out** - private means "please don't touch", not "impossible".
> Python never truly locks; the double underscore is a warning sign.

## Properties: doors with rules

A **property** looks like a plain attribute (`r.a`) but secretly calls
methods - a *getter* when read, a *setter* when written. Perfect for
rules like "width must never be negative":

```python
class Rectangle:
    def __init__(self, a, b):
        self.a = a        # goes through the setter!
        self.b = b
    def get_a(self):
        return self.__a
    def set_a(self, a):
        self.__a = max(0, a)      # rule: never negative
    def get_b(self):
        return self.__b
    def set_b(self, b):
        self.__b = max(0, b)
    def perimeter(self):
        return 2 * self.__a + 2 * self.__b
    def area(self):
        return self.__a * self.__b
    a = property(get_a, set_a)
    b = property(get_b, set_b)

r = Rectangle(10, 20)
r.a = -10               # the setter clamps it to 0
print(r.a, r.area())
```

> **What happens here**
>
> - line 20: `a = property(get_a, set_a)` wires the name `a` to the two
>   methods
> - line 24: `r.a = -10` calls `set_a(-10)` -> `max(0, -10)` -> 0 stored
> - line 25: reading `r.a` calls `get_a()`; `area()` uses the safe
>   private values

## Try it yourself

- Set `r.b = -5` and print `r.b` - what do you expect?
- Add `print('setter!')` inside `set_a` and watch when it fires.

## Key words

| Word | Meaning |
|---|---|
| private attribute (`__x`) | hidden-ish name, renamed by Python |
| name mangling | `__a` becomes `_ClassName__a` |
| property | method pair that looks like an attribute |
| getter / setter | read method / guarded write method |
""",
        },
        {
            "id": "ch08-quiz-1",
            "type": "quiz",
            "title": "self",
            "question": "Why does every method take `self` first?",
            "options": ["It's the class name", "It's the object the method was called on", "It's optional decoration", "It marks private methods"],
            "answer": 1,
            "explanation": "`robby.say_hello()` secretly becomes `Robot.say_hello(robby)` - self is which object we're talking about.",
        },
        {
            "id": "ch08-quiz-2",
            "type": "quiz",
            "title": "__str__",
            "question": "When does `__str__` run?",
            "options": ["When the object is created", "When the object is turned into a string (print/str)", "When it is deleted", "Never automatically"],
            "answer": 1,
            "explanation": "print(obj) and str(obj) ask __str__ for the text version. Creation is __init__'s job - easy mix-up.",
        },
        {
            "id": "ch08-quiz-3",
            "type": "quiz",
            "title": "Private attributes",
            "question": "A class stores `self.__x`. Can outside code still reach it?",
            "options": ["Yes, as a.__x", "Yes, as a._ClassName__x - it's just renamed", "No, never", "Only via get_x()"],
            "answer": 1,
            "explanation": "Python rewrites __x to _ClassName__x - a 'keep out' sign, not a vault. It prevents accidents, not attackers.",
        },
        {
            "id": "ch08-quiz-4",
            "type": "quiz",
            "title": "Properties",
            "question": "With `a = property(get_a, set_a)`, what does `r.a = 5` do?",
            "options": ["Stores 5 directly in r.a", "Calls set_a(5)", "Calls get_a()", "Error - properties are read-only"],
            "answer": 1,
            "explanation": "Writing to a property calls its setter - set_a(5) runs and decides what really gets stored.",
        },
        {
            "id": "ch08-warm-1",
            "type": "task",
            "title": "Pet blueprint",
            "difficulty": 1,
            "plain": "Build a Dog class that stores a name and can bark it.",
            "instructions": r"""
Write a class `Dog`:

- `__init__(self, name)` stores the name
- `bark()` prints `<name> says woof!`

```python
Dog("Bello").bark()   # Bello says woof!
```
""",
            "starter": """class Dog:
    # TODO: __init__ + bark
    pass

Dog("Bello").bark()
""",
            "hints": [
                "`def __init__(self, name): self.name = name`.",
                "`bark` prints an f-string using `self.name`.",
                "The call `Dog('Bello')` passes 'Bello' to __init__.",
            ],
            "solution": """class Dog:
    def __init__(self, name):
        self.name = name
    def bark(self):
        print(f"{self.name} says woof!")

Dog("Bello").bark()
""",
            "explanation": "`__init__` runs the moment `Dog('Bello')` is built - 'Bello' lands in `self.name`, this dog's own attribute. `bark` then reads it back and prints the sentence.\n\nWhat you learned: `self.x` is how an object remembers its own data.",
            "tests": [
                {"kind": "program", "expected": "Bello says woof!", "match": "exact"},
                {"kind": "stdout", "code": "Dog('Rex').bark()", "expected": "Rex says woof!", "match": "exact"},
            ],
        },
        {
            "id": "ch08-warm-2",
            "type": "task",
            "title": "Counter object",
            "difficulty": 1,
            "plain": "An object that counts upward each time you poke it.",
            "instructions": r"""
Write a class `Counter`:

- `__init__` starts at 0
- `tick()` adds 1 and **returns** the new count

```python
c = Counter(); c.tick(); c.tick()   # second tick returns 2
```
""",
            "starter": """class Counter:
    # TODO: __init__ + tick
    pass
""",
            "hints": [
                "`self.count = 0` in `__init__`.",
                "`tick`: `self.count += 1; return self.count`.",
                "Each object keeps its own count.",
            ],
            "solution": """class Counter:
    def __init__(self):
        self.count = 0
    def tick(self):
        self.count += 1
        return self.count
""",
            "explanation": "The count lives inside the object, so it survives between calls - each `tick()` nudges it up and returns the fresh value. Two Counters would count independently.\n\nWhat you learned: objects are little boxes of state that methods update.",
            "tests": [
                {"kind": "expr", "expr": "Counter().tick()", "expected": "1"},
                {"kind": "assert", "code": "c = Counter()\nc.tick()\nc.tick()\nassert c.tick() == 3", "desc": "three ticks give 3"},
            ],
        },
        {
            "id": "ch08-task-1",
            "type": "task",
            "title": "Circle class",
            "difficulty": 1,
            "plain": "A Circle blueprint: radius in, area and circumference out.",
            "instructions": r"""
Implement `Circle`:

- `__init__(self, radius)` stores the radius
- `area()` returns `π-r²`, `circumference()` returns `2-π-r`
  (use `math.pi`)
- `__str__` returns exactly `Circle r=<r> a=<area> u=<circumference>`
  (raw floats, no rounding)

```python
print(Circle(10.0))
# Circle r=10.0 a=314.1592653589793 u=62.83185307179586
```
""",
            "starter": """import math

class Circle:
    # TODO: __init__, area, circumference, __str__
    pass
""",
            "hints": [
                "`self.radius = radius` in `__init__`.",
                "Area: `math.pi * self.radius ** 2`; circumference: `2.0 * math.pi * self.radius`.",
                "`__str__` is one f-string calling `self.area()` and `self.circumference()`.",
            ],
            "solution": """import math

class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius ** 2
    def circumference(self):
        return 2.0 * math.pi * self.radius
    def __str__(self):
        return f"Circle r={self.radius} a={self.area()} u={self.circumference()}"
""",
            "explanation": "`__init__` stores the radius on the object; `area` and `circumference` are pure formulas reading it back. `__str__` assembles the labelled summary by calling the object's own methods - no duplicated math.\n\nWhat you learned: methods can call each other through `self`.",
            "tests": [
                {"kind": "expr", "expr": "Circle(10.0).area()", "expected": "314.1592653589793"},
                {"kind": "expr", "expr": "Circle(10.0).circumference()", "expected": "62.83185307179586"},
                {"kind": "expr", "expr": "str(Circle(10.0))",
                 "expected": "'Circle r=10.0 a=314.1592653589793 u=62.83185307179586'"},
            ],
        },
        {
            "id": "ch08-task-2",
            "type": "task",
            "title": "Traffic light",
            "difficulty": 2,
            "plain": "Model a real traffic light's cycle as a class with a hidden state.",
            "instructions": r"""
Implement `TrafficLight` with a **private** `__state`:

- states cycle `red -> red_yellow -> green -> yellow -> red`
- `__init__` starts at `'red'`
- `switch()` advances one state
- `get_state()` returns the state string
- `get_lamps()` returns `(red, yellow, green)` booleans:
  `'red'` -> `(True, False, False)`, `'red_yellow'` -> `(True, True, False)`,
  `'green'` -> `(False, False, True)`, `'yellow'` -> `(False, True, False)`
""",
            "starter": """class TrafficLight:
    def __init__(self):
        self.__state = 'red'

    def switch(self):
        # TODO: advance the state
        pass

    def get_state(self):
        # TODO
        pass

    def get_lamps(self):
        # TODO: return (red, yellow, green) booleans
        pass
""",
            "hints": [
                "An if/elif chain maps each state to its successor.",
                "The cycle: red -> red_yellow -> green -> yellow -> red.",
                "get_lamps is a second if-chain returning tuples - or reuse get_state().",
            ],
            "solution": """class TrafficLight:
    def __init__(self):
        self.__state = 'red'

    def switch(self):
        if self.__state == 'red':
            self.__state = 'red_yellow'
        elif self.__state == 'red_yellow':
            self.__state = 'green'
        elif self.__state == 'green':
            self.__state = 'yellow'
        elif self.__state == 'yellow':
            self.__state = 'red'

    def get_state(self):
        return self.__state

    def get_lamps(self):
        if self.__state == 'red':
            return (True, False, False)
        if self.__state == 'red_yellow':
            return (True, True, False)
        if self.__state == 'green':
            return (False, False, True)
        return (False, True, False)
""",
            "explanation": "The state is private (`__state`), so the only way to change it is `switch()` - the if/elif chain encodes the real German light cycle. `get_lamps` translates each state into its three bulb values; the final `return` covers 'yellow' since the other three already returned.\n\nWhat you learned: a private attribute + controlled methods = a state machine.",
            "tests": [
                {"kind": "expr", "expr": "TrafficLight().get_state()", "expected": "'red'"},
                {"kind": "expr", "expr": "TrafficLight().get_lamps()",
                 "expected": "(True, False, False)", "expected_type": "tuple"},
                {"kind": "assert",
                 "code": "a = TrafficLight()\na.switch()\nassert a.get_state() == 'red_yellow'\na.switch()\nassert a.get_lamps() == (False, False, True)",
                 "desc": "after 2 switches: green with lamps (False, False, True)"},
                {"kind": "assert",
                 "code": "a = TrafficLight()\nfor _ in range(4):\n    a.switch()\nassert a.get_state() == 'red'",
                 "desc": "4 switches cycle back to red"},
            ],
        },
        {
            "id": "ch08-task-3",
            "type": "task",
            "title": "Rectangle with properties",
            "difficulty": 2,
            "plain": "Rectangle whose sides can never be negative - properties enforce it.",
            "instructions": r"""
Implement `Rectangle(a, b)` with private `__a`, `__b` exposed through
properties `a` and `b`. Setters **clamp negatives to 0**.

Methods: `perimeter()` -> `2a + 2b`, `area()` -> `a * b`.

```python
r = Rectangle(10, 20)
r.a = -10            # becomes 0
print(r.a, r.b, r.perimeter(), r.area())   # 0 20 40 0
```
""",
            "starter": """class Rectangle:
    def __init__(self, a, b):
        self.a = a     # through the property setters
        self.b = b

    def get_a(self):
        # TODO
        pass

    def set_a(self, a):
        # TODO: clamp negatives to 0
        pass

    def get_b(self):
        # TODO
        pass

    def set_b(self, b):
        # TODO: clamp negatives to 0
        pass

    def perimeter(self):
        # TODO
        pass

    def area(self):
        # TODO
        pass

    a = property(get_a, set_a)
    b = property(get_b, set_b)
""",
            "hints": [
                "Getters return `self.__a`/`self.__b`; setters store `max(0, value)`.",
                "The `property(...)` lines are already in place.",
                "perimeter/area read `self.__a` and `self.__b`.",
            ],
            "solution": """class Rectangle:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_a(self):
        return self.__a

    def set_a(self, a):
        self.__a = max(0, a)

    def get_b(self):
        return self.__b

    def set_b(self, b):
        self.__b = max(0, b)

    def perimeter(self):
        return 2 * self.__a + 2 * self.__b

    def area(self):
        return self.__a * self.__b

    a = property(get_a, set_a)
    b = property(get_b, set_b)
""",
            "explanation": "Every write to `r.a` secretly calls `set_a`, which clamps with `max(0, a)` - even inside `__init__`, since `self.a = a` goes through the property too. The real storage lives in `__a`/`__b`, unreachable by accident.\n\nWhat you learned: properties let attribute syntax carry hidden rules.",
            "tests": [
                {"kind": "expr", "expr": "Rectangle(10, 20).area()", "expected": "200"},
                {"kind": "expr", "expr": "Rectangle(10, 20).perimeter()", "expected": "60"},
                {"kind": "assert",
                 "code": "r = Rectangle(10, 20)\nr.a = -10\nassert r.a == 0 and r.area() == 0",
                 "desc": "negative assignment clamped to 0"},
            ],
        },
        {
            "id": "ch08-task-4",
            "type": "task",
            "title": "Robot with a name property",
            "difficulty": 2,
            "plain": "A robot whose name can be set, read - and deleted.",
            "instructions": r"""
Implement `Robot` with private `__name`:

- `__init__(self, name)` sets the name
- `say_hello()` prints `Hello, my name is <name>` - after deletion it
  prints `Noname`
- `get_name()` returns `self.__name`, or `'Noname'` on
  `AttributeError`
- `set_name(name)`, `del_name()` manage it
- `name = property(get_name, set_name, del_name)`

```python
robby = Robot("Robby")
robby.name = "Robert"
robby.say_hello()      # Hello, my name is Robert
del robby.name
robby.say_hello()      # Hello, my name is Noname
```
""",
            "starter": """class Robot:
    def __init__(self, name):
        self.__name = name

    def say_hello(self):
        # TODO: print the greeting using get_name()
        pass

    def get_name(self):
        # TODO: return self.__name or 'Noname' (catch AttributeError)
        pass

    def set_name(self, name):
        # TODO
        pass

    def del_name(self):
        # TODO
        pass

    name = property(get_name, set_name, del_name)
""",
            "hints": [
                "get_name: `try: return self.__name` / `except AttributeError: return 'Noname'`.",
                "del_name is just `del self.__name`.",
                "say_hello prints `'Hello, my name is ' + self.get_name()`.",
            ],
            "solution": """class Robot:
    def __init__(self, name):
        self.__name = name

    def say_hello(self):
        print("Hello, my name is " + self.get_name())

    def get_name(self):
        try:
            return self.__name
        except AttributeError:
            return "Noname"

    def set_name(self, name):
        self.__name = name

    def del_name(self):
        del self.__name

    name = property(get_name, set_name, del_name)
""",
            "explanation": "Properties can carry a third handler - the deleter. `del robby.name` calls `del_name`, which removes `__name`; after that, `get_name` hits an AttributeError and the except branch supplies 'Noname'. `say_hello` never touches the attribute directly, so the fallback always applies.\n\nWhat you learned: `try/except AttributeError` is the polite way to handle a missing attribute.",
            "tests": [
                {"kind": "stdout", "code": "r = Robot('Robby')\nr.say_hello()",
                 "expected": "Hello, my name is Robby", "match": "exact"},
                {"kind": "stdout", "code": "r = Robot('Robby')\nr.name = 'Robert'\nr.say_hello()\ndel r.name\nr.say_hello()",
                 "expected": "Hello, my name is Robert\nHello, my name is Noname", "match": "exact"},
            ],
        },
        {
            "id": "ch08-boss",
            "type": "task",
            "title": "Pet shelter",
            "difficulty": 3,
            "boss": True,
            "plain": "A shelter keeps pets - each pet is an object, the shelter counts and lists them.",
            "instructions": r"""
**BOSS MISSION - run a pet shelter.**

Write two classes:

1. `Pet(name, species)` - stores both; `describe()` returns
   `"<name> the <species>"`.
2. `Shelter` - `add(pet)`, `count()` -> number of pets, `report()`
   returns the sorted list of `describe()` strings, and `__str__`
   returns `"Shelter: <n> pets"`.

```python
s = Shelter()
s.add(Pet("Bello", "dog")); s.add(Pet("Minka", "cat")); s.add(Pet("Flip", "parrot"))
print(s)              # Shelter: 3 pets
print(s.report())     # ['Bello the dog', 'Flip the parrot', 'Minka the cat']
```
""",
            "starter": """class Pet:
    # TODO: __init__ + describe
    pass


class Shelter:
    # TODO: __init__ (empty list), add, count, report, __str__
    pass
""",
            "example": """A small class with a method:

```python
class Plant:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"{self.name} is growing."

print(Plant("Fern").describe())
```
""",

            "hints": [
                "`Pet.__init__` stores name/species; `describe` is one f-string.",
                "Shelter keeps `self.pets = []`; `add` appends.",
                "`report`: `sorted(p.describe() for p in self.pets)`; `__str__` returns an f-string with `len(self.pets)`.",
            ],
            "solution": """class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    def describe(self):
        return f"{self.name} the {self.species}"


class Shelter:
    def __init__(self):
        self.pets = []
    def add(self, pet):
        self.pets.append(pet)
    def count(self):
        return len(self.pets)
    def report(self):
        return sorted(p.describe() for p in self.pets)
    def __str__(self):
        return f"Shelter: {len(self.pets)} pets"
""",
            "explanation": "`Pet` is a tiny record object; `Shelter` holds objects *inside* another object - `self.pets` is a list of Pets. `report` asks each pet to describe itself (a generator expression inside `sorted`), and `__str__` lets `print(shelter)` show the count line.\n\nWhat you learned: objects can contain other objects - that's how real programs model things.",
            "tests": [
                {"kind": "expr", "expr": "Pet('Bello', 'dog').describe()", "expected": "'Bello the dog'"},
                {"kind": "assert",
                 "code": "s = Shelter()\ns.add(Pet('Bello','dog'))\ns.add(Pet('Minka','cat'))\ns.add(Pet('Flip','parrot'))\nassert str(s) == 'Shelter: 3 pets'\nassert s.count() == 3\nassert s.report() == ['Bello the dog', 'Flip the parrot', 'Minka the cat']",
                 "desc": "shelter with 3 pets reports correctly"},
            ],
        },
    ],
}
