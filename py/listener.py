import time
import sys
import asyncio
import os
import handler



def return_message(msg,timestamp='tstamp'):
    print(str(timestamp)+msg)
    sys.stdout.flush()


def listener():
    while 1:
        for msg in sys.stdin:
            return_message(handler.interpret(msg.strip()))
            #return_message('return: '+msg.strip())
        time.sleep(1)

# return Image object
def request(filename):
    return imagelist[filename]

handler.initialize()
listener()
