#!/bin/bash

#This script when called will snap an still image and return its address

#Check if the camera directory exists
if [ ! -d "/home/pi/FinalYearProject/camera/video" ]; then
  mkdir -p /home/pi/FinalYearProject/camera/video
fi

DATE=$(date +"%Y-%m-%d_%H%M")

raspivid -o /home/pi/FinalYearProject/camera/video/$DATE.h264 -t 10000
