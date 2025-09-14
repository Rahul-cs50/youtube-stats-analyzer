import argparse
import re
from src.utils import YOUTUBE_API_KEY, extract_channel_id_from_url
from src.fetcher import channels_list_by_id, channels_list_by_username, playlist_items_list, videos_list
from src.analyzer import build_videos_dataframe
from src.viz import plot_top_videos, plot_upload_frequency
from src import cache
import pandas as pd

def guess_channel_id_or_username(inp: str):
    cid = extract_channel_id_from_url(inp)
    if cid:
        return ('id', cid)
    if re.match(r'^UC[0-9A-Za-z_-]{22,}$', inp):
        return ('id', inp)
    return ('raw', inp)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--channel', '-c', required=True, help='Channel URL or ID or username')
    parser.add_argument('--max', type=int, default=200, help='Max number of videos to fetch')
    parser.add_argument('--csv', help='Path to save CSV')
    parser.add_argument('--top-n', type=int, default=5, help='Number of top videos to show')
    args = parser.parse_args()

    if not YOUTUBE_API_KEY:
        print('YOUTUBE_API_KEY not set')
        return

    mode, val = guess_channel_id_or_username(args.channel)
    channel_json = None
    try:
        if mode == 'id':
            channel_json = channels_list_by_id(val)
        else:
            try:
                channel_json = channels_list_by_username(val)
            except Exception:
                channel_json = channels_list_by_id(val)
    except Exception as e:
        print('Failed to fetch channel:', e)
        return

    try:
        items = channel_json.get('items', [])
        ch = items[0]
        title = ch.get('snippet', {}).get('title')
        stats = ch.get('statistics', {})
        uploads_pl = ch.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads')
        print(f"Channel: {title}")
        print(f"Subscribers: {stats.get('subscriberCount')}")
        print(f"Total views: {stats.get('viewCount')}")
        print(f"Video count: {stats.get('videoCount')}")
    except Exception as e:
        print('Error parsing channel json:', e)
        return

    if not uploads_pl:
        print('No uploads playlist found')
        return

    cache_key = f"playlist_{uploads_pl}"
    cached = cache.load_json(cache_key)
    if cached:
        video_ids = cached
        print(f"Loaded {len(video_ids)} video ids from cache")
    else:
        print('Fetching video ids...')
        video_ids = playlist_items_list(uploads_pl, max_results=args.max)
        cache.save_json(cache_key, video_ids)
        print(f"Fetched {len(video_ids)} video ids and cached them")

    batches = [video_ids[i:i+50] for i in range(0, len(video_ids), 50)]
    all_videos = {"items": []}
    for batch in batches:
        batch_key = 'videos_' + '_'.join(batch[:3])
        cached_b = cache.load_json(batch_key)
        if cached_b:
            all_videos['items'].extend(cached_b.get('items', []))
        else:
            resp = videos_list(batch)
            cache.save_json(batch_key, resp)
            all_videos['items'].extend(resp.get('items', []))

    df = build_videos_dataframe(all_videos)
    if df.empty:
        print('No video metadata found')
        return

    print("\nTop videos by views:")
    print(df.sort_values('views', ascending=False).head(args.top_n)[['title', 'views', 'published_at']])

    if args.csv:
        df.to_csv(args.csv, index=False)
        print(f'Saved CSV to {args.csv}')

    plot_top_videos(df, top_n=args.top_n)
    plot_upload_frequency(df)

if __name__ == '__main__':
    main()