from flake8_aaa import Checker


def test():
    result = Checker(None, [], '__FILENAME__')

    assert result.tree is None
    assert result.lines == []
    assert result.filename == '__FILENAME__'
    assert result.ast_tokens is None
