from googleapiclient.discovery import build

def analyze_videos(videos: list[dict], api_key: str = None):
    """Fetch video statistics and enrich the video list."""
    if not api_key:
        return videos  # fallback if no key

    youtube = build("youtube", "v3", developerKey=api_key)
    video_ids = [v["video_id"] for v in videos]

    request = youtube.videos().list(
        part="statistics",
        id=",".join(video_ids)
    )
    response = request.execute()

    stats_map = {}
    for item in response.get("items", []):
        stats_map[item["id"]] = {
            "views": int(item["statistics"].get("viewCount", 0)),
            "likes": int(item["statistics"].get("likeCount", 0)),
            "comments": int(item["statistics"].get("commentCount", 0)),
        }

    enriched = []
    for v in videos:
        stats = stats_map.get(v["video_id"], {})
        enriched.append({
            **v,
            "views": stats.get("views", 0),
            "likes": stats.get("likes", 0),
            "comments": stats.get("comments", 0),
        })
    return enriched
