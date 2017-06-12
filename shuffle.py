#!/usr/bin/python

import RPi.GPIO as GPIO
import os
import Queue
import random
import time
from threading import Thread

# constants
buttonPin = 27                  # pin #13          
directory = "/home/pi/videos/"  # vid dir
btnDblBounceLimit = 0.15        # ignore dbl bounces on the button
btnAddToQueueTimeLimit = 2      # button presses within 2s of each other

# init
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN)
lastPressed = time.time()
q = Queue.Queue();


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
    
    if timeSinceLast < btnDblBounceLimit:
        # print '*** double bounce caught, ignoring', timeSinceLast
        continue
    elif timeSinceLast < btnAddToQueueTimeLimit:
        # print 'queueing up next episode', timeSinceLast
        q.put(random.choice(os.listdir(directory)))
    else:
        # print 'clearing queue and starting over', timeSinceLast
        with q.mutex:
            q.queue.clear()
        q.put(random.choice(os.listdir(directory)))

#    print "queue:"	
#    for elem in list(q.queue):
#    	print 'queue->', elem
#    print "end."
    lastPressed = time.time()

print '*** Main thread waiting'
q.join()
print '*** Done'
GPIO.cleanup()
