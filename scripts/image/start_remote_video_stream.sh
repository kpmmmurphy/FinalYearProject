#!/bin/bash

#Starts a video stream and pipes the output to vlc streamer
#raspivid -o - -t 99999 -hf -w 640 -h 360 -fps 25 | cvlc -vvv stream:///dev/stdin --miface 'wlan0' --sout '#transcode{fps=15,vcodec=mp4v,vb=500,scale=1,width=352,height=240,acodec=mp4a,ab=128,channels=2,samplerate=22050,deinterlace,audio-sync}:gather:rtp{sdp=rtsp://:8554/stream.sdp}' :demux=h264

#raspivid -o - -t 99999 -hf -w 640 -h 360 -fps 25 | cvlc -vvv -I v4l2://:vdev=/dev/video:width=640:height=480:fps=2 --sout "#transcode{vcodec=mp4v,fps=5,vb=800,acodec=mpga,samplerate=8000,ab=64,deinterlace,channels=1,sfilter='mosaic:marq{marquee=%m-%d-%Y_%H:%M:%S,size=16,color=16711680,position=5,opacity=64}'}:rtp{sdp=rtsp://:8554/stream.sdp}"                                                                                                         

sudo modprobe -r bcm2835-v4l2
sudo modprobe bcm2835-v4l2
cvlc --run-time 30 v4l2:///dev/video0 --v4l2-width 1920 --v4l2-height 1080 --v4l2-vflip --v4l2-chroma h264 --sout '#standard{access=http,mux=ts,dst=:12345}'                         
