from src.constants import OPERATION_MAP, OPERATION_PRIORITY
from src.domain.errors import InputError, MathError


class Expression:
    _nums: list
    _operations: list
    _last_sign: int
    _debug: bool
    _cur_multiplication: float

    def __init__(self, debug: bool = False) -> None:
        self._nums = []
        self._operations = []
        self._last_sign = 1
        self._debug = debug
        self._cur_multiplication = 0.1

    def append_num(self, num: int | float) -> None:
        """Append number in the stack"""
        self._cur_multiplication = 0.1

        self._nums.append(num)

        self._print_debug("append_num")

    def increase_last_num(self, num: int) -> None:
        """Add digit at the end of last number"""
        self._cur_multiplication = 0.1

        self._nums[-1] = self._nums[-1] * 10 + num

        self._print_debug("increase_last_num")

    def increase_last_float_num(self, num: int) -> None:
        """Add digit at the end of last float number"""
        self._nums[-1] = self._nums[-1] + num * self._cur_multiplication
        self._cur_multiplication /= 10

        self._print_debug("increase_last_float_num")

    def append_operation(self, operation: str) -> None:
        """Append operation in the stack"""
        self._cur_multiplication = 0.1

        self._nums[-1] *= self._last_sign
        self._last_sign = 1

        while (
            len(self._operations) > 0
            and OPERATION_PRIORITY[operation]
            <= OPERATION_PRIORITY[self._operations[-1]]
        ):
            if OPERATION_PRIORITY[operation] == 2:
                break

            self._compute_last()

        if operation == "-":
            operation = "+"
            self._last_sign = -1
        else:
            self._last_sign = 1

        self._operations.append(operation)

        self._print_debug("append_operation")

    def change_last_sign(self, sign: str) -> None:
        """Change last sign (- or +)"""
        self._cur_multiplication = 0.1

        if sign == "+":
            self._last_sign *= 1
        elif sign == "-":
            self._last_sign *= -1
        else:
            raise InputError("Undefined operation")

        self._print_debug("change_last_sign")

    def compute(self) -> float:
        """Compute whole expression"""
        if len(self._operations) >= len(self._nums):
            raise InputError("Expression is not finished")

        while len(self._operations) > 0:
            self._compute_last()

        return self._nums[0] * self._last_sign

    def _print_debug(self, method: str) -> None:
        """print debug"""
        if self._debug:
            print(f"{method}: ", self._nums, self._operations, self._last_sign)

    def _compute_last(self) -> None:
        """Compute last operation"""
        if len(self._operations) <= 0 or len(self._nums) <= 1:
            return

        self._print_debug("1 _compute_last")

        res: int = OPERATION_MAP[self._operations[-1]](
            self._nums[-2], self._nums[-1] * self._last_sign
        )
        self._last_sign = 1

        if isinstance(res, complex):
            raise MathError("No solutions in real numbers")

        self._nums.pop()
        self._nums.pop()
        self._operations.pop()

        self._nums.append(res)

        self._print_debug("2 _compute_last")
