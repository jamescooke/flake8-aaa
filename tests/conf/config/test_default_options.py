from flake8_aaa.conf import ActBlockStyle, Config


def test() -> None:
    result = Config.default_options()

    assert result == Config(act_block_style=ActBlockStyle.THIN)
