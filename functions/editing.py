"""Module edits all videos into one file"""
import random
import os
from moviepy.editor import VideoFileClip, clips_array, CompositeVideoClip
from functions.misc_functions import video_exists, paths, file_read
from functions.config_funcs import config_create
from functions.tiktok_uploader.tiktok import upload_video
from colorama import Fore, Style, init

config = config_create(paths["config"])
init(autoreset=True) # 

def video_edit(top_vid: list, bottom_vid: list):
    """Function edits top and bottom video into one final file"""
    print(Fore.CYAN + "Editing videos...")
    if isinstance(top_vid, list) is False or isinstance(bottom_vid, list) is False:
        top_vid = list(top_vid.split(" "))
        bottom_vid = list(bottom_vid.split(" "))
    
    total_videos = len(top_vid)
    print(Fore.GREEN + f"Total number of videos to be uploaded: {total_videos}")
    
    successful_uploads = 0
    for value in top_vid:
        try:
            value = str(value)
            final_name = value.replace("-temp", "")
            if video_exists(final_name + "-PT1.mp4", paths["videos_final"]):
                print(Fore.YELLOW + f"Skipped rendering {value} since it already exists!")
                continue

            if value == "None":
                print(Fore.RED + "This video does not exist!")
                continue
            
            top_clip = VideoFileClip(f"videos_temp/top/{value}.mp4")

            if top_clip.duration >= int(config["max_video_length"]):
                print(Fore.RED + f"Skipped {value} because it exceeds the maximum video length!")
                top_clip.close()
                continue
            
            bottom_vid_filtered = [vid for vid in bottom_vid if vid is not None]
            if not bottom_vid_filtered:
                print(Fore.RED + "No valid bottom videos available!")
                top_clip.close()
                continue
            
            bottom_clip = None
            while bottom_vid_filtered:
                bottom_choice = random.choice(bottom_vid_filtered)
                bottom_clip = VideoFileClip(f"./videos_temp/bottom/{bottom_choice}.mp4")
                if bottom_clip.duration >= top_clip.duration:
                    break
                bottom_vid_filtered.remove(bottom_choice)
                bottom_clip.close()
            
            if bottom_clip is None or bottom_clip.duration < top_clip.duration:
                print(Fore.RED + "No suitable bottom video found for synchronization!")
                top_clip.close()
                continue
            
            bottom_clip_edit = bottom_clip

            if config["mute_bottom_video"]:
                bottom_clip_edit = bottom_clip.without_audio()
            bottom_clip_edit = trim_bottom_to_top(top_clip, bottom_clip_edit)

            combined = clips_array([[top_clip], [bottom_clip_edit]])
            clips = trim_video(combined)
            
            num_parts = len(clips)
            print(Fore.GREEN + f"Video {final_name} is divided into {num_parts} parts.")
            
            for i, clip in enumerate(clips):
                clip_path = f"./videos_final/{final_name}-PT{i + 1}.mp4"
                clip.write_videofile(clip_path)
                clip.close()
                print(Fore.CYAN + f"Uploading {clip_path}")
                
                vidName = f"{final_name.replace('_', ' ')} - Part: {i + 1}"

                if config["add_hastags"]:
                    vidName += " "
                    hastags = file_read(paths["hastags"])
                    selected_hastags = []
                    while len(vidName) < 2200 and hastags:
                        hashtag = random.choice(hastags).strip()
                        if len(vidName) + len(hashtag) + 1 > 2200: 
                            break
                        selected_hastags.append(hashtag)
                        vidName += " " + hashtag

                if len(vidName) > 2200:
                    vidName = vidName[:2197] + "..."
                    
                upload_video("clips",f"{final_name}-PT{i + 1}.mp4", vidName)
                
                print(Fore.YELLOW + f"Uploaded {i + 1} of {num_parts} videos ({((i + 1) / num_parts) * 100:.2f}%)" if num_parts != 0 else "No parts to upload.")
                
                os.remove(clip_path)
                print(Fore.CYAN + f"Deleted {clip_path} after uploading.")
                
            successful_uploads += 1
                
            print(Fore.GREEN + f"\nExported and uploaded {len(clips)} video clips!")
            print(Fore.YELLOW + f"Total number of videos uploaded: {successful_uploads}/{total_videos} videos ({(successful_uploads / total_videos) * 100:.2f}%)" if total_videos != 0 else "No videos to upload.")
            combined.close()
            bottom_clip.close()
            top_clip.close()
            bottom_clip_edit.close()
        except Exception as e:
            print(Fore.RED + f"An error occurred processing {value}: {e}")
            print(Fore.RED + "Skipping to next video...")
            continue
    
    print(Fore.GREEN + f"Total number of videos successfully uploaded: {successful_uploads}")

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
            trimed_video = video.subclip(subclip_start, end)
            clips.append(trimed_video)
            break
        trimed_video = video.subclip(subclip_start, end)
        subclip_start = end

        clips.append(trimed_video)
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
