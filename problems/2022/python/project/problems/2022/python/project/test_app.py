import pytest
from src import utils

def test_extract_channel_id_from_url_valid():
    url = "https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw"
    assert utils.extract_channel_id_from_url(url) == "UC_x5XG1OV2P6uZZ5FSM9Ttw"

def test_extract_channel_id_from_url_invalid():
    url = "https://www.youtube.com/not_a_channel"
    assert utils.extract_channel_id_from_url(url) is None

def test_placeholder_math():
    assert 2 + 2 == 4
