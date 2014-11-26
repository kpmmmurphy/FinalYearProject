#Lists all available Wifi Networks
#Will be used when connecting via App

sudo iwlist wlan0 scan | grep ESSID
