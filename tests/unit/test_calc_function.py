import math
import pytest
from src.domain.calc_function import CalcFunction
from src.domain.calculator import Calculator
from src.domain.errors import InputError


@pytest.mark.parametrize(
    "var_names,expression,agrs,expected",
    [
        [["a", "b"], "a + b", ["5", "3"], 8],
        [["x", "y"], "x - y", ["10", "4"], 6],
        [["num1", "num2"], "num1 * num2", ["7", "6"], 42],
        [["a", "b"], "a / b", ["15", "3"], 5.0],
        [["a", "b", "c"], "a + b * c", ["3", "4", "5"], 23],
        [["x", "y", "z"], "(x + y) * z", ["2", "3", "4"], 20],
        [["a", "b"], "a - b", ["0", "0"], 0],
        [["num1", "num2"], "num1 / num2", ["1", "2"], 0.5],
        [["x", "y"], "x // y", ["10", "2"], 5],
        [["a", "b"], "a % b", ["10", "3"], 1],
        [["base", "exp"], "base ** exp", ["3", "3"], 27],
        [["a", "b", "c"], "a * b + c", ["2", "3", "1"], 7],
        [["x", "y", "z"], "x - y + z", ["10", "3", "2"], 9],
        [["a", "b"], "a / b", ["100", "4"], 25.0],
        [["num1", "num2"], "num1 // num2", ["20", "4"], 5],
        [["x", "y"], "x % y", ["7", "7"], 0],
        [["a", "b", "c"], "a ** b - c", ["2", "3", "1"], 7],
        [["a"], "sqrt(a)", ["16"], 4.0],
        [["x", "y"], "sqrt(x * y)", ["9", "4"], 6.0],
        [["a", "b"], "sqrt(a ** 2 + b ** 2)", ["3", "4"], 5.0],
        [["a"], "abs(a)", ["-5"], 5],
        [["x"], "abs(x)", ["7"], 7],
        [["a", "b"], "abs(a - b)", ["3", "8"], 5],
        [["a", "b"], "pow(a, b)", ["2", "3"], 8],
        [["x", "y"], "pow(x, y)", ["5", "2"], 25],
        [["a", "b", "c"], "min(a, b, c)", ["5", "2", "8"], 2],
        [["x", "y", "z"], "max(x, y, z)", ["3", "9", "4"], 9],
        [["a", "b"], "min(a, b)", ["7", "7"], 7],
        [["a", "b"], "sqrt(pow(a, 2) + pow(b, 2))", ["3", "4"], 5.0],
        [["x", "y", "z"], "max(min(x, y), z)", ["5", "3", "4"], 4],
        [["a", "b", "c"], "abs(min(a, b, c))", ["-2", "3", "-5"], 5],
        [["a", "b"], "(sqrt(a) + sqrt(b)) * 2", ["9", "16"], 14.0],
        [["x", "y"], "pow(x, 2) - pow(y, 2)", ["5", "3"], 16],
        [["a", "b", "c"], "max(a, b, c) - min(a, b, c)", ["10", "3", "7"], 7],
        [["a"], "a + 10 - (5 * 2)", ["7"], 7],
        [["x", "y"], "(x * 2) + (y * 3) - 5", ["4", "3"], 12],
        [["a", "b"], "sqrt(pow(abs(a), 2) + pow(abs(b), 2))", ["-3", "-4"], 5.0],
        [["x", "y", "z"], "max(x, min(y, z)) + abs(x - y)", ["5", "8", "3"], 8],
        [["a", "b", "c"], "((a + b) * c) // (a - b)", ["8", "2", "5"], 8],
        [["x", "y"], "(x ** 2 + y ** 2) % 10", ["3", "4"], 5],
        [["a", "b"], "pow(sqrt(a), sqrt(b))", ["16", "9"], 64.0],
        [["x", "y", "z"], "min(max(x, y), max(y, z))", ["2", "5", "3"], 5],
        [["a", "b"], "(a // b) + (a % b)", ["17", "5"], 5],
        [["x", "y"], "sqrt(x) / sqrt(y)", ["25", "4"], 2.5],
        [["a", "b", "c"], "pow(min(a, b, c), max(a, b, c))", ["2", "3", "1"], 1],
        [["x", "y"], "abs(sqrt(x) - sqrt(y))", ["25", "9"], 2.0],
        [["a", "b"], "a // b", ["17", "5"], 3],
        [["x", "y"], "x % y", ["17", "5"], 2],
        [["base", "exp"], "base ** exp", ["2", "8"], 256],
    ],
)
def test_compute_happy_path(
    var_names: list[str], expression: str, agrs: list[str], expected: float
) -> None:
    calc_func = CalcFunction(
        Calculator().compute_with_local_vars, "test", var_names, expression
    )
    assert math.isclose(calc_func.compute(agrs, True), expected)


@pytest.mark.parametrize(
    "var_names,expression,args,error_type,err_message",
    [
        [
            ["a", "b"],
            "a + b",
            ["1"],
            InputError,
            "Not enough arguments of function test",
        ],
        [
            ["a", "b"],
            "a + b",
            ["1", "2", "3"],
            InputError,
            "Too many arguments of function test",
        ],
    ],
)
def test_compute_errors(
    var_names: list[str],
    expression: str,
    args: list[str],
    error_type: type,
    err_message: str,
) -> None:
    calc_func = CalcFunction(
        Calculator().compute_with_local_vars, "test", var_names, expression
    )
    with pytest.raises(error_type) as err_info:
        calc_func.compute(args, True)
    assert str(err_info.value) == err_message
