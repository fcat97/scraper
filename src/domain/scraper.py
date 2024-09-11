from abc import ABC, abstractmethod

class Scraper(ABC):

    @abstractmethod
    def start_srcaping(self):
        pass

    @abstractmethod
    def get_next_url(self, current_url: str) -> str | None:
        pass