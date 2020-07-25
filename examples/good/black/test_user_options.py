from importlinter.adapters.user_options import IniFileUserOptionReader
from importlinter.application.app_config import settings

from tests.adapters.filesystem import FakeFileSystem


def test_ini_file_reader(filename, contents, expected_options):
    settings.configure(
        FILE_SYSTEM=FakeFileSystem(
            content_map={f"/path/to/folder/{filename}": contents},
            working_directory="/path/to/folder",
        )
    )

    result = IniFileUserOptionReader().read_options()

    assert result == expected_options
