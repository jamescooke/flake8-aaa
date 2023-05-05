import ast

import pytest

from flake8_aaa import Checker
from flake8_aaa.conf import ActBlockStyle, Config


@pytest.fixture
def ast_example() -> ast.AST:
    return ast.parse('pass')


# --- TESTS ---


def test(ast_example: ast.AST) -> None:
    result = Checker(ast_example, [], '__FILENAME__')

    assert result.tree == ast_example
    assert result.lines == []
    assert result.filename == '__FILENAME__'
    assert result.ast_tokens is None
    assert result.config == Config.default_options()


def test_set_config(ast_example: ast.AST) -> None:
    """
    Config can be set in Checker
    """
    Checker.default_config = Config(act_block_style=ActBlockStyle.LARGE)

    result = Checker(ast_example, [], '__FILENAME__')

    assert result.config.act_block_style == ActBlockStyle.LARGE
