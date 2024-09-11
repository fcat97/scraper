from abc import ABC, abstractmethod

class ContentProvider(ABC):

    @abstractmethod
    def save_content(self, url: str, html: str):
        pass

    @abstractmethod
    def get_content(self, url: str) -> str | None:
        pass