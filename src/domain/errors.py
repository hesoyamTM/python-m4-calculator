class CalculatorError(Exception):
    """Common programm exception"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MathError(CalculatorError):
    """Exception of math calculations"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InputError(CalculatorError):
    """Exception of wrong input data"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnknownVariableError(InputError):
    """Exception unknown var"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnknownFunctionError(InputError):
    """Exception unknown function"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DivisionByZeroError(MathError):
    """Exception division by zero"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
