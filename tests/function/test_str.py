import pytest

from flake8_aaa.function import Function


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
def test_unprocessed(function: Function) -> None:
    """
    No parsing has happened, no errors are passed in, lines are marked with ???
    """
    result = str(function)

    assert result == '''
------+------------------------------------------------------------------------
 2 ???|def test(file_resource):
 3 ???|    file_resource.connect()
 4 ???|    result = file_resource.retrieve()
 5 ???|
 6 ???|    assert result.success is True
------+------------------------------------------------------------------------
'''.lstrip()


@pytest.mark.parametrize(
    'code_str', [
        '''
def test(file_resource):
    """
    File resource can connect

    Ignores type of resource.
    """
    file_resource.connect()

    result = file_resource.retrieve()

    assert result.success is True
''',
    ]
)
def test_marked(function_bl_cmt_def: Function) -> None:
    """
    Function has marked itself, but no errors passed
    """
    result = str(function_bl_cmt_def)

    assert result == '''
------+------------------------------------------------------------------------
 2 DEF|def test(file_resource):
 3 ???|    """
 4 ???|    File resource can connect
 5 ???|
 6 ???|    Ignores type of resource.
 7 ???|    """
 8 ???|    file_resource.connect()
 9 BL |
10 ???|    result = file_resource.retrieve()
11 BL |
12 ???|    assert result.success is True
------+------------------------------------------------------------------------
'''.lstrip()
