import io
import tokenize

import pytest


@pytest.fixture
def first_token(code_str):
    """
    Args:
        code_str (str): Code to be tokenized.

    Return:
        tokenize.TokenInfo
    """
    return list(tokenize.generate_tokens(io.StringIO(code_str).readline))[0]
