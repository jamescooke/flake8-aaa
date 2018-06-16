import pytest


@pytest.mark.parametrize(
    'code_str', [
        '''

# stuff

def test():
    x = 1
    y = 2

    # Do stuff
    result = x + y
    # Finished stuff

    assert result == 4

# End
'''
    ]
)
@pytest.mark.parametrize('offset, expected_line', [
    [1, '    # Finished stuff\n'],
    [-1, '    # Do stuff\n'],
])
def test(function, offset, expected_line):
    act_block = function.load_act_block()

    result = function.get_line_relative_to_node(act_block.node, -1)

    assert result == '    # Do stuff\n'


# --- FAILURES ---


@pytest.mark.parametrize('code_str', [
    'def test():\n    pass',
])
def test_out_of_bounds(function, first_node_with_tokens):
    with pytest.raises(IndexError):
        function.get_line_relative_to_node(first_node_with_tokens, 2)
