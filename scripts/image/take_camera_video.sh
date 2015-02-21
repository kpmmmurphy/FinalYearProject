#!/bin/bash

#This script when called will snap an still image and return its address

#Check if the directory exists
if [ ! -d "/home/pi/FinalYearProject/camera/video" ]; then
  mkdir -p /home/pi/FinalYearProject/camera/video
fi

if [ ! -d "/home/pi/FinalYearProject/camera/video_backup" ]; then
  mkdir -p /home/pi/FinalYearProject/camera/video_backup
fi

mv /home/pi/FinalYearProject/camera/video/* /home/pi/FinalYearProject/camera/video_backup/

DATE=$(date +"%Y-%m-%d_%H%M")

raspivid -t 10000 -w 1280 -h 720 -b 8000000 -o /home/pi/FinalYearProject/camera/video/$DATE.h264  -vf
#ffmpeg -r 30 -i /home/pi/FinalYearProject/camera/video/$DATE.h264 -vcodec copy /home/pi/FinalYearProject/camera/video/$DATE.mkv
MP4Box -fps 30 -add /home/pi/FinalYearProject/camera/video/$DATE.h264 /home/pi/FinalYearProject/camera/video/$DATE.mp4
sudo rm /home/pi/FinalYearProject/camera/video/$DATE.h264
	