from googleapiclient.discovery import build
from dotenv import load_dotenv
import re
import os
load_dotenv()

api_key = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)

def obtener_videos_en_tendencia(region_code='ES', max_results=50):
    request = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        regionCode=region_code,
        maxResults=max_results
    )
    response = request.execute()

    videos = response.get('items', [])
    enlaces = []
    for video in videos:
        video_id = video['id']
        enlace = f"https://www.youtube.com/watch?v={video_id}"
        enlaces.append(enlace)
    
    return enlaces

def guardar_enlaces_en_archivo(enlaces, archivo='text_files/top_video_links.txt'):
    with open(archivo, 'w', encoding='utf-8') as file:
        for enlace in enlaces:
            file.write(f"{enlace}\n")

# Obtener los 50 videos en tendencia en la región especificada (por defecto 'ES')
videos_en_tendencia = obtener_videos_en_tendencia()

# Guardar los enlaces en un archivo de texto
guardar_enlaces_en_archivo(videos_en_tendencia)
