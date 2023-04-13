import argparse

from flake8_aaa import Checker
from flake8_aaa.conf import ActBlockStyle, Config


def test() -> None:
    options = argparse.Namespace(aaa_act_block_style='thin')

    result = Checker.parse_options(options)

    assert result is None
    assert isinstance(Checker.config, Config)
    assert Checker.config.act_block_style == ActBlockStyle.THIN
