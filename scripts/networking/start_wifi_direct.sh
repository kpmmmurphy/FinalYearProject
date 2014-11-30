#!/bin/bash
#Starts all programs for running Wifi-direct

sudo ifdown wlan0 -v

sudo ifup wlan0 -v

#Remove the wlan0 interface from the run dir
sudo rm /var/run/wpa_supplicant/wlan0

#Start the wpa_supplicant
sudo wpa_supplicant -i wlan0 -c /etc/p2p.conf -Dnl80211 -B -dt

#hostapd -d /etc/hostapd.conf
