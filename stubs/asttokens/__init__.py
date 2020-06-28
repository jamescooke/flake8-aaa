import ast
from typing import Generator, Optional

from .util import Token


class ASTTokens:

    def __init__(
        self,
        source_text: str,
        parse: bool = False,
        tree: Optional[ast.AST] = None,
        filename: str = '<unknown>',
    ):
        ...

    def get_tokens(self, node: ast.AST, include_extra: bool = False) -> Generator[Token, None, None]:
        ...
