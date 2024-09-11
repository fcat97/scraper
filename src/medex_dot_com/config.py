import json

from medex_dot_com.utils import IdGenerator
from medex_dot_com.utils import config_file_path

class MedexConfig:

    def __init__(self):
        self.get_id = IdGenerator().get_id

        try:
            with open(config_file_path, encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.config = {}

    def get_last_path(self):
        last_path = self.config.get('last_path')
        last_path = last_path if last_path is not None else "1"
        return last_path.replace("_", "")

    def save_last_path(self, url: str):
        id = self.get_id(url)
        self.config['last_path'] = id.replace("_", "")

    def save_failed(self, url):
        id = self.get_id(url).replace("_", "")
        failed = self.config.get('failed')
        if failed:
            failed.append(id)
        else:
            failed = [id]

        self.config['failed'] = failed

    def close(self):
        print(json.dumps(self.config))
        with open(config_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)


