def test() -> None:
    x = 3
    result = x**5
    assert result == 243


def test_b(hello_world_path) -> None:
    with open(hello_world_path) as f:
        result = f.read()
    assert result == 'Hello World!\n'
