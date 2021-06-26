import threading
import keyboard
import time

import shared
import autoLog
import listener

alog = threading.Thread(target=autoLog.alog)
lstn = threading.Thread(target=listener.main)


alog.start()
lstn.start()
time.sleep(1)
shared.build_message_info("Ready",1,1)

while 1:
    if keyboard.is_pressed('escape'):
        if shared.get('autoLog'):
            shared.set('threadStop',1)
            shared.set('autoLog',0)
            shared.build_message_command('tog-alo',0,1,0)
            time.sleep(.5)
            shared.set('threadStop',1)
