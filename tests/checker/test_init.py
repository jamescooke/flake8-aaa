from flake8_aaa import Checker


def test() -> None:
    result = Checker(None, [], '__FILENAME__', [])

    assert result.tree is None
    assert result.lines == []
    assert result.filename == '__FILENAME__'
    assert result.tokens == []
    assert result.ast_tokens is None
