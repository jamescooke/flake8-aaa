# Integration tests that flake8 runs and checks using this plugin


def test_installed(flake8dir):
    result = flake8dir.run_flake8(extra_args=['--version'])

    assert 'aaa: 0.1' in result.out


def test(flake8dir):
    flake8dir.make_py_files(
        test_plus='''
            def test():
                x = 1 + 1
                assert x == 2
        ''',
    )

    result = flake8dir.run_flake8()

    assert result.out_lines == ['./test_plus.py:3:5: AAA01 no result variable set in test']


def test_ignore(flake8dir):
    flake8dir.make_setup_cfg('''
        [flake8]
        ignore = AAA01
    ''')
    flake8dir.make_py_files(
        test_plus='''
            def test():
                x = 1 + 1
                assert x == 2
        ''',
    )

    result = flake8dir.run_flake8()

    assert result.out_lines == []


def test_noqa(flake8dir):
    flake8dir.make_py_files(
        test_plus='''
            def test():
                x = 1 + 1  # AAA act
                assert x == 2
        ''',
    )

    result = flake8dir.run_flake8()

    assert result.out_lines == []
