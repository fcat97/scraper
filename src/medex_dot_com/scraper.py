
from medex_dot_com.config import MedexConfig
from medex_dot_com.database import MedexDatabase
from medex_dot_com.parser import MedexParser
from medex_dot_com.repository import MedexRepository
from medex_dot_com.utils import IdGenerator, safe_run
from domain.scraper import Scraper

class MedexScraper(Scraper):
    def __init__(self, base_url: str, max_iter: int = 5):
        self.base_url = base_url
        self.max_iter = max_iter
        self.iter = 0
        self.parser = MedexParser()
        self.get_id = IdGenerator().get_id

    @safe_run
    def parse_content(self, content: str) -> dict|None:
        return self.parser.parse(content)

    @safe_run
    def get_next_url(self, current_url: str) -> str | None:
        """
        get next url to parse

        :return next url or None to terminate
        """
        if self.iter >= self.max_iter:
            return None

        id = self.get_id(url=current_url)
        if id == '':
            id = 0
        else:
            id = int(id)

        self.iter = self.iter + 1

        return f"{self.base_url}/{id + 1}"

    def start_srcaping(self):
        config = MedexConfig()
        repo = MedexRepository()
        database = MedexDatabase()

        last_path = config.get_last_path()
        current_url = f"{self.base_url}/{last_path}"

        while current_url is not None:
            print(f'getting {current_url}')
            content = repo.get_content(url = current_url)

            if content is not None:
                data = self.parse_content(content)

                if data is not None:
                    data['url'] = current_url
                    database.insert_record(data)
                    database.save_status(current_url, "success", None)
                    config.save_last_path(current_url)
                else:
                    config.save_failed(current_url)
                    database.save_status(current_url, "failed", "failed to parse")
            else:
                database.save_status(current_url, "failed", "no content")

            current_url = self.get_next_url(current_url)

        database.close()
        config.close()

        print("scraping done!")