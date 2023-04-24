from flake8_aaa.conf import ActBlockStyle, Config


def test() -> None:
    """
    Config object can build itself with default options set.
    """
    result = Config.default_options()

    assert result == Config(act_block_style=ActBlockStyle.DEFAULT)
