#!/bin/bash

#Install
sudo apt-get install libjpeg8-dev imagemagick libv4l-dev

#Add missing videodev.h
sudo ln -s /usr/include/linux/videodev2.h /usr/include/linux/videodev.h

#download MJPG streamer
wget http://sourceforge.net/code-snapshots/svn/m/mj/mjpg-streamer/code/mjpg-streamer-code-182.zip

#Unzip
unzip mjpg-streamer-code-182.zip

#Build Mjpg streamer
cd mjpg-streamer-code-182/mjpg-streamer
make mjpg_streamer input_file.so output_http.so

#Install
sudo cp mjpg_streamer /usr/local/bin
sudo cp output_http.so input_file.so /usr/local/lib/
sudo cp -R www /usr/local/www

