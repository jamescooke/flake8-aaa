from flake8_aaa import Checker


def test():
    result = Checker('__FILENAME__')

    assert result.filename == '__FILENAME__'
    assert result.tree is None
    assert result.ast_tokens is None
