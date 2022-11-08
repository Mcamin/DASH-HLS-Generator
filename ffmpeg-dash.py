import subprocess
import json
import os
import helpers.commandbuilder as cb

ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg"


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
    var_a = 10
    cmd = ffmpeg
    cmd = cb.add_input(cmd, cf)
    cmd = cb.add_preset(cmd, cf)
    cmd = cb.add_key_min(cmd, cf)
    cmd = cb.add_gop_size(cmd, cf)
    cmd = cb.add_threshold(cmd, cf)
    cmd = cb.add_fps(cmd, cf)
    cmd = cb.add_video_codec(cmd, cf)
    cmd = cb.add_pixel_format(cmd, cf)


    f"""{ffmpeg }This is my quoted variable: "{var_a}". """
    ## checkInpu

    command_list = [
        ffmpeg,
        "-re -i",
        cf["input_file"],
        "-y -preset",
        cf["preset"],
        "-keyint_min",
        cf["keyint_min"],
        "-g",
        cf["gop_size"],
        "-sc_threshold",
        cf["sc_threshold"],
        "-r",
        cf["fps"],
        "-c:v ",
        cf["codec_video"],
        "-pix_fmt",
        cf["pixel_format"],
        "-c:a",
        cf["codec_audio"],
        "-b:a",
        cf["bitrate_audio"],
        "-ac",
        cf["audio_channel"],
        "-ac",
        cf["audio_channel"],
        "-ar",
        cf["audio_rate"],
        "-map v:0 -s:0 $V_SIZE -b:v:0 2000K -maxrate:0 2000K -bufsize:0 2000K/2",
        "-map v:0 -s:1 $V_SIZE -b:v:1 1000K -maxrate:1 1000K -bufsize:1 1000K/2",
        "-map v:0 -s:2 $V_SIZE -b:v:2 500K -maxrate:2 500K -bufsize:2 500K/2",
        "-map 0:a",
        "-init_seg_name",
        cf["init_seg_name"],
        "-media_seg_name",
        cf["media_seg_name"],
        "-use_template",
        cf["use_template"],
        "-use_timeline",
        cf["use_timeline"],
        "-seg_duration",
        cf["segment_duration"],
        "-adaptation_sets",
        cf["adaptation_sets_fmt"],
        "-f dash",
        cf["mpd_filepath"],
        "index.mpd"
    ]
    return command_list


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("The new directory is created!")


def generate_dash_files(configs):
    for cf in configs:
        cmd = build_dash_command(cf)
        #cmd = [ffmpeg, "-i", "./media/4k60fps.webm ","./media/output.mp4"]
        create_directory(cf["mpd_filepath"])
        print(cmd)
        if subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).returncode == 0:
            print("FFmpeg Script Ran Successfully")
        else:
            print("There was an error running your FFmpeg script")


def generate_hls_files(configs):
    print(configs)


def run_ffmpeg():
    filepath = grab_user_input()
    config = read_config(filepath)
    generate_dash_files(config["dash"])
    # generate_hls_files(config.hls)


if __name__ == "__main__":
    run_ffmpeg()
