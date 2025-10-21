from src.application.interfaces.calculator_service import CalculatorService
from src.domain.calculator import Calculator


class Service(CalculatorService):
    """Represents calculator usecases"""

    _calculator: Calculator

    def __init__(self, calculator: Calculator) -> None:
        self._calculator = calculator

    def compute(self, expression: str) -> float:
        """Computes math expression"""
        return self._calculator.compute_with_vars(expression)

    def assign_function(self, name: str, args: list[str], expression: str) -> None:
        """Create new function"""
        self._calculator.assign_function(name, args, expression)

    def assign_new_var(self, name: str, value: str) -> None:
        """Create new variable"""
        self._calculator.assign_new_var(name, value)

    def assign_var(self, name: str, value: str) -> None:
        """Change value of existing variable"""
        self._calculator.assign_var(name, value)
