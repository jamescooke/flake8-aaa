"""
Failure of AAA01: when pytest context managers are not imported "in" pytest,
then they can't be found
"""

# Unusual import of raises and warns: docs / convention uses `import pytest` so
# preserves namespace.
from pytest import raises, warns


def test_imported() -> None:
    one_stuff = [1]

    with raises(IndexError):
        one_stuff[1]


def test_warns() -> None:
    with warns(UserWarning, match="yamlfix/pull/182"):
        pass
