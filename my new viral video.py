import streamlit as st
import requests
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = "Enter your API Key here"

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("YouTube Viral Topics Tool")

# Input Fields
days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# Keywords (UPDATED — AI + Faceless YouTube Automation Niche)
keywords = [
    "AI tools for YouTube",
    "Faceless YouTube Automation",
    "YouTube Automation AI",
    "AI Video Generation Tools",
    "Text to Video AI",
    "AI Video Generator Free",
    "Bulk AI Video Creation",
    "YouTube Automation Tutorial",
    "Faceless Channel Automation",
    "AI Tools for Content Creation",
    "AI Tools for YouTubers",
    "YouTube Automation with AI",
    "AI Shorts Generator",
    "AI Reel Generator",
    "YouTube Automation Workflow",
    "AI Voiceover for YouTube",
    "Text to Speech AI YouTube",
    "AI Script Writing Tool",
    "AI Thumbnail Generator",
    "New AI Tools 2024",
    "AI Tools Update",
    "AI Tools Review",
    "Best AI Tools for YouTube",
    "Automation Tools for YouTube",
    "Faceless YouTube Channel Growth"
]

# Fetch Data Button
if st.button("Fetch Data"):
    try:
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        for keyword in keywords:
            st.write(f"Searching for keyword: {keyword}")

            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY,
            }

            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()

            if "items" not in data or not data["items"]:
                st.warning(f"No videos found for keyword: {keyword}")
                continue

            videos = data["items"]
            video_ids = [v["id"]["videoId"] for v in videos if "videoId" in v["id"]]
            channel_ids = [v["snippet"]["channelId"] for v in videos]

            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
            stats_data = requests.get(YOUTUBE_VIDEO_URL, params=stats_params).json()

            channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
            channel_data = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params).json()

            for video, stat, channel in zip(videos, stats_data["items"], channel_data["items"]):
                subs = int(channel["statistics"].get("subscriberCount", 0))
                if subs < 3000:
                    all_results.append({
                        "Title": video["snippet"]["title"],
                        "Description": video["snippet"]["description"][:200],
                        "URL": f"https://www.youtube.com/watch?v={video['id']['videoId']}",
                        "Views": int(stat["statistics"].get("viewCount", 0)),
                        "Subscribers": subs
                    })

        if all_results:
            st.success(f"Found {len(all_results)} results!")
            for r in all_results:
                st.markdown(
                    f"**Title:** {r['Title']}  \n"
                    f"**Description:** {r['Description']}  \n"
                    f"**URL:** [Watch Video]({r['URL']})  \n"
                    f"**Views:** {r['Views']}  \n"
                    f"**Subscribers:** {r['Subscribers']}"
                )
                st.write("---")
        else:
            st.warning("No low-subscriber viral opportunities found.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
