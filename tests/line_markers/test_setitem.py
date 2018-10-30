import pytest

from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test():
    line_markers = LineMarkers(2)

    result = line_markers.__setitem__(0, LineType.func_def)

    assert result is None
    assert line_markers == [
        LineType.func_def,
        LineType.unprocessed,
    ]


# --- FAILURES ---


def test_reassign():
    line_markers = LineMarkers(2)
    line_markers[0] = LineType.func_def

    with pytest.raises(ValueError) as excinfo:
        line_markers[0] = LineType.act_block

    assert str(excinfo.value) == 'Collision when marking this line as ACT, was already DEF'


def test_out_of_range():
    line_markers = LineMarkers(2)

    with pytest.raises(IndexError):
        line_markers[10] = LineType.func_def


def test_not_line_type():
    line_markers = LineMarkers(2)

    with pytest.raises(ValueError) as excinfo:
        line_markers[0] = 1

    assert 'not LineType' in str(excinfo.value)


def test_not_slice():
    line_markers = LineMarkers(2)

    with pytest.raises(NotImplementedError):
        line_markers[:] = LineType.act_block
