from abc import ABC, abstractmethod
from .context import Context
import re


class Expression(ABC):
    def __init__(self):
        self._blank_line_pattern = "^ *$"
        self._blank_line_re = re.compile(self._blank_line_pattern)

    @abstractmethod
    def parse(context: Context):
        raise NotImplementedError()

    def _parse_blank_lines(self, context: Context):
        if context.pos.char != 0:
            return False

        blank_lines_found = False

        while self._blank_line_re.match(context.lines[context.pos.line]):
            context.pos.line += 1
            if not blank_lines_found:
                blank_lines_found = True

        return blank_lines_found
