import pytest

from flake8_aaa.helpers import node_is_result_assignment


@pytest.mark.parametrize(
    ('code_str', 'expected_result'),
    [
        ('result = 1', True),
        ('result = lambda x: x + 1', True),
        ('xresult = 1', False),
        ('result, _ = 1, 2', False),
        ('result[0] = 0', False),
        ('result += 1', False),
        ('result -= 1', False),
        ('result: int = 1', True),
        ('result: List[int] = [1]', True),
        ('xresult: int = 1', False),
    ],
)
def test_no(first_node_with_tokens, expected_result):
    result = node_is_result_assignment(first_node_with_tokens)

    assert result is expected_result
