from dotenv import load_dotenv
import os

load_dotenv()
base_path = os.environ.get("OUTPUT_BASE_PATH")


def add_input(cmd, cf):
    assert 'input_file' in cf, 'The config is missing mandatory attribute : input_file'
    return cmd + " -re -i " + cf['input_file']


def add_preset(cmd, cf):
    if 'preset' in cf:
        return cmd + " -y -preset " + cf['preset']
    return cmd


def add_key_min(cmd, cf):
    if 'keyint_min' in cf:
        return cmd + " -keyint_min " + str(cf['keyint_min'])
    return cmd


def add_gop_size(cmd, cf):
    if 'gop_size' in cf:
        return cmd + " -g " + str(cf['gop_size'])
    return cmd


def add_threshold(cmd, cf):
    if 'sc_threshold' in cf:
        return cmd + " -sc_threshold " + str(cf['sc_threshold'])
    return cmd


def add_fps(cmd, cf):
    if 'fps' in cf:
        return cmd + " -r " + str(cf['fps'])
    return cmd


def add_video_codec(cmd, cf):
    if 'codec_video' in cf:
        return cmd + " -c:v " + cf['codec_video']
    return cmd


def add_pixel_format(cmd, cf):
    if 'pixel_format' in cf:
        return cmd + " -pix_fmt " + cf['pixel_format']
    return cmd


def add_audio_bitrate(cmd, cf):
    if 'bitrate_audio' in cf:
        return cmd + " -b:a " + cf['bitrate_audio']
    return cmd


def add_audio_codec(cmd, cf):
    if 'codec_audio' in cf:
        return cmd + " -c:a " + cf['codec_audio']
    return cmd


def add_audio_channel(cmd, cf):
    if 'audio_channel' in cf:
        return cmd + " -ac " + str(cf['audio_channel'])
    return cmd


def add_audio_rate(cmd, cf):
    if 'audio_rate' in cf:
        return cmd + " -ar " + str(cf['audio_rate'])
    return cmd


def add_video_mapping(cmd, cf):
    # TODO: adjust it according to passed config
    maps = """ -map v:0 -s:0 1280x720 -b:v:0 2000K -maxrate:0 2000K -bufsize:0 2000K/2 \
    -map v:0 -s:1 1280x720 -b:v:1 1000K -maxrate:1 1000K -bufsize:1 1000K/2 \
    -map v:0 -s:2 1280x720 -b:v:2 500K -maxrate:2 500K -bufsize:2 500K/2 """
    return cmd + maps


def add_audio_mapping(cmd, cf):
    # TODO: adjust it according to passed config
    maps = """ -map 0:a """
    return cmd + maps


def add_filters(cmd, cf):
    return cmd


def add_dash_attributes(cmd, cf):
    assert 'output_path' in cf, 'The config is missing mandatory attribute : output_path'
    if 'init_seg_name' in cf:
        cmd = cmd + " -init_seg_name " + cf['init_seg_name']
    if 'media_seg_name' in cf:
        cmd = cmd + " -media_seg_name " + cf['media_seg_name']
    if 'use_template' in cf:
        cmd = cmd + " -use_template " + str(cf['use_template'])
    if 'use_timeline' in cf:
        cmd = cmd + " -use_timeline " + str(cf['use_timeline'])
    if 'segment_duration' in cf:
        cmd = cmd + " -seg_duration " + str(cf['segment_duration'])
    if 'adaptation_sets_fmt' in cf:
        cmd = cmd + f''' -adaptation_sets "{cf['adaptation_sets_fmt']}" '''
    cmd = cmd + " -f dash " + base_path + cf['output_path'] + "index.mpd"
    return cmd


def add_hls_attributes(cmd, cf):
    assert 'hls_playlist_type' in cf, 'The config is missing mandatory attribute : hls_playlist_type'
    assert 'hls_segment_filename' in cf, 'The config is missing mandatory attribute : hls_segment_filename'

    cmd = cmd + " -map a:0 -map a:0 -map a:0 "
    cmd = cmd + " -f hls "
    cmd = cmd + " -hls_playlist_type " + str(cf['hls_playlist_type'])
    cmd = cmd + " -master_pl_name index.m3u8  "
    cmd = cmd + ' -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" '
    if 'hls_time' in cf:
        cmd = cmd + " -hls_time " + str(cf['hls_time'])
    if 'hls_flags' in cf:
        cmd = cmd + " -hls_flags " + cf['hls_flags']
    if 'strftime_mkdir' in cf:
        cmd = cmd + " -strftime_mkdir " + str(cf['strftime_mkdir'])
    if 'hls_segment_filename' in cf:
        cmd = cmd + " -hls_segment_filename " + cf['output_path'] + str(cf['hls_segment_filename'])
    if 'hls_segment_filename' in cf:
        cmd = cmd + " " + base_path + cf['output_path'] + str(cf['stream_filename'])
    return cmd
