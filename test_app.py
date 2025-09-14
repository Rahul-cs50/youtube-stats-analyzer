import pandas as pd
import os
import pytest

from src.analyzer import build_videos_dataframe
from src.utils import extract_channel_id_from_url
from src.cache import save_json, load_json


def test_extract_channel_id_from_url():
    url = "https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw"
    cid = extract_channel_id_from_url(url)
    assert cid == "UC_x5XG1OV2P6uZZ5FSM9Ttw"


def test_build_videos_dataframe():
    fake_json = {
        "items": [
            {
                "id": "abc123",
                "snippet": {
                    "title": "Test Video",
                    "publishedAt": "2024-01-01T00:00:00Z"
                },
                "statistics": {"viewCount": "100", "likeCount": "10", "commentCount": "5"},
                "contentDetails": {"duration": "PT5M"}
            }
        ]
    }
    df = build_videos_dataframe(fake_json)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["views"] == 100
    assert df.iloc[0]["duration_seconds"] == 300  # 5 minutes = 300 seconds


def test_cache_save_and_load(tmp_path):
    sample = {"hello": "world"}
    test_file = "pytest_cache_test"

    # Temporarily override cache directory
    from src import cache
    cache.CACHE_DIR = tmp_path
    cache.CACHE_DIR.mkdir(exist_ok=True)

    save_json(test_file, sample)
    loaded = load_json(test_file)

    assert sample == loaded