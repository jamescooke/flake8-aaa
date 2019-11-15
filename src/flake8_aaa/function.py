import ast
from typing import Generator, List, Optional

from .act_node import ActNode
from .block import Block
from .exceptions import AAAError, EmptyBlock, ValidationError
from .helpers import find_stringy_lines, format_errors, function_is_noop, get_first_token, get_last_token
from .line_markers import LineMarkers
from .types import ActNodeType, LineType


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
        self.first_line_no = get_first_token(self.node).start[0]  # type: int
        end = get_last_token(self.node).end[0]  # type: int
        self.lines = file_lines[self.first_line_no - 1:end]  # type: List[str]
        self.arrange_block = None  # type: Optional[Block]
        self.act_node = None  # type: Optional[ActNode]
        self.act_block = None  # type: Optional[Block]
        self.assert_block = None  # type: Optional[Block]
        self.line_markers = LineMarkers(self.lines, self.first_line_no)  # type: LineMarkers

    def __str__(self, errors: Optional[List[AAAError]] = None) -> str:
        out = '------+------------------------------------------------------------------------\n'
        for i, line in enumerate(self.lines):
            out += '{line_no:>2} {block}|{line}'.format(
                line_no=i + self.first_line_no,
                block=str(self.line_markers[i]),
                line=line,
            )
            if errors:
                for error in errors:
                    if error[0] == i + self.first_line_no:
                        out += '       {}^ {}\n'.format(error[1] * ' ', error[2])
        out += '------+------------------------------------------------------------------------\n'
        if errors is not None:
            out += format_errors(len(errors))
        return out

    def check_all(self) -> Generator[AAAError, None, None]:
        """
        Run everything required for checking this function.

        Returns:
            A generator of errors.

        Raises:
            ValidationError: A non-recoverable linting error is found.
        """
        # Function def
        if function_is_noop(self.node):
            return
        self.mark_bl()
        self.mark_def()
        # ACT
        # Load act block and kick out when none is found
        self.act_node = self.load_act_node()
        self.act_block = Block.build_act(self.act_node.node, self.node)
        act_block_first_line_no, act_block_last_line_no = self.act_block.get_span(0)
        # ARRANGE
        self.arrange_block = Block.build_arrange(self.node.body, act_block_first_line_no)
        # ASSERT
        assert self.act_node
        self.assert_block = Block.build_assert(self.node.body, act_block_last_line_no)
        # SPACING
        for block in ['arrange', 'act', 'assert']:
            self_block = getattr(self, '{}_block'.format(block))
            try:
                span = self_block.get_span(self.first_line_no)
            except EmptyBlock:
                continue
            self.line_markers.update(span, self_block.line_type)
        yield from self.line_markers.check_arrange_act_spacing()
        yield from self.line_markers.check_act_assert_spacing()
        yield from self.line_markers.check_blank_lines()

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
            if a_n.block_type in [ActNodeType.marked_act, ActNodeType.result_assignment]:
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
        Mark unprocessed lines that have no content and no string nodes
        covering them as blank line BL.

        Returns:
            Number of blank lines found with no stringy parent node.
        """
        counter = 0
        stringy_lines = find_stringy_lines(self.node, self.first_line_no)
        for relative_line_number, line in enumerate(self.lines):
            if relative_line_number not in stringy_lines and line.strip() == '':
                counter += 1
                self.line_markers[relative_line_number] = LineType.blank_line

        return counter
