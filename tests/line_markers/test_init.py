from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test():
    result = LineMarkers(5)

    assert result == [
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
        LineType.unprocessed,
    ]
