def test(flake8dir):
    flake8dir.make_example_py('''
    def test():
        result = 1 + 1

        assert result == 2
    ''')

    result = flake8dir.run_flake8()

    assert result.out_lines == []
