from src.application.interfaces.calculator_service import CalculatorService
import re

from src.domain.errors import CalculatorError


class Parser:
    """Parser of CLI"""

    _calculator_service: CalculatorService
    _re_assignment_new_var: re.Pattern
    _re_assignment_var: re.Pattern
    _re_assignment_new_func: re.Pattern

    def __init__(self, calculator_service: CalculatorService) -> None:
        self._calculator_service = calculator_service

        self._re_assignment_new_var = re.compile(
            r"\s*let\s+([A-Za-z_]+[A-Za-z_0-9]*)\s*=\s*(.+)\s*"
        )
        self._re_assignment_var = re.compile(
            r"\s*([A-Za-z_]+[A-Za-z_0-9]*)\s*=\s*(.+)\s*"
        )
        self._re_assignment_new_func = re.compile(
            r"\s*fn\s+([A-Za-z_]+[A-Za-z_0-9]*)\((.*?)\)\s*->\s*(.+)\s*"
        )

    def parse(self, expr: str) -> str:
        """parse input message"""
        m = self._re_assignment_new_var.match(expr)
        if m:
            var_name = m.group(1)
            var_value = m.group(2)

            try:
                self._calculator_service.assign_new_var(var_name, var_value)
            except CalculatorError as e:
                return self._error_message(e)

            return self._successful_message(
                f'new variable "{var_name}" is assigned the value "{var_value}"'
            )

        m = self._re_assignment_var.match(expr)
        if m:
            var_name = m.group(1)
            var_value = m.group(2)

            try:
                self._calculator_service.assign_var(var_name, var_value)
            except CalculatorError as e:
                return self._error_message(e)

            return self._successful_message(
                f'variable "{var_name}" is assigned the value "{var_value}"'
            )
        m = self._re_assignment_new_func.match(expr)
        if m:
            func_name = m.group(1)
            arguments = m.group(2).replace(" ", "").split(",")
            expression = m.group(3)

            try:
                self._calculator_service.assign_function(
                    func_name, arguments, expression
                )
            except CalculatorError as e:
                return self._error_message(e)

            return self._successful_message(f'function "{func_name}" is created')
        try:
            return self._successful_message(str(self._calculator_service.compute(expr)))
        except CalculatorError as e:
            return self._error_message(e)

    def _error_message(self, exception: Exception) -> str:
        return f"\033[91m{exception}\033[0m"

    def _successful_message(self, message: str) -> str:
        return f"\033[92m{message}\033[0m"
