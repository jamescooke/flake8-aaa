import ast
from typing import List, Optional, Tuple

from .act_block import ActBlock
from .arrange_block import ArrangeBlock
from .assert_block import AssertBlock
from .exceptions import ValidationError
from .helpers import format_errors, function_is_noop
from .types import ActBlockType, LineType


class Function:
    """
    Attributes:
        act_block: Act block for the test. Defaults to ``None``.
        _errors: List of errors for this Function. Defaults to ``None`` when
            Function has not been checked. Empty list ``[]`` means that the
            Function has been checked and is free of errors.
        first_line_no
        lines
        line_types
        node: AST for the test under lint.
    """

    def __init__(self, node: ast.FunctionDef, file_lines: List[str]):
        """
        Args:
            node
            file_lines: Lines of file under test.
        """
        self.node = node  # type: ast.FunctionDef
        self.first_line_no = self.node.lineno  # type: int
        # Ignore type because last_token is added by asttokens
        end = self.node.last_token.end[0]  # type: ignore
        self.lines = file_lines[self.first_line_no - 1:end]  # type: List[str]
        self.act_block = None  # type: Optional[ActBlock]
        self._errors = None  # type: Optional[List[Tuple[int, int, str, type]]]
        self.line_types = len(self.lines) * [LineType.unprocessed]  # type: List[LineType]

    def __str__(self) -> str:
        out = '------+------------------------------------------------------------------------\n'
        for i, line in enumerate(self.lines):
            out += ' {line_no} {block}|{line}'.format(
                line_no=i + self.first_line_no,
                block=str(self.line_types[i]),
                line=line,
            )
        out += '------+------------------------------------------------------------------------\n'
        out += format_errors(self._errors)
        return out

    def check_all(self) -> None:
        """
        Run everything required for checking this function.

        Raises:
            ValidationError: When an error is found.
        """
        if function_is_noop(self.node):
            return

        self.act_block = self.load_act_block()
        self.arrange_block = self.load_arrange_block()
        self.check_arrange_act_spacing()
        self.assert_block = self.load_assert_block()
        self.check_act_assert_spacing()

    def get_errors(self) -> List[Tuple[int, int, str, type]]:
        """
        Currently, any function can only have a single error - exceptions are
        used to pass that single error up the chain with a ValidationError.
        This wrapper flattens that exception into a list so that the API can be
        used more easily with the command line wrappers.

        Returns:
            List of errors found for this function.
        """
        self._errors = []
        try:
            self.check_all()
        except ValidationError as error:
            # Warning: Flake8 wants to know the class that raised the error,
            # this should really be changed to Checker if this function gets
            # used for ``Checker.run()``.
            self._errors = [error.to_flake8(Function)]
        return self._errors

    def load_act_block(self) -> ActBlock:
        """
        Raises:
            ValidationError
        """
        act_blocks = ActBlock.build_body(self.node.body)

        if not act_blocks:
            raise ValidationError(self.first_line_no, self.node.col_offset, 'AAA01 no Act block found in test')

        # Allow `pytest.raises` and `self.assertRaises()` in assert blocks - if
        # any of the additional act blocks are `pytest.raises` blocks, then
        # raise
        for a_b in act_blocks[1:]:
            if a_b.block_type in [ActBlockType.marked_act, ActBlockType.result_assignment]:
                raise ValidationError(
                    self.first_line_no,
                    self.node.col_offset,
                    'AAA02 multiple Act blocks found in test',
                )

        return act_blocks[0]

    def load_arrange_block(self) -> Optional[ArrangeBlock]:
        assert self.act_block
        arrange_block = ArrangeBlock()
        for node in self.node.body:
            if node == self.act_block.node:
                break
            arrange_block.add_node(node)

        if arrange_block.nodes:
            return arrange_block

        return None

    def load_assert_block(self) -> Optional[AssertBlock]:
        assert self.act_block
        assert_block = AssertBlock()
        for node in self.node.body:
            if node.lineno > self.act_block.node.lineno:
                assert_block.add_node(node)

        if assert_block.nodes:
            return assert_block

        return None

    def check_arrange_act_spacing(self) -> None:
        """
        When Function has an Arrange block, then ensure that there is a blank
        line between that and the Act block.

        Raises:
            ValidationError: When no space found.

        Note:
            Due to Flake8's error ``E303``, we do not have to check that there
            is more than one space.
        """
        assert self.act_block
        if self.arrange_block:
            line_before_act = self.get_line_relative_to_node(self.act_block.node, -1)
            if line_before_act != '\n':
                raise ValidationError(
                    line_number=self.act_block.node.lineno,
                    offset=self.act_block.node.col_offset,
                    text='AAA03 expected 1 blank line before Act block, found none',
                )

    def check_act_assert_spacing(self) -> None:
        """
        Raises:
            ValidationError: When no space found
        """
        if self.assert_block:
            line_before_assert = self.get_line_relative_to_node(self.assert_block.nodes[0], -1)
            if line_before_assert != '\n':
                raise ValidationError(
                    line_number=self.assert_block.nodes[0].lineno,
                    offset=self.assert_block.nodes[0].col_offset,
                    text='AAA04 expected 1 blank line before Assert block, found none',
                )

    def get_line_relative_to_node(self, target_node: ast.AST, offset: int) -> str:
        """
        Raises:
            IndexError: when ``offset`` takes the request out of bounds of this
                Function's lines.
        """
        return self.lines[target_node.lineno - self.node.lineno + offset]
