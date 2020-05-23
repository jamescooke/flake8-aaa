import pathlib

import pytest


@pytest.fixture
def hello_world_path() -> pathlib.Path:
    """
    Location of hello_world.txt
    """
    return pathlib.Path(__file__).parent / 'data' / 'hello_world.txt'
