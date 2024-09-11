import os

import requests
from bs4 import BeautifulSoup

import utils
from utils import get_id, safe_run
from utils import content_dir

class MedexRepository:

    def __init__(self):
        pass

    def write_to_file(self, url: str, content: str) -> None:
        file_name = get_id(url)
        with open(f'{content_dir}/{file_name}.html', "w", encoding='utf-8') as f:
            f.write(content)

    @safe_run
    def get_content(self, url: str) -> str | None:
        file_name = get_id(url)
        try:
            with open(f'{content_dir}/{file_name}.html', "r", encoding='utf-8') as f:
                content = f.read()
                if content is not None:
                    if len(content) > 0:
                        return content
        except:
            utils.create_dir(content_dir)

        response = requests.get(url=url)
        if len(response.content) > 0:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.prettify()
            self.write_to_file(url, content)
            return content
        else:
            return None

    def close(self):
        pass