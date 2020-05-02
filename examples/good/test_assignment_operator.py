# This is not a test, but an example of walrus used in a test file.
def assert_list_len(a):
    """
    Check list length with message. Example from
    https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions
    """
    if (n := len(a)) > 10:
            print(f"List is too long ({n} elements, expected <= 10)")

def test():
    result = Factory.create()

    assert (target := result.get())
