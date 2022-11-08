#!/bin/bash
#Dash and fallback code from zazu.berlin 2020, Version 20200424
# https://blog.zazu.berlin/internet-programmierung/mpeg-dash-and-hls-adaptive-bitrate-streaming-with-ffmpeg.html

VIDEO_IN=../media/4k60fps.webm
FPS=30
GOP_SIZE=60
PRESET_P=veryfast
V_SIZE=1280x720


ffmpeg -i $VIDEO_IN -y \
    -preset $PRESET_P -keyint_min $GOP_SIZE -g $GOP_SIZE -sc_threshold 0 -r $FPS -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 128k -ac 1 -ar 44100 \
    -filter_complex "split=3[s0][s1][s2];\
    [s0]drawtext=text='$V_SIZE-2.0M':x=(w-text_w)/2:y=(h-text_h)/4:box=1:boxcolor=black@0.8:\
    fontsize=80:fontcolor=white;\
    [s1]drawtext=text='$V_SIZE-1.0M':x=(w-text_w)/2:y=(h-text_h)/4:box=1: boxcolor=black@0.8:\
    fontsize=80:fontcolor=white;\
    [s2]drawtext=text='$V_SIZE-0.5M':x=(w-text_w)/2:y=(h-text_h)/4:box=1: boxcolor=black@0.8:\
    fontsize=80:fontcolor=white" \
    -map v:0 -s:0 $V_SIZE -b:v:0 2000K -maxrate:0 2000K -bufsize:0 2000K/2 \
    -map v:0 -s:1 $V_SIZE -b:v:1 1000K -maxrate:1 1000K -bufsize:1 1000K/2 \
    -map v:0 -s:2 $V_SIZE -b:v:2 500K -maxrate:2 500K -bufsize:2 500K/2 \
    -map 0:a \
    -init_seg_name init\$RepresentationID\$.\$ext\$ -media_seg_name chunk\$RepresentationID\$-\$Number%05d\$.\$ext\$ \
    -use_template 1 -use_timeline 1  \
    -seg_duration 4 -adaptation_sets "id=0,streams=v id=1,streams=a" \
    -f dash ../media/dash/index.mpd




