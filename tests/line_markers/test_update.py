import pytest

from flake8_aaa.exceptions import ValidationError
from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test() -> None:
    """
    Diagram of line markers at start of test:

    # line 10
    DEF      # line 11
        QQQ  # line 12
        BL
        QQQ  # line 14
        QQQ
        QQQ
    # line 17
    """
    line_markers = LineMarkers(6 * [''], 11)
    line_markers.types[0] = LineType.func_def
    line_markers.types[2] = LineType.blank_line

    result = line_markers.update(12, 14, LineType.act)

    assert result == 2
    assert line_markers.types == [
        LineType.func_def,
        LineType.act,
        LineType.blank_line,
        LineType.act,
        LineType.unprocessed,
        LineType.unprocessed,
    ]


# --- FAILURE ---


def test_collision() -> None:
    """
    Diagram of line markers at start of test:

    # line 45
    DEF             # line 46   <- try to set Act
        QQQ                     <- ""
        BL
        QQQ
    # line 50
    """
    line_markers = LineMarkers(4 * [''], 46)
    line_markers.types[0] = LineType.func_def
    line_markers.types[2] = LineType.blank_line

    with pytest.raises(ValidationError) as excinfo:
        line_markers.update(46, 47, LineType.act)

    assert excinfo.value.line_number == 46
    assert excinfo.value.offset == 1
    assert excinfo.value.text.startswith('AAA99 ')
