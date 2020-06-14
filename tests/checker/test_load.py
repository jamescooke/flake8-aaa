import ast

from flake8_aaa import Checker


def test(tmpdir) -> None:
    """
    Checker is able to parse provided file at load time
    """
    target_file = tmpdir.join('test.py')
    target_file.write('assert 1 + 2 == 3\n')
    tree = ast.parse(target_file.read())
    checker = Checker(tree, ['assert 1 + 2 == 3\n'], target_file.strpath)

    checker.load()  # act

    assert len(checker.tree.body) == 1  # type: ignore
    assert type(checker.tree.body[0]) == ast.Assert  # type: ignore
    assert len(checker.ast_tokens.tokens) == 8  # type: ignore
