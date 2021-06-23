import time
import sys
import asyncio
import os
import keyboard
import threading

import handler


def return_message(msg):
    sys.stdout.write(msg+'\n')
    sys.stdout.flush()


def comListener():
    return_message('@tim<<Ready')
    for msg in sys.stdin:
        if handler.args['debug']:
            con = msg.split('*')
            con[1] = '*'*len(con[1])
            return_message("   "+str(con[0]+con[1]))
        rm = handler.interpret(msg.strip())
        return_message(rm)
        #time.sleep(1)

# return Image object
def request(filename):
    return imagelist[filename]


handler.initialize()
comListener()
