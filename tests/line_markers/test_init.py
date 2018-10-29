from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test():
    result = LineMarkers(1, 5)

    assert result.first_line_no == 1
    assert result.data == [
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
    ]
