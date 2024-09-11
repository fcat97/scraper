
from bs4 import BeautifulSoup
from six import print_

import utils
from config import MedexConfig
from db import MedexDatabase
from parser import MedexParser
from repository import MedexRepository

def parse_content(content: str) -> dict:
    soup = BeautifulSoup(content, 'html.parser')
    parser = MedexParser(soup)
    return parser.parse()

def scrap_site():
    config = MedexConfig()
    repo = MedexRepository()
    database = MedexDatabase()

    last_path = config.get_last_path()

    for path in range(int(last_path), int(last_path) + 5):
        url = f"{utils.base_url}/{path}"
        print(f'getting {url}')
        content = repo.get_content(url = url)

        if content is not None:
            # write_to_file(url, content)
            data = parse_content(content)

            if data is not None:
                data['url'] = url
                database.post_row(data)
                config.save_last_path(url)
            else:
                config.save_failed(url)

    repo.close()
    database.close()
    config.close()

if __name__ == "__main__":
    scrap_site()