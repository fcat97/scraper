

base_url = "https://medex.com.bd/brands"

def get_id(url: str) -> str:
    return url.replace(base_url, "").replace("/", "_")