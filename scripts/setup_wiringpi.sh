#Installs and build the c GPIO lib : wiring pi

sudo apt-get update

sudo apt-get upgrade

apt-get install git-core

git clone git://git.drogon.net/wiringPi

cd wiringPi

git pull origin

cd wiringPi

./build
