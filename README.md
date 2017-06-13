generic rpi video shuffler.

- single button press plays a random video.
- pressing again within 2 seconds will add another random video to the playlist
- after 2 seconds, button press will stop current video, clear playlist and start a new random video.

RPI GPIO pin layout info:
https://pinout.xyz/

idea from:
http://stephencoyle.net/the-pi-zero-simpsons-shuffler/

installation:
burn raspbian jessie lite img to 64gb SD card
sudo apt-get install fbi
sudo apt-get install omxplayer

put video files in ~/videos/
put splash screen images in ~/splash/
put shuffle.py in ~/
update .profile (see below)

set rpi to auto login via raspi-config

copy splash screen images to splash/
copy videos to videos/

add below to .profile

# start splash screen if not already running
F_COUNT=$(pgrep fbi | wc -l)
if [ "$F_COUNT" -eq "0" ]; then
    sudo fbi -T 7 -t 4 -noverbose -a /home/pi/splash/*.*
#else
#    echo "$F_COUNT fbi procs running"
fi

# start shuffle if not already running
S_COUNT=$(pgrep shuffle.py | wc -l)
if [ "$S_COUNT" -eq "0" ]; then
    /home/pi/shuffle.py
#else
#    echo "$S_COUNT shuffle.py procs running"
fi


momentary button:
solder momentary button to desired GPIO pin, ground and 3.3v. 
see circuit diagram: button-schematic.png
