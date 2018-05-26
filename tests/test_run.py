# encoding: utf-8

# Integration tests that flake8 runs and checks using this plugin

# Some unicode text: Réne has £10 - ensure that this file is loaded with Python 2

from flake8_aaa.__about__ import __version__


def test_installed(flake8dir):
    result = flake8dir.run_flake8(extra_args=['--version'])

    assert 'aaa: {}'.format(__version__) in result.out


def test(flake8dir):
    flake8dir.make_py_files(
        test_plus='''
            def test():
                x = 1 + 1
                assert x == 2
        ''',
    )

    result = flake8dir.run_flake8()

    assert len(result.out_lines)
    assert result.out_lines[0] == './test_plus.py:1:1: AAA01 no Act block found in test'


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
                x = 1 + 1  # act
                assert x == 2
        ''',
    )

    result = flake8dir.run_flake8()

    assert result.out_lines == []
