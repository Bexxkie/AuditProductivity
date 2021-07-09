#
# btn-autolog
# btn-departures
# btn-folios
# btn-audit
import os
import sys
import time
import multiprocessing as mp
from PIL import Image

import shared
import departures
import exclusionRates

import mproc.mp_alog as alo
# we need to read the message and determine what JS wants
# theres just a few things were gonna needs
# we just need to listen for it asking us to start the autologin loop
# we need it to also run the commands for doing the normal
#
# This is stuff JS is asking/telling us
# split by %
# @commd%command name
# @ctrl%set/get(bool)%controlName(%?value to set()

def interpret(input):
    pwd = input.split('*')
    shared.set('pass',pwd[1])
    msg = pwd[0].split('%')
    if msg[0]=='@comd':                                 # this should be used to start a command
        globals()[msg[1]]()                             # this starts the function by string
    if msg[0]=='@ctrl':                                 # this is used to get/set a value
        if bool(int(msg[1])):                           # convert to int, to get bool, if 1:
            shared.set(msg[2],int(msg[3]))              # replace the args value

def kill():
    # check all threads before closing
    for threadName in ['alog_thread','departures_thread']:
        if shared.get(threadName) is not None:
            shared.get(threadName).terminate()
            shared.get(threadName).join()
            shared.set(threadName, None)
            if threadName == 'alog_thread':
                shared.build_message_command('tog-alo',0,1,0)
    shared.return_message('@kill%')
    sys.exit()

def set_auto_log():
    # repurpose to handle multiprocessing
    # create/start proc here
    if shared.get('alog_thread') is None:
        proc = mp.Process(target=alo.start, args = [shared.get_alog_ass()],name='autologProc')
        shared.set('alog_thread', proc)
        proc.start()
        #shared.build_message_info(str(proc),0,1)
        return
    else:
        shared.get('alog_thread').terminate()
        shared.get('alog_thread').join()
        shared.set('alog_thread', None)
        #shared.build_message_info(str(shared.get('alog_thread')),0,1)
        return

    #shared.set('autoLog',shared.get('autoLog'))

def getIrate():
    shared.build_message_info(str(exclusionRates.main()),1,1)

def print_departures_list():
    # ok so the new system should have a system that ensures its on the--
    # --right step, if not move up a step until it finds what its meant to be on.
    # so ill probably have an array of steps that it should refer to.
    # like ['reports_window', 'reports', 'btn_search']
    # say it gets to 'btn_search' but it isnt visible, move up and see if--
    # --'reports' is visible, if so, open it.. its not? ok lets see if we have the 'reports_window' open
    # nope? ok open it then, otherwise try looking for reports again
    # I think i will put this in a seperate file and import 'interactor' to it.
    if shared.get('departures_thread') is None:
        proc = mp.Process(target = departures.start,args = [shared.get_dep_ass()],name='departProc')
        shared.set('departures_thread', proc)
        proc.start()
        return
    else:
        shared.get('departures_thread').terminate()
        shared.get('departures_thread').join()
        shared.set('departures_thread', None)
        return


def initialize():
    ind = 0
    maxSize = len(shared.image_list)
    for image in shared.image_list.keys():
        shared.image_list[image] = Image.open(shared.image_list[image])
        ind+=1
    shared.build_message_info('files loaded..',1,1)
