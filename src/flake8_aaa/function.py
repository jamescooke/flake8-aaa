import ast
from typing import List, Optional, Tuple

from .act_node import ActNode
from .block import Block
from .exceptions import ValidationError
from .helpers import (
    add_node_parents,
    build_act_block_footprint,
    build_footprint,
    format_errors,
    function_is_noop,
    get_first_token,
    get_last_token,
)
from .line_markers import LineMarkers
from .types import ActBlockType, LineType


class Function:
    """
    Attributes:
        act_node: Act Node for the test. This is the node of the AST that looks
            like the action. Distinguish between this and the Act Block - the
            Act Block can be larger than just the node, mainly because it could
            be wrapped in context managers. Defaults to ``None``.
        arrange_block: Arrange block for this test. Defaults to ``None``.
        assert_block: Assert block. Defaults to ``None``.
        _errors: List of errors for this Function. Defaults to ``None`` when
            Function has not been checked. Empty list ``[]`` means that the
            Function has been checked and is free of errors.
        first_line_no
        lines
        line_markers: Line-wise marking for this function.
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
        self.arrange_block = None  # type: Optional[Block]
        self.act_node = None  # type: Optional[ActNode]
        self.assert_block = None  # type: Optional[Block]
        self._errors = None  # type: Optional[List[Tuple[int, int, str, type]]]
        self.line_markers = LineMarkers(len(self.lines), self.first_line_no)  # type: LineMarkers

    def __str__(self) -> str:
        out = '------+------------------------------------------------------------------------\n'
        for i, line in enumerate(self.lines):
            out += '{line_no:>2} {block}|{line}'.format(
                line_no=i + self.first_line_no,
                block=str(self.line_markers[i]),
                line=line,
            )
            if self._errors:
                for error in self._errors:
                    if error[0] == i + self.first_line_no:
                        out += '       {}^ {}\n'.format(error[1] * ' ', error[2])
        out += '------+------------------------------------------------------------------------\n'
        out += format_errors(self._errors)
        return out

    def check_act(self):
        """
        Look for an Act Node, keep it in ``act_node`` attr if found.
        """
        self.act_node = self.load_act_node()
        add_node_parents(self.node)
        self.line_markers.update(
            build_act_block_footprint(self.act_node.node, self.first_line_no, self.node),
            LineType.act_block,
        )

    def check_all(self) -> None:
        """
        Run everything required for checking this function.

        Raises:
            ValidationError: When an error is found.
        """
        # Function def
        self.mark_def()
        if function_is_noop(self.node):
            return
        # ACT
        self.check_act()
        # ARRANGE
        act_block_lineno = self.line_markers.get_first_block_lineno(LineType.act_block)
        self.arrange_block = Block.build_arrange(self.node.body, act_block_lineno)
        # ASSERT
        assert self.act_node
        self.assert_block = Block.build_assert(self.node.body, self.act_node.node.lineno)
        # SPACING
        for block in ['arrange', 'assert']:
            self.line_markers.update(
                getattr(self, '{}_block'.format(block)).get_span(self.first_line_no),
                getattr(self, '{}_block'.format(block)).line_type,
            )
        self.mark_bl()
        self.line_markers.check_arrange_act_spacing()
        self.line_markers.check_act_assert_spacing()

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

    def load_act_node(self) -> ActNode:
        """
        Raises:
            ValidationError: AAA01 when no act block is found and AAA02 when
                multiple act blocks are found.
        """
        act_nodes = ActNode.build_body(self.node.body)

        if not act_nodes:
            raise ValidationError(self.first_line_no, self.node.col_offset, 'AAA01 no Act block found in test')

        # Allow `pytest.raises` and `self.assertRaises()` in assert nodes - if
        # any of the additional nodes are `pytest.raises`, then raise
        for a_n in act_nodes[1:]:
            if a_n.block_type in [ActBlockType.marked_act, ActBlockType.result_assignment]:
                raise ValidationError(
                    self.first_line_no,
                    self.node.col_offset,
                    'AAA02 multiple Act blocks found in test',
                )

        return act_nodes[0]

    def get_line_relative_to_node(self, target_node: ast.AST, offset: int) -> str:
        """
        Raises:
            IndexError: when ``offset`` takes the request out of bounds of this
                Function's lines.
        """
        return self.lines[target_node.lineno - self.node.lineno + offset]

    def mark_def(self) -> int:
        """
        Marks up this Function's definition lines (including decorators) into
        the ``line_markers`` attribute.

        Returns:
            Number of lines found for the definition.

        Note:
            Does not spot the closing ``):`` of a function when it occurs on
            its own line.

        Note:
            Can not use ``helpers.build_footprint()`` because function nodes
            cover the whole function. In this case, just the def lines are
            wanted with any decorators.
        """
        first_line = get_first_token(self.node).start[0] - self.first_line_no  # Should usually be 0
        try:
            end_token = get_last_token(self.node.args.args[-1])
        except IndexError:
            # Fn has no args, so end of function is the fn def itself...
            end_token = get_first_token(self.node)
        last_line = end_token.end[0] - self.first_line_no
        self.line_markers.update((first_line, last_line), LineType.func_def)
        return last_line - first_line + 1

    def mark_bl(self) -> int:
        """
        Mark unprocessed lines that have no content and no nodes covering them
        as blank line BL.

        Returns:
            Number of blank lines found with no parent node.
        """
        counter = 0
        for i, line_marker in enumerate(self.line_markers):
            if line_marker is not LineType.unprocessed or self.lines[i].strip() != '':
                continue
            covered = False
            for node in self.node.body:
                # Check if this line is covered by any nodes in the function
                # and if so, then set the covered flag and bail out
                if i in build_footprint(node, self.first_line_no):
                    covered = True
                    break
            if covered:
                continue

            counter += 1
            self.line_markers[i] = LineType.blank_line

        return counter
