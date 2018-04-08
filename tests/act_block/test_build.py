import astroid
import asttokens
import pytest

from flake8_aaa.act_block import ActBlock
from flake8_aaa.exceptions import NotActionBlock


@pytest.mark.parametrize(
    'code_str, expected_type', [
        ('result = do_thing()', ActBlock.RESULT_EQUALS),
        ('with pytest.raises(Exception):\n    do_thing()', ActBlock.PYTEST_RAISES),
        ('data[new_key] = value  # act', ActBlock.MARKED_ACT),
    ]
)
def test(code_str, expected_type):
    node = astroid.extract_node(code_str)
    tokens = asttokens.ASTTokens(code_str, tree=node)

    result = ActBlock.build(node, tokens)

    assert isinstance(result, ActBlock)
    assert result.node == node
    assert result.block_type == expected_type


@pytest.mark.parametrize(
    'code_str', [
        'person = User("Rene")',
        'results = news.post()',
        'act = "#"',
        'with open("data.txt") as f:\n    f.read()',
        'actions +=1  # actions speak louder than words!',
    ]
)
def test_not_actions(code_str):
    node = astroid.extract_node(code_str)
    tokens = asttokens.ASTTokens(code_str, tree=node)

    with pytest.raises(NotActionBlock):
        ActBlock.build(node, tokens)
