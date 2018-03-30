import pytest


@pytest.mark.parametrize('code_str', ["""
def test():
    pass
"""])
def test_pass(function):
    result = function.check()

    assert result == []


@pytest.mark.parametrize('code_str', ["""
def test():
    result = 1

    assert result == 1
"""])
def test_result_assigned(function):
    result = function.check()

    assert result == []


@pytest.mark.parametrize('code_str', ["""
def test():
    assert 1 + 1 == 2
"""])
def test_no_result(function):
    result = function.check()

    assert result == [
        # (line_number, offset, text)
        (3, 4, 'AAA01 no result variable set in test'),
    ]


@pytest.mark.parametrize('code_str', ["""
def test():
    x = 1 + 1  # AAA act
    assert x == 2
"""])
def test_no_qa(function):
    result = function.check()

    assert result == []
