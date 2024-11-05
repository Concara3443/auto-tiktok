"""Main program loop"""
import sys
from utils.misc_functions import start, clear, folder_file_create, paths
from functions.choices import single_vid, clear_temp_files, clear_video_files, multiple_vids
from utils.links import get_trending_videos, get_playlist_videos, save_file
from functions.config_funcs import config_create

folder_file_create()  # Creates folders / files for videos (skips if they already exist)
config_create(paths["config"])
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
