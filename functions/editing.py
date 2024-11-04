"""Module edits all videos into one file"""
import random
from moviepy.editor import VideoFileClip, clips_array, CompositeVideoClip
from utils.misc_functions import video_exists, paths
from functions.config_funcs import config_create

config = config_create(paths["config"])

def video_edit(top_vid: list, bottom_vid: list):
    """Function edits top and bottom video into one final file"""

    if not isinstance(top_vid, list) or not isinstance(bottom_vid, list):
        top_vid = list(top_vid.split(" "))
        bottom_vid = list(bottom_vid.split(" "))

    for value in top_vid:
        try:
            value = str(value)
            final_name = value.replace("-temp", "")
            if video_exists(final_name + "-PT1.mp4", paths["videos_final"]):
                print(f"Skipped rendering {value} since it already exists!")
                continue

            if value == "None":
                print("No valid top videos available!")
                continue

            top_clip = VideoFileClip(f"videos_temp/top/{value}.mp4")

            bottom_vid_filtered = [vid for vid in bottom_vid if vid is not None]
            if not bottom_vid_filtered:
                print("No valid bottom videos available!")
                continue

            # Find bottom videos longer than top video
            suitable_bottom_vids = []
            for bottom_value in bottom_vid_filtered:
                bottom_clip_candidate = VideoFileClip(f"./videos_temp/bottom/{bottom_value}.mp4")
                if bottom_clip_candidate.duration >= top_clip.duration:
                    suitable_bottom_vids.append(bottom_value)
                bottom_clip_candidate.close()

            if not suitable_bottom_vids:
                print("No bottom videos longer than the top video available!")
                continue

            bottom_choice = random.choice(suitable_bottom_vids)
            bottom_clip = VideoFileClip(f"./videos_temp/bottom/{bottom_choice}.mp4")
            bottom_clip_edit = bottom_clip

            if config["mute_bottom_video"]:
                bottom_clip_edit = bottom_clip.without_audio()
            bottom_clip_edit = trim_bottom_to_top(top_clip, bottom_clip_edit)

            combined = clips_array([[top_clip], [bottom_clip_edit]])
            clips = trim_video(combined)

            for i, clip in enumerate(clips):
                clip.write_videofile(f"./videos_final/{final_name}-PT{i + 1}.mp4")
                clip.close()
            print(f"\nExported {len(clips)} video clips!")
            print("Find them in the 'videos_final' folder")
            combined.close()
            bottom_clip.close()
            top_clip.close()
            bottom_clip_edit.close()
        except Exception as e:
            print(f"An error occurred while processing {value}: {e}")


def trim_video(video: CompositeVideoClip):
    """Function trims video to fit certain length"""
    config = config_create(paths["config"])
    clips = []
    subclip_start = 0
    end = int(video.duration)

    if end < int(config["max_clip_length"]):
        clips.append(video)
        return clips

    while True:
        end = trim_math(int(video.duration), subclip_start)
        if end == int(video.duration):
            try:
                trimed_video = video.subclip(subclip_start, end)
                clips.append(trimed_video)
            except OSError as e:
                print(f"Error al leer el archivo de video {video}: {e}")
            break
        try:
            trimed_video = video.subclip(subclip_start, end)
            subclip_start = end
            clips.append(trimed_video)
        except OSError as e:
            print(f"Error al leer el archivo de video {video}: {e}")
    return clips


def trim_math(duration: int, curr: int):
    """Function does math for trim_video function"""
    config = config_create(paths["config"])
    target = curr + int(config["max_clip_length"])
    difference = duration - target
    if difference <= 0:
        return duration
    duration = duration - difference
    return duration


def trim_bottom_to_top(top_video: CompositeVideoClip, bottom_video: CompositeVideoClip):
    """Function trims bottom video to top videos length"""
    if int(top_video.duration) < int(bottom_video.duration):
        bottom_video = bottom_video.subclip(0, int(top_video.duration))
    return bottom_video
