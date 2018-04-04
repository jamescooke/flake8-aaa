import astroid

import pytest

from flake8_aaa.function import Function


@pytest.fixture
def function(code_str, file_tokens):
    """
    Args:
        code_str (str): Should contain only one function which can be
            extracted.

    Returns:
        Function
    """
    return Function(astroid.extract_node(code_str))
