import matplotlib.pyplot as plt
import pandas as pd

def plot_top_videos(df: pd.DataFrame, top_n=5, save_path=None):
    if df.empty:
        return
    top = df.sort_values("views", ascending=False).head(top_n)
    ax = top.plot.bar(x="title", y="views", legend=False)
    ax.set_ylabel("Views")
    ax.set_title(f"Top {top_n} videos by views")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def plot_upload_frequency(df: pd.DataFrame, by='M', save_path=None):
    if df.empty:
        return
    series = df.set_index('published_at').resample(by).size()
    ax = series.plot(kind='bar')
    ax.set_ylabel('Number of videos')
    ax.set_title('Upload frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()