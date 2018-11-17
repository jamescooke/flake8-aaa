from flake8_aaa.helpers import format_errors


def test_none():
    result = format_errors(None)

    assert result == '    0 | ERRORS (yet)\n'


def test_clean():
    result = format_errors([])

    assert result == '    0 | ERRORS\n'


def test_single_error():
    result = format_errors([()])

    assert result == '    1 | ERROR\n'
