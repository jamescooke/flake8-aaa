import argparse
import dataclasses
import enum
from typing import List

from .exceptions import UnexpectedConfigValue


@enum.unique
class ActBlockStyle(enum.Enum):
    THIN = 'thin'
    # FAT = 'fat'  # TODO200

    @classmethod
    def allowed_values(cls) -> List[str]:
        """
        List of allowed values for this setting
        """
        return [item.value for item in cls]


@dataclasses.dataclass
class Config:
    """
    Note:
        Externally (flake8 and command line side) settings have the 'aaa_'
        prefix, e.g. 'aaa_act_block_style'. However internally flake8-aaa, the
        'aaa_' prefix is dropped. This happens during loading time in
        `load_options()`.
    """
    act_block_style: ActBlockStyle

    @classmethod
    def default_options(cls):
        """
        Returns:
            Config instance with default options set.
        """
        return cls(act_block_style=ActBlockStyle.THIN)

    @classmethod
    def load_options(cls, options: argparse.Namespace):
        """
        Parse custom configuration options given to flake8.

        Raises:
            UnexpectedConfigValue

        Returns:
            Config instance with values set from passed options.
        """
        try:
            act_block_style = ActBlockStyle[options.aaa_act_block_style.upper()]
        except KeyError:
            raise UnexpectedConfigValue(
                option_name='aaa_act_block_style',
                value=options.aaa_act_block_style,
                allowed_values=ActBlockStyle.allowed_values(),
            )

        return cls(act_block_style=act_block_style)
