import json

from utils import get_id


class MedexConfig:

    def __init__(self):
        try:
            with open("../config.json", encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.config = {}

    def get_last_path(self):
        last_path = self.config.get('last_path')
        last_path = last_path if last_path is not None else "1"
        return last_path.replace("_", "")

    def save_last_path(self, url: str):
        id = get_id(url)
        self.config['last_path'] = id.replace("_", "")

    def save_failed(self, url):
        id = get_id(url).replace("_", "")
        failed = self.config.get('failed')
        if failed:
            failed.append(id)
        else:
            failed = []
            failed.append(id)

        self.config['failed'] = failed

    def close(self):
        print(json.dumps(self.config))
        with open("../config.json", 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)


