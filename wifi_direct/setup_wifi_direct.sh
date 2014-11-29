#Sets up Wifi Direct

#Author: Kevin Murphy
#Date  : 27 - Oct - 14

#Get the latest version of the wpa_supplicant
#git clone git://w1.fi/srv/git/hostap.git

#Install the dev version of OpenSSL
#sudo apt-get install libssl-dev

#Install Netlink Protocol Library Suite
#sudo apt-get install libnl-dev

#Install libpcsclite for interfacing with smart cards 
sudo apt-get install libpcsclite-dev 

#Install DBUS for application communication
sudo apt-get install libdbus-1-dev

#Make and make install 
sudo make && make install

#Create p2p interface
#iw phy 'ls /sys/class/ieee80211/' interface add p2p0 type managed
