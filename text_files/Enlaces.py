from googleapiclient.discovery import build
import re

# Tu clave de API de YouTube
api_key = 'AIzaSyCePCgJSv_CneuqN6HBd_xqjiIcs0VLB00'

# Crear un cliente para la API de YouTube
youtube = build('youtube', 'v3', developerKey=api_key)

def obtener_videos_en_tendencia(region_code='ES', max_results=50):
    # Llamada a la API para obtener los videos en tendencia
    request = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        regionCode=region_code,
        maxResults=max_results
    )
    response = request.execute()

    # Obtener los enlaces de los videos
    videos = response.get('items', [])
    enlaces = []
    for video in videos:
        video_id = video['id']
        enlace = f"https://www.youtube.com/watch?v={video_id}"
        enlaces.append(enlace)
    
    return enlaces

def guardar_enlaces_en_archivo(enlaces, archivo='top_video_links.txt'):
    with open(archivo, 'w', encoding='utf-8') as file:
        for enlace in enlaces:
            file.write(f"{enlace}\n")

# Obtener los 50 videos en tendencia en la región especificada (por defecto 'ES')
videos_en_tendencia = obtener_videos_en_tendencia()

# Guardar los enlaces en un archivo de texto
guardar_enlaces_en_archivo(videos_en_tendencia)
