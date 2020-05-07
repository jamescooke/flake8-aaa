import pytest

from flake8_aaa.types import LineType


@pytest.mark.parametrize('code_str', [
    '''
def test():
    result = 1

    assert result == 1
''',
])
def test(function):
    result = function.mark_def()

    assert result == 1
    assert function.line_markers.types == [
        LineType.func_def,
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
    ]


@pytest.mark.parametrize(
    'code_str', [
        '''
@pytest.mark.skip(reason='maths is too hard :D')
@pytest.mark.parametrize('value', [
    1,
    2,
    3,
])
def test(value):
    result = 1 + value

    assert result == 1
''',
    ]
)
def test_decorated(function):
    result = function.mark_def()

    assert result == 7
    assert function.line_markers.types == [
        LineType.func_def,  # @pytest.mark.skip(...)
        LineType.func_def,  # @pytest.mark.param...
        LineType.func_def,  # 1,
        LineType.func_def,  # 2,
        LineType.func_def,  # 3,
        LineType.func_def,  # ])
        LineType.func_def,  # def test(...
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
    ]


@pytest.mark.parametrize(
    'code_str', [
        '''
def test(
    fixture_a,

    fixture_b,
):  # < This line will remain unprocessed
    result = 1

    assert result == 1
''',
    ]
)
def test_multi(function):
    result = function.mark_def()

    assert result == 4
    assert function.line_markers.types == [
        LineType.func_def,
        LineType.func_def,
        LineType.func_def,
        LineType.func_def,
        LineType.unprocessed,  # < This is the ): line
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
    ]
