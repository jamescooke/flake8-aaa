import argparse
from ast import AST
from typing import Generator, List, Optional, Tuple

import asttokens
from flake8.options.manager import OptionManager

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

    default_config = Config.default_options()

    def __init__(self, tree: AST, lines: List[str], filename: str):
        self.tree = tree
        self.lines = lines
        self.filename = filename
        self.ast_tokens: Optional[asttokens.ASTTokens] = None

        self.config: Config = self.default_config

    @staticmethod
    def add_options(option_manager: OptionManager) -> None:
        option_manager.add_option(
            '--aaa-act-block-style',
            parse_from_config=True,
            default='default',
            help='Style of Act block parsing with respect to surrounding lines. (Default: default)',
        )

    @classmethod
    def parse_options(cls, option_manager: OptionManager, options: argparse.Namespace, args) -> None:
        """
        Store options passed to flake8 in config instance. Only called when
        user passes flags or sets config.

        Raises:
            UnexpectedConfigValue: When config can't be loaded.
        """
        cls.default_config = Config.load_options(options)

    def load(self) -> None:
        # ASTTokens.__init__(tree) kwarg is too strictly annotated as a Module,
        # but really I think it should be an ast.AST *or* whatever astroid
        # returns.
        # https://github.com/gristlabs/asttokens/blob/2e7470e/asttokens/asttokens.py#L110
        # We have received `tree` as `ast.AST` from Flake8 as per plugins:
        # https://github.com/PyCQA/flake8/blob/b3cee18653dff5258644963f18144c4acfe3e659/src/flake8/plugins/pyflakes.py#L75
        self.ast_tokens = asttokens.ASTTokens(''.join(self.lines), tree=self.tree)  # type: ignore[arg-type]

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
