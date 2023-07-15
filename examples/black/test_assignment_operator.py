def test():
    """
    clear() removes all items from a list
    """
    shopping = ["apples", "bananas", "cabbages"]

    result = shopping.clear()

    assert result is None
    assert (n := len(shopping)) == 0, f"Expected 0 items of shopping, got {n}"
