from typing import Generator

import pytest

from flake8_aaa.exceptions import TokensNotLoaded


def test(checker) -> None:
    """
    all_funcs() works when there are no tests functions in module. Empty
    generator as result.
    """
    checker.load()

    result = checker.all_funcs()

    assert isinstance(result, Generator)
    assert list(result) == []


# --- FAILURES ---


def test_not_loaded(checker) -> None:
    """
    Attemping to run all_funcs() method without doing load first, raises
    """
    result = checker.all_funcs()

    assert isinstance(result, Generator)
    with pytest.raises(TokensNotLoaded):
        next(result)
