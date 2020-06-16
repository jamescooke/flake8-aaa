import ast

import pytest

from flake8_aaa import Checker


@pytest.fixture
def checker(tmpdir) -> Checker:
    target_file = tmpdir.join('test.py')
    target_file.write('assert 1 + 2 == 3\n')
    tree = ast.parse(target_file.read())
    return Checker(tree, ['assert 1 + 2 == 3\n'], target_file.strpath)
