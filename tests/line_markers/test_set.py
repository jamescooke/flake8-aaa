import pytest

from flake8_aaa.exceptions import ValidationError
from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test():
    line_markers = LineMarkers(2 * [''], 1)

    result = line_markers.set(0, LineType.func_def)

    assert result is True
    assert line_markers.types == [
        LineType.func_def,
        LineType.unprocessed,
    ]


# --- FAILURES ---


def test_reassign():
    """
    First line of test is reassigned. (index=0)
    """
    line_markers = LineMarkers(2 * [''], 7)
    line_markers.types[0] = LineType.func_def

    with pytest.raises(ValidationError) as excinfo:
        line_markers.set(0, LineType.act)

    assert excinfo.value.line_number == 7
    assert excinfo.value.offset == 1
    assert excinfo.value.text == 'AAA99 collision when marking line 7 (index=0) as ACT, was already DEF'


def test_out_of_range():
    line_markers = LineMarkers(2 * [''], 1)

    with pytest.raises(IndexError):
        line_markers.set(10, LineType.func_def)


def test_not_line_type():
    line_markers = LineMarkers(2 * [''], 1)

    with pytest.raises(ValueError) as excinfo:
        line_markers.set(1, 2)

    assert 'not LineType' in str(excinfo.value)
