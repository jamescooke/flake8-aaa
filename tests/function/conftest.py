import pytest

from flake8_aaa.function import Function

# Fixtures provide function instances in states of marking as per the order in
# the `check_all()` method.


@pytest.fixture
def function(first_node_with_tokens, lines, tokens) -> Function:
    """
    Naked unmarked function.

    Returns:
        Function created with ``first_node_with_tokens`` node and lines of
        test.
    """
    return Function(first_node_with_tokens, lines, tokens)


@pytest.fixture
def function_bl(function) -> Function:
    function.mark_bl()
    return function


@pytest.fixture
def function_bl_cmt(function_bl) -> Function:
    function_bl.mark_comments()
    return function_bl


@pytest.fixture
def function_bl_cmt_def(function_bl_cmt) -> Function:
    function_bl_cmt.mark_def()
    return function_bl_cmt


@pytest.fixture
def function_bl_cmt_def_act(function_bl_cmt_def) -> Function:
    function_bl_cmt_def.mark_act()
    return function_bl_cmt_def


@pytest.fixture
def function_bl_cmt_def_act_arr(function_bl_cmt_def_act) -> Function:
    function_bl_cmt_def_act.mark_arrange()
    return function_bl_cmt_def_act
