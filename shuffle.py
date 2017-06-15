#!/usr/bin/python

import RPi.GPIO as GPIO
import os
import Queue
import random
import time
import readline
import logging as log, logging.config
from threading import Thread

# constants
BUTTON_PIN = 27         	# pin #13
VIDEO_DIR = "/home/pi/videos/"  # vid dir
btnDblBounceLimit = 0.15        # ignore dbl bounces on the button
btnAddToQueueTimeLimit = 2      # button presses within 2s of each other

# logging
log.config.fileConfig('log.conf')

# init
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
lastPressed = time.time()
q = Queue.Queue();
playing = None

log.info('INITIALIZATION')
log.info('VIDEO_DIR=%s', VIDEO_DIR)
log.info('BUTTON_PIN=%s', BUTTON_PIN)

def play(item):
    global playing
    log.info('consumer->playing %s. qsize=%s', item, q.qsize())
    if playing:
        stop()
    playing = item
    os.system("omxplayer -b -o hdmi "+"'"+VIDEO_DIR+item+"' > /dev/null 2>&1")
    playing = None
    log.info('consumer->finished %s. qsize=%s', item, q.qsize())

def stop(item):
    log.info('stopping current %s. qsize=%s', item, q.qsize())
    os.system('killall omxplayer.bin > /dev/null 2>&1')
    
def consumer():
    global playing
    while True:
        q.get() # this will wait until there is a token in the queue
        play( random.choice(os.listdir(VIDEO_DIR)) )

def keyPress():
    while True:
	try:
            x = raw_input("")
            fired("")
        except Exception as err:
            log.error('raw_input error', exc_info=True)
            raise err

def fired(channel):
    global lastPressed
    timeSinceLast = (time.time()-lastPressed)

    if timeSinceLast < btnDblBounceLimit:
        log.debug('double bounce caught, ignoring. qsize=%s', q.qsize())
        return 
    elif timeSinceLast > btnAddToQueueTimeLimit:
        if q.qsize() > 0:
            log.info('clearing queue and starting over. qsize=%s', q.qsize())
            with q.mutex:
                q.queue.clear()
        if playing:
            stop(playing)

    lastPressed = time.time()
    log.info('adding item to queue. qsize=%s', (1+q.qsize()))
    q.put(lastPressed)


def main():
    try:
        # Set the interrupt - call gpio switch function on button press - set debounce
        GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback = fired, bouncetime = 200)

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
        log.error("stopping", exc_info=True)
    except Exception:
        log.error('exception', exc_info=True)

if __name__ == '__main__':
    main()
