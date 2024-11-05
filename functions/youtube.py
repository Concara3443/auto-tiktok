"""Módulo para descargar videos de YouTube utilizando pytubefix"""
from pathlib import Path
from pytubefix import YouTube
from functions.misc_functions import clean_title, video_exists, paths
from functions.config_funcs import config_create
from pytubefix.cli import on_progress  # Para mostrar el progreso de la descarga

def yt_downloader(urls, folder):
    """Función que toma URLs de YouTube y descarga los videos usando pytubefix"""
    config = config_create(paths["config"])
    vid_downloaded = 0
    vid_title = ""

    # Asegurar que urls sea una lista
    if not isinstance(urls, list):
        urls = urls.split()

    for url in urls:
        try:
            yt = YouTube(url, "MWEB", on_progress_callback=on_progress)
            
            # Obtener el stream de mayor resolución
            ys = yt.streams.get_highest_resolution()
            
            # Obtener y limpiar el título del video
            vid_title = clean_title(yt.title)
            vid_filename_perm = f"{vid_title}-perm.mp4"
            vid_filename_temp = f"{vid_title}-temp.mp4"

            # Verificar si el video ya existe en las carpetas temporales
            if video_exists(vid_filename_perm, paths["temp_bottom"]) or video_exists(vid_filename_perm, paths["temp_top"]):
                print(f"Skipping the download of {vid_title} because already exsists as '-perm'!")
                vid_downloaded = 0
                continue
            if video_exists(vid_filename_temp, paths["temp_bottom"]) or video_exists(vid_filename_temp, paths["temp_top"]):
                print(f"Skipping the download of {vid_title} because already exsists as '-temp'!")
                vid_downloaded = 0
                continue

            if folder == "bottom":
                vid_title += "-perm"
            else:
                vid_title += "-temp"

            print(f"Downloading video {vid_title}...")
            ys.download(output_path=Path(paths["videos_temp"], folder), filename=f"{vid_title}.mp4")
            vid_downloaded = 1

        except Exception as e:
            print(f"An error ocurred downloading {url}: {e}")

    return vid_downloaded, vid_title if vid_downloaded else None