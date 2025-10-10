from abc import ABC, abstractmethod


class CalculatorService(ABC):
    """Interface of calculator service"""

    @abstractmethod
    def compute(self, expression: str) -> float:
        """compute the expression"""
        pass

    @abstractmethod
    def assign_function(self, name: str, args: list[str], expression: str) -> None:
        """create new function"""
        pass

    @abstractmethod
    def assign_new_var(self, name: str, value: str) -> None:
        """assign new variable"""
        pass

    @abstractmethod
    def assign_var(self, name: str, value: str) -> None:
        """assign variable"""
        pass
