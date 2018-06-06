# ReallySmartLights
This project takes IKEA's amazing Trådfri light bulbs and bump them to the next level. ReallySmartLights simply simulates daylight. This projct could improve your workflow and also improve your life.

## Table of Contents
[TOC]

## Requirements
* IKEA Trådfri gateway
* IKEA Trådfri bulb
* Raspberry Pi with ArchLinuxARM and these packages:
    * Python 3

## Installation of ArchLinuxuARM
Replace sdX in the following instructions with the device name for the SD card as it appears on your computer.

1. Start fdisk to partition the SD card: `fdisk /dev/sdX`
2. At the fdisk prompt, delete old partitions and create a new one:
    * Type **o**. This will clear out any partitions on the drive.
    * Type **p** to list partitions. There should be no partitions left.
    * Type **n**, then **p** for primary, **1** for the first partition on the drive, press **ENTER** to accept the default first sector, then type **+100M** for the last sector.
    * Type **t**, then **c** to set the first partition to type W95 FAT32 (LBA).
    * Type **n**, then **p** for primary, **2** for the second partition on the drive, and then press **ENTER** twice to accept the default first and last sector.
    * Write the partition table and exit by typing **w**.
3. Create and mount the FAT filesystem: `mkfs.vfat /dev/sdX1; mkdir boot; mount /dev/sdX1 boot;`
4. Create and mount the ext4 filesystem: `mkfs.ext4 /dev/sdX2; mkdir root; mount /dev/sdX2 root;`
5. Download and extract the root filesystem (as root, not via sudo): `wget http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-latest.tar.gz`
`bsdtar -xpf ArchLinuxARM-rpi-latest.tar.gz -C root`
`sync`
6. Move boot files to the first partition:
`mv root/boot/* boot`
7. Unmount the two partitions:
`umount boot root`
8. Insert the SD card into the Raspberry Pi, connect ethernet, and apply 5V power.
9. Use the serial console or SSH to the IP address given to the board by your router.
    * Login as the default user alarm with the password alarm.
    * The default root password is root.

## Preparing of enviroment
* `sudo pacman -S python3 python-pip git`
* `pip3 install ephem pytradfri`
* Run this script from: [ggravlingen/pytradfri](https://github.com/ggravlingen/pytradfri/blob/master/script/install-coap-client.sh)
* `cd ..`

## Obtain and configure ReallySmartLights
* `git clone https://github.com/hrubymar10/ReallySmartLights`
* `cd ReallySmartLights`
* Run once `python3 ReallySmartLights.py` and copy your identity and PSK for later usage.
* In your favourite text editor (nano, vim, gedit, VSCode, ..) edit `ReallySmartLights.py` and edit these values:
    * **__DEBUG__** - True/False - Show more logs? good for development.
    * **__verbosity__** - 0/1/2 - How much output will be shown.
    * **city** - Prague/New York - add name of coty where are you located.
    * **force_RSL_values** - True/False - Do you want RSL to override values setted up manually during day?
    * **bulbs** - Array of ids of bulbs.
    * **IP** - IP of Trådfri gateway.
    * **key** - security key of Trådfri gateway.
    * **identity** - Paste identity obtained in first run here.
    * **psk** - Paste psk obtained in first run here.

    * Example:

```
######################### CONFIG #########################
__DEBUG__ = True
__verbosity__ = 2

time_diff = 102 # Default: 102
min_light = 4540 # Default: 4540
max_light = 2500 # Default: 2500

city = "Prague" # Enter here name of city where do you live.

force_RSL_values = True # Do you want force RSL values during day and night?

bulbs = [3, 4] # id or ids of bulbs

IP = "192.168.0.24" # IP address of your IKEA Trådfri gateway
key = "vxtOmQ88e5DSS1JG" # Security key of your IKEA Trådfri gateway

#### Fill these informations after first run ####
identity = "61111fc660d348f995cbc48e991219bc"
psk = "DO8fUI1jhqlqZnJt"
#### /Fill these informations after first run ####

######################### /CONFIG #########################
```
* Now you can run `python3 ReallySmartLights.py` and enjoy your smart lights.

