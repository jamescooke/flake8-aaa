import pytest

from flake8_aaa.exceptions import ValidationError
from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test_comment_before_act():
    """
    Comment before Act passes
    """
    line_markers = LineMarkers(7)
    line_markers[0] = LineType.arrange_block  # x = 1
    line_markers[1] = LineType.arrange_block  # y = 2
    line_markers[2] = LineType.blank_line
    line_markers[3] = LineType.unprocessed  # Sum x and y
    line_markers[4] = LineType.act_block  # result = x + y
    line_markers[5] = LineType.blank_line
    line_markers[6] = LineType.assert_block  # assert result == 2

    result = line_markers.check_arrange_act_spacing()

    assert result is None


def test_no_arrange():
    """
    Tests without arrangement pass
    """
    line_markers = LineMarkers(7)
    line_markers[0] = LineType.unprocessed  # Some docstring
    line_markers[1] = LineType.unprocessed  # Some docstring
    line_markers[2] = LineType.unprocessed  # Some docstring
    line_markers[3] = LineType.act_block  # result = 2 + 0
    line_markers[4] = LineType.blank_line
    line_markers[5] = LineType.assert_block  # assert result == 2

    result = line_markers.check_arrange_act_spacing()

    assert result is None
