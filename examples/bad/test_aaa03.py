def test() -> None:
    x = 1
    result = x**2

    assert result == 1


def test_b(hello_world_path) -> None:
    with open(hello_world_path) as f:
        result = f.read()

    assert result == 'Hello World!\n'
