import pytest

from flake8_aaa.helpers import is_test_file


@pytest.mark.parametrize(
    'path, expected_result',
    [
        # Non-test files give False.
        ('./helper.py', False),
        ('tests/conftest.py', False),
        ('./greatest.py', False),
        ('./greatest_dancer.py', False),
        # Finds files that start with 'test_' to be test files.
        ('./test_helpers.py', True),
        ('test_.py', True),
        ('tests/helpers/test_is_test_file.py', True),
        # Finds files that end with '_test' as test files
        ('./helpers_test.py', True),
        ('tests/helpers/is_test_file_test.py', True),
        # Finds simple test file names "test.py" and "tests.py".
        ('./test.py', True),
        ('project/app/tests.py', True),
        # Finds accidental additional underscore test file
        ('project/app/test_.py', True),
    ]
)
def test(path: str, expected_result: bool) -> None:
    result = is_test_file(path)

    assert result is expected_result
