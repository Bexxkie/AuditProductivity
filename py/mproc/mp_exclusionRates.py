# # # # # # # # # # # #
# Title: Sensible reward reimbursment calculator
# Author: BrianKG |  7-7-21
# website: https://github.com/BrianKG/AuditProductivity
#
#
# for more helpful tools, or to report bugs visit my github (link above)
#
#
# Version 1.0 d.7-7-21
# ------------------------
# + initial build
# +
#
# Version 1.2 d.7-20-21
# ------------------------
# + fixed room count errors
# + added total rooms to config
# + automatically detect if standalone or dependent
# +
#
# # # # # # # # # # # #
import sys
import os
import configparser
import ctypes
import time
import asyncio
import tkinter as tk

import pyautogui as pg
from tkinter import filedialog
import pygetwindow as gw

import shared
import interactor
#
# return vs displayDialog [0,1]
# is this being run by itself? set to 0 to call from another script
config = configparser.ConfigParser()
config.read('erates.ini')
# [adr]
# [occ]
# split by \n
# deduct [occ] from room count when calc
# deduct [adr+occ] from rev when calc
#
# we need the following info:
# Read the OccForecast into a map
# search the exclusion rates (config) and get total ct and rev from them
# last line, index 1 = total room revenue
#
fileMap = {}
#rateCode [roomCount(0), revenue(1), excludeFromOccupancyBOOL(2)]
exclusionMap = {}
penMap = {  '1' : [.30,.50,.80],
            '2' : [.35,.55,.90],
            '3' : [.40,.75,.95]
            }
args = {}
# return list of all lines excluded, called at init
def setExclusionList():
    for index in fileMap:
        for rate in config['ADR']['rtc'].split('\n'):
            if rate in fileMap[index]:
                rateCode = fileMap[index].split('\t')[2]
                roomCnt = fileMap[index].split('\t')[6]
                roomRev = fileMap[index].split('\t')[8]
                roomOcc = 1
                if rateCode in config['OCC']['rtc']:
                    roomOcc = 0
                exclusionMap[rateCode] = [roomCnt,roomRev,roomOcc]

#
def getRevenueDeduction():
    deductRev = 0
    for index in exclusionMap:
        deductRev+=int(exclusionMap[index][1])        #totalRev for RTC
    return deductRev

#
def getPenetrationLevel():
    level = config['GEN']['penetration-level']
    return(level)

def getTotalRooms():
    roomCount = config['GEN']['total-rooms']
    return(roomCount)
#
def getOccupancyDeduction():
    deductOcc = 0
    for index in exclusionMap:
        if exclusionMap[index][2]:                   # RoomOccDeductionBool
            deductOcc+=int(exclusionMap[index][0])   # RoomOccCount
    return deductOcc
#
def getTotalRev():
    return(fileMap[len(fileMap)-1].split('\t')[1])
#
def calcIrate():
    rev = getTotalRev()
    occ = fileMap[len(fileMap)-1].split('\t')[0]
    occD = getOccupancyDeduction()
    revD = getRevenueDeduction()
    tRoom = getTotalRooms()

    adjustedOcc = int(occ)-int(occD)
    adjustedRev = float(rev)-float(revD)
    percentage = (adjustedOcc/int(tRoom))*100
    level = getPenetrationLevel()
    split = penMap[level][0]
    if percentage >96:
        split = penMap[level][2]
    elif percentage >=90:
        split = penMap[level][1]
    rate = (adjustedRev/adjustedOcc)*split
    if rate <25.00:
        rate = 25.00
    # subtract excluded rooms from adjustedOcc
    return('IVANI RATE: $'+str(round(rate,2)))
    # <90 35
    # <96 55
    # >96 90

#
def init(file):
    # gonna be the res forcast file, have it save as a specified filename at a specific location)
    for i, line in enumerate(open(file,'r')):
        if i == 0 and not 'RESERVATION_DATE' in line:
            return 0
        fileMap[i]=line
    return 1

#
async def getFile():
    await generateReport()
    return(filedialog.askopenfilename(filetypes = [('text document','.txt')], title = 'Select report'))

#
async def generateReport():
    if await window_exists():
        await ensure_root()
        await click_object(await find_object('misc'))
        await click_object(await find_object('reports_window'))
        await click_object(await find_object('reports'))
        pg.typewrite('res_forecast1')
        await click_object(await find_object('btn_search'))
        await click_object(await find_object('res_forecast1'))
        await click_object(await find_object('print_to_file'))
        await click_object(await find_object('dropdown'))
        await click_object(await find_object('deliminated_data'))
        await click_object(await find_object('btn_ok'))
        pg.hotkey('ctrl','c')
        pg.press('TAB')
        pg.hotkey('ctrl','v')
        await click_object(await find_object('rate_code'))
        await click_object(await find_object('block'))
        await click_object(await find_object('block_def'))
        pg.typewrite('DEF')
        await click_object(await find_object('file'))
        while not await find_object('save'):
            await asyncio.sleep(.2)
        await click_object(await find_object('save'))
        return 1

#
async def window_exists():
    try:
        window = gw.getWindowsWithTitle('OPERA PMS')[0]
    except IndexError:
        return None
    #if !window.isActive:
    #    pg.application.Application().connect(handle=window._hWnd).top_window().set_focus()
    window.restore()
    return window

#
async def find_object(image_string):
    """RETRIEVE RECT, STRING"""
    # print(image_string)
    try:
        rect = pg.locateOnScreen(args[image_string], grayscale=1)
        return rect
    except OSError as _err:
        shared.build_message_info(_err,1,1)

#
async def click_object(rect, dbl=0):
    """SEND CLICK EVENT, RECT, BOOL"""
    if rect is None:
        return 0
    if dbl:
        pg.doubleClick(rect)
    else:
        pg.click(rect)
    time.sleep(shared.get("delay"))
    return 1

#
async def ensure_root():
    while await find_object('ico_root_t') is None:
        for obj in ['btn_close', 'btn_exit']:
            rect = await find_object(obj)
            if rect is not None:
                 await click_object(rect)

#
def getConfig():
    return(filedialog.askopenfilename(filetypes = [('config file','.ini')], title = 'Select config'))

#
def start(arg):
    main(arg)
    tk.Tk().withdraw()
    #conFile = None
    #conFile = getConfig()
    file = asyncio.run(getFile())
    if file == '':
        return('no file selected')
    if not init(file):
        return('Invalid file')
    setExclusionList()
    rVal = calcIrate()
    tk.messagebox.showinfo("info", rVal)
    sys.exit(rVal)
#
def main(arg):
    #handle return messages
    args['misc'] = arg[0]
    args['reports_window'] = arg[1]
    args['reports'] = arg[2]
    args['res_forecast1'] = arg[3]
    args['btn_search'] = arg[4]
    args['print_to_file'] = arg[5]
    args['dropdown'] = arg[6]
    args['deliminated_data'] = arg[7]
    args['btn_ok'] = arg[8]
    args['rate_code'] = arg[9]
    args['block'] = arg[10]
    args['block_def'] = arg[11]
    args['file'] = arg[12]
    args['save'] = arg[13]
    args['ico_root_t'] = arg[14]
    args['btn_close'] = arg[15]
    args['btn_exit'] = arg[16]
    #config.read('erates.ini')
    #returnValue = asyncio.run(start())
    #sys.exit(returnValue)
    #tk.messagebox.showinfo("info",returnValue)
#
