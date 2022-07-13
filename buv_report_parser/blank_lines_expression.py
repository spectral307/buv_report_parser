from .context import Context
from .multiline_expression import MultilineExpression
import re


class BlankLinesExpression(MultilineExpression):
    pattern = "^ *$"

    def __init__(self):
        super().__init__()

    @classmethod
    def parse(cls, context: Context):
        if context.pos.char != 0:
            return None

        pattern_re = re.compile(cls.pattern)

        blank_lines_found = None

        while pattern_re.match(context.lines[context.pos.line]):
            context.pos.line += 1
            if not blank_lines_found:
                blank_lines_found = True

        return blank_lines_found
