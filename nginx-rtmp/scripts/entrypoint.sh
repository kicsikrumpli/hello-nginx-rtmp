#!/bin/bash

# start nginx
/usr/local/nginx/sbin/nginx

# start streaming
echo "go to http://localhost:8080/hls/stream.m3u8 to play stream"
echo "------------\n"

if [ -z "$1" ]
then
      source="https://www.rmp-streaming.com/media/big-buck-bunny-360p.mp4"
else
      source="$1"
fi

# NB!
# -re -f mjpeg -i $source for MJPG (NOT mpjpeg)
# mjpeg sources don't need this proxy:
#   - real time,
#   - low fps,
#   - can be passed directly to opencv video capture
ffmpeg -re -i $source \
    -vprofile baseline \
    -g 30 \
    -strict -2 \
    -f flv \
    -c:a aac \
    -c:v libx264 \
    rtmp://localhost/show/stream

echo "----- done -----"

# sleep infinity

