from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test():
    result = LineMarkers(5 * [''], 7)

    assert result.types == [
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
    ]
    assert result.lines == ['', '', '', '', '']
    assert result.fn_offset == 7
