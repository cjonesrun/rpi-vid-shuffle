#!/usr/bin/python

import os
import Queue
import random
import time
from threading import Thread

# constants
#directory = "/home/pi/videos/"  # vid dir
directory = "/home/cjones/tmp/"  # vid dir
btnDblBounceLimit = 0.15        # ignore dbl bounces on the button
btnAddToQueueTimeLimit = 2      # button presses within 2s of each other

# init
lastPressed = time.time()
q = Queue.Queue();
playing = None

def play(item):
    global playing
    print 'consumer->playing', item, 'remaining', q.qsize()
    playing = item
    time.sleep(2)
    playing = None
    print 'consumer->finished', item, 'remaining', q.qsize()

def stop(item):
    print '-->stopping current', playing, q.qsize()
    
def consumer():
    global playing
    while True:
        q.get() # this will wait until there is a token in the queue
        play( random.choice(os.listdir(directory)) )

def keyPress():
    while True:
        x = raw_input()
        print x
        fired()

def fired():
    global lastPressed
    timeSinceLast = (time.time()-lastPressed)

    if timeSinceLast < btnDblBounceLimit:
        # print '->double bounce caught, ignoring', q.qsize()
        return 
    elif timeSinceLast > btnAddToQueueTimeLimit:
        if q.qsize() > 0:
            print '-->clearing queue and starting over', q.qsize()
            with q.mutex:
                q.queue.clear()
        if playing:
            stop(playing)

    lastPressed = time.time()
    print '-->adding item to queue', (1+q.qsize())
    q.put(lastPressed)


def main():
    try:
        # hook GPIO pin waiting here to call fired()

        # start up a consumer thread thread to grab queued events
        t = Thread(target=consumer)
        t.daemon = True
        t.start()

        # start up a worker thread to listen for key presses
        t2 = Thread(target=keyPress)
        t2.daemon = True
        t2.start()

        # wait for consumer thread to be done.
        t.join()

        time.sleep(10)
    except KeyboardInterrupt:
        print "stopping"
    except Exception:
        print "exception"

if __name__ == '__main__':
    main()
