
from bs4 import BeautifulSoup
import utils
from config import MedexConfig
from db import MedexDatabase
from parser import MedexParser
from repository import MedexRepository
from utils import safe_run
import sys

@safe_run
def parse_content(content: str) -> dict:
    soup = BeautifulSoup(content, 'html.parser')
    parser = MedexParser(soup)
    return parser.parse()

def scrap_site(parse_next_n_url: int):
    config = MedexConfig()
    repo = MedexRepository()
    database = MedexDatabase()

    last_path = config.get_last_path()

    for path in range(int(last_path), int(last_path) + parse_next_n_url):
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
    parse_next_n_url = 5
    print(sys.argv)
    if len(sys.argv) <= 1:
        print('-' * 20)
        print('parsing next 5 url. run "python /src/scraper.py 10" to parse next 10 url and so on..')
        print('-' * 20)
    else:
        parse_next_n_url = int(sys.argv[1])
    scrap_site(parse_next_n_url)