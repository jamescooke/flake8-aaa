from flake8_aaa.conf import Config
import pytest


@pytest.mark.parametrize('value', ['thin', 'THIN'])
def test(value: str) -> None:
    result = Config(act_block_style=value)

    assert result.act_block_style == 'thin'


# --- FAILURES ---


# TODOBLACK: make this strict
@pytest.mark.xfail
def test_not_value() -> None:
    with pytest.raises(ValueError):
        Config(act_block_style='x')
