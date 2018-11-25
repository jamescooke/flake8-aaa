import pytest

from flake8_aaa.helpers import build_footprint


@pytest.mark.parametrize(
    'code_str, first_line_no, expected_lines', [
        ('''
def test():  # 0
    with pytest.raises(Exception):  # 1
        do_thing()  # 2

    other_thing()  # 4
''', 2, set([1, 2])),
        (
            '''
@pytest.mark.xfail()  # 0
def test_other():  # 1
    result = do_thing(  # 2
        'yes',  # 3
        None,  # 4
    )  # 5

    assert result is None  # 7
''', 2, set([2, 3, 4, 5])
        ),
    ]
)
def test(first_node_with_tokens, first_line_no, expected_lines):
    first_test_node = first_node_with_tokens.body[0]

    result = build_footprint(first_test_node, first_line_no)

    assert result == expected_lines


@pytest.mark.parametrize(
    'code_str', [
        '''
# Do a test


def test(api_client, url):  # 0
    data = {  # 1
        'user_id': 0,  # 2
        'project_permission': 'admin',  # 3
    }  # 4

    with catch_signal(user_perms_changed) as callback:  # 6
        result = api_client.put(url, data=data)  # 7

    assert result.status_code == 400
    assert callback.call_count == 0
    ''',
    ]
)
def test_context_manager(first_node_with_tokens):
    """
    Act block is selected result assignment, which is wrapped in the context
    manager. The footprint analysis widens the footprint to include the context
    manager that wraps the act.
    """
    context_manager = first_node_with_tokens.body[1]
    result_assignment = context_manager.body[0]

    result = build_footprint(result_assignment, 5)

    assert result == set([6, 7])
