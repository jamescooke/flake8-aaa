import pytest

from flake8_aaa.exceptions import ValidationError
from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test():
    line_markers = LineMarkers(1, 5)

    result = line_markers.update([2, 3], LineType.act_block)

    assert result is None
    assert line_markers.data == [
        LineType.unprocessed,
        LineType.act_block,
        LineType.act_block,
        LineType.unprocessed,
        LineType.unprocessed,
    ]


# --- FAILURE ---


def test_collision():
    line_markers = LineMarkers(10, 4)
    line_markers.data = [
        LineType.func_def,
        LineType.unprocessed,
        LineType.blank_line,
        LineType.unprocessed,
    ]

    with pytest.raises(ValidationError) as excinfo:
        line_markers.update([11, 12], LineType.act_block)

    assert excinfo.value.line_number == 12
    assert excinfo.value.offset == 1
    assert excinfo.value.text.startswith('AAA99 ')
