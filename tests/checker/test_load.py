import ast
import tokenize

from flake8_aaa import Checker


def test(tmpdir):
    """
    Checker is able to parse provided file at load time
    """
    target_file = tmpdir.join('test.py')
    target_file.write('assert 1 + 2 == 3\n')
    tree = ast.parse(target_file.read())
    tokens = tokenize.generate_tokens(target_file.readlines)
    checker = Checker(tree, ['assert 1 + 2 == 3\n'], target_file.strpath, tokens)

    result = checker.load()

    assert result is None
    assert len(checker.tree.body) == 1
    assert type(checker.tree.body[0]) == ast.Assert
    assert len(checker.ast_tokens.tokens) == 8
