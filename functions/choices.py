"""Module handles user choice"""
import pyinputplus as pyip
from functions.youtube import yt_downloader
from functions.misc_functions import clear, folder_clear, delete_dup_links, file_read, paths
import functions.editing as editing
import os


def single_vid():
    """Function handles single video flow"""
    url = pyip.inputURL(prompt="Enter top video URL: ")
    downloads, top_video = yt_downloader(url, "top")

    url = pyip.inputURL(prompt="Enter bottom video URL: ")
    downloads, bottom_video = yt_downloader(url, "bottom")
    clear()

    editing.video_edit(top_video, bottom_video)


def clear_temp_files():
    """Function clears all -temp video files"""
    folder_clear(paths["temp_bottom"])
    folder_clear(paths["temp_top"])
    print("Cleared all temp files!")

def clear_video_files():
    """Function clears all -final video files"""
    for file in os.listdir(paths["videos_final"]):
        os.remove(os.path.join(paths["videos_final"], file))

def multiple_vids():
    """Function handles multiple video flow"""
    delete_dup_links(paths["top_video_links"])
    delete_dup_links(paths["bottom_video_links"])

    top_video_links = file_read(paths["top_video_links"])
    bottom_video_links = file_read(paths["bottom_video_links"])

    top_file_list = []
    bottom_file_list = []
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    top_dir = os.path.join(base_dir, 'videos_temp', 'top')
    bottom_dir = os.path.join(base_dir, 'videos_temp', 'bottom')

    for filename in os.listdir(top_dir):
        top_file_list.append(filename[:-4])

    for filename in os.listdir(bottom_dir):
        bottom_file_list.append(filename[:-4])

    for top_link in top_video_links:
        downloads, top_video = yt_downloader(top_link, "top")
        top_file_list.append(top_video)

    for bottom_link in bottom_video_links:
        downloads, bottom_video = yt_downloader(bottom_link, "bottom")
        bottom_file_list.append(bottom_video)
    clear()
    editing.video_edit(top_file_list, bottom_file_list)