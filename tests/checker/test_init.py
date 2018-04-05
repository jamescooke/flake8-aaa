from flake8_aaa import Checker


def test():
    result = Checker('__FILENAME__')

    assert result.filename == '__FILENAME__'
