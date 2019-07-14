# Checks that noqa is specific - ignoring errors from AAA does not prevent
# other errors from being raised.


def test( ):  # noqa: AAA01
    assert True


def test2():
    x = 1
    result = x ++ 1  # noqa: AAA03

    assert result == 2
