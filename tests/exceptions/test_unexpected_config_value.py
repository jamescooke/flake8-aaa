from flake8_aaa.exceptions import UnexpectedConfigValue


def test_message() -> None:
    exc = UnexpectedConfigValue(
        option_name='aaa_SOME_OPTION',
        value='__SOME_VALUE__',
        allowed_values=['__FIRST__', '__ALLOWED__', '__ALSO_ALLOWED__'],
    )

    result = str(exc)

    assert result == """Error loading option / configuration...
    Option: aaa_SOME_OPTION
    Want:   "__FIRST__", "__ALLOWED__" or "__ALSO_ALLOWED__"
    Got:    "__SOME_VALUE__"
"""
