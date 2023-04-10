import typing

import enum


@enum.unique
class ActBlockStyle(enum.Enum):
    THIN = 'thin'
    # FAT = 'fat'


Config = typing.NamedTuple('Config', [
    ('act_block_style', ActBlockStyle),
])
