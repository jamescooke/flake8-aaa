import astroid
import pytest

from flake8_aaa.helpers import function_is_noop


@pytest.mark.parametrize(
    'code_str', [
        'def test():\n    pass',
        'def test_docstring():\n    """This test will work great"""',
    ]
)
def test(code_str):
    node = astroid.extract_node(code_str)

    result = function_is_noop(node)

    assert result is True


@pytest.mark.parametrize('code_str', [
    'def test_tomorrow():\n    # TODO write this test\n    result = 1',
])
def test_not_noop(code_str):
    node = astroid.extract_node(code_str)

    result = function_is_noop(node)

    assert result is False
