import ast

from flake8_aaa import Checker


def test_async_test_function_without_act() -> None:
    code = """async def test_async():
    setup = 1

    await thing()

    assert setup == 1
"""
    checker = Checker(ast.parse(code), code.splitlines(keepends=True), 'test.py')

    result = list(checker.run())

    assert result[0][:3] == (1, 0, 'AAA01 no Act block found in test')
