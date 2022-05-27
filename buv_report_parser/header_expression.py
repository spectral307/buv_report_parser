from .context import Context
from .expression import Expression
import re
from datetime import datetime


class HeaderExpression(Expression):
    def __init__(self):
        super().__init__()

        self.date = None
        self.comment = None
        self.dut = None
        self.temperature = None
        self.atmospheric_pressure_kPa = None
        self.atmospheric_pressure_mm_Hg = None
        self.relative_humidity = None
        self.test_frequency = None
        self.user = None

        self.__title_pattern = "^Протокол измерений №\d+ от (?P<date>\d{2}.\d{2}.\d{2})\s*$"
        self.__temperature_pattern = "^Температура, °С:\s+(?P<temperature>\d{2})\s*"
        self.__atmospheric_pressure_pattern = ("^Атм. давление, кПа \(мм рт. ст.\):\s+"
                                               "(?P<atmospheric_pressure_kPa>\d{2,3},\d)\s+"
                                               "\((?P<atmospheric_pressure_mm_Hg>\d{3})\)\s*")
        self.__relative_humidity_pattern = "^Относительная влажность, %:\s+(?P<relative_humidity>\d{2})\s*"
        self.__test_frequency_pattern = "^Поверочная частота, Гц:\s+(?P<test_frequency>\d{3})\s*"
        self.__user_pattern = "^Поверитель:\s+(?P<user>[\w .-]+)\s*"

        self.__title_re = re.compile(self.__title_pattern)
        self.__temperature_re = re.compile(self.__temperature_pattern)
        self.__atmospheric_pressure_re = re.compile(
            self.__atmospheric_pressure_pattern)
        self.__relative_humidity_re = re.compile(
            self.__relative_humidity_pattern)
        self.__test_frequency_re = re.compile(self.__test_frequency_pattern)
        self.__user_re = re.compile(self.__user_pattern)

    def parse(self, context: Context):
        if context.pos.char != 0:
            return False

        if not self.__parse_title(context):
            return False

        self._parse_blank_lines(context)
        blank_lines_end_pos = context.pos.line

        if not self.__search_and_parse_temperature(context):
            return False

        temperature_line_pos = context.pos.line - 1
        context.pos.line = temperature_line_pos - 1

        if not self.__parse_dut(context):
            return False

        dut_line_pos = context.pos.line - 1
        if not (dut_line_pos == blank_lines_end_pos):
            context.pos.line = blank_lines_end_pos
            self.__parse_comment(context, dut_line_pos)
            self._parse_blank_lines(context)

        context.pos.line = temperature_line_pos + 1

        if not self.__parse_atmospheric_pressure(context):
            return False

        if not self.__parse_relative_humidity(context):
            return False

        if not self.__parse_test_frequency(context):
            return False

        self._parse_blank_lines(context)

        if not self.__parse_user(context):
            return False

    def __parse_title(self, context: Context):
        self.date = None

        match = self.__title_re.match(context.lines[context.pos.line])

        if match:
            self.date = datetime.strptime(
                match.group("date"), "%d.%m.%y").date()
            context.pos.line += 1
            return True

        return False

    def __parse_comment(self, context: Context, dut_line_pos):
        self.comment = None
        comment_lines = []
        comment_start_line_pos = context.pos.line

        for i, line in enumerate(context.lines[comment_start_line_pos:]):
            if (comment_line := line.strip()):
                if context.pos.line == dut_line_pos:
                    break
                context.pos.line += 1
                comment_lines.append(comment_line)
            else:
                break

        if (comment := "\n".join(comment_lines)):
            self.comment = comment
            return True
        return False

    def __search_and_parse_temperature(self, context: Context):
        self.temperature = None

        for i, line in enumerate(context.lines[context.pos.line:]):
            match = self.__temperature_re.match(line)
            if match:
                self.temperature = int(match.group("temperature"))
                context.pos.line += i + 1
                return True

        return False

    def __parse_dut(self, context: Context):
        self.dut = None

        self.dut = context.lines[context.pos.line].strip()

        if self.dut:
            context.pos.line += 1
            return True
        return False

    def __parse_atmospheric_pressure(self, context: Context):
        self.atmosperic_pressure_kPa = None
        self.atmosperic_pressure_mm_Hg = None

        match = self.__atmospheric_pressure_re.match(
            context.lines[context.pos.line])

        if match:
            self.atmospheric_pressure_kPa = float(
                match.group("atmospheric_pressure_kPa").replace(",", "."))
            self.atmospheric_pressure_mm_Hg = int(
                match.group("atmospheric_pressure_mm_Hg"))
            context.pos.line += 1
            return True

        return False

    def __parse_relative_humidity(self, context: Context):
        self.relative_humidity = None

        match = self.__relative_humidity_re.match(
            context.lines[context.pos.line])

        if match:
            self.relative_humidity = int(
                match.group("relative_humidity"))
            context.pos.line += 1
            return True

        return False

    def __parse_test_frequency(self, context: Context):
        self.test_frequency = None

        match = self.__test_frequency_re.match(
            context.lines[context.pos.line])

        if match:
            self.test_frequency = int(
                match.group("test_frequency"))
            context.pos.line += 1
            return True

        return False

    def __parse_user(self, context: Context):
        self.user = None

        match = self.__user_re.match(
            context.lines[context.pos.line])

        if match:
            self.user = match.group("user")
            context.pos.line += 1
            return True

        return False
