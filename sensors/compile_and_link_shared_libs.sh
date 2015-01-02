#!/bin/bash

LIBS="libs"

#Comiple all files and create shared object
<<<<<<< HEAD
sudo g++ -Wall -fPIC -v -shared *.h *.cpp -o lib_SensorManager.so -lwiringPi
=======
sudo g++ -Wall -fPIC -shared  *.cpp -o lib_SensorManager.so -lwiringPi
>>>>>>> b44f4aa3ecf2801294bedf3fd41f540fbd010418

#Move all .so files in to ./libs dir
if [ ! -d "./$LIBS" ]; then
    sudo mkdir $LIBS
fi

sudo mv *.so ./$LIBS
