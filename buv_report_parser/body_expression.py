from .context import Context
from .expression import Expression
import re


class BodyExpression(Expression):
    def __init__(self):
        super().__init__()

        self.__separator_line_pattern = "^-{10,}$"

        self.__separator_line_re = re.compile(self.__separator_line_pattern)

    def parse(self, context: Context):
        if context.pos.char != 0:
            return False

        self._parse_blank_lines(context)

        self.__parse_separator_line(context)

    def __parse_separator_line(self, context: Context):
        match = self.__separator_line_re.match(context.lines[context.pos.line])
        if match:
            context.pos.line += 1
            return True
        return False
