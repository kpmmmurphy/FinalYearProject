#!/bin/bash

#Starts a video stream and pipes the output to vlc streamer
raspivid -o - -t 99999 -hf -w 640 -h 360 -fps 25 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264                                                                                                                                  