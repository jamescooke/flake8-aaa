import pytest

from flake8_aaa.exceptions import ValidationError
from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType

"""
          Mark as ...
        +-------+-------+-------+-------+-------+-------+
        |   BL  |   CMT |   DEF |   ACT |   ARR |   ASS |
+-------+-------+-------+-------+-------+-------+-------+
| QQQ   |  SET  |   SET |   SET |   SET |   SET |   SET |

|  BL   | RAISE | RAISE |  SKIP |  SKIP |  SKIP |  SKIP |
| CMT   | RAISE | RAISE |  SKIP |  SKIP |  SKIP |  SKIP |

| DEF   | RAISE | RAISE | RAISE | RAISE | RAISE | RAISE |
| ACT   | RAISE | RAISE | RAISE | RAISE | RAISE | RAISE |
| ARR   | RAISE | RAISE | RAISE | RAISE | RAISE | RAISE |
| ASS   | RAISE | RAISE | RAISE | RAISE | RAISE | RAISE |
+-------+-------+-------+-------+-------+-------+-------+
"""  # yapf: disable


@pytest.mark.parametrize('new_type', [t for t in LineType if t != LineType.unprocessed])
def test_mark_qqq(new_type) -> None:
    """
    Unprocessed lines can be set as any line type

            +-------+-------+-------+-------+-------+-------+
            |   BL  |   CMT |   DEF |   ACT |   ARR |   ASS |
    +-------+-------+-------+-------+-------+-------+-------+
    | QQQ   |  SET  |   SET |   SET |   SET |   SET |   SET |
    +-------+-------+-------+-------+-------+-------+-------+
    """
    line_markers = LineMarkers(2 * [''], 1)

    result = line_markers.set(0, new_type)

    assert result is True
    assert line_markers.types == [
        new_type,
        LineType.unprocessed,
    ]


@pytest.mark.parametrize('new_type', [LineType.func_def, LineType.act, LineType.arrange, LineType._assert])
@pytest.mark.parametrize('existing_type', [LineType.blank_line, LineType.comment])
def test_mark_skip(existing_type, new_type) -> None:
    """
            +-------+-------+-------+-------+
            |   DEF |   ACT |   ARR |   ASS |
    +-------+-------+-------+-------+-------+
    |  BL   |  SKIP |  SKIP |  SKIP |  SKIP |
    | CMT   |  SKIP |  SKIP |  SKIP |  SKIP |
    +-------+-------+-------+-------+-------+
    """
    line_markers = LineMarkers([''], 0)
    line_markers.set(0, existing_type)

    result = line_markers.set(0, new_type)

    assert result is False
    assert line_markers.types == [existing_type]


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


@pytest.mark.parametrize('new_type', [LineType.blank_line, LineType.comment])
@pytest.mark.parametrize('existing_type', [LineType.blank_line, LineType.comment])
def mark_bl_cmt_on_bl_cmt(existing_type, new_type) -> None:
    """
            +-------+-------+
            |   BL  |   CMT |
    +-------+-------+-------+
    |  BL   | RAISE | RAISE |
    | CMT   | RAISE | RAISE |
    +-------+-------+-------+
    """
    line_markers = LineMarkers([''], 0)
    line_markers.set(0, existing_type)

    with pytest.raises(ValidationError):
        line_markers.set(0, new_type)

    assert line_markers.types == [existing_type]


@pytest.mark.parametrize('existing_type', [LineType.func_def, LineType.act, LineType.arrange, LineType._assert])
@pytest.mark.parametrize('new_type', [t for t in LineType if t != LineType.unprocessed])
def test_blocks_not_overwritten(existing_type, new_type) -> None:
    """
            +-------+-------+-------+-------+-------+-------+
            |   BL  |   CMT |   DEF |   ACT |   ARR |   ASS |
    +-------+-------+-------+-------+-------+-------+-------+
    | DEF   | RAISE | RAISE | RAISE | RAISE | RAISE | RAISE |
    | ACT   | RAISE | RAISE | RAISE | RAISE | RAISE | RAISE |
    | ARR   | RAISE | RAISE | RAISE | RAISE | RAISE | RAISE |
    | ASS   | RAISE | RAISE | RAISE | RAISE | RAISE | RAISE |
    +-------+-------+-------+-------+-------+-------+-------+
    """
    line_markers = LineMarkers([''], 0)
    line_markers.set(0, existing_type)

    with pytest.raises(ValidationError):
        line_markers.set(0, new_type)

    assert line_markers.types == [existing_type]


def test_out_of_range():
    line_markers = LineMarkers(2 * [''], 1)

    with pytest.raises(IndexError):
        line_markers.set(10, LineType.func_def)


def test_unprocessed():
    """
    A line can not be set as unprocessed
    """
    line_markers = LineMarkers(2 * [''], 1)

    with pytest.raises(ValueError) as excinfo:
        line_markers.set(0, LineType.unprocessed)

    assert '"???"' in str(excinfo.value)


def test_not_line_type():
    line_markers = LineMarkers(2 * [''], 1)

    with pytest.raises(ValueError) as excinfo:
        line_markers.set(1, 2)

    assert 'not LineType' in str(excinfo.value)
