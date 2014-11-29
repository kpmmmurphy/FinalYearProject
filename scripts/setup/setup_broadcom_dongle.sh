#!/bin/bash

#Install the nessesary firmware for the Broadcom Pi dongle
git clone --depth=1 git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git

#Copy the firemware into the OS firware dir
echo "Copying Firmware Files.."
cd linux-firmware
sudo cp -R * /lib/firmware

#clean up
echo "Cleaning Up..."
cd ..
rm -rf linux-firmware

echo "Done!"
