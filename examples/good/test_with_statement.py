import io
import pathlib

import pytest

# Maybe crazy, but in an effort to get the good and bad examples to be
# runnable, this is the first stab at writing "real" examples.


@pytest.fixture
def hello_world_path() -> str:
    """
    Location of hello_world.txt
    """
    return pathlib.Path(__file__).parent.parent / 'data' / 'hello_world.txt'


# --- TESTS ---


def test_simple(hello_world_path):
    """
    `with` statement is part of arrange. Blank lines are maintained around Act.
    """
    with open(hello_world_path) as f:

        result = f.read()

    assert result == 'Hello World!\n'


def test_whole(hello_world_path):
    """
    `with` statement wraps whole of test
    """
    with open(hello_world_path) as f:

        result = f.read()

        assert result == 'Hello World!\n'


def test_extra_arrange(hello_world_path):
    """
    Any extra arrangement goes in the `with` block.
    """
    with open(hello_world_path) as f:
        f.read()

        result = f.read()

    assert result == ''


def test_assert_in_block(hello_world_path):
    """
    Any assertion that needs the `with` block open, goes after Act and a BL.
    """
    with open(hello_world_path) as f:
        f.read()

        result = f.read()

        assert not f.closed
    assert f.closed
    assert result == ''


def test_pytest_assert_raises_in_block(hello_world_path):
    """
    Checking on a raise in a with block works with Pytest.
    """
    with open(hello_world_path) as f:

        with pytest.raises(io.UnsupportedOperation):
            f.write('hello back')

        assert f.read() == 'Hello World!\n'


def test_pytest_assert_raises_on_with(hello_world_path):
    """
    Checking on the raise from a with statement works with Pytest.
    """
    with pytest.raises(ValueError) as excinfo:
        with open(hello_world_path, 'zz'):
            pass

    assert 'invalid mode' in str(excinfo.value)
