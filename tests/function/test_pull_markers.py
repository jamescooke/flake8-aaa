import pytest


@pytest.fixture
def code_str():
    return """def test():
    pass"""


def test_none(function):
    result = function.pull_markers({})

    assert result == 0
    assert function.markers == {}


def test_one(function):
    function.start_line = 3
    function.end_line = 5
    markers = {
        1: '__FIRST__',
        2: '__SECOND__',
        3: '__THIRD__',
        4: '__FOURTH__',
        5: '__FIFTH__',
        6: '__SIXTH__',
    }

    result = function.pull_markers(markers)

    assert result == 3
    assert function.markers == {
        3: '__THIRD__',
        4: '__FOURTH__',
        5: '__FIFTH__',
    }
