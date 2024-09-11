from abc import ABC, abstractmethod

class Parser(ABC):

    @abstractmethod
    def parse(self, html: str) -> dict | None:
        pass