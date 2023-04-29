from flake8_aaa.conf import ActBlockStyle


def test() -> None:
    result = ActBlockStyle.allowed_values()

    assert result == ['default', 'large']
