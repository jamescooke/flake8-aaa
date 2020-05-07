import pytest

from flake8_aaa.exceptions import ValidationError
from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test():
    line_markers = LineMarkers(6 * [''], 1)
    line_markers.types[2] = LineType.blank_line

    result = line_markers.update(1, 3, LineType.act)

    assert result == 2
    assert line_markers.types == [
        LineType.unprocessed,
        LineType.act,
        LineType.blank_line,
        LineType.act,
        LineType.unprocessed,
        LineType.unprocessed,
    ]


# --- FAILURE ---


def test_collision():
    """
    Line Markers at start of test = [
        LineType.func_def,          < Act
        LineType.unprocessed,       < Act
        LineType.blank_line,
        LineType.unprocessed,
    ]
    """
    line_markers = LineMarkers(4 * [''], 10)
    line_markers.types[0] = LineType.func_def
    line_markers.types[2] = LineType.blank_line

    with pytest.raises(ValidationError) as excinfo:
        line_markers.update(0, 1, LineType.act)

    assert excinfo.value.line_number == 10
    assert excinfo.value.offset == 1
    assert excinfo.value.text.startswith('AAA99 ')
