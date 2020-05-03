def test():
    x = 1

    result = x**2
    assert result == 4


def test_b():
    with open('f.txt') as f:

        result = f.read()
    assert result == 'Hello World!\n'
