from collections.abc import Generator

import pytest

from flake8_aaa.exceptions import AAAError


@pytest.mark.parametrize(
    'code_str',
    [
        'def test():\n    pass',
        'def test_docstring():\n    """This test will work great"""',
    ],
    ids=['pass', 'docstring'],
)
def test_noop(function):
    result = function.check_all()

    assert isinstance(result, Generator)
    assert list(result) == []


@pytest.mark.parametrize(
    'code_str', [
        '''
def test(api_client, url):
    data = {
        'user_id': 0,
        'project_permission': 'admin',
    }
    with catch_signal(user_perms_changed) as callback:

        result = api_client.put(url, data=data)

    assert result.status_code == 400
    assert callback.call_count == 0
    ''',
    ]
)
def test_context_manager(function):
    result = list(function.check_all())

    assert result == []


# --- FAILURES ---


@pytest.mark.parametrize(
    'code_str',
    [
        '''
def test(file_resource):
    file_resource.connect()
    result = file_resource.retrieve()

    assert result.success is True
''',
        '''
def test_push(queue):
    item = Document()
    queue.push(item)  # act

    assert queue.pop() == item
''',
    ],
    ids=['no line before result= act', 'no line before marked act'],
)
def test_missing_space_before_act(function):
    result = function.check_all()

    assert isinstance(result, Generator)
    errors = list(result)
    assert len(errors) == 1
    assert isinstance(errors[0], AAAError)
    assert errors[0].line_number == 4
    assert errors[0].offset == 4
    assert errors[0].text == 'AAA03 expected 1 blank line before Act block, found none'


@pytest.mark.parametrize(
    'code_str',
    [
        '''
def test(file_resource):
    file_resource.connect()

    result = file_resource.retrieve()
    assert result.success is True
''',
        '''
def test_push(queue):
    item = Document()

    queue.push(item)  # act
    assert queue.pop() == item
''',
    ],
    ids=['no line before assert', 'no line before assert with marked act'],
)
def test_missing_space_before_assert(function):
    result = function.check_all()

    assert isinstance(result, Generator)
    errors = list(result)
    assert len(errors) == 1
    assert errors[0].line_number == 6
    assert errors[0].offset == 4
    assert errors[0].text == 'AAA04 expected 1 blank line before Assert block, found none'


@pytest.mark.parametrize(
    'code_str', [
        '''
def test(file_resource):
    file_resource.connect()
    result = file_resource.retrieve()
    assert result.success is True
''',
    ]
)
def test_multi(function):
    """
    No space before or after act - two errors are returned
    """
    result = function.check_all()

    assert isinstance(result, Generator)
    errors = list(result)
    assert len(errors) == 2
