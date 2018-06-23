import pytest

from flake8_aaa.exceptions import ValidationError


@pytest.mark.parametrize(
    'code_str',
    ['''
def test():
    result = 1

    assert result == 1
'''],
    ids=['no arrange'],
)
def test_no_arrange(function_with_arrange_act_blocks):
    result = function_with_arrange_act_blocks.check_act_arrange_spacing()

    assert result is None


@pytest.mark.parametrize(
    'code_str',
    [
        '''
def test():
    x = 1
    y = 2

    result = x + y

    assert result == 3
''', '''
def test(person):
    """
    Person can't be loaded
    """
    with pytest.raises(KeyError):
        person.load(-1)

    assert person.loaded is False
'''
    ],
    ids=['well spaced test', 'spaced test with pytest.raises'],
)
def test_has_act_block_good_spacing(function_with_arrange_act_blocks):
    result = function_with_arrange_act_blocks.check_act_arrange_spacing()

    assert result is None


# --- FAILURES ---


@pytest.mark.parametrize(
    'code_str',
    ['''
def test():
    x = 1
    y = 2
    result = x + y
    assert result == 3
'''],
    ids=['compact test'],
)
def test_missing_leading_space(function_with_arrange_act_blocks):
    with pytest.raises(ValidationError) as excinfo:
        function_with_arrange_act_blocks.check_act_arrange_spacing()

    assert excinfo.value.line_number == 5
    assert excinfo.value.offset == 4
    assert excinfo.value.text.startswith('AAA03 ')
