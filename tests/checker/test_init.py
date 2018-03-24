import ast
import io
import tokenize

from flake8_aaa import Checker


def test():
    file_contents = """
def test():
    pass
"""
    tree = ast.parse(file_contents)
    file_tokens = list(tokenize.generate_tokens(io.StringIO(file_contents).readline))

    result = Checker(tree, '__FILENAME__', file_tokens)

    assert result.tree == tree
    assert result.filename == '__FILENAME__'
    assert result.file_tokens == file_tokens
    assert result.markers == {}
