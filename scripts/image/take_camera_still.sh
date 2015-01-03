#!/bin/bash

#This script when called will snap an still image and return its address

#Check if the camera directory exists
if [ ! -d "/home/pi/FinalYearProject/camera/still" ]; then
  mkdir -p /home/pi/FinalYearProject/camera/still
fi

if [ ! -d "/home/pi/FinalYearProject/camera/still_backup" ]; then
  mkdir -p /home/pi/FinalYearProject/camera/still_backup
fi

mv /home/pi/FinalYearProject/camera/still/* /home/pi/FinalYearProject/camera/still_backup/

DATE=$(date +"%Y-%m-%d_%H%M")

raspistill -vf -hf --width 1080 --height 720 --quality 100 -o /home/pi/FinalYearProject/camera/still/$DATE.jpg
