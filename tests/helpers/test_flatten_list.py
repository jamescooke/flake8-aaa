from typing import List

import pytest

from flake8_aaa.helpers import flatten_list


@pytest.mark.parametrize(
    'items, expected_out', [
        (['X'], '"X"'),
        (['X', 'Y'], '"X" or "Y"'),
        (['X', 'Y', 'Z'], '"X", "Y" or "Z"'),
        (['X', 'Y', 'Z', 'infinity'], '"X", "Y", "Z" or "infinity"'),
    ]
)
def test(items: List[str], expected_out: str) -> None:
    items_before = items.copy()

    result = flatten_list(items)

    assert result == expected_out
    assert items == items_before


# --- FAILURES ---


def test_empty() -> None:
    """
    Empty list raises
    """
    with pytest.raises(ValueError) as excinfo:
        flatten_list([])

    assert 'Empty' in str(excinfo.value)
