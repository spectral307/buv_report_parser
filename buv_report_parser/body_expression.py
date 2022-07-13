from .context import Context
from .multiline_expression import MultilineExpression
from .blank_lines_expression import BlankLinesExpression
from .separator_line_expression import SeparatorLineExpression
import re


class BodyExpression(MultilineExpression):
    def __init__(self):
        super().__init__()

    @classmethod
    def parse(cls, context: Context):
        if context.pos.char != 0:
            return None

        BlankLinesExpression.parse(context)

        SeparatorLineExpression.parse(context)
