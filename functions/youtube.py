"""Module for downloading videos from YouTube using pytubefix"""
from pathlib import Path
from pytubefix import YouTube
from functions.misc_functions import clean_title, video_exists, paths
from functions.config_funcs import config_create
from pytubefix.cli import on_progress
from colorama import init, Fore, Style

init(autoreset=True)

def yt_downloader(urls, folder):
    """Function that takes YouTube URLs and downloads the videos using pytubefix, storing the IDs in a text file"""
    config = config_create(paths["config"])
    vid_downloaded = 0
    vid_title = ""
    downloaded_ids_file = Path(paths["text_files"], "downloaded_videos.txt")

    if downloaded_ids_file.exists():
        with open(downloaded_ids_file, "r") as f:
            downloaded_ids = set(line.strip() for line in f)
    else:
        downloaded_ids = set()

    if not isinstance(urls, list):
        urls = urls.split()

    for url in urls:
        try:
            yt = YouTube(url, "MWEB", on_progress_callback=on_progress)
            video_id = yt.video_id

            if video_id in downloaded_ids:
                print(Fore.YELLOW + f"Skipping download of {yt.title} because it has already been downloaded.")
                vid_downloaded = 0
                continue
            
            ys = yt.streams.get_highest_resolution()
            
            vid_title = clean_title(yt.title)
            vid_filename_perm = f"{vid_title}-perm.mp4"
            vid_filename_temp = f"{vid_title}-temp.mp4"

            if video_exists(vid_filename_perm, paths["temp_bottom"]) or video_exists(vid_filename_perm, paths["temp_top"]):
                print(Fore.YELLOW + f"Skipping the download of {vid_title} because it already exists as '-perm'!")
                vid_downloaded = 0
                continue
            if video_exists(vid_filename_temp, paths["temp_bottom"]) or video_exists(vid_filename_temp, paths["temp_top"]):
                print(Fore.YELLOW + f"Skipping the download of {vid_title} because it already exists as '-temp'!")
                vid_downloaded = 0
                continue

            if folder == "bottom":
                vid_title += "-perm"
            else:
                vid_title += "-temp"

            print(Fore.GREEN + f"Downloading video {vid_title}...")
            ys.download(output_path=Path(paths["videos_temp"], folder), filename=f"{vid_title}.mp4")
            vid_downloaded = 1
            print(Fore.GREEN + f"Successfully downloaded {vid_title}.mp4")

            with open(downloaded_ids_file, "a") as f:
                f.write(f"{video_id}\n")
            downloaded_ids.add(video_id)

        except Exception as e:
            print(Fore.RED + f"An error occurred downloading {url}: {e}")

    return vid_downloaded, vid_title if vid_downloaded else None