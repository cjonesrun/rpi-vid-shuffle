#!/usr/bin/python

import RPi.GPIO as GPIO
import os
import Queue
import random
import time
from threading import Thread

buttonPin = 27 #pin#13
directory = "/home/pi/videos/"
lastPressed = time.time()
q = Queue.Queue();

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN)

def worker():
    while True:
        item = q.get()
	print 'worker->playing', item
	#cmd = "nohup omxplayer -b -o hdmi "+"'"+directory+item+"' > /dev/null 2>&1 &"
	cmd = "omxplayer -b -o hdmi "+"'"+directory+item+"'"
        os.system('killall omxplayer.bin')
        os.system(cmd)
	#time.sleep(2)
	q.task_done()
	print 'worker->finished', item

# start up a single listener thread
for i in range(1):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

while True:
    GPIO.wait_for_edge(buttonPin, GPIO.FALLING)
    #raw_input("")
    timeSinceLast = (time.time()-lastPressed)
    
    if timeSinceLast < 0.15:
#	print '*** double bounce caught, ignoring', timeSinceLast
	continue
    elif timeSinceLast < 1:
#	print 'queueing up next episode', timeSinceLast
	q.put(random.choice(os.listdir(directory)))
    else:
#        print 'clearing queue and starting over', timeSinceLast
	with q.mutex:
    	    q.queue.clear()
	q.put(random.choice(os.listdir(directory)))
	

    for elem in list(q.queue):
	print 'queue->', elem

    lastPressed = time.time()
    #print 'time since last press', (time.time()-lastPressed)
    #lastPressed = time.time()
    #q.put("pressed")

print '*** Main thread waiting'
q.join()
print '*** Done'
GPIO.cleanup()
