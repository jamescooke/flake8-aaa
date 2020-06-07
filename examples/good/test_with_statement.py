import io
from typing import Generator, List

import pytest


def test_simple(hello_world_path) -> None:
    """
    `with` statement is part of arrange. Blank lines are maintained around Act.
    """
    with open(hello_world_path) as f:

        result = f.read()

    assert result == 'Hello World!\n'


def test_whole(hello_world_path) -> None:
    """
    `with` statement wraps whole of test
    """
    with open(hello_world_path) as f:

        result = f.read()

        assert result == 'Hello World!\n'


def test_extra_arrange(hello_world_path) -> None:
    """
    Any extra arrangement goes in the `with` block.
    """
    with open(hello_world_path) as f:
        f.read()

        result = f.read()

    assert result == ''


def test_assert_in_block(hello_world_path) -> None:
    """
    Any assertion that needs the `with` block open, goes after Act and a BL.
    """
    with open(hello_world_path) as f:
        f.read()

        result = f.read()

        assert not f.closed
    assert f.closed
    assert result == ''


def test_pytest_assert_raises_in_block(hello_world_path) -> None:
    """
    Checking on a raise in a with block works with Pytest.
    """
    with open(hello_world_path) as f:

        with pytest.raises(io.UnsupportedOperation):
            f.write('hello back')

        assert f.read() == 'Hello World!\n'


def test_pytest_assert_raises_on_with(hello_world_path) -> None:
    """
    Checking on the raise from a with statement works with Pytest.
    """
    with pytest.raises(ValueError) as excinfo:
        with open(hello_world_path, 'zz'):
            pass

    assert 'invalid mode' in str(excinfo.value)


def test_with_in_assert(hello_world_path) -> None:
    """
    Using with statement in Assert block is valid
    """
    words = ['Hello', 'World!\n']

    result = ' '.join(words)

    with open(hello_world_path) as f:
        assert result == f.read()


def test_with_raises_in_assert() -> None:
    """
    A generator with no items will raise StopIteration
    """
    items: List[int] = []

    result = (x for x in items)

    assert isinstance(result, Generator)
    with pytest.raises(StopIteration):
        next(result)
