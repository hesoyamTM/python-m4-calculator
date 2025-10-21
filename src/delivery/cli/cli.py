from src.application.interfaces.calculator_service import CalculatorService
from src.delivery.cli_interface import CLI

from src.delivery.cli.parser import Parser


class CalculatorCLI(CLI):
    """Represents CLI handler"""

    _parser: Parser
    _calculator_service: CalculatorService

    def __init__(self, calculator_service: CalculatorService) -> None:
        self._calculator_service: CalculatorService = calculator_service
        self._parser: Parser = Parser(self._calculator_service)

    def serve(self) -> None:
        """listen messages from cli and process them"""

        while True:
            expr = input(">> ")
            print(self._parser.parse(expr))
