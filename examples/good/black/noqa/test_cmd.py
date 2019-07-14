def test():  # noqa
    assert 1 + 1 == 2


def test_multi_line_args(math_fixture, *args, **kwargs):  # noqa
    assert 1 + 1 == 2
