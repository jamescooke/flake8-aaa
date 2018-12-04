from flake8_aaa.line_markers import LineMarkers
from flake8_aaa.types import LineType


def test():
    line_markers = LineMarkers(8, 5)
    line_markers[0] = LineType.func_def
    line_markers[1] = LineType.unprocessed
    line_markers[2] = LineType.unprocessed
    line_markers[3] = LineType.unprocessed
    line_markers[4] = LineType.act_block  # Line 9 (4 + offset of 5)
    line_markers[5] = LineType.unprocessed
    line_markers[6] = LineType.unprocessed
    line_markers[7] = LineType.unprocessed

    result = line_markers.get_first_block_lineno(LineType.act_block)

    assert result == 9
