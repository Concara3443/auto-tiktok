"""Main program loop"""
import sys
import os
import argparse
from functions.misc_functions import start, clear, folder_file_create, paths, wait_for_input
from functions.choices import single_vid, clear_temp_files, clear_video_files, multiple_vids
from utils.links import get_trending_videos, get_playlist_videos, save_file
from functions.config_funcs import config_create

parser = argparse.ArgumentParser(description="Iniciar el bot de Auto TikTok")
parser.add_argument('-n', '--no-shutdown', action='store_true', help="Desactivar el autoapagado")
args = parser.parse_args()

folder_file_create()  # Creates folders / files for videos (skips if they already exist)
config = config_create(paths["config"])

if config["automatic_mode"]:
    clear_temp_files()
    trend_vids = get_trending_videos()
    save_file(trend_vids)
    multiple_vids()
    clear_temp_files()
    clear()
    if config["shutdown_after_upload"]:
        if not wait_for_input(60):
            os.system("shutdown /s /t 60")

while True:
    startResp = start()

    if startResp == "Single Video":
        single_vid()
        clear_temp_files()
        clear()
    elif startResp == "Multiple Videos":
        multiple_vids()
        clear_temp_files()
        clear()
    elif startResp == "Clear Temp Files":
        clear_temp_files()
    elif startResp == "Clear Video Files":
        clear_video_files()
    elif startResp == "Get Top Videos":
        trend_vids = get_trending_videos()
        save_file(trend_vids)
    elif startResp == "Get Videos from Playlist":
        playlist_id = input("Enter playlist ID: ")
        playlist_vids = get_playlist_videos(playlist_id)
        save_file(playlist_vids, 'text_files/playlist_links.txt')
    elif startResp == "Cancel":
        sys.exit()
    else:
        sys.exit()
