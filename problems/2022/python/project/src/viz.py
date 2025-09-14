import matplotlib.pyplot as plt
import pandas as pd

def plot_views_over_time(videos: list[dict]):
    if not videos:
        print("No videos to plot")
        return

    df = pd.DataFrame(videos)
    if "published_at" not in df or "views" not in df:
        print("Missing fields in video data")
        return

    df["published_at"] = pd.to_datetime(df["published_at"])
    df = df.sort_values("published_at")

    plt.figure(figsize=(10, 6))
    plt.plot(df["published_at"], df["views"], marker="o")
    plt.xlabel("Date Published")
    plt.ylabel("Views")
    plt.title("Views Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
