from flake8_aaa.conf import Config


def test(faker) -> None:
    """
    Any value can be set via dunder init
    """
    value = faker.pystr()

    result = Config(act_block_style=value)

    assert result.act_block_style == value
