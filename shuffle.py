#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os
import random

buttonPin = 17

directory = "/home/pi/videos/"

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN)

def playEpisode():
    episode = random.choice(os.listdir(directory))
    print "Randomly Grabbed:", directory+episode
    cmd = "nohup omxplayer -b -o hdmi "+"'"+directory+episode+"' > /dev/null 2>&1 &"
    os.system('killall omxplayer.bin')
    os.system(cmd)

try:
    while True:
       GPIO.wait_for_edge(buttonPin, GPIO.FALLING)
       playEpisode()

    print "Serenity Now!"

except KeyboardInterrupt:
    GPIO.cleanup()
