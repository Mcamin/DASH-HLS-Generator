import subprocess
import json

ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg"


def grab_user_input():
    def filter_input(message, default):
        user_input = input(message)

        if user_input == "":
            user_input = default
        return user_input

    print("Hit enter for default value\n")
    return filter_input("Config File: ", "./config.json")


def read_config(filepath='./config.json'):
    with open(filepath, 'r') as f:
        data = json.load(f)
        return data


def build_dash_command(cf):
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
        "-filter_complex",
        "-adaptation_sets",
        cf["adaptation_sets_fmt"],
        "-f dash",
        cf["mpd_filepath"],
    ]


def generate_dash_files(configs):
    print(configs)
    dash_cmds_list = []
    for cf in configs:
        dash_cmds_list.append(build_dash_command(cf))


def generate_hls_files(configs):
    print(configs)


def run_ffmpeg():
    filepath = grab_user_input()
    config = read_config(filepath)
    generate_dash_files(config.dash)
    generate_hls_files(config.hls)


if __name__ == "__main__":
    run_ffmpeg()
