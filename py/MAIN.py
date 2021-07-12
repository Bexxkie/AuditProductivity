import threading
import keyboard
import time

import shared
import listener
#cmnd.start()

def main():
    lstn = threading.Thread(target=listener.main)
    lstn.start()
    while 1:
        if keyboard.is_pressed('escape'):
            for threadName in ['alog_thread','departures_thread']:
                if shared.get(threadName) is not None:
                    shared.get(threadName).terminate()
                    shared.get(threadName).join()
                    shared.set(threadName, None)
                    if threadName == 'alog_thread':
                        shared.build_message_command('tog-alo',0,1,0)
                    time.sleep(.5)

# this is needed otherwise we get an infinite loop when spawning a child process
if __name__=='__main__':
    # uncomment if compiling to executable
    #multiprocessing.freeze_support()
    main()

# So mpc is pretty much done, i just need a better way to package everything
# i also need to finish making all the commands and work on increasing speed
# if i could compile things it would load and run faster, but running from...
# ...script is like 30-50% slower according to my previous tests in verion 4
# if i can increase the speed at which 'locateOnScreen' runs then that would...
# ...help greatly, maybe adjust resolutions of everything by 25% and check...
# ...for accuracy. get the lowest resolution to search for while maintaining...
# ...high reliability. 0 tolerance, must not have any false positives.
#
#
# After compiling with pyinstaller i cant seem to get spawned processes to end
# Since they need to be able to close at any point in time at random i cant...
# ...really open a pipe cause that could cause me to run into invalid memory
# and i really don't want that
