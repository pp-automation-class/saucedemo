"""Step decorators the Cucumber extension can read.

It only knows {string}, {int}, {float}, {word}. Those names are the
function arguments pytest-bdd injects. {string} includes the quotes
in the feature line; we strip them before the step body runs.
"""

from pytest_bdd import given as _given
from pytest_bdd import parsers
from pytest_bdd import then as _then
from pytest_bdd import when as _when


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _step(decorator, name):
    converters = {}
    if isinstance(name, str) and "{" in name:
        if "{string}" in name:
            converters["string"] = _unquote
        if "{int}" in name:
            converters["int"] = int
        name = parsers.parse(name)
    return decorator(name, converters=converters or None)


def given(name):
    return _step(_given, name)


def when(name):
    return _step(_when, name)


def then(name):
    return _step(_then, name)
