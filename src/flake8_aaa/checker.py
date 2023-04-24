import argparse
from ast import AST
from typing import Generator, List, Optional, Tuple

import asttokens

from .__about__ import __short_name__, __version__
from .conf import Config
from .exceptions import TokensNotLoaded, ValidationError
from .function import Function
from .helpers import find_test_functions, is_test_file


class Checker:
    """
    Attributes:
        ast_tokens: Tokens for the file.
        filename: Name of file under check.
        lines
        tree: Tree passed from flake8.
        config: A Config instance containing passed options.
    """

    name = __short_name__
    version = __version__

    def __init__(self, tree: AST, lines: List[str], filename: str):
        self.tree = tree
        self.lines = lines
        self.filename = filename
        self.ast_tokens: Optional[asttokens.ASTTokens] = None
        self.config: Config = Config.default_options()

    @staticmethod
    def add_options(option_manager) -> None:
        """
        Note:
            No type annotation on `option_manager` because current flake8
            version required to maintain support for py37 causes problems. This
            should be fixed (or at the least rechecked) when py37 is dropped in
            #198
        """
        option_manager.add_option(
            '--aaa-act-block-style',
            parse_from_config=True,
            default='default',
            help='Style of Act block parsing with respect to surrounding lines. (Default: default)',
        )

    @classmethod
    def parse_options(cls, option_manager, options: argparse.Namespace, args) -> None:
        """
        Store options passed to flake8 in config instance. Only called when
        user passes flags or sets config.

        Raises:
            UnexpectedConfigValue: When config can't be loaded.
        """
        cls.config = Config.load_options(options)

    def load(self) -> None:
        self.ast_tokens = asttokens.ASTTokens(''.join(self.lines), tree=self.tree)

    def all_funcs(self, skip_noqa: bool = False) -> Generator[Function, None, None]:
        """
        Note:
            Checker is responsible for slicing the tokens passed to the
            Function, BUT the function is reponsible for slicing the lines.
            This is a bit strange - instead the lines should be sliced here and
            passed in so that the Function only receives data about itself.

        Raises:
            TokensNotLoaded: On fetching first value, when `load()` has not
                been called to populate `ast_tokens`.
        """
        if self.ast_tokens is None:
            raise TokensNotLoaded("ast_tokens is `None`")
        for f in find_test_functions(self.tree, skip_noqa=skip_noqa):
            yield Function(f, self.lines, list(self.ast_tokens.get_tokens(f, include_extra=True)))

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        """
        Yields:
            tuple (line_number, offset, text, check)
        """
        if is_test_file(self.filename):
            self.load()
            for func in self.all_funcs():
                try:
                    for error in func.check_all(self.config):
                        yield (error.line_number, error.offset, error.text, Checker)
                except ValidationError as error:
                    yield error.to_flake8(Checker)
