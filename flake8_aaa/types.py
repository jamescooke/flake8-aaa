from enum import Enum

ActBlockType = Enum(  # pylint: disable=invalid-name
    'ActBlockType',
    'marked_act pytest_raises result_assignment unittest_raises',
)
