from src.domain.errors import InputError
from abc import ABC, abstractmethod


class Function(ABC):
    """Represents function of calculator"""

    @abstractmethod
    def compute(self, vars: list, debug: bool) -> float:
        """Compute function expression"""
        pass


class CalcFunction(Function):
    """Represents custom function of calculator"""

    _expression: str
    name: str
    local_var_names: list
    _debug: bool

    def __init__(self, compute, name: str, var_names: list, expr: str) -> None:
        self.name = name
        self.local_var_names = var_names
        self._compute = compute
        self._expression = expr

    def compute(self, vars: list, debug: bool) -> float:
        """Compute function expression"""

        if len(vars) > len(self.local_var_names):
            raise InputError(f"Too many arguments of function {self.name}")
        if len(vars) < len(self.local_var_names):
            raise InputError(f"Not enough arguments of function {self.name}")

        res = self._compute(self._expression, dict(zip(self.local_var_names, vars)))

        if debug:
            print(f"function name: {self.name}")
            print(f"arguments: {dict(zip(self.local_var_names, vars))}")
            print(f"_expression: {self._expression}")
            print(f"result: {res}")

        return res


class SystemFunction(Function):
    """Represents system function of calculator"""

    name: str
    local_var_names: str

    def __init__(self, name: str, func) -> None:
        self.name = name
        self._func = func

    def compute(self, vars: list, debug: bool) -> float:
        """Compute function expression"""

        res = self._func(*map(float, vars))

        if debug:
            print(f"function name: {self.name}")
            print(f"result: {res}")

        return res
