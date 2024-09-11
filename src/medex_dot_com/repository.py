import requests
from bs4 import BeautifulSoup
from domain.content_provider import ContentProvider
from medex_dot_com.utils import content_dir, create_dir, IdGenerator, safe_run


class MedexRepository(ContentProvider):

    def __init__(self):
        self.get_id = IdGenerator().get_id
        pass

    def save_content(self, url: str, html: str):
        file_name = self.get_id(url)
        with open(f'{content_dir}/{file_name}.html', "w", encoding='utf-8') as f:
            f.write(html)

    @safe_run
    def get_content(self, url: str) -> str | None:
        file_name = self.get_id(url)
        try:
            with open(f'{content_dir}/{file_name}.html', "r", encoding='utf-8') as f:
                content = f.read()
                if content is not None:
                    if len(content) > 0:
                        return content
        except:
            create_dir(content_dir)

        response = requests.get(url=url)
        if len(response.content) > 0:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.prettify()
            self.save_content(url, content)
            return content
        else:
            return None