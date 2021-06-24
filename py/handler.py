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
import autoLog

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
    if msg[0]=='@comd':                         # this should be used to start a command
        globals()[msg[1]]()                     # this starts the function
    if msg[0]=='@ctrl':                         # this is used to get/set a value
        if bool(int(msg[1])):                   # convert to int, to get bool, if 1:
            shared.set(msg[2],int(msg[3])) # replace the args value
        shared.return_message(returnVariable(msg[2]))           # get args value

def returnVariable(argName):
    return('@info%1%'+argName+" "+str(shared.get(argName)))

def set_auto_log():
    shared.set('autoLog',shared.get('autoLog'))
    #autoLog.alog()

def initialize():
    ind = 0
    maxSize = len(shared.image_list)
    for image in shared.image_list.keys():
        shared.image_list[image] = Image.open(shared.image_list[image])
        ind+=1
    shared.return_message('@info%1%files loaded')
initialize()
