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

def search_video(query="", region_code='ES', max_results=50):
    request = youtube.search().list(
        part="snippet",
        maxResults=max_results,
        q=query,
        regionCode=region_code, # https://www.iso.org/obp/ui/#search
        safeSearch="none",
        type="video",
        videoDuration="short" # long +20min / medium 4-20min / short -4min
    )
    return fetch_videos(request)

def get_trending_videos(region_code='ES', max_results=50):
    request = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        regionCode=region_code,
        maxResults=max_results
    )
    return fetch_videos(request)

def get_playlist_videos(playlist_id, max_results=50):
    if 'list=' in playlist_id:
        playlist_id = playlist_id.split('list=')[1].split('&')[0]
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