import pytest

from flake8_aaa.exceptions import ValidationError


@pytest.mark.parametrize(
    'code_str', [
        'def test():\n    pass',
        'def test_docstring():\n    """This test will work great"""',
    ]
)
def test_noop(function):
    result = function.check_all()

    assert result is None


@pytest.mark.parametrize(
    'code_str', [
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
    ]
)
def test_missing_space_before_act(function):
    with pytest.raises(ValidationError) as excinfo:
        function.check_all()

    assert excinfo.line_number == 2
    assert excinfo.offset == 0
    assert excinfo.text == 'AAA03 expected 1 blank line before Act block, found none'
