import argparse
import dataclasses
import enum
from typing import List, Type, TypeVar

from .exceptions import UnexpectedConfigValue

_ActBlockStyle = TypeVar('_ActBlockStyle', bound='ActBlockStyle')


@enum.unique
class ActBlockStyle(enum.Enum):
    DEFAULT = 'default'
    LARGE = 'large'

    @classmethod
    def allowed_values(cls: Type[_ActBlockStyle]) -> List[str]:
        """
        List of allowed values for this setting
        """
        return [item.value for item in cls]


_Config = TypeVar('_Config', bound='Config')


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
    def default_options(cls: Type[_Config]) -> _Config:
        """
        Returns:
            Config instance with default options set.
        """
        return cls(act_block_style=ActBlockStyle.DEFAULT)

    @classmethod
    def load_options(cls: Type[_Config], options: argparse.Namespace) -> _Config:
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
