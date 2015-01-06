#Sets up all neeeded componented for Wifi Direct on the Raspberry Pi

#Author: Kevin Murphy
#Date  : 27 - Oct - 14

#Get the latest version of the wpa_supplicant and hostapd
#git clone git://w1.fi/srv/git/hostap.git

#Install Hostapd
#sudo apt-get install hostapd

#Copy custom .config into ./hostap/hostap
##------------

#Make hostapd and move the compiled version to /usr/sbins
#sudo ./hostap/hostapd make 
#sudo cp hostadp /usr/sbin/

#Install the dev version of OpenSSL
sudo apt-get install libssl-dev

#Install Netlink Protocol Library Suite	
sudo apt-get install libnl-3-dev
sudo apt-get install libnl-genl-3-dev

#Install libpcsclite for interfacing with smart cards 
sudo apt-get install libpcsclite-dev 

#Install DBUS for application communication
sudo apt-get install libdbus-1-dev

#Install Readline
sudo apt-get install libreadline-dev

#Install LibnCurses
sudo apt-get install libncurses5-dev

#Untar the files
tar -zxvf ./wpa_supplicant-2.3.tar.gz

#Copy custom wpa_supplicant .config file
sudo cp ./config/def_p2p_config ./wpa_supplicant-2.3/wpa_supplicant/.config

#Make and make install wpa_supplicant
sudo ./wpa_supplicant-2.3/wpa_supplicant/ make BINDIR=/sbin LIBDIR=/lib && sudo ./wpa_supplicant-2.3/wpa_supplicant/ make install

#Create p2p interface
#iw phy 'ls /sys/class/ieee80211/' interface add p2p0 type manage
