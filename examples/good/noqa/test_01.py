def test():  # noqa
    assert 1 + 1 == 2


def test_multi_line_args(  # noqa
    math_fixture,
    *args,
    **kwargs
):
    assert 1 + 1 == 2
