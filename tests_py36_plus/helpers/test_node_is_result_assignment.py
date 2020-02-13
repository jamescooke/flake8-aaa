import pytest

from flake8_aaa.helpers import node_is_result_assignment


@pytest.mark.parametrize(
    ('code_str', 'expected_result'),
    [
        ('result: int = 1', True),
        ('result: List[int] = [1]', True),
        ('xresult: int = 1', False),
    ],
)
def test_no(first_node_with_tokens, expected_result):
    result = node_is_result_assignment(first_node_with_tokens)

    assert result is expected_result
