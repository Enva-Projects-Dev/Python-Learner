"""Unit-tests für app/errors.py - ein fall pro friendly-message."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import errors

T = """Traceback (most recent call last):
  File "main.py", line 1, in <module>
    print("x)
"""


def case(name, stderr, timed_out, needle):
    msg = errors.friendly(stderr, timed_out)
    assert msg is not None, f"{name}: no friendly message"
    assert needle.lower() in msg.lower(), f"{name}: {needle!r} not in {msg!r}"
    print(f"ok    {name}")


case("timeout", "", True, "never ends")
case("unterminated string", T + 'SyntaxError: unterminated string '
     'literal (detected at line 1)', False, "closing quote")
case("generic syntax", T + "SyntaxError: invalid syntax", False,
     "can't read this line")
case("indentation", T + "IndentationError: unexpected indent", False,
     "spaces at the start")
case("name error", T + "NameError: name 'Print' is not defined. "
     "Did you mean: 'print'?", False, "doesn't know the name 'Print'")
case("concat typeerror", T + "TypeError: can only concatenate str "
     '(not "int") to str', False, "glue text and a number")
case("missing arg", T + "TypeError: f() missing 1 required positional "
     "argument: 'x'", False, "too few values")
case("int literal", T + "ValueError: invalid literal for int() with "
     "base 10: 'abc'", False, "isn't a whole number")
case("zero division", T + "ZeroDivisionError: division by zero", False,
     "divided by zero")
case("index", T + "IndexError: list index out of range", False,
     "locker number")
case("key error", T + "KeyError: 'Potter'", False, "no key 'Potter'")
case("attribute", T + "AttributeError: 'Dog' object has no attribute "
     "'bark'", False, "A Dog has no 'bark'")
case("eof", T + "EOFError: No more input available (the program asked "
     "for more input than provided).", False, "more input than it was given")
case("recursion", T + "RecursionError: maximum recursion depth "
     "exceeded", False, "kept calling itself forever")

# nix gematcht -> None
assert errors.friendly("some random warning\n", False) is None
assert errors.friendly("", False) is None
print("ok    no-match returns None")
print("all error-helper tests pass")
