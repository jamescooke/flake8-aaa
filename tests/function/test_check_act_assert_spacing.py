import pytest


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
