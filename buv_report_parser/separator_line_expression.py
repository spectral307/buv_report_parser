from .context import Context
from .line_expression import LineExpression
import re


class SeparatorLineExpression(LineExpression):
    pattern = "^-{10,}$"

    def __init__(self):
        super().__init__()

    @classmethod
    def parse(cls, context: Context):
        if context.pos.char != 0:
            return None

        pattern_re = re.compile(cls.pattern)

        match = pattern_re.match(context.lines[context.pos.line])
        if match:
            context.pos.line += 1
            return True

        return None
