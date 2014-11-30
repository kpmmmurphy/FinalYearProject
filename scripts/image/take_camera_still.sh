#!/bin/bash

#This script when called will snap an still image and return its address

#Check if the camera directory exists
if [ ! -d "/home/pi/camera" ]; then
  mkdir /home/pi/camera
fi

DATE=$(date +"%Y-%m-%d_%H%M")

raspistill -vf -hf -o /home/pi/camera/$DATE.jpg
