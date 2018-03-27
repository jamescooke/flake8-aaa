import six
import tokenize

import pytest


@pytest.fixture
def first_token(code_str):
    """
    Args:
        code_str (str): Code to be tokenized.

    Returns:
        tuple (py2)
        tokenize.TokenInfo (py3)
    """
    string_io = six.StringIO(code_str)
    return list(tokenize.generate_tokens(string_io.readline))[0]
