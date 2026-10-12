"""Kapitel 14 - Vererbung."""

CHAPTER = {
    "id": "ch14",
    "number": 14,
    "title": "OOP Inheritance",
    "summary": "Classes that inherit from other classes, super(), overriding, and multiple parents.",
    "items": [
        {
            "id": "ch14-lesson",
            "type": "lesson",
            "title": "Inheritance and super()",
            "body": r"""
Building a `Student` class that repeats everything `Person` already
does would be wasteful. **Inheritance** solves it: a *child class* gets
everything its *parent class* has - and can add more. The parent goes
in parentheses after the class name.

> **Think of it like...** a recipe card passed down in a family. The
> child inherits the whole card - same ingredients, same steps - and
> can scribble its own additions in the margin.

```python
class Vehicle:
    pass

class LandVehicle(Vehicle):      # IS-A Vehicle
    pass

class TrackedVehicle(LandVehicle):
    pass
```

> **What happens here**
>
> - line 1: `Vehicle` is the base - empty but still a class
> - line 4: `LandVehicle(Vehicle)` declares "a land vehicle IS a
>   vehicle" - it inherits everything Vehicle has
> - line 7: TrackedVehicle inherits from LandVehicle - and transitively
>   from Vehicle too

Asking about the family tree - **issubclass** asks about classes,
**isinstance** asks about objects:

```python
class Vehicle:
    pass

class LandVehicle(Vehicle):      # IS-A Vehicle
    pass

class TrackedVehicle(LandVehicle):
    pass

print(issubclass(TrackedVehicle, Vehicle))       # True
print(isinstance(TrackedVehicle(), LandVehicle)) # True
```

> **What happens here**
>
> - lines 1-7: rebuild the family - Vehicle -> LandVehicle ->
>   TrackedVehicle, so this example stands alone
> - line 9: "is TrackedVehicle inside the Vehicle family?" -> True
> - line 10: build a TrackedVehicle object and ask "is it a
>   LandVehicle?" -> True - the whole family chain counts

## Overriding and super()

When a child redefines a parent's method, that's called **overriding**
- the child's version wins. `super()` calls the parent's version
without naming the parent:

```python
class Person:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "My name is " + self.name

class Student(Person):
    def __init__(self, name, course):
        super().__init__(name)
        self.course = course
    def __str__(self):
        return super().__str__() + " and I study " + self.course

print(Student("Andy", "CS"))
```

> **What happens here**
>
> - line 8: Student declares Person as its parent
> - line 10: `super().__init__(name)` runs the PARENT's constructor -
>   `self.name` gets set without rewriting it
> - line 11: then Student stores its extra `course`
> - line 13: `super().__str__()` grabs the parent's string and appends
>   the student part - no duplicated text

> **Watch out** - if a child's `__init__` forgets `super().__init__()`,
> the parent's attributes silently never get created. Bugs that only
> show up later are the worst kind.

## Try it yourself

- Add `Teacher(Person)` whose `__str__` ends with " and I teach X".
- Check `isinstance(Student("A", "B"), Person)` - True?

## Key words

| Word | Meaning |
|---|---|
| inherit | a child class gets the parent's attributes and methods |
| parent / superclass | the class being inherited from |
| child / subclass | the class doing the inheriting |
| override | the child replaces an inherited method |
| super() | calls the parent's version from the child |
| isinstance / issubclass | check an object's / class's family |
""",
        },
        {
            "id": "ch14-lesson-2",
            "type": "lesson",
            "title": "Two parents, search order and composition",
            "body": r"""
One parent is the normal case - but Python lets a class inherit from
several parents at once. That raises an obvious question: if two
parents both have `fun()`, whose version wins?

## Multiple parents - left wins

Python searches the parents **left to right**, in the order they're
listed. This search order has a fancy name: the **method resolution
order** (MRO).

> **Think of it like...** two aunts both wrote "their" pancake recipe on
> the card - the one whose card is stacked first gets used.

```python
class Left:
    var = "L"
    var_left = "LL"
    def fun(self):
        return "Left"

class Right:
    var = "R"
    var_right = "RR"
    def fun(self):
        return "Right"

class Sub(Left, Right):
    pass

obj = Sub()
print(obj.var, obj.var_left, obj.var_right, obj.fun())
# L LL RR Left - 'Left' wins because it's listed first
```

> **What happens here**
>
> - lines 1-4: Left defines `var` ("L"), a unique `var_left`, and `fun`
> - lines 6-9: Right defines its own `var` ("R") - a conflict! - plus
>   `var_right`
> - line 11: `Sub(Left, Right)` inherits both - Left is listed FIRST
> - line 14: `obj.var` is 'L' (Left wins), `var_left` and `var_right`
>   come through (no conflict), `fun()` answers 'Left'

> **Watch out** - two parents sharing one grandparent (a *diamond*) can
> produce impossible orderings and a `TypeError`. If you need a family
> tree map, prefer single inheritance and keep it shallow.

## Composition - the calmer alternative

Instead of *being* a kind of thing, an object can **have** a helper
object that does the work:

```python
class Wheels:
    def change_direction(self, left, on):
        print("wheels:", left, on)

class Vehicle:
    def __init__(self, controller):
        self.controller = controller
    def turn(self, left):
        self.controller.change_direction(left, True)
```

> **What happens here**
>
> - line 2-3: Wheels knows HOW to steer - that's its whole job
> - line 7: Vehicle stores whatever controller it was handed -
>   Wheels, Tracks, anything with `change_direction`
> - line 9: `turn` forwards the call to the helper - Vehicle never
>   learns wheel details

> **Think of it like...** inheritance says "a car IS a vehicle";
> composition says "a car HAS wheels". Often 'has' is easier to reason
> about - you can swap the wheels without changing the car's blueprint.

## Try it yourself

- Swap to `class Sub(Right, Left)` and predict `obj.var` before
>  running.
- Build `Vehicle(Wheels())` and call `.turn(True)`.

## Key words

| Word | Meaning |
|---|---|
| multiple inheritance | a class with several parents |
| MRO (method resolution order) | the left-to-right search order |
| diamond | two parents sharing one grandparent |
| composition | an object holding a helper object |
| delegate | forward the work to the helper |
""",
        },
        {
            "id": "ch14-quiz-1",
            "type": "quiz",
            "title": "isinstance",
            "question": "`class A: pass`, `class B(A): pass`. What is `isinstance(B(), A)`?",
            "options": ["False", "True", "Error", "None"],
            "answer": 1,
            "explanation": "A B object IS an A - isinstance checks the whole family chain, not just the direct class.",
        },
        {
            "id": "ch14-quiz-2",
            "type": "quiz",
            "title": "MRO",
            "question": "`class Sub(Left, Right)` where both define `fun`. `Sub().fun()` calls...",
            "options": ["Left's version", "Right's version", "both", "an error"],
            "answer": 0,
            "explanation": "Python searches parents left to right - Left is listed first, so its `fun` wins.",
        },
        {
            "id": "ch14-quiz-3",
            "type": "quiz",
            "title": "is operator",
            "question": "`a = [1]; b = a; a is b` evaluates to...",
            "options": ["False - different objects", "True - same object", "Error", "depends on contents"],
            "answer": 1,
            "explanation": "`b = a` copies the arrow, not the list - both names point at one object, so `is` is True.",
        },
        {
            "id": "ch14-quiz-4",
            "type": "quiz",
            "title": "super()",
            "question": "Inside `Student.__init__`, what does `super().__init__(name)` do?",
            "options": ["Creates a second object", "Calls the parent's constructor", "Calls itself", "Imports Person"],
            "answer": 1,
            "explanation": "super() means 'the parent class' - its __init__ sets self.name so the child doesn't repeat that line.",
        },
        {
            "id": "ch14-warm-1",
            "type": "task",
            "title": "A simple child",
            "difficulty": 1,
            "plain": "A Dog class that inherits Animal's greet method.",
            "instructions": r"""
`Animal` has `greet()` returning `"I am an animal"`. Create
`Dog(Animal)` with an extra method `bark()` returning `"Woof!"`.

Then print `Dog().greet()` and `Dog().bark()` on two lines.

Expected output:

```text
I am an animal
Woof!
```
""",
            "starter": """class Animal:
    def greet(self):
        return "I am an animal"

# TODO: class Dog(Animal) with bark()

dog = Dog()
# TODO: print greet() then bark()
""",
            "hints": [
                "`class Dog(Animal):` - the parent in parentheses.",
                "Dog needs only `def bark(self): return 'Woof!'`.",
                "greet comes free through inheritance.",
            ],
            "solution": """class Animal:
    def greet(self):
        return "I am an animal"

class Dog(Animal):
    def bark(self):
        return "Woof!"

dog = Dog()
print(dog.greet())
print(dog.bark())""",
            "explanation": "Dog declares only its new trick; `greet` is inherited untouched - `dog.greet()` finds it on the parent automatically. That's the deal: children get everything for free.\n\nWhat you learned: `(Parent)` in the class line means 'inherit from'.",
            "tests": [
                {"kind": "program", "expected": "I am an animal\nWoof!", "match": "exact"},
            ],
        },
        {
            "id": "ch14-warm-2",
            "type": "task",
            "title": "Who am I?",
            "difficulty": 1,
            "plain": "Check whether a Cat object counts as an Animal.",
            "instructions": r"""
`Animal` is empty; `Cat(Animal)` too. Print `isinstance(Cat(), Animal)`
and `issubclass(Cat, Animal)` - both should say `True`.

Expected output:

```text
True
True
```
""",
            "starter": """class Animal:
    pass

class Cat(Animal):
    pass

# TODO: two prints
""",
            "hints": [
                "`isinstance(obj, Class)` asks about an object.",
                "`issubclass(Child, Parent)` asks about classes.",
                "Both take two arguments.",
            ],
            "solution": """class Animal:
    pass

class Cat(Animal):
    pass

print(isinstance(Cat(), Animal))
print(issubclass(Cat, Animal))""",
            "explanation": "A Cat object is built from a blueprint whose parent is Animal - so both checks report True: the object IS an Animal, and the class IS a subclass.\n\nWhat you learned: isinstance for objects, issubclass for classes.",
            "tests": [
                {"kind": "program", "expected": "True\nTrue", "match": "exact"},
            ],
        },
        {
            "id": "ch14-task-1",
            "type": "task",
            "title": "Person and Student",
            "difficulty": 1,
            "plain": "A Student is a Person who also studies something.",
            "instructions": r"""
Implement two classes:

- `Person`: `__init__(self, name)` stores `name`; `__str__` ->
  `'My name is <name>'`.
- `Student(Person)`: `__init__(self, name, course)` calls the parent
  with `super().__init__(name)` and stores `course`; `__str__` ->
  `'My name is <name> and I study <course>'` (reuse
  `super().__str__()`).

```python
print(Student("Andy", "CS"))
# My name is Andy and I study CS
```
""",
            "starter": """class Person:
    def __init__(self, name):
        # TODO
        pass

    def __str__(self):
        # TODO
        pass


class Student(Person):
    def __init__(self, name, course):
        # TODO: call the parent constructor, store course
        pass

    def __str__(self):
        # TODO: extend the parent string
        pass
""",
            "hints": [
                "`super().__init__(name)` runs Person's constructor.",
                "`super().__str__()` returns Person's string - append ' and I study ...'.",
                "Student only adds `self.course`.",
            ],
            "solution": """class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "My name is " + self.name


class Student(Person):
    def __init__(self, name, course):
        super().__init__(name)
        self.course = course

    def __str__(self):
        return super().__str__() + " and I study " + self.course
""",
            "explanation": "Student inherits `name` handling and the 'My name is' prefix, then appends its own clause - both times through `super()`, which means 'the parent's version'. Nothing is written twice.\n\nWhat you learned: super() = reuse the parent, then add your part.",
            "tests": [
                {"kind": "expr", "expr": "str(Student('Andy', 'CS'))",
                 "expected": "'My name is Andy and I study CS'"},
                {"kind": "expr", "expr": "str(Person('Tom'))", "expected": "'My name is Tom'"},
                {"kind": "assert", "code": "assert isinstance(Student('A', 'B'), Person)",
                 "desc": "Student is a Person"},
            ],
        },
        {
            "id": "ch14-task-2",
            "type": "task",
            "title": "Three-level inheritance",
            "difficulty": 2,
            "plain": "Grandparent, parent, child - all nine values reachable from the child.",
            "instructions": r"""
Implement the three-level chain:

- `Level1`: class var `variable_1 = 100`; `__init__` sets
  `self.var_1 = 101`; `fun_1()` -> `102`.
- `Level2(Level1)`: `variable_2 = 200`, `var_2 = 201`, `fun_2()` ->
  `202`, calling `super().__init__()`.
- `Level3(Level2)`: `variable_3 = 300`, `var_3 = 301`, `fun_3()` ->
  `302`, calling `super().__init__()`.

A `Level3` object must reach **all nine** values.
""",
            "starter": """class Level1:
    # TODO
    pass


class Level2(Level1):
    # TODO
    pass


class Level3(Level2):
    # TODO
    pass


obj = Level3()
print(obj.variable_1, obj.var_1, obj.fun_1())
print(obj.variable_2, obj.var_2, obj.fun_2())
print(obj.variable_3, obj.var_3, obj.fun_3())
""",
            "hints": [
                "Each `__init__` must call `super().__init__()` or the lower attributes never get created.",
                "Class variables in the class body; instance variables in `__init__`.",
                "Expected output: `100 101 102` / `200 201 202` / `300 301 302`.",
            ],
            "solution": """class Level1:
    variable_1 = 100
    def __init__(self):
        self.var_1 = 101
    def fun_1(self):
        return 102


class Level2(Level1):
    variable_2 = 200
    def __init__(self):
        super().__init__()
        self.var_2 = 201
    def fun_2(self):
        return 202


class Level3(Level2):
    variable_3 = 300
    def __init__(self):
        super().__init__()
        self.var_3 = 301
    def fun_3(self):
        return 302


obj = Level3()
print(obj.variable_1, obj.var_1, obj.fun_1())
print(obj.variable_2, obj.var_2, obj.fun_2())
print(obj.variable_3, obj.var_3, obj.fun_3())
""",
            "explanation": "Level3 reaches everything because each `__init__` hands control to the parent first - the chain runs Level1->Level2->Level3, building all instance vars. Class vars and methods are found by walking the same chain at call time.\n\nWhat you learned: without super() in __init__, parent attributes silently never exist.",
            "tests": [
                {"kind": "program",
                 "expected": "100 101 102\n200 201 202\n300 301 302",
                 "match": "exact"},
                {"kind": "assert",
                 "code": "assert issubclass(Level3, Level1) and issubclass(Level3, Level2)",
                 "desc": "Level3 subclasses both levels"},
            ],
        },
        {
            "id": "ch14-task-3",
            "type": "task",
            "title": "Abstract shape with area",
            "difficulty": 2,
            "plain": "A Shape blueprint that can't compute its own area - children fill it in.",
            "instructions": r"""
Implement a small hierarchy:

- `Shape`: stores `self.name`; `area()` raises
  `NotImplementedError` ("must be overridden"); `describe()` ->
  `'<name> area=<area()>'` - calling the *overridden* area.
- `Square(Shape)`: `__init__(side)` sets name `'Square'` via
  `super().__init__('Square')`; `area()` -> `side²`.
- `Disk(Shape)`: `__init__(radius)`, name `'Disk'`; `area()` ->
  `math.pi * radius ** 2`.

```python
Square(3).describe()   # 'Square area=9'
Disk(1).describe()     # 'Disk area=3.141592653589793'
```
""",
            "starter": """import math

class Shape:
    def __init__(self, name):
        # TODO
        pass

    def area(self):
        # TODO: raise NotImplementedError
        pass

    def describe(self):
        # TODO
        pass


class Square(Shape):
    # TODO
    pass


class Disk(Shape):
    # TODO
    pass
""",
            "hints": [
                "`raise NotImplementedError` inside Shape.area().",
                "describe: `return f'{self.name} area={self.area()}'` - Python picks the child's area automatically.",
                "Square: `self.side ** 2`; Disk: `math.pi * self.radius ** 2`.",
            ],
            "solution": """import math

class Shape:
    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError

    def describe(self):
        return f"{self.name} area={self.area()}"


class Square(Shape):
    def __init__(self, side):
        super().__init__('Square')
        self.side = side

    def area(self):
        return self.side ** 2


class Disk(Shape):
    def __init__(self, radius):
        super().__init__('Disk')
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2
""",
            "explanation": "`describe` lives once on Shape but calls `self.area()` - at runtime that resolves to Square's or Disk's override (polymorphism in action). Shape.area raising NotImplementedError makes the contract explicit: children MUST override it.\n\nWhat you learned: a shared method can call child overrides - that's the magic of polymorphism.",
            "tests": [
                {"kind": "expr", "expr": "Square(3).describe()", "expected": "'Square area=9'"},
                {"kind": "expr", "expr": "Disk(1).describe()",
                 "expected": "'Disk area=3.141592653589793'"},
                {"kind": "assert",
                 "code": "try:\n    Shape('X').area()\n    assert False\nexcept NotImplementedError:\n    pass",
                 "desc": "Shape.area() raises NotImplementedError"},
                {"kind": "assert", "code": "assert isinstance(Square(2), Shape)",
                 "desc": "Square is a Shape"},
            ],
        },
        {
            "id": "ch14-task-4",
            "type": "task",
            "title": "Multiple inheritance & MRO",
            "difficulty": 2,
            "plain": "Two parents, left one wins - prove it both ways.",
            "instructions": r"""
Reproduce the search-order demo:

- `Left`: class vars `var = "L"`, `var_left = "LL"`; `fun()` ->
  `'Left'`.
- `Right`: `var = "R"`, `var_right = "RR"`; `fun()` -> `'Right'`.
- `Sub(Left, Right)`: empty body - inherits everything.
- `SubReversed(Right, Left)`: same parents, reversed order.

`Sub().var` and `Sub().fun()` must resolve to `Left`;
`SubReversed()` to `Right`.
""",
            "starter": """class Left:
    # TODO
    pass


class Right:
    # TODO
    pass


class Sub(Left, Right):
    # TODO
    pass


class SubReversed(Right, Left):
    # TODO
    pass
""",
            "hints": [
                "Class variables in the class body; `fun` is a plain method.",
                "`class Sub(Left, Right): pass` inherits both parents.",
                "The FIRST parent listed that has the attribute wins.",
            ],
            "solution": """class Left:
    var = "L"
    var_left = "LL"
    def fun(self):
        return "Left"


class Right:
    var = "R"
    var_right = "RR"
    def fun(self):
        return "Right"


class Sub(Left, Right):
    pass


class SubReversed(Right, Left):
    pass
""",
            "explanation": "Both `var` and `fun` exist on both parents, so the order in `(Left, Right)` decides - Python checks Left first, finds them, stops. Reversing the parent list flips every winner; unique attributes (var_left, var_right) come through regardless of order.\n\nWhat you learned: parent order is the tie-breaker in multiple inheritance.",
            "tests": [
                {"kind": "expr", "expr": "Sub().var", "expected": "'L'"},
                {"kind": "expr", "expr": "Sub().fun()", "expected": "'Left'"},
                {"kind": "expr", "expr": "(Sub().var_left, Sub().var_right)",
                 "expected": "('LL', 'RR')"},
                {"kind": "expr", "expr": "SubReversed().var", "expected": "'R'"},
                {"kind": "expr", "expr": "SubReversed().fun()", "expected": "'Right'"},
            ],
        },
        {
            "id": "ch14-task-5",
            "type": "task",
            "title": "Composition: steerable vehicles",
            "difficulty": 2,
            "plain": "A vehicle that HAS a steering part - no inheritance needed.",
            "instructions": r"""
Implement steering via composition:

- `Wheels` and `Tracks` each have `change_direction(left, on)`
  printing `'wheels: <left> <on>'` / `'tracks: <left> <on>'`.
- `Vehicle(controller)` stores the controller; `turn(left)` calls
  `change_direction(left, True)` then `change_direction(left, False)`.

```python
wheeled = Vehicle(Wheels())
wheeled.turn(True)
# wheels: True True
# wheels: True False
```
""",
            "starter": """class Tracks:
    def change_direction(self, left, on):
        # TODO
        pass


class Wheels:
    def change_direction(self, left, on):
        # TODO
        pass


class Vehicle:
    def __init__(self, controller):
        # TODO
        pass

    def turn(self, left):
        # TODO: turn on, then off
        pass
""",
            "hints": [
                "Store the controller in `self.controller`.",
                "turn calls `self.controller.change_direction(left, True)` then `(left, False)`.",
                "Print: `'wheels:', left, on` (print adds the spaces).",
            ],
            "solution": """class Tracks:
    def change_direction(self, left, on):
        print("tracks:", left, on)


class Wheels:
    def change_direction(self, left, on):
        print("wheels:", left, on)


class Vehicle:
    def __init__(self, controller):
        self.controller = controller

    def turn(self, left):
        self.controller.change_direction(left, True)
        self.controller.change_direction(left, False)
""",
            "explanation": "Vehicle knows nothing about wheels or tracks - it just forwards two calls to whatever controller it was handed. Swapping `Wheels()` for `Tracks()` changes behaviour with zero changes to Vehicle - that's why 'has-a' often beats 'is-a'.\n\nWhat you learned: composition = delegate work to a held object.",
            "tests": [
                {"kind": "stdout", "code": "wheeled = Vehicle(Wheels())\nwheeled.turn(True)",
                 "expected": "wheels: True True\nwheels: True False", "match": "exact"},
                {"kind": "stdout", "code": "tracked = Vehicle(Tracks())\ntracked.turn(False)",
                 "expected": "tracks: False True\ntracks: False False", "match": "exact"},
            ],
        },
        {
            "id": "ch14-boss",
            "type": "task",
            "title": "Zoo of animals",
            "difficulty": 3,
            "boss": True,
            "plain": "One animal family, many voices - every animal speaks its own sound.",
            "instructions": r"""
**BOSS MISSION - open the zoo.**

- `Animal(name)`: stores name; `speak()` -> `"..."`; `describe()` ->
  `"<name> says <speak()>"`.
- `Dog(Animal)`: `speak()` -> `"Woof!"`.
- `Cat(Animal)`: `speak()` -> `"Meow!"`.
- `roll_call(animals)` (a function, not a method): returns a list of
  `describe()` strings for every animal.

```python
roll_call([Dog("Rex"), Cat("Mimi"), Animal("Blob")])
# ['Rex says Woof!', 'Mimi says Meow!', 'Blob says ...']
```
""",
            "starter": """class Animal:
    def __init__(self, name):
        # TODO
        pass

    def speak(self):
        # TODO
        pass

    def describe(self):
        # TODO
        pass


class Dog(Animal):
    # TODO
    pass


class Cat(Animal):
    # TODO
    pass


def roll_call(animals):
    # TODO
    pass
""",
            "example": """Inherit, override, done:

```python
class Vehicle:
    def describe(self):
        return "a vehicle"

class Bike(Vehicle):
    def describe(self):
        return "a bike with 2 wheels"

print(Bike().describe())
```
""",

            "hints": [
                "describe calls `self.speak()` - the right sound is chosen automatically.",
                "Dog/Cat only override `speak`; `describe` is inherited.",
                "roll_call: `[a.describe() for a in animals]`.",
            ],
            "solution": """class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def describe(self):
        return f"{self.name} says {self.speak()}"


class Dog(Animal):
    def speak(self):
        return "Woof!"


class Cat(Animal):
    def speak(self):
        return "Meow!"


def roll_call(animals):
    return [a.describe() for a in animals]
""",
            "explanation": "`describe` is written once on Animal but calls `self.speak()` - for a Dog that resolves to 'Woof!', for a Cat 'Meow!'. That's polymorphism: same message, different answer depending on the actual class. roll_call treats every animal uniformly.\n\nWhat you learned: override the varying piece; share the common machinery.",
            "tests": [
                {"kind": "expr", "expr": "Dog('Rex').describe()", "expected": "'Rex says Woof!'"},
                {"kind": "expr", "expr": "Cat('Mimi').describe()", "expected": "'Mimi says Meow!'"},
                {"kind": "expr",
                 "expr": "roll_call([Dog('Rex'), Cat('Mimi'), Animal('Blob')])",
                 "expected": "['Rex says Woof!', 'Mimi says Meow!', 'Blob says ...']"},
                {"kind": "assert", "code": "assert isinstance(Dog('x'), Animal)",
                 "desc": "Dog is an Animal"},
            ],
        },
    ],
}
