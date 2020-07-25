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
def test_marked(function_bl_cmt_def):
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
    errors = list(function.check_all())

    result = function.__str__(errors)

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


@pytest.mark.parametrize(
    'code_str', ['''
def test():
    x = 1
    y = 1


    result = x + y

    assert result == 2
''']
)
def test_multi_spaces(function):
    errors = list(function.check_all())

    result = function.__str__(errors)

    assert result == '''
------+------------------------------------------------------------------------
 2 DEF|def test():
 3 ARR|    x = 1
 4 ARR|    y = 1
 5 BL |
 6 BL |
 7 ACT|    result = x + y
           ^ AAA03 expected 1 blank line before Act block, found 2
 8 BL |
 9 ASS|    assert result == 2
------+------------------------------------------------------------------------
    1 | ERROR
'''.lstrip()


@pytest.mark.parametrize('code_str', ['''
def test():
    x = 1
    result = x * 5
    assert result == 5
'''])
def test_multi_errors(function):
    errors = list(function.check_all())

    result = function.__str__(errors)

    assert result == '''
------+------------------------------------------------------------------------
 2 DEF|def test():
 3 ARR|    x = 1
 4 ACT|    result = x * 5
           ^ AAA03 expected 1 blank line before Act block, found none
 5 ASS|    assert result == 5
           ^ AAA04 expected 1 blank line before Assert block, found none
------+------------------------------------------------------------------------
    2 | ERRORS
'''.lstrip()
