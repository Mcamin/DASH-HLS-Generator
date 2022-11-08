#!/bin/bash
#HLS and fallback code from zazu.berlin 2020, Version 20200424
# https://blog.zazu.berlin/internet-programmierung/mpeg-dash-and-hls-adaptive-bitrate-streaming-with-ffmpeg.html

VIDEO_IN=./4k60fps.webm
VIDEO_OUT=./HLS/20
HLS_TIME=4
FPS=30
GOP_SIZE=60
PRESET_P=veryfast
V_SIZE_1=1280x720


# HLS
ffmpeg -i $VIDEO_IN -y \
    -preset $PRESET_P -keyint_min $GOP_SIZE -g $GOP_SIZE -sc_threshold 0 -r $FPS -c:v libx264 -pix_fmt yuv420p \
     -filter_complex "split=3[s0][s1][s2];\
        [s0]drawtext=text='1280x720-2000K':x=(w-text_w)/2:y=(h-text_h)/4:box=1:boxcolor=black@0.8:\
        fontsize=80:fontcolor=white;\
        [s1]drawtext=text='1280x720-1600K':x=(w-text_w)/2:y=(h-text_h)/4:box=1: boxcolor=black@0.8:\
        fontsize=80:fontcolor=white;\
        [s2]drawtext=text='1280x720-1280K':x=(w-text_w)/2:y=(h-text_h)/4:box=1: boxcolor=black@0.8:\
        fontsize=80:fontcolor=white" \
    -map v:0 -s:0 $V_SIZE_1 -b:v:0 2000K -maxrate:0 2000K -bufsize:0 2000K/2 \
    -map v:0 -s:1 $V_SIZE_1 -b:v:1 1600K -maxrate:1 1600K -bufsize:1 1600K/2 \
    -map v:0 -s:2 $V_SIZE_1 -b:v:2 1280K -maxrate:2 1280K -bufsize:2 1280K/2 \
    -map a:0 -map a:0 -map a:0 -c:a aac -b:a 128k -ac 1 -ar 44100\
    -f hls -hls_time $HLS_TIME -hls_playlist_type vod -hls_flags independent_segments \
    -master_pl_name index.m3u8 \
    -hls_segment_filename $VIDEO_OUT/stream_%v/s%06d.ts \
    -strftime_mkdir 1 \
    -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" $VIDEO_OUT/stream_%v.m3u8
