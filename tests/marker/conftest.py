import pytest
from flake8.defaults import MAX_LINE_LENGTH
from flake8.processor import FileProcessor


class FakeOptions:
    pass


@pytest.fixture
def fake_options():
    """
    Returns:
        FakeOptions
    """
    options = FakeOptions()
    options.hang_closing = False
    options.max_line_length = MAX_LINE_LENGTH
    options.verbose = False
    return options


@pytest.fixture
def first_token(code_str, tmpdir, fake_options):
    """
    Args:
        code_str (str): Code to be tokenized.

    Returns:
        tuple (py2)
        tokenize.TokenInfo (py3)
    """
    code_file = tmpdir.join('code_file.py')
    code_file.write(code_str)
    file_processor = FileProcessor(str(code_file), options=fake_options)
    tokens = file_processor.generate_tokens()
    return list(tokens)[0]
