import typing

from flake8_aaa.exceptions import AAAError
from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test_ok():
    line_markers = LineMarkers(6 * [''], 7)
    line_markers.types[0] = LineType.func_def
    line_markers.types[1] = LineType.arrange
    line_markers.types[2] = LineType.blank_line
    line_markers.types[3] = LineType.act
    line_markers.types[4] = LineType.blank_line
    line_markers.types[5] = LineType._assert

    result = line_markers.check_blank_lines()

    assert isinstance(result, typing.Generator)
    assert list(result) == []


# --- FAILURES ---


def test_arrange():
    line_markers = LineMarkers(8 * [''], 7)
    line_markers.types[0] = LineType.func_def
    line_markers.types[1] = LineType.arrange
    line_markers.types[2] = LineType.blank_line
    line_markers.types[3] = LineType.arrange
    line_markers.types[4] = LineType.blank_line
    line_markers.types[5] = LineType.act
    line_markers.types[6] = LineType.blank_line
    line_markers.types[7] = LineType._assert

    result = line_markers.check_blank_lines()

    assert isinstance(result, typing.Generator)
    assert list(result) == [
        AAAError(
            line_number=9,
            offset=0,
            text='AAA05 blank line in block',
        ),
    ]


def test_func_def():
    """
    Function definition has some funky call args separated by a blank line
    """
    line_markers = LineMarkers(3 * [''], 7)
    line_markers.types[0] = LineType.func_def
    line_markers.types[1] = LineType.blank_line
    line_markers.types[2] = LineType.func_def

    result = line_markers.check_blank_lines()

    assert isinstance(result, typing.Generator)
    assert list(result) == [
        AAAError(
            line_number=8,
            offset=0,
            text='AAA05 blank line in block',
        ),
    ]
