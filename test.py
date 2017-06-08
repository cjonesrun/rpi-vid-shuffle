#!/usr/bin/python

import RPi.GPIO as GPIO
import os
import Queue
import random
import time
from threading import Thread

buttonPin = 17
directory = "/home/pi/videos/"
lastPressed = time.time()
q = Queue.Queue();

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN)

def worker():
    while True:
	print 'waiting'
        item = q.get()
	print 'handling', item
        #do_work(item)
        q.task_done()
	print "Done:", item

for i in range(1):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

#for item in ['1', '2', '3','4']:
#    q.put(item)
#    time.sleep(2)

while True:
    GPIO.wait_for_edge(buttonPin, GPIO.FALLING)
    timeSinceLast = (time.time()-lastPressed)
    
    if timeSinceLast < 0.15:
#	print '*** double bounce caught, ignoring', timeSinceLast
	continue
    elif timeSinceLast < 1:
	print 'queueing up next episode', timeSinceLast
	q.put(random.choice(os.listdir(directory)))
    else:
        print 'clearing queue and starting over', timeSinceLast
	with q.mutex:
    	    q.queue.clear()
	q.put(random.choice(os.listdir(directory)))
	

    lastPressed = time.time()
    #print 'time since last press', (time.time()-lastPressed)
    #lastPressed = time.time()
    #q.put("pressed")

print '*** Main thread waiting'
q.join()
print '*** Done'
