#
#
#
#
import sys
import os
import configparser

__FILENAME__ = 'f.txt'
__TOTALROOMS__ = 80
exclusionRates = configparser.ConfigParser()
exclusionRates.read('erates.ini')
# [adr]
# [occ]
# split by \n
# deduct [occ] from room count when calc
# deduct [adr+occ] from rev when calc
#
# we need the following info:
# Read the OccForecast into a map
# search the exclusionRates and get total ct and rev from them
# last line, index 1 = total room revenue
#
fileMap = {}
#rateCode [roomCount(0), revenue(1), excludeFromOccupancyBOOL(2)]
exclusionMap = {}

# return list of all lines excluded, called at init
def setExclusionList():
    for index in fileMap:
        for rate in exclusionRates['ADR']['rtc'].split('\n'):
            if rate in fileMap[index]:
                rateCode = fileMap[index].split('\t')[2]
                roomCnt = fileMap[index].split('\t')[6]
                roomRev = fileMap[index].split('\t')[8]
                roomOcc = 0
                if rateCode in exclusionRates['OCC']['rtc']:
                    roomOcc = 1
                exclusionMap[rateCode] = [roomCnt,roomRev,roomOcc]
#
def getRevenueDeduction():
    deductRev = 0
    for index in exclusionMap:
        deductRev+=int(exclusionMap[index][1])        #totalRev for RTC
    return deductRev

#
def getOccupancyDeduction():
    deductOcc = 0
    for index in exclusionMap:
        if exclusionMap[index][2]:              # RoomOccDeductionBool
            deductOcc+=int(exclusionMap[index][0])   # RoomOccCount
    return deductOcc

def getTotalRev():
    return(fileMap[len(fileMap)-1].split('\t')[1])

def calcIrate():
    rev = getTotalRev()
    occ = fileMap[len(fileMap)-1].split('\t')[0]
    occD = getOccupancyDeduction()
    revD = getRevenueDeduction()

    adjustedOcc = int(occ)-int(occD)
    adjustedRev = float(rev)-float(revD)
    percentage = (adjustedOcc/__TOTALROOMS__)*100
    split = 0.35
    if percentage >=96:
        split = 0.90
    elif percentage >=90:
        split = 0.55
    rate = (adjustedRev/adjustedOcc)*split
    if rate <25.00:
        rate = 25.00
    return('IVANI RATE: $'+str(round(rate,2)))
    # <90 35
    # <96 55
    # >96 90
def init():
    # gonna be the res forcast file, have it save as a specified filename at a specific location)
    for i, line in enumerate(open(__FILENAME__,'r')):
        fileMap[i]=line
def main():
    init()
    setExclusionList()
    return(calcIrate())
