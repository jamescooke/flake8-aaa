import ast

import pytest

from flake8_aaa.helpers import node_is_result_equals


@pytest.mark.parametrize('code_str', (
    'result = 1',
    'result = lambda x: x + 1',
))
def test(code_str):
    node = ast.parse(code_str).body[0]

    result = node_is_result_equals(node)

    assert result is True


@pytest.mark.parametrize('code_str', (
    'xresult = 1',
    'result, _ = 1, 2',
    'result[0] = 0',
))
def test_no(code_str):
    node = ast.parse(code_str).body[0]

    result = node_is_result_equals(node)

    assert result is False
