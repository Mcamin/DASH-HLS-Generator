import subprocess
import json
import re
import os
import helpers.commandbuilder as cb
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
ffmpeg = os.environ.get("FFMPEG")


def grab_user_input():
    def filter_input(message, default):
        user_input = input(message)

        if user_input == "":
            user_input = default
        return user_input

    print("Hit enter for default value\n")
    return filter_input("Enter the config filepath: ", "./config.json")


def read_config(filepath='./config.json'):
    with open(filepath, 'r') as f:
        data = json.load(f)
        return data


def build_dash_command(cf):
    cmd = ffmpeg
    cmd = cb.add_input(cmd, cf)
    cmd = cb.add_preset(cmd, cf)
    cmd = cb.add_key_min(cmd, cf)
    cmd = cb.add_gop_size(cmd, cf)
    cmd = cb.add_threshold(cmd, cf)
    cmd = cb.add_fps(cmd, cf)
    cmd = cb.add_video_codec(cmd, cf)
    cmd = cb.add_pixel_format(cmd, cf)
    cmd = cb.add_audio_codec(cmd, cf)
    cmd = cb.add_audio_bitrate(cmd, cf)
    cmd = cb.add_audio_channel(cmd, cf)
    cmd = cb.add_audio_rate(cmd, cf)
    cmd = cb.add_filters(cmd, cf)
    cmd = cb.add_video_mapping(cmd, cf)
    cmd = cb.add_audio_mapping(cmd, cf)
    cmd = cb.add_dash_attributes(cmd, cf)
    return cmd


def build_hls_command(cf):
    cmd = ffmpeg
    cmd = cb.add_input(cmd, cf)
    cmd = cb.add_preset(cmd, cf)
    cmd = cb.add_key_min(cmd, cf)
    cmd = cb.add_gop_size(cmd, cf)
    cmd = cb.add_threshold(cmd, cf)
    cmd = cb.add_fps(cmd, cf)
    cmd = cb.add_video_codec(cmd, cf)
    cmd = cb.add_pixel_format(cmd, cf)
    cmd = cb.add_audio_codec(cmd, cf)
    cmd = cb.add_audio_bitrate(cmd, cf)
    cmd = cb.add_audio_channel(cmd, cf)
    cmd = cb.add_audio_rate(cmd, cf)
    cmd = cb.add_filters(cmd, cf)
    cmd = cb.add_video_mapping(cmd, cf)
    cmd = cb.add_hls_attributes(cmd, cf)
    return cmd


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("The new directory is created!")


def generate_dash_files(configs):
    for cf in configs:
        cmd = re.sub(' +', ' ', build_dash_command(cf))
        create_directory(cf["mpd_filepath"])
        print(cmd)
        # shell=True,
        if subprocess.run(cmd,  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).returncode == 0:
            # TODO: Save config in the database with the media url
            print("FFmpeg Script Ran Successfully")
        else:
            print("There was an error running your FFmpeg script")


def generate_hls_files(configs):
    for cf in configs:
        cmd = re.sub(' +', ' ', build_hls_command(cf))
        create_directory(cf["output_path"])
        print(re.sub(' +', ' ', cmd))
        # shell=True,
        if subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).returncode == 0:
            # TODO: Save config in the database with the media url
            print("FFmpeg Script Ran Successfully")
        else:
            print("There was an error running your FFmpeg script")


def run_ffmpeg():
    filepath = grab_user_input()
    config = read_config(filepath)
    # generate_dash_files(config["dash"])
    generate_hls_files(config["hls"])


if __name__ == "__main__":
    run_ffmpeg()
