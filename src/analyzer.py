import pandas as pd
from isodate import parse_duration

def build_videos_dataframe(videos_json: dict) -> pd.DataFrame:
    rows = []
    for item in videos_json.get("items", []):
        snip = item.get("snippet", {})
        stats = item.get("statistics", {})
        content = item.get("contentDetails", {})
        try:
            duration = parse_duration(content.get("duration")) if content.get("duration") else None
        except Exception:
            duration = None
        rows.append({
            "id": item.get("id"),
            "title": snip.get("title"),
            "published_at": pd.to_datetime(snip.get("publishedAt")),
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount")) if stats.get("likeCount") else None,
            "comments": int(stats.get("commentCount")) if stats.get("commentCount") else None,
            "duration_seconds": int(duration.total_seconds()) if duration else None
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("published_at")
        df = df.reset_index(drop=True)
    return df