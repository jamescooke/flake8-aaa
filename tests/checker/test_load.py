import ast


def test(checker) -> None:
    """
    Checker is able to parse provided file at load time
    """
    checker.load()  # act

    # TODO strip ignores
    assert len(checker.tree.body) == 1  # type: ignore
    assert isinstance(checker.tree.body[0], ast.Assert)
    assert len(checker.ast_tokens.tokens) == 8  # type: ignore
