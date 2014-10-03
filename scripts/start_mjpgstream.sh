#!/bin/bash

mkdir /tmp/stream

#Start the camera capturing images periodically
raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0 &

#Get the IP address, and time the trailing whitespace
HOST_IP_ADDRESS=$(hostname -I | tr -d ' ')

echo -e "\n\----- Visit http://$HOST_IP_ADDRESS:8080 for the stream -----\\n"

LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /usr/local/www"

