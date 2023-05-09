import io
import pathlib
import warnings
from typing import Generator, List

import pytest

# --- Pytest context managers ---


def test_pytest_raises() -> None:
    with pytest.raises(IndexError):
        list()[0]


def test_deprecation_warning() -> None:
    with pytest.deprecated_call():
        warnings.warn("deprecate warning", DeprecationWarning)


def test_user_warning() -> None:
    with pytest.warns(UserWarning):
        warnings.warn("my warning", UserWarning)


# --- Use of context managers in tests ---


def test_simple(hello_world_path: pathlib.Path) -> None:
    """
    Test checks "simple" context manager in both Act block styles:

    * DEFAULT: `with` statement is part of arrange. Blank lines are maintained
        around Act.
    * LARGE: When formatted with Black, context manager is squashed against act
        node. Large act block mode allows the context manager to join the act
        block and linting passes.
    """
    with open(hello_world_path) as f:

        result = f.read()

    assert result == 'Hello World!\n'


def test_whole(hello_world_path: pathlib.Path) -> None:
    """
    `with` statement wraps whole of test. This checks context manager in both
    Act block styles:

    * DEFAULT: `with` statement is part of Arrange. Result assignment is Act.
        Blank lines are maintained.
    * LARGE: When formatted with Black, context manager is squashed against
        result assignment. Act block grows to consume context manager because
        it's the first node in the context manager body. However, new large Act
        block _still_ finishes at the end of the result assignment. There is
        then a blank line and the assert block, even though that's inside the
        context manager.
    """
    with open(hello_world_path) as f:

        result = f.read()

        assert result == 'Hello World!\n'
        assert f.fileno() > 0


def test_extra_arrange(hello_world_path: pathlib.Path) -> None:
    """
    Any extra arrangement goes in the `with` block. Works "as-is" for Large act
    block style because `f.read()` node prevents the `result = ` act node from
    joining the `with` context manager.
    """
    with open(hello_world_path) as f:
        f.read()

        result = f.read()

    assert result == ''


def test_assert_in_block(hello_world_path: pathlib.Path) -> None:
    """
    Any assertion that needs the `with` block open, goes after Act and a BL.
    """
    with open(hello_world_path) as f:
        f.read()

        result = f.read()

        assert not f.closed
    assert f.closed
    assert result == ''


def test_pytest_assert_raises_in_block(hello_world_path: pathlib.Path) -> None:
    """
    Checking on a raise in a with block works with Pytest.
    """
    with open(hello_world_path) as f:

        with pytest.raises(io.UnsupportedOperation):
            f.write('hello back')

        assert f.read() == 'Hello World!\n'


def test_pytest_assert_raises_on_with(hello_world_path: pathlib.Path) -> None:
    """
    Checking on the raise from a with statement works with Pytest.
    """
    with pytest.raises(ValueError) as excinfo:
        with open(hello_world_path, 'zz'):
            pass

    assert 'invalid mode' in str(excinfo.value)


def test_with_in_assert(hello_world_path: pathlib.Path) -> None:
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
