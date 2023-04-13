import argparse

import pytest

from flake8_aaa.conf import ActBlockStyle, Config
from flake8_aaa.exceptions import UnexpectedConfigValue


@pytest.mark.parametrize('value', ['thin', 'THIN', 'tHiN'])
def test(value: str) -> None:
    """
    Setting is case-insensitive
    """
    options = argparse.Namespace(aaa_act_block_style=value)

    result = Config.load_options(options)

    assert result == Config(act_block_style=ActBlockStyle.THIN)


# --- FAILURES ---


def test_unknown(faker) -> None:
    """
    Unknown value for setting raises
    """
    unknown_value = faker.pystr(min_chars=5)
    options = argparse.Namespace(aaa_act_block_style=unknown_value)

    with pytest.raises(UnexpectedConfigValue) as excinfo:
        Config.load_options(options)

    assert excinfo.value.option_name == 'aaa_act_block_style'
    assert excinfo.value.value == unknown_value
    assert excinfo.value.allowed_values == ['thin']
