import tokenize

import pytest


@pytest.mark.parametrize('code_str', ['# stuff'])
def test_comment_token(first_token):
    result = first_token

    assert result.type == tokenize.COMMENT
    assert result.string == '# stuff'
