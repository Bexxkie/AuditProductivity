# # # # # # # # # # # #
# Title: Sensible reward reimbursment calculator
# Author: BrianKG |  7-7-21
# website: https://github.com/BrianKG
#
# for more helpful tools visit my github (link above)
#
#
# # # # # # # # # # # #
import sys
import os
import configparser
import tkinter as tk
from tkinter import filedialog

#
# return vs displayDialog [0,1]
# is this being run by itself? set to 0 to call from another script
standalone = 0

__TOTALROOMS__ = 80
config = configparser.ConfigParser()
if not standalone:
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
# return list of all lines excluded, called at init
def setExclusionList(conFile=None):
    if standalone:
        config.read(conFile)
    for index in fileMap:
        for rate in config['ADR']['rtc'].split('\n'):
            if rate in fileMap[index]:
                rateCode = fileMap[index].split('\t')[2]
                roomCnt = fileMap[index].split('\t')[6]
                roomRev = fileMap[index].split('\t')[8]
                roomOcc = 0
                if rateCode in config['OCC']['rtc']:
                    roomOcc = 1
                exclusionMap[rateCode] = [roomCnt,roomRev,roomOcc]

#
def getRevenueDeduction():
    deductRev = 0
    for index in exclusionMap:
        deductRev+=int(exclusionMap[index][1])        #totalRev for RTC
    return deductRev

#
def getPenetrationLevel(conFile = None):
    if standalone:
        config.read(conFile)
    level = config['GEN']['penetration-level']
    return(level)

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
def calcIrate(conFile = None):
    if standalone:
        config.read(conFile)
    rev = getTotalRev()
    occ = fileMap[len(fileMap)-1].split('\t')[0]
    occD = getOccupancyDeduction()
    revD = getRevenueDeduction()

    adjustedOcc = int(occ)-int(occD)
    adjustedRev = float(rev)-float(revD)
    percentage = (adjustedOcc/__TOTALROOMS__)*100
    level = getPenetrationLevel(config)
    split = penMap[level][0]
    if percentage >96:
        split = penMap[level][2]
    elif percentage >=90:
        split = penMap[level][1]
    rate = (adjustedRev/adjustedOcc)*split
    if rate <25.00:
        rate = 25.00
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
def getFile():
    return(filedialog.askopenfilename(filetypes = [('text document','.txt')], title = 'Select report'))

def getConfig():
    return(filedialog.askopenfilename(filetypes = [('config file','.ini')], title = 'Select config'))

#
def start():
    tk.Tk().withdraw()
    conFile = None
    if standalone:
        conFile = getConfig()
    file = getFile()
    if file == '':
        return('no file selected')
    if not init(file):
        return('Invalid file')
    setExclusionList(conFile)
    return(calcIrate(conFile))
def main():
    #handle return messages
    returnValue = start();
    if not standalone:
        return returnValue
    tk.messagebox.showinfo("info",returnValue)


if standalone:
    main()
