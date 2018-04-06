import astroid

from flake8_aaa import Checker


def test(tmpdir):
    target_file = tmpdir.join('test.py')
    target_file.write('assert 1 + 2 == 3')
    checker = Checker(target_file.strpath)

    result = checker.load()

    assert result is None
    assert len(checker.tree.body) == 1
    assert type(checker.tree.body[0]) == astroid.Assert
    assert len(checker.ast_tokens.tokens) == 7
