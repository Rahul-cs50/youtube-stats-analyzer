import argparse
from src.utils import YOUTUBE_API_KEY, extract_channel_id_from_url
from src.fetcher import fetch_channel_stats, fetch_videos
from src.analyzer import analyze_videos
from src.viz import plot_views_over_time

def main():
    parser = argparse.ArgumentParser(description="YouTube Stats Analyzer")
    parser.add_argument("url", help="YouTube channel URL")
    parser.add_argument("--csv", help="Path to save CSV output", default=None)
    args = parser.parse_args()

    channel_id = extract_channel_id_from_url(args.url)
    if not channel_id:
        print("Invalid channel URL")
        return

    stats = fetch_channel_stats(channel_id, YOUTUBE_API_KEY)
    print("Channel stats:", stats)

    videos = fetch_videos(channel_id, YOUTUBE_API_KEY)
    analyzed = analyze_videos(videos)

    if args.csv:
        import pandas as pd
        df = pd.DataFrame(analyzed)
        df.to_csv(args.csv, index=False)
        print(f"Saved data to {args.csv}")

    plot_views_over_time(analyzed)

if __name__ == "__main__":
    main()
