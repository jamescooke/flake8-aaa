import ast
import tokenize
from typing import List

import asttokens
import pytest
from flake8.defaults import MAX_LINE_LENGTH  # type: ignore
from flake8.processor import FileProcessor  # type: ignore


class FakeOptions:
    hang_closing: bool
    max_line_length: int
    max_doc_length: int
    verbose: bool


@pytest.fixture
def fake_options() -> FakeOptions:
    options = FakeOptions()
    options.hang_closing = False
    options.max_line_length = MAX_LINE_LENGTH
    options.max_doc_length = MAX_LINE_LENGTH
    options.verbose = False
    return options


@pytest.fixture
def file_tokens(code_str: str, tmpdir, fake_options: FakeOptions) -> List[tokenize.TokenInfo]:
    """
    Args:
        code_str: Code to be tokenized.

    Returns:
        Tokens for code to be checked. This emulates the behaviour of Flake8's
        ``FileProcessor`` which is using ``tokenize.generate_tokens``.
    """
    code_file = tmpdir.join('code_file.py')
    code_file.write(code_str)
    file_processor = FileProcessor(str(code_file), options=fake_options)
    tokens = file_processor.generate_tokens()
    return list(tokens)


@pytest.fixture
def first_token(file_tokens: List[tokenize.TokenInfo]) -> tokenize.TokenInfo:
    """
    Returns:
        First token of provided list.
    """
    return file_tokens[0]


@pytest.fixture
def tree(code_str: str) -> ast.Module:
    return ast.parse(code_str)


@pytest.fixture
def asttok(code_str: str, tree: ast.Module) -> asttokens.ASTTokens:
    return asttokens.ASTTokens(code_str, tree=tree)


@pytest.fixture
def first_node_with_tokens(code_str: str, tree: ast.Module, asttok: asttokens.ASTTokens):
    """
    Given ``code_str`` fixture, parse that string with ``ast.parse`` and then
    augment it with ``asttokens.ASTTokens``.

    Returns:
        ast.node: First node in parsed tree.
    """
    return tree.body[0]


@pytest.fixture
def tokens(asttok, first_node_with_tokens) -> List[tokenize.TokenInfo]:
    return list(asttok.get_tokens(
        first_node_with_tokens,
        include_extra=True,
    ))


@pytest.fixture
def lines(code_str) -> List[str]:
    """
    Given ``code_str`` chop it into lines as Flake8 would pass to a plugin -
    each line includes its newline terminator.

    Returns:
        list
    """
    return code_str.splitlines(True)
