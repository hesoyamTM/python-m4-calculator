import pytest
import math
from src.domain.calculator import Expression
from src.domain.errors import InputError, MathError


def test_change_last_sign_happy_path() -> None:
    expression = Expression()
    expression.change_last_sign("-")
    expression.change_last_sign("+")


@pytest.mark.parametrize(
    "op,expected_error,error_message",
    [
        ("*", InputError, "Undefined operation"),
        ("/", InputError, "Undefined operation"),
        ("%", InputError, "Undefined operation"),
    ],
)
def test_change_last_sign_undefined_operation(
    op: str, expected_error: type, error_message: str
) -> None:
    expression = Expression()
    with pytest.raises(expected_error) as err_info:
        expression.change_last_sign(op)
    assert str(err_info.value) == error_message


@pytest.mark.parametrize(
    "nums,ops,expected",
    [
        ([123, 23], ["-"], 100),
        ([123, 23], ["+"], 146),
        ([100, 23], ["*"], 2300),
        ([100, 25], ["/"], 4),
        ([123, 23], ["//"], 5),
        ([123, 23], ["/"], 123 / 23),
        ([123, 23], ["%"], 8),
        ([2, 4], ["**"], 16),
        ([2, 3, 2], ["**", "**"], 512),
        ([2, 4, 6], ["**", "+"], 22),
        ([2, 2, 4, 2], ["*", "**", "*"], 64),
        ([1, 2, 3, 4], ["/", "/", "/"], 0.04166666666),
        ([1, 2, 3, 4], ["/", "-", "/"], 1 / 2 - 3 / 4),
        ([12, 6, 5, 12], ["+", "%", "*"], 24),
        ([26, 23, 3, 5, 12], ["+", "//", "%", "*"], 50),
        ([23, 11, 4, 6, 2, 8], ["*", "+", "+", "**", "-"], 285),
        ([2, 2, 2], ["*", "-"], 2),
        ([2, 2, 2], ["+", "-"], 2),
        ([2], [], 2),
        ([2, 2, 2], ["-", "-"], -2),
        ([2, 4, 2, 3], ["-", "+", "-"], -3),
    ],
)
def test_compute_happy_path(nums: list[float], ops: list[str], expected: float) -> None:
    expression = Expression(True)
    for num in nums:
        expression.append_num(num)
        if len(ops) > 0:
            expression.append_operation(ops.pop(0))

    assert math.isclose(expression.compute(), expected)


@pytest.mark.parametrize(
    "nums,ops,expected_error,error_message",
    [
        ([12], ["+"], InputError, "Expression is not finished"),
        ([-1, 0.5], ["**"], MathError, "No solutions in real numbers"),
    ],
)
def test_compute_errors(
    nums: list[float], ops: list[str], expected_error: type, error_message: str
) -> None:
    expression = Expression(True)
    with pytest.raises(expected_error) as err_info:
        for num in nums:
            expression.append_num(num)
            if len(ops) > 0:
                expression.append_operation(ops.pop(0))
        expression.compute()
    assert str(err_info.value) == error_message
