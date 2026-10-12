"""Tracebacks in einen satz + tipp übersetzen, den kids verstehen."""
import re


def friendly(stderr, timed_out=False):
    """Gibt eine plain-english erklärung für stderr zurück, sonst None."""
    if timed_out:
        return ("Your program ran for more than 5 seconds - probably a "
                "loop that never ends. Does the loop's condition ever "
                "become False?")
    if not stderr:
        return None

    last = [l for l in stderr.strip().splitlines() if l.strip()]
    if not last:
        return None
    tail = last[-1]

    if "EOFError" in tail or "No more input available" in stderr:
        return ("Your program asked for more input than it was given. "
                "Does it call input() too many times - or did you forget "
                "the Program input box?")
    if "IndentationError" in tail:
        return ("The spaces at the start of a line are wrong. Only lines "
                "inside an if/for/while/def get indented - and always by "
                "the same amount (4 spaces).")
    if "SyntaxError" in tail:
        if "unterminated string" in tail:
            return ("A text is missing its closing quote. Every opening "
                    "\" needs a closing \" on the same line.")
        return ("Python can't read this line. Check for a missing "
                "bracket, quote or colon - the ^ mark shows where it "
                "got confused.")
    m = re.search(r"NameError: name '(\w+)' is not defined", tail)
    if m:
        tip = ("Python doesn't know the name '%s'. Did you spell it "
               "exactly the same as where you created it? "
               "(Capital letters matter.)" % m.group(1))
        hint = re.search(r"Did you mean[^.]*\?", tail)
        if hint:
            tip += " " + hint.group(0).rstrip("'\"") 
        return tip
    if "ZeroDivisionError" in tail:
        return ("You divided by zero - maths doesn't allow that. "
                "Check the value before dividing.")
    if "TypeError" in tail:
        if "can only concatenate" in tail or "unsupported operand" in tail:
            return ("You tried to glue text and a number together. "
                    "Turn the number into text with str(), or use an "
                    "f-string.")
        if "positional argument" in tail:
            return ("The function was called with too few values. "
                    "Check how many inputs it expects.")
        return ("A value had the wrong type - like adding text to a "
                "number. Check what type each variable really is.")
    if "invalid literal for int()" in tail:
        return ("int() got something that isn't a whole number "
                "(for example 'abc' or '3.5'). Check what is being "
                "converted.")
    if "IndexError" in tail:
        return ("You asked for a locker number that doesn't exist. "
                "Remember: the first item is 0 and the last is "
                "len(list) - 1.")
    m = re.search(r"KeyError: (.+)$", tail)
    if m:
        return ("The dictionary has no key %s. Check the spelling, or "
                "use .get() to be safe." % m.group(1))
    m = re.search(r"AttributeError: '(\w+)' object has no attribute '(\w+)'",
                  tail)
    if m:
        return ("A %s has no '%s'. Check the spelling, or whether you "
                "meant a different method." % (m.group(1), m.group(2)))
    if "AttributeError" in tail:
        return ("That object doesn't have the thing you asked for. "
                "Check the method or attribute name.")
    if "RecursionError" in tail:
        return ("A function kept calling itself forever. Make sure it "
                "has a stopping condition.")
    if "FileNotFoundError" in tail:
        return ("The file isn't there. Check the filename and whether "
                "it sits in the working folder.")
    return None
