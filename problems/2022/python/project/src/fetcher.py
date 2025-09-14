from googleapiclient.discovery import build

def fetch_channel_stats(channel_id: str, api_key: str):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()
    if "items" not in response or not response["items"]:
        return None
    item = response["items"][0]
    return {
        "title": item["snippet"]["title"],
        "subscribers": int(item["statistics"].get("subscriberCount", 0)),
        "views": int(item["statistics"].get("viewCount", 0)),
        "videos": int(item["statistics"].get("videoCount", 0))
    }

def fetch_videos(channel_id: str, api_key: str, max_results: int = 20):
    youtube = build("youtube", "v3", developerKey=api_key)

    # Get uploads playlist
    playlists = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    uploads_id = playlists["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Get videos
    videos = []
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=uploads_id,
        maxResults=max_results
    )
    response = request.execute()
    for item in response["items"]:
        videos.append({
            "video_id": item["contentDetails"]["videoId"],
            "title": item["snippet"]["title"],
            "published_at": item["contentDetails"]["videoPublishedAt"]
        })

    return videos
