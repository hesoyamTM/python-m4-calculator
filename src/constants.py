import operator

NONE_STATE: int = 0
DIGIT_STATE: int = 1
OPERATION_STATE: int = 2
FLOAT_DIGIT_STATE: int = 3

DIGITS: str = "0123456789"

OPERATION_MAP = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "**": operator.pow,
}

OPERATION_PRIORITY = {
    "+": 0,
    "-": 0,
    "*": 1,
    "/": 1,
    "//": 1,
    "%": 1,
    "**": 2,
}

OPERATIONS = {"+", "-", "*", "/", "//", "%", "**"}
