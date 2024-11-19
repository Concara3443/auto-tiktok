from googleapiclient.discovery import build
from dotenv import load_dotenv
import re
import os
load_dotenv()

api_key = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)

def fetch_videos(request):
    response = request.execute()
    videos = response.get('items', [])
    links = []
    for video in videos:
        video_id = video['id']['videoId'] if isinstance(video['id'], dict) else video['id']
        link = f"https://www.youtube.com/watch?v={video_id}"
        links.append(link)
    return links

def get_trending_videos(region_code='ES', max_results=50):
    request = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        regionCode=region_code,
        maxResults=max_results
    )
    return fetch_videos(request)

def get_playlist_videos(playlist_id, max_results=50):
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=max_results
    )
    return fetch_videos(request)

def save_file(links, file_path='text_files/top_video_links.txt'):
    with open(file_path, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(f"{link}\n")