import pytest

from flake8_aaa.arrange_block import ArrangeBlock


@pytest.mark.parametrize('code_str', ['''
def test():
    pass
'''])
def test(first_node_with_tokens):
    arrange_block = ArrangeBlock()

    result = arrange_block.add_node(first_node_with_tokens)

    assert result is None
    assert arrange_block.nodes == [first_node_with_tokens]
