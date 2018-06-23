import pytest

from flake8_aaa.exceptions import ValidationError


@pytest.mark.parametrize(
    'code_str', ['''
def test():
    with pytest.raises(KeyError):
        load_news('tomorrow')
'''],
    ids=['no assert']
)
def test_no_assert(function_aaa_blocks):
    result = function_aaa_blocks.check_act_assert_spacing()

    assert result is None


@pytest.mark.parametrize(
    'code_str', ['''



def test():
    result = 1 + 2
    assert result == 3
'''], ids=['no spacing']
)
def test_no_spacing(function_aaa_blocks):
    """
    Exception points at first line of assert block
    """
    with pytest.raises(ValidationError) as excinfo:
        function_aaa_blocks.check_act_assert_spacing()

    assert excinfo.value.line_number == 7
    assert excinfo.value.offset == 4
    assert excinfo.value.text.startswith('AAA04 ')
