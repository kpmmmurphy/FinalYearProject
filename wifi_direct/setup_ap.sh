#Author: Kevin Murphy
#Date:   6 - Jan - 15
#Sets up raspberry pi as an access point

sudo apt-get install hostapd udhcpd

sudo cp ./ap_config_files/udhcpd.conf /etc/udhcpd.conf

sudo cp ./ap_config_files/udhcpd /etc/default/udhcpd

sudo cp ./ap_config_files/interfaces /etc/network/interfaces 

sudo cp ./ap_config_files/hostapd.conf /etc/hostapd/hostapd.conf 

sudo cp ./ap_config_files/hostapd /etc/default/hostapd 

sudo echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

#Setting up IP Tables
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

sudo update-rc.d hostapd enable
sudo update-rc.d udhcpd enable
