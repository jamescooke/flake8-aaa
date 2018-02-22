def test(flake8dir):
    flake8dir.make_py_files(example='''
def test():
    x = 1 + 1
    assert x == 2
''')

    result = flake8dir.run_flake8()

    assert result.out_lines == ['./example.py:1:2: AAA01 no result variable set in test']
