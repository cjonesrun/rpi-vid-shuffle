generic rpi video shuffler.

idea from:
http://stephencoyle.net/the-pi-zero-simpsons-shuffler/

usage:
single press starts a random episode
subsequent presses within 2s add another random episode to the queue. queue up N episodes at a time.

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

