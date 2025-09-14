import requests
from src.utils import YOUTUBE_API_KEY

BASE = "https://www.googleapis.com/youtube/v3"

class YouTubeAPIError(Exception):
    pass

def channels_list_by_id(channel_id: str):
    url = f"{BASE}/channels"
    params = {
        "part": "snippet,statistics,contentDetails",
        "id": channel_id,
        "key": YOUTUBE_API_KEY
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    if not data.get("items"):
        raise YouTubeAPIError("No channel found for id")
    return data

def channels_list_by_username(username: str):
    url = f"{BASE}/channels"
    params = {
        "part": "snippet,statistics,contentDetails",
        "forUsername": username,
        "key": YOUTUBE_API_KEY
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

def playlist_items_list(playlist_id: str, max_results=200):
    url = f"{BASE}/playlistItems"
    params = {
        "part": "contentDetails,snippet",
        "playlistId": playlist_id,
        "maxResults": 50,
        "key": YOUTUBE_API_KEY
    }
    video_ids = []
    next_token = None
    fetched = 0
    while True:
        if next_token:
            params["pageToken"] = next_token
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        for item in data.get("items", []):
            vid = item.get("contentDetails", {}).get("videoId")
            if vid:
                video_ids.append(vid)
                fetched += 1
                if fetched >= max_results:
                    return video_ids
        next_token = data.get("nextPageToken")
        if not next_token:
            break
    return video_ids

def videos_list(video_ids: list[str]):
    url = f"{BASE}/videos"
    params = {
        "part": "snippet,statistics,contentDetails",
        "id": ",".join(video_ids),
        "key": YOUTUBE_API_KEY
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()