"""Module contains random useful functions across the project"""
import os
from pathlib import Path
import re
import msvcrt
import time
import pyinputplus as pyip
from termcolor import colored

base_dir = Path(__file__).resolve().parent.parent

paths = {
    "bottom_video_links": base_dir / "text_files" / "bottom_video_links.txt",
    "top_video_links": base_dir / "text_files" / "top_video_links.txt",
    "config": base_dir / "text_files" / "config.toml",
    "videos_final": base_dir / "videos_final",
    "temp_top": base_dir / "videos_temp" / "top",
    "temp_bottom": base_dir / "videos_temp" / "bottom",
    "text_files": base_dir / "text_files",
    "videos_temp": base_dir / "videos_temp",
    "hastags": base_dir / "text_files" / "hastags.txt"
}

def folder_file_create():
    """Function creates all neccesary folders and files for the project"""
    folders = [Path("videos_final"), Path("videos_temp"), Path("text_files")]
    sub_folders = [Path("top"), Path("bottom")]
    files = [Path("top_video_links.txt"), Path("bottom_video_links.txt"), Path("hastags.txt")]

    for folder in folders:  # Creates base folders
        path = os.path.join(folder)
        try:
            os.makedirs(path)
        except FileExistsError:
            continue

    for sub_folder in sub_folders:  # Creates sub folders
        path = os.path.join(paths["videos_temp"], sub_folder)
        try:
            os.makedirs(path)
        except FileExistsError:
            continue

    for file in files:
        path = os.path.join(paths["text_files"], file)
        try:
            with open(path, "x", encoding="utf-8"):
                continue
        except FileExistsError:
            continue


def start():
    """Function handles intial start flow"""
    print_logo()
    response = pyip.inputMenu(choices=["Log new account", "Multiple Videos", "Clear Temp Files", "Clear Video Files", "Get Top Videos", "Get Videos from Playlist", "Cancel"], numbered=True)
    clear()

    return response


def clear():  # Clears terminal
    """Function clears terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def folder_clear(path):
    """Function deletes all files in given path"""
    files = os.listdir(path)
    temp_files = check_file_ending(files)

    for file in temp_files:
        try:
            os.remove(os.path.join(path, file))
        except PermissionError:
            print(f"Cannot delete {file} because it is being used by another process.")
            continue


def check_folders():
    """Function check if temp files exist and clears them if True"""
    top_files = os.listdir(paths["temp_top"])
    bottom_files = os.listdir(paths["temp_bottom"])

    if len(top_files) != 0:
        folder_clear(paths["temp_top"])
    if len(bottom_files) != 0:
        folder_clear(paths["temp_bottom"])


def check_file_ending(files: list):
    """Function checks if files ends with -temp or not"""
    delete_files = []
    for file in files:
        file = str(file)
        if file.endswith("-temp.mp4"):
            delete_files.append(file)
    return delete_files


def file_read(file):
    """Function used to read file lines"""
    with open(file, encoding="utf-8") as open_file:
        lines = open_file.readlines()
        return lines


def clean_title(title):
    """Function uses regex to clean YT video titles into usable file names"""
    temp = re.sub(r"\.[a-zA-Z]{,4}$", "", title)  # remove any file ending ex: ".exe"
    temp = re.sub(r"\s", "_", temp)  # replace white spaces with an underscore
    temp = re.sub(r"\W", "", temp)  # remove any slashes

    # removes any emojis
    emoji_regex_pattern = re.compile(pattern="["
                                             u"\U0001F600-\U0001F64F"
                                             u"\U0001F300-\U0001F5FF"
                                             u"\U0001F680-\U0001F6FF"
                                             u"\U0001F1E6-\U0001F1FF"
                                             "]+", flags=re.UNICODE)
    temp = re.sub(emoji_regex_pattern, "", temp)
    return temp


def delete_dup_links(file):
    """Function delete duplicate URL links"""
    raw_dup_lines = file_read(file)
    cleaned_dup_lines = []
    for i in raw_dup_lines:
        cleaned_dup_lines.append(i.replace("\n", ""))
    lines = [*set(cleaned_dup_lines)]

    file_write(file, lines)


def file_write(file, links):
    """Function writes to files"""
    with open(file, "w", encoding="utf-8") as open_file:
        open_file.writelines(link + "\n" for link in links)


def video_exists(file_name, path):
    """Function checks if videos in path exist"""
    files = os.listdir(path)

    if file_name in files:
        return True
    else:
        return False

def wait_for_input(timeout):
    start_time = time.time()
    txt = f"Press any key to continue or wait {timeout} seconds"
    print(colored(f"+{'-' * (len(txt) + 2)}+", 'red', 'on_white'))
    print(colored(f"| {txt} |", 'red', 'on_white'))
    print(colored(f"+{'-' * (len(txt) + 2)}+", 'red', 'on_white'))
    while True:
        if msvcrt.kbhit():
            return True
        if time.time() - start_time > timeout:
            return False
        time.sleep(0.1)

def print_logo():
    """Function print starting logo"""
    guillermo = r"""
   ___       _ _ _                           
  / _ \_   _(_) | | ___ _ __ _ __ ___   ___  
 / /_\/ | | | | | |/ _ \ '__| '_ ` _ \ / _ \ 
/ /_\\| |_| | | | |  __/ |  | | | | | | (_) |
\____/ \__,_|_|_|_|\___|_|  |_| |_| |_|\___/ 
                                                                            
"""
    colored_avc = colored(guillermo, color="blue")
    print(colored_avc)
