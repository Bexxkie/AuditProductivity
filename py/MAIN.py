import threading
import keyboard
import time

import shared
import autoLog
import listener

alog = threading.Thread(target=autoLog.alog)
lstn = threading.Thread(target=listener.main)
#cmnd = threading.Thread(target=)


alog.start()
lstn.start()
#cmnd.start()

while 1:
    if keyboard.is_pressed('escape'):
        if shared.get('autoLog'):
            shared.set('threadStop',1)
            shared.set('autoLog',0)
            shared.build_message_command('tog-alo',0,1,0)
            time.sleep(.5)


# i think im going to use multoprocessing for handling the commands
# I cant interrupt a thread whenever i want so look mproc is what i gotta do
# gonna have to setup ipc for step breakdowns
#
# start with the basics we need to open reporting window
#   first step of all commands will be ensuring focus and root
#   window.activate() doesnt work for some reason so i need a new way
#   but ill get to that later, i wanna get the basic handling down
#  >so we'll start by ensuring root
#   - search for ico_root
#       - if we cant find it, look for a close or exit button
#  >next we need to open the reporting window
#   - look in the banner for 'misc' and open it
#       - find reporting in the misc dropdown
#  >so now we can branch off and do whatever reports we need
#   - need to pass a report name when starting the process
#   - type the report name, look for the search button (or press enter)
#       - find the report we need and open it
#  some reports need different parameters so we need to account for that
#   - the departure list needs the next business day.
#   - pressing tab twice will update other fields so we just need to do that
#   - afterwards we can print the report if we want
#        - alt+p or just click the print button
#
#
#
#
