import ast

import asttokens

from flake8_aaa.helpers import find_test_functions


def make_tree_with_tokens(code_str: str):
    tree = ast.parse(code_str)
    asttokens.ASTTokens(code_str, tree=tree)
    return tree


# --- TESTS ---


def test_empty():
    tree = make_tree_with_tokens("print('hi')")

    result = find_test_functions(tree)

    assert result == []


def test_some():
    tree = make_tree_with_tokens(
        """
import pytest


@pytest.fixture
def a_number():
    return 1


def test():
    pass


def test_thing(a_number):
    result = a_number == 1

    assert result is True
"""
    )

    result = find_test_functions(tree)

    assert [fn.name for fn in result] == ['test', 'test_thing']


def test_async_some():
    tree = make_tree_with_tokens(
        """
async def test():
    pass


async def test_thing():
    result = await a_number()

    assert result == 1
"""
    )

    result = find_test_functions(tree)

    assert [fn.name for fn in result] == ['test', 'test_thing']


def test_skip_noqa():
    tree = make_tree_with_tokens(
        """
def test_one():
    pass


def test_two(a_number):  # noqa
    result = a_number == 1

    assert result is True


def test_three(noqa):
    result = noqa.works()

    assert result is True
"""
    )

    result = find_test_functions(tree, skip_noqa=True)

    assert [fn.name for fn in result] == ['test_one', 'test_three']


def test_skip_async_noqa():
    tree = make_tree_with_tokens(
        """
async def test_one():
    pass


async def test_two(a_number):  # noqa
    result = await a_number()

    assert result == 1


async def test_three(noqa):
    result = await noqa.works()

    assert result is True
"""
    )

    result = find_test_functions(tree, skip_noqa=True)

    assert [fn.name for fn in result] == ['test_one', 'test_three']
