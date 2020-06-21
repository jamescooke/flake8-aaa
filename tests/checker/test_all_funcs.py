from typing import Generator

import pytest

from flake8_aaa.exceptions import TokensNotLoaded


def test(checker) -> None:
    checker.load()

    result = checker.all_funcs()

    assert isinstance(result, Generator)
    assert list(result) == []


def test_not_loaded(checker) -> None:
    result = checker.all_funcs()

    assert isinstance(result, Generator)
    with pytest.raises(TokensNotLoaded):
        next(result)
