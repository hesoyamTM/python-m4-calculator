import math
from math import pow, sqrt
import pytest
from src.domain.calculator import Calculator
from src.domain.errors import (
    DivisionByZeroError,
    InputError,
    UnknownFunctionError,
    UnknownVariableError,
)


def test_assign_function_happy_path() -> None:
    calculator = Calculator()
    calculator.assign_function("new_func", ["a"], "a ** 2")


def test_assign_function_already_exist_new_func() -> None:
    calculator = Calculator()
    calculator.assign_function("new_func", ["a"], "a ** 2")

    with pytest.raises(InputError) as err_info:
        calculator.assign_function("new_func", ["a"], "a ** 2")
    assert str(err_info.value) == 'function "new_func" already exists'


def test_assign_function_already_exist_system_func() -> None:
    calculator = Calculator()

    with pytest.raises(InputError) as err_info:
        calculator.assign_function("sqrt", ["a"], "a ** (1/2)")
    assert str(err_info.value) == 'function "sqrt" already exists'


def test_assign_new_var_happy_path() -> None:
    calculator = Calculator()
    calculator.assign_new_var("a", "123 / 2")


def test_assign_new_var_already_exist() -> None:
    calculator = Calculator()
    calculator.assign_new_var("a", "123 * 2")

    with pytest.raises(InputError) as err_info:
        calculator.assign_new_var("a", "2 ** 2")
    assert str(err_info.value) == 'variable "a" already exists'


def test_assign_var_happy_path() -> None:
    calculator = Calculator()
    calculator.assign_new_var("a", "123 / 2")

    calculator.assign_var("a", "a + 1")


def test_assign_var_does_not_exist() -> None:
    calculator = Calculator()

    with pytest.raises(InputError) as err_info:
        calculator.assign_var("a", "2 ** 2")
    assert str(err_info.value) == 'variable "a" is not exists'


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("(((2 + 3) * (4 - 1)) ** 2) // (5 + 1)", ((2 + 3) * (4 - 1)) ** 2 // (5 + 1)),
        (
            "((8 * (3 + 2)) - ((10 - 4) ** 2)) % 7",
            ((8 * (3 + 2)) - ((10 - 4) ** 2)) % 7,
        ),
        (
            "(((15 // 3) + (2 ** 4)) * (7 - 4)) // 2",
            (((15 // 3) + (2**4)) * (7 - 4)) // 2,
        ),
        (
            "((((12 * 2) - 8) + 4) ** 2) // (3 * 2)",
            ((((12 * 2) - 8) + 4) ** 2) // (3 * 2),
        ),
        (
            "((25 - (3 * 4)) ** 2) + ((8 // 2) * 3)",
            ((25 - (3 * 4)) ** 2) + ((8 // 2) * 3),
        ),
        (
            "(((100 // 5) * (2 + 1)) - ((8 ** 2) // 4))",
            (((100 // 5) * (2 + 1)) - ((8**2) // 4)),
        ),
        (
            "((((15 + 5) * 2) - 10) ** 2) // (3 + 2)",
            ((((15 + 5) * 2) - 10) ** 2) // (3 + 2),
        ),
        (
            "((36 // (2 + 1)) ** 2) + ((5 * 3) - 2)",
            ((36 // (2 + 1)) ** 2) + ((5 * 3) - 2),
        ),
        (
            "(((8 * (4 - 1)) + (2 ** 3)) // (5 + 1)) * 3",
            (((8 * (4 - 1)) + (2**3)) // (5 + 1)) * 3,
        ),
        (
            "((((20 - 5) * 2) ** 2) // (3 * 2)) + 1",
            ((((20 - 5) * 2) ** 2) // (3 * 2)) + 1,
        ),
        ("((100 - (4 ** 3)) * ((3 + 2) // 1))", ((100 - (4**3)) * ((3 + 2) // 1))),
        (
            "(((25 * 2) - (3 ** 3)) // (4 + 1)) ** 2",
            (((25 * 2) - (3**3)) // (4 + 1)) ** 2,
        ),
        (
            "((((8 + 4) * 3) - 10) // (2 ** 2)) * 5",
            ((((8 + 4) * 3) - 10) // (2**2)) * 5,
        ),
        (
            "((15 ** 2) - ((3 * 4) + 1)) // (2 + 3)",
            ((15**2) - ((3 * 4) + 1)) // (2 + 3),
        ),
        (
            "(((100 // 4) * (2 + 1)) - ((5 ** 2) // 5))",
            (((100 // 4) * (2 + 1)) - ((5**2) // 5)),
        ),
        (
            "((((((((((2 + 3) * 4) - 5) ** 2) + 6) // 7) * 8) - 9) // 10) + 11)",
            ((((((((((2 + 3) * 4) - 5) ** 2) + 6) // 7) * 8) - 9) // 10) + 11),
        ),
        (
            "((((((((((15 - 3) * 2) + 4) // 2) ** 2) - 8) * 3) + 1) // 5) - 2)",
            ((((((((((15 - 3) * 2) + 4) // 2) ** 2) - 8) * 3) + 1) // 5) - 2),
        ),
        (
            "((((((((((8 * 3) - 4) + 2) ** 2) // 5) * 6) - 7) // 8) + 9) * 2)",
            ((((((((((8 * 3) - 4) + 2) ** 2) // 5) * 6) - 7) // 8) + 9) * 2),
        ),
        (
            "((((((((((20 + 5) - 3) * 2) // 4) ** 3) + 1) // 2) * 3) - 4) // 5)",
            ((((((((((20 + 5) - 3) * 2) // 4) ** 3) + 1) // 2) * 3) - 4) // 5),
        ),
        (
            "((((((((((100 // 5) + 3) * 2) - 4) // 2) ** 2) + 8) // 3) * 2) - 1)",
            ((((((((((100 // 5) + 3) * 2) - 4) // 2) ** 2) + 8) // 3) * 2) - 1),
        ),
        (
            "((((((((((12 * 2) - 8) + 4) ** 2) // 3) + 5) * 2) - 6) // 4) + 7)",
            ((((((((((12 * 2) - 8) + 4) ** 2) // 3) + 5) * 2) - 6) // 4) + 7),
        ),
        (
            "((((((((((25 - 5) * 3) + 2) // 2) ** 2) - 10) * 3) + 5) // 4) - 2)",
            ((((((((((25 - 5) * 3) + 2) // 2) ** 2) - 10) * 3) + 5) // 4) - 2),
        ),
        (
            "((((((((((30 + 2) - 4) * 3) // 2) ** 2) + 6) // 5) * 4) - 8) // 3)",
            ((((((((((30 + 2) - 4) * 3) // 2) ** 2) + 6) // 5) * 4) - 8) // 3),
        ),
        (
            "((((((((((18 // 2) + 3) * 4) - 5) // 3) ** 2) + 7) * 2) - 9) // 4)",
            ((((((((((18 // 2) + 3) * 4) - 5) // 3) ** 2) + 7) * 2) - 9) // 4),
        ),
        (
            "((((((((((40 - 8) * 2) + 4) // 3) ** 2) - 12) * 2) + 6) // 5) - 1)",
            ((((((((((40 - 8) * 2) + 4) // 3) ** 2) - 12) * 2) + 6) // 5) - 1),
        ),
        (
            "sqrt(pow(max(2, 3, 4), min(2, 3)) + abs(min(-5, -3, -1)))",
            sqrt(pow(max(2, 3, 4), min(2, 3)) + abs(min(-5, -3, -1))),
        ),
        (
            "pow(sqrt(max(16, 25, 36)), min(abs(-2), abs(-3)))",
            pow(sqrt(max(16, 25, 36)), min(abs(-2), abs(-3))),
        ),
        (
            "max(sqrt(pow(3, 2)), pow(min(2, 3), max(2, 3))) - abs(min(-10, -5))",
            max(sqrt(pow(3, 2)), pow(min(2, 3), max(2, 3))) - abs(min(-10, -5)),
        ),
        (
            "(pow(sqrt(abs(-64)), min(2, 1)) + max(sqrt(9), 5)) % pow(2, 3)",
            (pow(sqrt(abs(-64)), min(2, 1)) + max(sqrt(9), 5)) % pow(2, 3),
        ),
        (
            "min(pow(max(2, 1), min(4, 3)), sqrt(abs(-100))) // sqrt(pow(2, 2))",
            min(pow(max(2, 1), min(4, 3)), sqrt(abs(-100))) // sqrt(pow(2, 2)),
        ),
        (
            "sqrt(pow(abs(min(-3, -2)), max(2, 3)) + pow(sqrt(16), 2))",
            sqrt(pow(abs(min(-3, -2)), max(2, 3)) + pow(sqrt(16), 2)),
        ),
        (
            "(max(pow(2, 3), sqrt(81)) * min(abs(-4), 3)) ** sqrt(4)",
            (max(pow(2, 3), sqrt(81)) * min(abs(-4), 3)) ** sqrt(4),
        ),
        (
            "pow(min(sqrt(100), 8), max(1, 2)) % max(abs(-5), 4)",
            pow(min(sqrt(100), 8), max(1, 2)) % max(abs(-5), 4),
        ),
        (
            "abs(sqrt(pow(4, 2)) - pow(min(3, 4), sqrt(4))) * max(2, 1)",
            abs(sqrt(pow(4, 2)) - pow(min(3, 4), sqrt(4))) * max(2, 1),
        ),
        (
            "(sqrt(max(25, 36, 49)) + pow(min(1, 2), max(2, 3))) // abs(-3)",
            (sqrt(max(25, 36, 49)) + pow(min(1, 2), max(2, 3))) // abs(-3),
        ),
        (
            "pow(sqrt(abs(min(-16, -9))), sqrt(max(4, 9))) + min(pow(2, 3), 10)",
            pow(sqrt(abs(min(-16, -9))), sqrt(max(4, 9))) + min(pow(2, 3), 10),
        ),
        (
            "max(sqrt(pow(5, 2)), pow(2, min(4, 3))) - abs(sqrt(81) - max(10, 15))",
            max(sqrt(pow(5, 2)), pow(2, min(4, 3))) - abs(sqrt(81) - max(10, 15)),
        ),
        (
            "(min(pow(3, 2), sqrt(100)) * abs(-max(2, 3))) ** sqrt(min(4, 9))",
            (min(pow(3, 2), sqrt(100)) * abs(-max(2, 3))) ** sqrt(min(4, 9)),
        ),
        (
            "sqrt(pow(max(2, 3), min(3, 4)) + abs(min(-8, -4))) % pow(2, 2)",
            sqrt(pow(max(2, 3), min(3, 4)) + abs(min(-8, -4))) % pow(2, 2),
        ),
        (
            "pow(abs(sqrt(25) - max(6, 7)), min(2, 1)) + sqrt(pow(3, 2))",
            pow(abs(sqrt(25) - max(6, 7)), min(2, 1)) + sqrt(pow(3, 2)),
        ),
        (
            "max(sqrt(abs(-64)), pow(min(2, 1), max(3, 4))) // min(4, 3)",
            max(sqrt(abs(-64)), pow(min(2, 1), max(3, 4))) // min(4, 3),
        ),
        (
            "(pow(sqrt(max(9, 16)), min(3, 2)) + abs(min(-5, -3))) * sqrt(4)",
            (pow(sqrt(max(9, 16)), min(3, 2)) + abs(min(-5, -3))) * sqrt(4),
        ),
        (
            "min(pow(max(1, 2), sqrt(4)), sqrt(abs(-81))) % max(3, 4)",
            min(pow(max(1, 2), sqrt(4)), sqrt(abs(-81))) % max(3, 4),
        ),
        (
            "sqrt(pow(abs(min(-2, -1)), max(2, 3)) + sqrt(pow(4, 2)))",
            sqrt(pow(abs(min(-2, -1)), max(2, 3)) + sqrt(pow(4, 2))),
        ),
        (
            "(max(pow(2, sqrt(9)), 10) - min(abs(-5), 3)) ** sqrt(min(1, 4))",
            (max(pow(2, sqrt(9)), 10) - min(abs(-5), 3)) ** sqrt(min(1, 4)),
        ),
        (
            "pow(sqrt(abs(min(-25, -16))), min(2, 1)) + max(sqrt(36), 7)",
            pow(sqrt(abs(min(-25, -16))), min(2, 1)) + max(sqrt(36), 7),
        ),
        (
            "abs(sqrt(pow(3, 2)) - pow(min(2, 3), max(1, 2))) * min(4, 3)",
            abs(sqrt(pow(3, 2)) - pow(min(2, 3), max(1, 2))) * min(4, 3),
        ),
        (
            "(sqrt(max(100, 81)) + pow(min(1, 2), sqrt(4))) // abs(-max(2, 3))",
            (sqrt(max(100, 81)) + pow(min(1, 2), sqrt(4))) // abs(-max(2, 3)),
        ),
        (
            "pow(min(sqrt(144), 11), max(1, sqrt(1))) % sqrt(abs(-25))",
            pow(min(sqrt(144), 11), max(1, sqrt(1))) % sqrt(abs(-25)),
        ),
        (
            "max(sqrt(pow(6, 2)), pow(2, min(5, 4))) - abs(sqrt(64) - max(9, 10))",
            max(sqrt(pow(6, 2)), pow(2, min(5, 4))) - abs(sqrt(64) - max(9, 10)),
        ),
        (
            "(min(pow(2, 3), sqrt(121)) * abs(-min(3, 4))) ** sqrt(max(1, 4))",
            (min(pow(2, 3), sqrt(121)) * abs(-min(3, 4))) ** sqrt(max(1, 4)),
        ),
        (
            "sqrt(pow(max(3, 4), min(2, 1)) + abs(min(-7, -5))) % pow(2, min(3, 2))",
            sqrt(pow(max(3, 4), min(2, 1)) + abs(min(-7, -5))) % pow(2, min(3, 2)),
        ),
        (
            "pow(abs(sqrt(36) - max(5, 6)), min(3, 2)) + sqrt(pow(4, 2))",
            pow(abs(sqrt(36) - max(5, 6)), min(3, 2)) + sqrt(pow(4, 2)),
        ),
        (
            "max(sqrt(abs(-81)), pow(min(3, 2), max(2, 3))) // min(5, 4)",
            max(sqrt(abs(-81)), pow(min(3, 2), max(2, 3))) // min(5, 4),
        ),
        (
            "(pow(sqrt(max(25, 36)), min(2, 1)) + abs(min(-6, -4))) * sqrt(min(9, 16))",
            (pow(sqrt(max(25, 36)), min(2, 1)) + abs(min(-6, -4))) * sqrt(min(9, 16)),
        ),
        (
            "sqrt(pow(sqrt(abs(-16)), min(3, 2)) + pow(max(2, 3), sqrt(4)))",
            sqrt(pow(sqrt(abs(-16)), min(3, 2)) + pow(max(2, 3), sqrt(4))),
        ),
        (
            "(max(pow(2, sqrt(4)), 9) - min(abs(-7), 4)) ** sqrt(min(1, 9))",
            (max(pow(2, sqrt(4)), 9) - min(abs(-7), 4)) ** sqrt(min(1, 9)),
        ),
        (
            "pow(min(sqrt(169), 12), max(1, sqrt(4))) % sqrt(abs(-36))",
            pow(min(sqrt(169), 12), max(1, sqrt(4))) % sqrt(abs(-36)),
        ),
        (
            "abs(sqrt(pow(5, 2)) - pow(min(4, 3), max(2, 1))) * min(5, 4)",
            abs(sqrt(pow(5, 2)) - pow(min(4, 3), max(2, 1))) * min(5, 4),
        ),
        (
            "(sqrt(max(144, 121)) + pow(min(2, 1), sqrt(9))) // abs(-max(3, 4))",
            (sqrt(max(144, 121)) + pow(min(2, 1), sqrt(9))) // abs(-max(3, 4)),
        ),
    ],
)
def test_compute_with_vars_simple(expr: str, expected: float) -> None:
    calculator = Calculator()
    assert math.isclose(calculator.compute_with_vars(expr), expected)


def a(alpha, beta, gamma, delta):
    return sqrt(pow(alpha, 2) + pow(gamma, 2)) / (
        abs(max(alpha, beta, gamma, delta) - min(alpha, beta, gamma, delta)) + 1
    )


def b(x, y, z, w, v):
    return (abs(x - y) * pow(z, 2)) // (abs(sqrt(v) + min(x, y, z, w, v)) + 1)


def c(t1, t2, t3, s1, s2, s3):
    return ((max(t1, t2, t3) - min(s1, s2, s3)) ** sqrt(abs(t1 - t2))) % (
        abs(t3 * s1) + 1
    )


def d(m, n, o, p, q, r, s):
    return pow(min(m, n, o), 2) + (sqrt(s) * abs(m - n)) // (o % (abs(p) + 1) + 1)


def e(a, b, c, d, e, f, g):
    return (sqrt(pow(a, 2)) * max(c, d, e)) - (min(f, g) ** abs(a - b)) // (
        abs(c % (abs(d) + 1)) + 1
    )


def f(x, y, z, w, v, u, t):
    return (a(x, y, z, w) * b(y, z, w, v, u) - c(z, w, v, u, t, x)) // (
        abs(d(x, y, z, w, v, u, t) % (abs(e(y, z, w, v, u, t, x)) + 1) + 1)
    )


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("a(2, 3, 4, 5)", a(2, 3, 4, 5)),
        ("a(1, 2, 3, 4)", a(1, 2, 3, 4)),
        ("b(2, 3, 4, 3, 9)", b(2, 3, 4, 3, 9)),
        ("b(5, 1, 2, 3, 16)", b(5, 1, 2, 3, 16)),
        ("c(3, 5, 7, 2, 4, 6)", c(3, 5, 7, 2, 4, 6)),
        ("c(1, 2, 3, 4, 5, 6)", c(1, 2, 3, 4, 5, 6)),
        ("d(2, 3, 4, 1, 2, 3, 16)", d(2, 3, 4, 1, 2, 3, 16)),
        ("d(5, 1, 3, 2, 4, 1, 9)", d(5, 1, 3, 2, 4, 1, 9)),
        ("e(3, 2, 5, 4, 3, 2, 1)", e(3, 2, 5, 4, 3, 2, 1)),
        (
            "b(a(2, 3, 4, 5), c(1, 2, 3, 4, 5, 6), d(2, 3, 1, 4, 5, 6, 16), e(3, 2, 1, 4, 5, 6, 9), a(1, 2, 3, 4))",
            b(
                a(2, 3, 4, 5),
                c(1, 2, 3, 4, 5, 6),
                d(2, 3, 1, 4, 5, 6, 16),
                e(3, 2, 1, 4, 5, 6, 9),
                a(1, 2, 3, 4),
            ),
        ),
        (
            "d(a(1, 2, 3, 4), b(2, 1, 3, 2, 9), c(3, 2, 1, 4, 5, 6), e(4, 3, 2, 1, 5, 6, 4), a(2, 3, 4, 5), b(1, 2, 3, 2, 4), c(2, 3, 1, 4, 5, 6))",
            d(
                a(1, 2, 3, 4),
                b(2, 1, 3, 2, 9),
                c(3, 2, 1, 4, 5, 6),
                e(4, 3, 2, 1, 5, 6, 4),
                a(2, 3, 4, 5),
                b(1, 2, 3, 2, 4),
                c(2, 3, 1, 4, 5, 6),
            ),
        ),
        ("f(1, 2, 3, 4, 5, 6, 7)", f(1, 2, 3, 4, 5, 6, 7)),
        ("f(2, 3, 4, 5, 6, 7, 8)", f(2, 3, 4, 5, 6, 7, 8)),
        ("sqrt(pow(f(1,2,3,4,5,6,7), 2))", sqrt(pow(f(1, 2, 3, 4, 5, 6, 7), 2))),
        (
            "max(f(1,2,3,4,5,6,7), f(2,3,4,5,6,7,8), f(3,4,5,6,7,8,9))",
            max(f(1, 2, 3, 4, 5, 6, 7), f(2, 3, 4, 5, 6, 7, 8), f(3, 4, 5, 6, 7, 8, 9)),
        ),
        (
            "f(a(1,2,3,4), f(2,3,4,5,6,7,8), c(3,4,5,6,7,8), d(4,5,6,7,8,9,10), e(5,6,7,8,9,10,11), f(6,7,8,9,10,11,12), 7)",
            f(
                a(1, 2, 3, 4),
                f(2, 3, 4, 5, 6, 7, 8),
                c(3, 4, 5, 6, 7, 8),
                d(4, 5, 6, 7, 8, 9, 10),
                e(5, 6, 7, 8, 9, 10, 11),
                f(6, 7, 8, 9, 10, 11, 12),
                7,
            ),
        ),
    ],
)
def test_compute_with_vars_custom_functions(expr: str, expected: float) -> None:
    calculator = Calculator()

    calculator.assign_function(
        "a",
        ["alpha", "beta", "gamma", "delta"],
        "sqrt(pow(alpha, 2) + pow(gamma, 2)) / (abs(max(alpha, beta, gamma, delta) - min(alpha, beta, gamma, delta)) + 1)",
    )
    calculator.assign_function(
        "b",
        ["x", "y", "z", "w", "v"],
        "(abs(x - y) * pow(z, 2)) // (abs(sqrt(v) + min(x, y, z, w, v)) + 1)",
    )
    calculator.assign_function(
        "c",
        ["t1", "t2", "t3", "s1", "s2", "s3"],
        "((max(t1, t2, t3) - min(s1, s2, s3)) ** sqrt(abs(t1 - t2))) % (abs(t3 * s1) + 1)",
    )
    calculator.assign_function(
        "d",
        ["m", "n", "o", "p", "q", "r", "s"],
        "pow(min(m, n, o), 2) + (sqrt(s) * abs(m - n)) // (o % (abs(p) + 1) + 1)",
    )
    calculator.assign_function(
        "e",
        ["a", "b", "c", "d", "e", "f", "g"],
        "(sqrt(pow(a, 2)) * max(c, d, e)) - (min(f, g) ** abs(a - b)) // (abs(c % (abs(d) + 1)) + 1)",
    )
    calculator.assign_function(
        "f",
        ["x", "y", "z", "w", "v", "u", "t"],
        "(a(x, y, z, w) * b(y, z, w, v, u) - c(z, w, v, u, t, x)) // (abs(d(x, y, z, w, v, u, t)) % (abs(e(y, z, w, v, u, t, x)) + 1) + 1)",
    )

    print(calculator.compute_with_vars(expr), expected)
    assert math.isclose(calculator.compute_with_vars(expr), expected)


@pytest.mark.parametrize(
    "expr,expected_error",
    [
        ["12 + (2 - 4))", InputError],
        ["a(123)", UnknownFunctionError],
        ["12 + (2 - a)", UnknownVariableError],
        ["12 / (2 - 2)", DivisionByZeroError],
        ["12 % 0", DivisionByZeroError],
        ["12 // 0", DivisionByZeroError],
        ["(12 + 3", InputError],
    ],
)
def test_compute_with_vars_errors(expr: str, expected_error: type) -> None:
    with pytest.raises(expected_error) as err_info:
        Calculator().compute_with_vars(expr)
    assert err_info.type is expected_error
