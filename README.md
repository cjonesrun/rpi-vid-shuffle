generic rpi video shuffler.

idea from:
http://stephencoyle.net/the-pi-zero-simpsons-shuffler/

put video files in ~/videos/
put splash screen images in ~/splash/
put shuffle.py in ~/
update .profile (see below)

installation:
partition 64gb sd card into a FAT32 boot partition (4GB?) and an exFAT partition with the remaining space.
see: https://www.raspberrypi.org/documentation/installation/sdxc_formatting.md

burn raspbian jessie lite to SD card
sudo apt-get install fbi
sudo apt-get install omxplayer

set rpi to auto login via raspi-config

cp shuffle.py to ~/
mkdir ~/splash/
mkdir ~/videos/

copy splash screen images to splash/
copy videos to videos/

add this to .profile

# start splash screen if not already running
# pgrep fbi || sudo fbi -T 7 -t 4 -noverbose -a /home/pi/splash/*.jpg # this barfs a procid to stdout
F_COUNT=$(pgrep fbi | wc -l)
if [ "$F_COUNT" -eq "0" ]; then
    sudo fbi -T 7 -t 4 -noverbose -a /home/pi/splash/*.jpg
#else
#    echo "$F_COUNT fbi procs running"
fi

# start shuffle if not already running
# pgrep shuffle.py || /home/pi/shuffle.py # this barfs a procid to stdout
S_COUNT=$(pgrep shuffle.py | wc -l)
if [ "$S_COUNT" -eq "0" ]; then
    /home/pi/shuffle.py
#else
#    echo "$S_COUNT shuffle.py procs running"
fi

