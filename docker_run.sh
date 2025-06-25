#!/bin/bash

while true; do
    python /extract_stream_url.py $CHANNEL $LOGO_URL $STREAM_TYPE > /out/tv.m3u
    echo "extracted stream url"
    sleep $INTERVAL
done
