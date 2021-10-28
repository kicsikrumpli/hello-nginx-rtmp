#!/usr/bin/env bash

echo "sample sources: "
echo "https://www.rmp-streaming.com/media/big-buck-bunny-360p.mp4"
echo "..."
echo "---"

docker run -it \
  -p 8080:8080 \
  -v "`pwd`/conf/nginx.conf:/usr/local/nginx/conf/nginx.conf" \
  -v "`pwd`/rec:/nginx/rec/" \
  kicsikrumpli/nginx \
  $1