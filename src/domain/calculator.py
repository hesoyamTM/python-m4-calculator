from typing import Callable, Generator
from src.constants import (
    NONE_STATE,
    DIGIT_STATE,
    OPERATION_STATE,
    DIGITS,
    FLOAT_DIGIT_STATE,
    OPERATIONS,
)
from src.domain.errors import (
    DivisionByZeroError,
    InputError,
    UnknownFunctionError,
    UnknownVariableError,
)
from src.domain.expression import Expression
import re

from src.domain.calc_function import CalcFunction, SystemFunction


class Calculator:
    """Represents calculator model"""

    _variables: dict[str, float]
    _functions: dict[str, Callable[[list[str], bool], float]]

    def __init__(self) -> None:
        self._variables = {"DEBUG": 0}

        sqrt_func = CalcFunction(
            self.parse_and_compute_with_vars, "sqrt", ["a"], "a ** (1/2)"
        )
        pow_func = CalcFunction(
            self.parse_and_compute_with_vars, "pow", ["a", "b"], "a ** b"
        )
        abs_func = SystemFunction("abs", abs)
        max_func = SystemFunction("max", max)
        min_func = SystemFunction("min", min)

        self._functions = {
            sqrt_func.name: sqrt_func.compute,
            pow_func.name: pow_func.compute,
            abs_func.name: abs_func.compute,
            max_func.name: max_func.compute,
            min_func.name: min_func.compute,
        }

    def assign_function(self, name: str, args: list[str], expression: str) -> None:
        """Create new function"""

        if name in self._functions:
            raise InputError('function "{}" already exists'.format(name))

        func = CalcFunction(
            self.parse_and_compute_with_vars,
            name,
            args,
            expression,
        )
        self._functions[name] = func.compute

    def assign_new_var(self, name: str, value: str) -> None:
        """Create new variable"""

        if name in self._variables:
            raise InputError('variable "{}" already exists'.format(name))

        computed_value = self.parse_and_compute(value)

        self._variables[name] = computed_value

    def assign_var(self, name: str, value: str) -> None:
        """Change value of existing variable"""

        if name not in self._variables:
            raise InputError('variable "{}" is not exists'.format(name))

        var_value = self.parse_and_compute(value)

        self._variables[name] = var_value

    def parse_and_compute_with_vars(self, data: str, vars: dict) -> float:
        """Parse with local variables and compute expression"""

        for var, value in vars.items():
            data = re.sub(rf"(?<=[^\w)]){var}(?=[^\w(])", str(value), f" {data} ")

        for var, value in self._variables.items():
            data = re.sub(rf"(?<=[^\w)]){var}(?=[^\w(])", str(value), f" {data} ")

        for func_name, func_compute in self._functions.items():
            found_index = data.find(func_name + "(")

            while found_index != -1:
                start = found_index + len(func_name) + 1
                end = start
                bracket_cnt = 1

                for i, c in enumerate(data[start:]):
                    if c == "(":
                        bracket_cnt += 1
                    if c == ")":
                        bracket_cnt -= 1

                    end = start + i

                    if bracket_cnt == 0:
                        break

                data = data.replace(
                    data[start - len(func_name) - 1 : end + 1],
                    str(
                        func_compute(
                            [
                                str(self.parse_and_compute(num))
                                for num in self._split_arguments(data[start:end])
                            ],
                            self._variables["DEBUG"] == 1,
                        )
                    ),
                    1,
                )

                found_index = data.find(func_name)

        return self.compute(data)

    def _split_arguments(self, args: str) -> Generator[str]:
        args = args.replace(" ", "")
        left_ptr = 0
        bracket_cnt = 0

        for right_ptr, c in enumerate(args):
            if c == "(":
                bracket_cnt += 1
            if c == ")":
                bracket_cnt -= 1

            if c == "," and bracket_cnt == 0:
                yield args[left_ptr:right_ptr]
                left_ptr = right_ptr + 1

        yield args[left_ptr:]

    def parse_and_compute(self, data: str) -> float:
        """Parse global variables and functions and compute expression"""
        return self.parse_and_compute_with_vars(data, {})

    def compute(self, expr: str) -> float:
        """Read input expression and compute it"""

        expressions = [Expression(self._variables["DEBUG"] == 1)]

        state = NONE_STATE
        next = False

        for i, c in enumerate(expr):
            if c == " " or c == "\n" or next:
                next = False
                continue

            try:
                if c in DIGITS:
                    if state == DIGIT_STATE:
                        expressions[-1].increase_last_num(int(c))
                    elif state == NONE_STATE or state == OPERATION_STATE:
                        expressions[-1].append_num(int(c))
                        state = DIGIT_STATE
                    elif state == FLOAT_DIGIT_STATE:
                        expressions[-1].increase_last_float_num(int(c))

                elif c == "(":
                    expressions.append(Expression(self._variables["DEBUG"] == 1))
                elif c == ")":
                    try:
                        res: float = expressions[-1].compute()
                        expressions.pop()
                        expressions[-1].append_num(res)
                    except IndexError:
                        pointes = "".join(
                            [" " for i in range(i)]
                            + ["^" for i in range(i, i + 1)]
                            + [" " for i in range(i + 1, len(expr))]
                        )
                        message_error = f"{expr}\n{pointes}"
                        raise InputError(
                            f"Unnecessary bracket at {i}:\n\n{message_error}\n"
                        )

                elif c == ".":
                    state = FLOAT_DIGIT_STATE

                elif c in OPERATIONS:
                    op = c
                    if c + expr[i + 1] == "//" or c + expr[i + 1] == "**":
                        op = c + expr[i + 1]
                        next = True

                    if state == OPERATION_STATE or state == NONE_STATE:
                        expressions[-1].change_last_sign(op)
                    else:
                        expressions[-1].append_operation(op)
                        state = OPERATION_STATE

                else:
                    right = i
                    isFuncError = False
                    for r, rc in enumerate(expr[i + 1 :]):
                        right = r
                        if rc == "(":
                            isFuncError = True
                            break
                        elif rc in DIGITS or rc in OPERATIONS or rc == " ":
                            break

                    pointes = "".join(
                        [" " for i in range(i)]
                        + ["^" for i in range(i, i + right + 1)]
                        + [" " for i in range(i + right + 1, len(expr))]
                    )
                    message_error = f"{expr}\n{pointes}"

                    if isFuncError:
                        raise UnknownFunctionError(
                            f'Unknown function "{expr[i : i + right + 1]}()" at {i}:\n\n{message_error}\n'
                        )
                    else:
                        raise UnknownVariableError(
                            f'Unknown variable "{expr[i : i + right + 1]}" at {i}:\n\n{message_error}\n'
                        )
            except ZeroDivisionError:
                pointes = "".join(
                    [" " for i in range(i)]
                    + ["^" for i in range(i, i + 1)]
                    + [" " for i in range(i + 1, len(expr))]
                )
                message_error = f"{expr}\n{pointes}"
                raise DivisionByZeroError(
                    f"Division by zero at {i}:\n\n{message_error}\n"
                )

        if len(expressions) > 1:
            pointes = "".join([" " for i in range(len(expr) - 2)] + ["^"])
            message_error = f"{expr}\n{pointes}"
            raise InputError(f"Unnecessary bracket:\n\n{message_error}\n")

        try:
            return expressions[-1].compute()
        except ZeroDivisionError:
            message_error = f"{expr}"
            raise DivisionByZeroError(f"Division by zero:\n\n{message_error}\n")
