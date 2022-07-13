from .context import Context
from .line_expression import LineExpression


class BodyHeaderExpression(LineExpression):
    measurement_number_pattern = "№п/п"
    serial_number_pattern = "Зав.№"
    axis_pattern = "Ось"
    charge_sensitivity_pattern = "S,пКл/м/с2"
    iepe_sensitivity_pattern = "S,мВ/м/с2"
    bias_voltage_pattern = "Uсм,В"
    noise_pattern = "Шум,мкВ"
    axeleration_pattern = "a,м/с2"
    time_pattern = "Время"
    capacity_pattern = "C,пФ"
    resistance_pattern = "R,ГОм"

    def __init__(self):
        super().__init__()

    @classmethod
    def parse(cls, context: Context):
        if context.pos.char != 0:
            return None
