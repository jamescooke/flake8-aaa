# You know it"s black because it does the double quotes :D


def test_simple(hello_world_path) -> None:
    """
    `with` statement is part of arrange. Blank lines are maintained around Act.
    """
    with open(hello_world_path) as f:

        result = f.read()

    assert result == "Hello World!\n"
