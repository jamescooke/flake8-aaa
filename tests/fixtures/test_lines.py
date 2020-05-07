import pytest


@pytest.mark.parametrize('code_str', ["""
def test():
    pass
"""])
def test_lines(lines):
    result = lines

    assert result == [
        '\n',
        'def test():\n',
        '    pass\n',
    ]
