from collections.abc import Generator

from flake8_aaa.exceptions import AAAError
from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test_comment_before_act():
    """
    Comment before Act passes
    """
    line_markers = LineMarkers(8 * [''], 5)
    line_markers.types[0] = LineType.func_def
    line_markers.types[1] = LineType.arrange  # x = 1
    line_markers.types[2] = LineType.arrange  # y = 2
    line_markers.types[3] = LineType.blank_line
    line_markers.types[4] = LineType.unprocessed  # Sum x and y
    line_markers.types[5] = LineType.act  # result = x + y
    line_markers.types[6] = LineType.blank_line
    line_markers.types[7] = LineType._assert  # assert result == 2

    result = line_markers.check_arrange_act_spacing()

    assert isinstance(result, Generator)
    assert list(result) == []


def test_no_arrange():
    """
    Tests without arrangement pass
    """
    line_markers = LineMarkers(7 * [''], 5)
    line_markers.types[0] = LineType.func_def
    line_markers.types[1] = LineType.unprocessed  # Some docstring
    line_markers.types[2] = LineType.unprocessed  # Some docstring
    line_markers.types[3] = LineType.unprocessed  # Some docstring
    line_markers.types[4] = LineType.act  # result = 2 + 0
    line_markers.types[5] = LineType.blank_line
    line_markers.types[6] = LineType._assert  # assert result == 2

    result = line_markers.check_arrange_act_spacing()

    assert isinstance(result, Generator)
    assert list(result) == []


# --- FAILURES ---


def test_no_gap():
    """
    No gap raises - error points at act block
    """
    line_markers = LineMarkers(6 * [''], 5)
    line_markers.types[0] = LineType.func_def
    line_markers.types[1] = LineType.arrange  # x = 1
    line_markers.types[2] = LineType.unprocessed  # Sum do stuff
    line_markers.types[3] = LineType.act  # result = x + 3
    line_markers.types[4] = LineType.blank_line
    line_markers.types[5] = LineType._assert  # assert result == 4

    result = line_markers.check_arrange_act_spacing()

    assert isinstance(result, Generator)
    result_list = list(result)
    assert len(result_list) == 1
    assert result_list[0] == AAAError(
        line_number=8,
        offset=0,
        text='AAA03 expected 1 blank line before Act block, found none',
    )


def test_too_big_gap():
    """
    Multiple BL raises. Act block is pointed to.
    """
    line_markers = LineMarkers(8 * [''], 5)
    line_markers.types[0] = LineType.func_def
    line_markers.types[1] = LineType.arrange  # x = 1
    line_markers.types[2] = LineType.blank_line
    line_markers.types[3] = LineType.blank_line
    line_markers.types[4] = LineType.unprocessed  # Sum do stuff
    line_markers.types[5] = LineType.act  # result = x + 3
    line_markers.types[6] = LineType.blank_line
    line_markers.types[7] = LineType._assert  # assert result == 4

    result = line_markers.check_arrange_act_spacing()

    assert isinstance(result, Generator)
    result_list = list(result)
    assert len(result_list) == 1
    assert result_list[0] == AAAError(
        line_number=10,
        offset=0,
        text='AAA03 expected 1 blank line before Act block, found 2',
    )
