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
#import exclusionRates

import mproc.mp_alog as alo
import mproc.departures as dep
import mproc.mp_exclusionRates as er
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
    if shared.get('eRate_thread') is None:
        proc = mp.Process(target = er.start, args = [shared.get_er_ass()],name='erateProc')
        shared.set('eRate_thread', proc)
        proc.start()
        return
    else:
        shared.get('eRate_thread').terminate()
        shared.get('eRate_thread').join()
        shared.set('eRate_thread', None)
        return
    #shared.build_message_info(str(exclusionRates.main()),1,1)

def print_departures_list():
    if shared.get('departures_thread') is None:
        proc = mp.Process(target = dep.start, args = [shared.get_dep_ass()],name='departProc')
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
