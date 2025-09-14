from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def extract_channel_id_from_url(url: str) -> str | None:
    if not url:
        return None
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    parts = path.split("/")
    if len(parts) >= 2 and parts[0] == "channel":
        return parts[1]
    return None