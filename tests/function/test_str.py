import pytest


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
def test_unprocessed(function):
    """
    No parsing has happened, lines are marked with ???
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
    0 | ERRORS (yet)
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
def test_marked(function):
    """
    Function has marked itself, but not processed errors
    """
    function.mark_def()
    function.mark_bl()

    result = str(function)

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
    0 | ERRORS (yet)
'''.lstrip()


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
def test_processed(function):
    function.get_errors()

    result = str(function)

    assert result == '''
------+------------------------------------------------------------------------
 2 DEF|def test(file_resource):
 3 ARR|    file_resource.connect()
 4 ACT|    result = file_resource.retrieve()
           ^ AAA03 expected 1 blank line before Act block, found none
 5 BL |
 6 ASS|    assert result.success is True
------+------------------------------------------------------------------------
    1 | ERROR
'''.lstrip()
