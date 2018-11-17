import pytest

from flake8_aaa.exceptions import ValidationError
from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test():
    line_markers = LineMarkers(5, 1)

    result = line_markers.update(range(1, 3), LineType.act_block)

    assert result is None
    assert line_markers == [
        LineType.unprocessed,
        LineType.act_block,
        LineType.act_block,
        LineType.unprocessed,
        LineType.unprocessed,
    ]


# --- FAILURE ---


def test_collision():
    """
    Line Markers at start of test = [
        LineType.func_def,
        LineType.unprocessed,
        LineType.blank_line,
        LineType.unprocessed,
    ]
    """
    line_markers = LineMarkers(4, 10)
    line_markers[0] = LineType.func_def
    line_markers[2] = LineType.blank_line

    with pytest.raises(ValidationError) as excinfo:
        line_markers.update(set([1, 2]), LineType.act_block)

    assert excinfo.value.line_number == 12
    assert excinfo.value.offset == 1
    assert excinfo.value.text.startswith('AAA99 ')
