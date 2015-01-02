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

raspivid -o /home/pi/FinalYearProject/camera/video/$DATE.h264 -t 10000
