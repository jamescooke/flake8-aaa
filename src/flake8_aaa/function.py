import ast
import tokenize
from typing import Generator, List, Optional

from asttokens.util import Token as ASTToken

from .act_node import ActNode
from .block import Block
from .conf import ActBlockStyle, Config
from .exceptions import AAAError, EmptyBlock, ValidationError
from .helpers import function_is_noop, get_first_token, get_last_token, line_is_comment
from .line_markers import LineMarkers
from .types import ActNodeType, LineType


class Function:
    """
    Attributes:
        act_block: Block wrapper around the single Act node.
        act_node: Act Node for the test. This is the node of the AST that looks
            like the Action. Distinguish between this and the Act Block - the
            Act Block can be larger than just the node, mainly because it could
            be wrapped in context managers. Defaults to ``None``.
        arrange_block: Arrange block for this test. Defaults to ``None``.
        assert_block: Assert block. Defaults to ``None``.
        _errors: List of errors for this Function. Defaults to ``None`` when
            Function has not been checked. Empty list ``[]`` means that the
            Function has been checked and is free of errors.
        first_line_no: Line number of the first token in the test. Used to hop
            to and from relative line numberings.
        lines: Slice of the file lines that make up this test function /
            method.
        line_markers: Line-wise marking for this function.
        node: AST for the test function / method.
        tokens: Slice of the file's tokens that make up this test function.

    Note:
        "line number" means the number of the line in the file (the usual
        definition). "offset" means the number of the line in the test relative
        to the test definition.
    """

    def __init__(self, node: ast.FunctionDef, file_lines: List[str], file_tokens: List[ASTToken]):
        """
        Args:
            node
            file_lines: Lines of file under test.
            file_tokens: Tokens for file passed by Flake8.
        """
        self.node = node
        self.first_line_no: int = get_first_token(self.node).start[0]
        end: int = get_last_token(self.node).end[0]
        self.lines: List[str] = file_lines[self.first_line_no - 1:end]
        self.arrange_block: Optional[Block] = None
        self.act_node: Optional[ActNode] = None
        self.act_block: Optional[Block] = None
        self.assert_block: Optional[Block] = None
        self.line_markers = LineMarkers(self.lines, self.first_line_no)
        self.tokens = file_tokens

    def __str__(self) -> str:
        out = '------+------------------------------------------------------------------------\n'
        for i, line in enumerate(self.lines):
            out += '{line_no:>2} {block}|{line}'.format(
                line_no=i + self.first_line_no,
                block=str(self.line_markers.types[i]),
                line=line,
            )
        out += '------+------------------------------------------------------------------------\n'
        return out

    def check_all(self, config: Config) -> Generator[AAAError, None, None]:
        """
        Run everything required for checking this test. Selects relevant
        options from received config instance to pass to each "mark_" and
        "check_" method.

        Args:
            config: Instance of Config class.

        Returns:
            A generator of errors.

        Raises:
            ValidationError: A non-recoverable linting error is found.
        """
        # Function def
        if function_is_noop(self.node):
            return

        self.mark_bl()
        self.mark_comments()
        self.mark_def()

        self.mark_act(config.act_block_style)
        self.mark_arrange()
        self.mark_assert()

        yield from self.line_markers.check_arrange_act_spacing()
        yield from self.line_markers.check_act_assert_spacing()
        yield from self.line_markers.check_blank_lines()
        yield from self.line_markers.check_comment_in_act()

    def mark_bl(self) -> int:
        """
        Mark unprocessed lines that have no content and no string nodes
        covering them as blank line BL.

        Returns:
            Number of blank lines found.
        """
        counter = 0
        previous = None
        for t in self.tokens:
            if t.type == tokenize.NL:
                assert previous is not None, "Unexpected NL token before any other tokens seen"
                if previous.type == tokenize.NL or previous.type == tokenize.NEWLINE:
                    self.line_markers.types[t.start[0] - self.first_line_no] = LineType.blank_line
                    counter += 1
            previous = t

        return counter

    def mark_comments(self) -> int:
        """
        Mark unprocessed lines that are just `#` comments as CMT.

        Returns:
            Number of comment lines found.
        """
        counter = 0
        previous = None
        for t in self.tokens:
            if t.type == tokenize.COMMENT:
                assert previous is not None, "Unexpected COMMENT token before any other tokens seen"
                if previous.type == tokenize.NL or previous.type == tokenize.NEWLINE:
                    self.line_markers.types[t.start[0] - self.first_line_no] = LineType.comment
                    counter += 1
            previous = t

        return counter

    def mark_def(self) -> int:
        """
        Marks up this Function's definition lines (including decorators) into
        the ``line_markers`` attribute.

        Returns:
            Number of lines found for the definition.

        Note:
            Does not spot the closing ``):`` of a function when it occurs on
            its own line.
        """
        first_line_no = get_first_token(self.node).start[0]
        assert first_line_no == self.first_line_no

        try:
            end_token = get_last_token(self.node.args.args[-1])
        except IndexError:
            # Fn has no args, so end of function is the fn def itself...
            end_token = get_first_token(self.node)
        last_line_no = end_token.end[0]

        self.line_markers.update(first_line_no, last_line_no, LineType.func_def)
        return last_line_no - first_line_no + 1

    def mark_act(self, act_block_style: ActBlockStyle) -> int:
        """
        Finds Act node, builds it into an Act block and marks the associated
        lines in ``line_markers``.

        Args:
            act_block_style: Passed through to `build_act()` method.

        Returns:
            Number of lines covered by the Act block (used for debugging /
            testing only). Includes any comment or blank lines already marked
            inside the block's span.

        Raises:
            ValidationError: Muliple possible fatal errors:
                * AAA01 no act block found.
                * AAA02 multiple act blocks found.
                * AAA99 marking caused a collision.
        """
        # Load act block and kick out when none is found
        self.act_node = self.load_act_node()
        self.act_block = Block.build_act(
            node=self.act_node.node, test_func_node=self.node, act_block_style=act_block_style
        )
        self.line_markers.update(self.act_block.first_line_no, self.act_block.last_line_no, LineType.act)
        return self.act_block.last_line_no - self.act_block.first_line_no + 1

    def mark_arrange(self) -> int:
        """
        Mark all lines of code *before* the Act block as Arrange in
        ``line_markers``. Location of Act block is sniffed from
        ``line_markers``.

        Returns:
            Number of lines covered by the Arrange block (used for debugging /
            testing only).

        Raises:
            ValidationError: Marking caused a collision.
            ValueError: No Act block has been marked.
        """
        assert self.act_block is not None
        try:
            arrange_block = Block.build_arrange(self.node.body, self.act_block.first_line_no)
        except EmptyBlock:
            return 0

        # Prevent overhanging arrangement, for example in context manager. Stop
        # at line before Act block first line offset.
        return self.line_markers.update(
            arrange_block.first_line_no,
            min(arrange_block.last_line_no, self.act_block.first_line_no - 1),
            LineType.arrange,
        )

    def mark_assert(self) -> int:
        """
        Mark all lines of code *after* the Act block as Assert in
        ``line_markers``.

        Returns:
            Number of lines covered by the Assert block (used for debugging /
            testing only).

        Raises:
            ValidationError: AAA99 marking caused a collision.
        """
        count = 0
        # TODO get this from self.act_block
        # TODO keep length of function around instead of counting lines
        act_block_last_index = len(self.line_markers.types) - 1 - self.line_markers.types[::-1].index(LineType.act)

        # Starting from the line after the last line of Act block, to the end
        # of the test, mark everything that's unprocessed, and not a comment,
        # as an Assert block item.
        # TODO keep length of function around instead of counting lines
        for offset in range(act_block_last_index + 1, len(self.line_markers.types)):
            if self.line_markers.types[offset] == LineType.unprocessed and not line_is_comment(self.lines[offset]):
                count += 1
                self.line_markers.types[offset] = LineType._assert

        return count

    def load_act_node(self) -> ActNode:
        """
        Raises:
            ValidationError:
                * AAA01 no act block found.
                * AAA02 multiple act blocks found.
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
