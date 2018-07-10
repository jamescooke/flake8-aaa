import pytest

from flake8_aaa.act_block import ActBlock
from flake8_aaa.exceptions import NotActionBlock
from flake8_aaa.types import ActBlockType

# TODO act blocks need testing with 'result =' indented
# TODO act blocks need testing with indentation in general


@pytest.mark.parametrize(
    'code_str', [
        """
def test_not_actions(first_node_with_tokens):
    with pytest.raises(NotActionBlock):
        ActBlock.build(first_node_with_tokens)
"""
    ]
)
def test_raises_block(first_node_with_tokens):
    result = ActBlock.build(first_node_with_tokens.body[0])

    assert isinstance(result, ActBlock)
    assert result.node == first_node_with_tokens.body[0]
    assert result.block_type == ActBlockType.pytest_raises


@pytest.mark.parametrize(
    'code_str, expected_type', [
        ('result = do_thing()', ActBlockType.result_assignment),
        ('with pytest.raises(Exception):\n    do_thing()', ActBlockType.pytest_raises),
        ('data[new_key] = value  # act', ActBlockType.marked_act),
    ]
)
def test(expected_type, first_node_with_tokens):
    result = ActBlock.build(first_node_with_tokens)

    assert isinstance(result, ActBlock)
    assert result.node == first_node_with_tokens
    assert result.block_type == expected_type


@pytest.mark.parametrize(
    'code_str', [
        "with mock.patch('stats.deletion_manager.deleted'):\n    result = existing_user.delete()",
    ]
)
def test_nested(first_node_with_tokens):
    result = ActBlock.build(first_node_with_tokens)

    assert isinstance(result, ActBlock)
    assert result.block_type == ActBlockType.result_assignment
    assert result.node == first_node_with_tokens.body[0]


@pytest.mark.parametrize(
    'code_str', [
        'act = "#"',
        'actions +=1  # actions speak louder than words!',
        'person = User("Rene")',
        'result += 1',
        'results = news.post()',
        'with open("data.txt") as f:\n    f.read()',
    ]
)
def test_not_actions(first_node_with_tokens):
    with pytest.raises(NotActionBlock):
        ActBlock.build(first_node_with_tokens)
