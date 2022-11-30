import subprocess
import re
import glob
import sys
import fileinput
import os
import helpers.commandbuilder as cb
import helpers.mongohandler as mongo
import helpers.s3handler as s3
import json
from dotenv import load_dotenv

load_dotenv()
ffmpeg = os.environ.get("FFMPEG")
base_path = os.environ.get("OUTPUT_ABSOLUTE_PATH")
db = None


def upload_files(input_dir, s3_path):
    """
    Upload the files to the s3 bucket
    Args:
        input_dir: The directory to upload
        s3_path:  The path in the s3 bucket
    """
    if s3.AWS_ACCESS_KEY_ID and s3.AWS_SECRET_ACCESS_KEY and s3.BUCKET_NAME:
        s3.upload_folder_to_s3(input_dir, s3_path)


def save_config(col_name, cf):
    """
    Save a config in the database
    Args:
        col_name:  The collection name
        cf: the config to save
    """
    col = mongo.get_collection(db, col_name)
    mongo.insert_config(col, cf)


def clean_hls_stream_paths(filepath):
    m3u8_files = [file for file in glob.glob(filepath + "/" + "*.m3u8")]
    for path in m3u8_files:
        fin = open(path, "rt")
        # read file contents to string
        data = fin.read()
        # replace all occurrences of the required string
        data = data.replace(filepath, '.')
        # close the input file
        fin.close()
        # open the input file in write mode
        fin = open(path, "wt")
        # overwrite the input file with the resulting data
        fin.write(data)
        # close the file
        fin.close()


def process_configs(stream_type, configs):
    assert base_path, 'OUTPUT_BASE_PATH must be configured in the as an environment variable.'
    """
    Process the passed configs and generate media streams, store them on s3 and keep the config data in a mongo db
    Args:
        stream_type: The type of configs to process ['hls', 'dash']
        configs: An array of configs to process
    """
    for cf in configs:
        filepath = base_path + cf["output_path"]
        if stream_type == 'dash':
            cmd = build_dash_command(cf)
        else:
            cmd = build_hls_command(cf)
        create_directory(filepath)
        cmd = re.sub(' +', ' ', cmd)
        print("Executing the following command:")
        print(cmd)
        # shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        if subprocess.run(cmd).returncode == 0:
            print("FFmpeg Script Ran Successfully")
            if stream_type == 'hls':
                clean_hls_stream_paths(filepath)
                upload_files(filepath, cf["output_path"])
            else:
                upload_files(filepath, cf["output_path"])
            if not (db is None):
                save_config(stream_type, cf)
        else:
            print("There was an error running your FFmpeg script")


def generate_streams(config):
    """
    Take a config and start generating hls and dash compliant media  streams
    Args:
        config: The config to use
    """
    if mongo.MONGO_URI and mongo.MONGO_DB:
        global db
        db = mongo.connect()
    if 'hls' in config:
        process_configs('hls', config['hls'])
    if 'dash' in config:
        print("Processing dash configs")
        process_configs('dash', config['dash'])


def build_base_command(cf):
    """
    Build the first part of the ffmpeg command
    Args:
        cf: The config to use to build the command
    Returns:  The command in string format

    """
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
    return cmd


def build_dash_command(cf):
    """
    Build the hls command to generate dash compliant media stream
    Args:
        cf: the config to use
    Returns: The command in string format
    """
    cmd = build_base_command(cf)
    cmd = cb.add_dash_attributes(cmd, cf)
    return cmd


def build_hls_command(cf):
    """
    Build the hls command to generate hls compliant media stream
    Args:
        cf: the config to use
    Returns: The command in string format
    """
    cmd = build_base_command(cf)
    cmd = cb.add_hls_attributes(cmd, cf)
    return cmd


def create_directory(path):
    """
    create the output directory if it doesn't exist
    Args:
        path: The path to create
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print("The new directory is created!")


if __name__ == "__main__":
    with open("../config.json", 'r') as f:
        generate_streams(json.load(f))
