from functools import wraps
import traceback

base_url = "https://medex.com.bd/brands"

def get_id(url: str) -> str:
    return url.replace(base_url, "").replace("/", "_")

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