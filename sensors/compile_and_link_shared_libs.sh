#!/bin/bash

LIBS="libs"

#Comiple all files and create shared object
sudo g++ -Wall -fPIC -shared *.cpp -o lib_SensorManager.so -lwiringPi

#Move all .so files in to ./libs dir
if [ ! -d "./$LIBS" ]; then
    sudo mkdir $LIBS
fi

sudo mv *.so ./$LIBS
