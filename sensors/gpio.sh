# Copy this file to /etc/init.d/gpio and run 
#   update-rc.d -f gpio defaults
# to run it on every boot.
# This code is for Raspberry Pi
# Do what you want with this script

for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 21 22 23 24 25 26
do
    echo $i > /sys/class/gpio/export
    chmod 777 /sys/class/gpio/gpio$i/*
done

exit 0

