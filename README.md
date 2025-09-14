# YouTube Stats Analyzer

#### Video Demo: <URL HERE>

---

## Introduction

Welcome to **YouTube Stats Analyzer**, my final project for **CS50’s Introduction to Programming with Python (CS50P)**.  
This project is a command-line tool written entirely in Python that fetches, analyzes, and visualizes public statistics from YouTube channels using the **YouTube Data API v3**.

The motivation behind this project is twofold:

1. **Practicality**: I often watch YouTube and wondered about the patterns behind a channel’s growth. How frequently do they upload? Which videos bring in the most engagement? This tool provides insights in a straightforward way.

2. **Learning Goals**: I wanted a project that required:
   - API calls (HTTP requests, JSON parsing)  
   - Data handling (using `pandas`)  
   - Visualization (with `matplotlib`)  
   - Environment management (`dotenv`)  
   - Structuring Python code into multiple modules  

This project demonstrates all of these in action while producing something useful.

---

## Features

- Fetch channel statistics:
  - Subscriber count  
  - Total views  
  - Video count  

- Gather metadata from uploaded videos:
  - Video title  
  - Publish date  
  - View count  
  - Like count  
  - Comment count  
  - Duration (in seconds, parsed from ISO 8601)  

- Visualizations:
  - **Top N videos by views** (bar chart)  
  - **Upload frequency over time** (histogram, resampled by month)  

- Export:
  - Save all results into a CSV file for further analysis  

- Caching:
  - Store API responses locally to save quota and speed up repeated runs  

---

## Setup

### Step 1: Clone or copy the project
Make sure the folder structure looks like this:
youtube-stats-analyzer/
├─ README.md
├─ requirements.txt
├─ .env
├─ venv/
└─ src/
├─ init.py
├─ main.py
├─ utils.py
├─ fetcher.py
├─ analyzer.py
├─ viz.py
├─ cache.py
### Step 2: Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
Step 3: Install dependencies
pip install -r requirements.txt
Step 4: Create .env file

In the project root, create .env and paste your API key:
    YOUTUBE_API_KEY=YOUR_API_KEY_HERE
Usage

From the project root, run:
python -m src.main --channel CHANNEL_URL --csv out.csv
Example:
python -m src.main --channel https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw --csv google.csv
Options:
	•	--max N → limit number of videos to fetch
	•	--top-n N → number of top videos displayed in chart
	•	--csv FILENAME → save results into CSV
File Descriptions

src/main.py
	•	CLI entrypoint.
	•	Parses command-line arguments.
	•	Loads API key, fetches channel, videos, builds DataFrame, calls analysis + visualization, exports CSV.

src/utils.py
	•	Loads environment variables (python-dotenv).
	•	Extracts channel ID from URLs.

src/fetcher.py
	•	Handles all API calls (channels.list, playlistItems.list, videos.list).
	•	Uses requests library.
	•	Batches requests (50 video IDs per call).

src/analyzer.py
	•	Converts raw API JSON into a pandas.DataFrame.
	•	Normalizes fields like views, likes, comments, duration.
	•	Sorts data by publish date.

src/viz.py
	•	Visualization functions using matplotlib.
	•	plot_top_videos: bar chart of top videos by views.
	•	plot_upload_frequency: histogram of upload frequency.

src/cache.py
	•	Simple local caching using JSON files.
	•	Stores playlist IDs and video metadata responses.
	•	Prevents wasting API quota during development.
## Testing

This project includes a small test suite written with **pytest**.

### Running the tests
First, install pytest (if not already installed):
```bash
pip install pytest
Then run all tests from the project root:
pytest -v

⸻

Design Choices
	•	API Client: I used requests instead of Google’s official google-api-python-client because it’s lighter, transparent, and easy to explain in a CS50P context.
	•	Caching: YouTube API has a daily quota. Caching responses saves quota and ensures smoother demos.
	•	DataFrame: Using pandas made it easier to sort, filter, and visualize data.
	•	Visualization: matplotlib is reliable for static plots. If I expand this later, I might use plotly or streamlit.
	•	Project Structure: Keeping everything inside src/ with modular files makes the project cleaner and maintainable.

⸻

Limitations
	•	API quota (10,000 units per day). Large channels with thousands of videos may exceed quota.
	•	Only works with public channel data (no private analytics).
	•	Duration is parsed but not yet deeply analyzed (e.g., average video length).
	•	Currently CLI-only; no web or GUI yet.

⸻

Future Work
	•	Add engagement rate analysis (likes + comments per view).
	•	Add sentiment analysis of comments.
	•	Add channel comparison (side-by-side stats).
	•	Add Streamlit interface for web dashboard.
	•	Add SQLite backend to store historical data (track channel growth over time).

⸻

Reflection

Through this project, I learned how to:
	•	Interact with external APIs using Python
	•	Manage API quotas and caching strategies
	•	Structure Python code into multiple modules
	•	Work with pandas DataFrames for real-world data
	•	Create plots with matplotlib
	•	Manage secrets with .env files
	•	Use virtual environments for clean dependency management


This project pushed me to think like a developer: structuring code, planning around limitations (quota), and documenting my work.

I’m proud of how this project turned out. It’s both practical and a demonstration of what I’ve learned in CS50P.

⸻

Conclusion

YouTube Stats Analyzer is a functional, modular, and extendable tool that demonstrates Python fundamentals, APIs, data analysis, and visualization. It’s my CS50P final project and I hope you enjoy exploring it as much as I enjoyed building it. 🚀