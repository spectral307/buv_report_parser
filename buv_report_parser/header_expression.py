from .context import Context
from .multiline_expression import MultilineExpression
from .blank_lines_expression import BlankLinesExpression
import re
from datetime import datetime


class HeaderExpression(MultilineExpression):
    title_pattern = "^Протокол измерений №\d+ от (?P<date>\d{2}.\d{2}.\d{2})\s*$"
    temperature_pattern = "^Температура, °С:\s+(?P<temperature>\d{2})\s*"
    atmospheric_pressure_pattern = ("^Атм. давление, кПа \(мм рт. ст.\):\s+"
                                    "(?P<atmospheric_pressure_kPa>\d{2,3},\d)\s+"
                                    "\((?P<atmospheric_pressure_mm_Hg>\d{3})\)\s*")
    relative_humidity_pattern = "^Относительная влажность, %:\s+(?P<relative_humidity>\d{2})\s*"
    test_frequency_pattern = "^Поверочная частота, Гц:\s+(?P<test_frequency>\d{3})\s*"
    user_pattern = "^Поверитель:\s+(?P<user>[\w .-]+)\s*"

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

    @classmethod
    def parse(cls, context: Context):
        if context.pos.char != 0:
            return None

        cls.__title_re = re.compile(cls.title_pattern)
        cls.__temperature_re = re.compile(cls.temperature_pattern)
        cls.__atmospheric_pressure_re = re.compile(
            cls.atmospheric_pressure_pattern)
        cls.__relative_humidity_re = re.compile(
            cls.relative_humidity_pattern)
        cls.__test_frequency_re = re.compile(cls.test_frequency_pattern)
        cls.__user_re = re.compile(cls.user_pattern)

        if not (date := cls.__parse_title(context)):
            return None

        BlankLinesExpression.parse(context)
        blank_lines_end_pos = context.pos.line

        if not (temperature := cls.__search_and_parse_temperature(context)):
            return None

        temperature_line_pos = context.pos.line - 1
        context.pos.line = temperature_line_pos - 1

        if not (dut := cls.__parse_dut(context)):
            return None

        dut_line_pos = context.pos.line - 1
        comment = None
        if not (dut_line_pos == blank_lines_end_pos):
            context.pos.line = blank_lines_end_pos
            comment = cls.__parse_comment(context, dut_line_pos)
            BlankLinesExpression.parse(context)

        context.pos.line = temperature_line_pos + 1

        if not (atmospheric_pressure := cls.__parse_atmospheric_pressure(context)):
            return None

        if not (relative_humidity := cls.__parse_relative_humidity(context)):
            return None

        if not (test_frequency := cls.__parse_test_frequency(context)):
            return None

        BlankLinesExpression.parse(context)

        if not (user := cls.__parse_user(context)):
            return None

        header = HeaderExpression()

        header.date = date
        header.comment = comment
        header.dut = dut
        header.temperature = temperature
        header.atmospheric_pressure_kPa = atmospheric_pressure[0]
        header.atmospheric_pressure_mm_Hg = atmospheric_pressure[1]
        header.relative_humidity = relative_humidity
        header.test_frequency = test_frequency
        header.user = user

        return header

    @classmethod
    def __parse_title(cls, context: Context):
        date = None

        match = cls.__title_re.match(context.lines[context.pos.line])

        if match:
            date = datetime.strptime(
                match.group("date"), "%d.%m.%y").date()
            context.pos.line += 1

        return date

    @classmethod
    def __parse_comment(cls, context: Context, dut_line_pos):
        comment = None
        comment_lines = []
        comment_start_line_pos = context.pos.line

        for line in context.lines[comment_start_line_pos:]:
            if (comment_line := line.strip()):
                if context.pos.line == dut_line_pos:
                    break
                context.pos.line += 1
                comment_lines.append(comment_line)
            else:
                break

        if (c := "\n".join(comment_lines)):
            comment = c

        return comment

    @classmethod
    def __search_and_parse_temperature(cls, context: Context):
        temperature = None

        for i, line in enumerate(context.lines[context.pos.line:]):
            match = cls.__temperature_re.match(line)
            if match:
                temperature = int(match.group("temperature"))
                context.pos.line += i + 1

        return temperature

    @classmethod
    def __parse_dut(cls, context: Context):
        dut = None

        dut = context.lines[context.pos.line].strip()

        if dut:
            context.pos.line += 1

        return dut

    @classmethod
    def __parse_atmospheric_pressure(cls, context: Context):
        atmospheric_pressure_kPa = None
        atmospheric_pressure_mm_Hg = None

        match = cls.__atmospheric_pressure_re.match(
            context.lines[context.pos.line])

        if match:
            atmospheric_pressure_kPa = float(
                match.group("atmospheric_pressure_kPa").replace(",", "."))
            atmospheric_pressure_mm_Hg = int(
                match.group("atmospheric_pressure_mm_Hg"))
            context.pos.line += 1

        return atmospheric_pressure_kPa, atmospheric_pressure_mm_Hg

    @classmethod
    def __parse_relative_humidity(cls, context: Context):
        relative_humidity = None

        match = cls.__relative_humidity_re.match(
            context.lines[context.pos.line])

        if match:
            relative_humidity = int(
                match.group("relative_humidity"))
            context.pos.line += 1

        return relative_humidity

    @classmethod
    def __parse_test_frequency(cls, context: Context):
        test_frequency = None

        match = cls.__test_frequency_re.match(
            context.lines[context.pos.line])

        if match:
            test_frequency = int(
                match.group("test_frequency"))
            context.pos.line += 1

        return test_frequency

    @classmethod
    def __parse_user(cls, context: Context):
        user = None

        match = cls.__user_re.match(
            context.lines[context.pos.line])

        if match:
            user = match.group("user")
            context.pos.line += 1

        return user
