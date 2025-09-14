import os
import re
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def extract_channel_id_from_url(url: str) -> str | None:
    match = re.search(r"(?:channel/)([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else None
