import pytest


@pytest.mark.parametrize(
    'code_str', [
        'def test():\n    pass',
        'def test_docstring():\n    """This test will work great"""',
    ]
)
def test_noop(function):
    result = function.check_all()

    assert result is None
