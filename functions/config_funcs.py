"""Module handles config and config writing"""
from pathlib import Path
import toml
import os

CONFIG_DEFAULT_STRING = """
max_clip_length = 180 # How long each clip should be when rendering video. default 3 mins (counted in seconds).
max_video_length = 1800 # How long the final video should be. default 30 mins (counted in seconds).
mute_bottom_video = true # mutes bottom video. (should only be true or false).
save_bottom_video = false # saves temp bottom videos. default false (should only be true or false).
add_hastags = false # adds hastags to the video. default false (should only be true or false).
"""
config_parsed = toml.loads(CONFIG_DEFAULT_STRING)
#config = toml.load(f="text_files/config.toml")

def config_write(file, content):
    directory = os.path.dirname(file)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Abre el archivo en modo escritura
    with open(file, "w", encoding="utf-8") as open_file:
        open_file.write(content)
        
def config_create(path):
    if path.is_file() is False:
        config_write(path, CONFIG_DEFAULT_STRING)
    config = toml.load(Path("text_files", "config.toml"))
    return config