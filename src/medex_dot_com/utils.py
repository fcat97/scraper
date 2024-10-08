import os
from functools import wraps
import traceback

site_name = "medex"
data_dir = "./data"
config_file_path = f"{data_dir}/config.json"
content_dir = f"{data_dir}/contents"
db_directory = data_dir

def create_dir(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def safe_run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"exception caught {e}")
            traceback.print_exc()
            return None

    return wrapper

class IdGenerator:
    def __init__(self):
        pass

    @safe_run
    def get_id(self, url: str) -> str|None:
        return url.split("/")[-1]