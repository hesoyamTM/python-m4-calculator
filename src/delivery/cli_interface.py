from abc import ABC, abstractmethod


class CLI(ABC):
    """Interface of CLI"""

    @abstractmethod
    def serve(self) -> None:
        """listen messages from cli and process them"""
        pass
