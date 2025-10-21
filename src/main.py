from src.application.calculator.calculator_service import Service
from src.delivery.cli.cli import CalculatorCLI
from src.domain.calculator import Calculator


def main() -> None:
    """
    It is the entry point to the application
    """

    calculator: Calculator = Calculator()
    calc_service: Service = Service(calculator)
    calculator_cli: CalculatorCLI = CalculatorCLI(calc_service)

    calculator_cli.serve()


if __name__ == "__main__":
    main()
