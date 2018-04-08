import pytest

from flake8_aaa.exceptions import FunctionNotParsed


@pytest.mark.parametrize('code_str', ["""
def test():
    pass
"""])
def test_pass(function):
    function.parse()

    result = function.check()

    assert result == []


@pytest.mark.parametrize('code_str', ["""
def test():
    result = 1

    assert result == 1
"""])
def test_result_assigned(function):
    function.parse()

    result = function.check()

    assert result == []


@pytest.mark.parametrize('code_str', ["""
def test():
    assert 1 + 1 == 2
"""])
def test_no_result(function):
    function.parse()

    result = function.check()

    assert result == [
        # (line_number, offset, text)
        (2, 0, 'AAA01 no result variable set in test'),
    ]


@pytest.mark.parametrize('code_str', ["""
def test():
    x = 1 + 1  # act
    assert x == 2
"""])
def test_no_qa(function):
    function.parse()

    result = function.check()

    assert result == []


# --- FAILURES ---


@pytest.mark.parametrize('code_str', ['x = 1'])
def test_not_parsed(function):
    with pytest.raises(FunctionNotParsed):
        function.check()
