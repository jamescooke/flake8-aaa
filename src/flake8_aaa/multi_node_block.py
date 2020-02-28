import ast
from abc import ABCMeta, abstractmethod
from typing import List  # noqa: F401

from .types import LineType


class MultiNodeBlock(metaclass=ABCMeta):

    @property
    @abstractmethod
    def line_type(self) -> LineType:
        pass

    def __init__(self) -> None:
        self.nodes: List[ast.AST] = []

    @abstractmethod
    def add_node(self, node: ast.AST) -> bool:
        pass
