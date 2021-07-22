###
#       ____        _      __      ___             ___ __ 
#      / __ \__  __(_)____/ /__   /   | __  ______/ (_) /_
#     / / / / / / / / ___/ //_/  / /| |/ / / / __  / / __/
#    / /_/ / /_/ / / /__/ ,<    / ___ / /_/ / /_/ / / /_  
#    \___\_\__,_/_/\___/_/|_|  /_/  |_\__,_/\__,_/_/\__/  
##

__AUTHOR__ =  'BrianG'
__VERSION__ = '1.3'
__DEPENDS__ = 'AHK> test.ahk | pynput'

#   intent: Increase productivity during night audit by semi-automating some tasks
################
##
## IMPORTS ##
import asyncio
import os
import sys
import subprocess
import ctypes
import datetime
from os import system
from datetime import date
from pynput.keyboard import Key, Controller

##
## VARIABLES ##
kbd = Controller()
slp = 5
#pth = 'C://Users//Jeddy.ALMHR//Documents//Audit_productivity//AHK//'
pth = os.getcwd().replace('Python', 'AHK\\')


#Temp var, this will later change to a dict when more stuff is found.
str_nte = 'Known prepaid sources: Hotels.com, Expedia.com, Hotels.com, RateCodes: IDAVC'
str_wrn = 'Before running commands. Is Opera running? Are there NO windows open within Opera? If both answers are yes, then you are all set.'
wrn_len = len(str_wrn)

##
## Dictionaries ##
com_lst = {
'rpt_sht':['csh_adt','rat_chk','cdt_lmt','cdt_rcn','dwn_r04'],
'rpt_lng':['csh_adt','rat_chk','cdt_lmt','cdt_rcn','dwn_r13'],
'csh_adt':[Key.f20, '1'],
'rat_chk':[Key.f20, '2'],
'cdt_lmt':[Key.f20, '3'],
'cdt_rcn':[Key.f20, '4'],
'dwn_r04':[Key.f20, '5'],
'dwn_r13':[Key.f20, '6'],
'com_int':[Key.f20, '0'],
'com_ext':[Key.f20, 'x'],
'dep_lst':[Key.f20, '7'],
'bat_fol':[Key.f20, '8'],
'ihg_rep':[Key.f20, '9'],
'com_opg':[Key.f20, Key.f19],
'com_qck':[Key.f19, '1'],
'com_gih':[Key.f19, '2']
}

com_gid = {
'rpt_sht':'all, short downtime',
'rpt_lng':'all, first shift, long downtime',
'csh_adt':'cashier audit',
'rat_chk':'rate check',
'cdt_lmt':'credit limit all payment types',
'cdt_rcn':'credit card reconciliation',
'dwn_r04':'downtime (4)',
'dwn_r13':'downtime (13)',
'com_int':'!login',
'com_ext':'!quit',
'com_als':'!command aliases',
'com_hlp':'!command list',
'dep_lst':'!print departures list',
'bat_fol':'!load batch folios',
'ihg_rep':'!load IHG reports page',
'com_nte':'!show notes',
'com_opg':'!print occupancy graph',
'com_qck':'!open quick checkout',
'com_gih':'Guests in-house by room'
}


com_als = {
'rpt_sht':['reps','rps'],
'rpt_lng':['repl','rpl'],
'com_ext':['quit','exit','stop'],
'com_int':['login','init'],
'com_als':['alias','als','.'],
'com_hlp':['?','help','/'],
'com_int':['init','login'],
'com_nte':['note','nte'],
'com_gih':['house','guest']
}

com_history = {}

##
## Begin functions ##

# FUNCTION history
# VARIABLE bool as boolean, command as string
# RETURN none
# INFO log commands used during session
async def history(bool,command):
    x = len(com_history)
    if bool == False:
        #return history
        for a in com_history:
            print(str(a)+' : '+com_history[str(a)])
    else:
        #add history
        com_history[str(x)]= str(datetime.datetime.now().time().hour)+':'+str(datetime.datetime.now().time().minute) +' '+ command
 

 
# FUNCTION reset
# VARIABLE none
# RETURN none
# INFO sends reset code (just spams alt+c)
async def reset():
    kbd.press(Key.f19)
    kbd.press('0')
    kbd.release(Key.f19)
    kbd.release('0')
    await asyncio.sleep(2)
    return
    
    
    
# FUNCTION snd_keys
# VARIABLE key_cmb as arraylist
# RETURN none
# INFO sends keyboard inputs, usually F20 & number
async def snd_kys(key_cmb,command):
    await history(True,command)
    await set_ttl(await unpack(command))
    if command != "com_ext" and command != "com_int":
        print('sending reset code...')
        await reset()
    print('sending '+command)
    kbd.press(key_cmb[0])
    kbd.press(key_cmb[1])
    kbd.release(key_cmb[0])
    kbd.release(key_cmb[1])
    if command !="com_ext" and command!= "com_int":
        print('<<'+command+'>> sleeping for '+str(slp)+' seconds')
        await asyncio.sleep(slp)
    system('cls')
    await help()
    return
    
    
    
# FUNCTION set_ttl
# VARIABLE string as string
# RETURN none
# INFO Sets the terminal title
async def set_ttl(string):
    title = 'QuickAudit       -a['+__AUTHOR__+']       -v['+__VERSION__+']       -date['+str(date.today())+']       -task: '+string.replace('*','').strip()
    ctypes.windll.kernel32.SetConsoleTitleW(title)
    return
    
    
    
# FUNCTION decode
# VARIABLE cmd as String
# RETURN none
# INFO raw text data from input sent here, checks if input corresponds to a command
# relays the command information to the apropriate functions
async def decode(cmd):
    if cmd == '':                    # no command entered
        system('cls')                # clear the screen [does not work as a subprocess]
        await help()                 # call the help function   
        return                       # exit this function, return to main()
    # Check for command alias
    for x in com_als:                # check if an alias was sent
        for a in com_als[x]:    
            if cmd in a:    
                cmd = x          
                system('cls')        # clear the screen [does not work as a subprocess]
                break;
    # run commands
    if cmd == 'com_nte':
        print(str_nte)
        return
    if cmd == 'com_hlp':
        #system('cls')
        await help()                 # call the help function
        return                       # exit this function, return to main()
    if cmd == 'com_als':
       # system('cls')
        await alias()                # call the alias function
        return                       # exit this function, return to main()
    if cmd == 'rpt_sht' or cmd == 'rpt_lng':                
        for com in com_lst[cmd]:
            key_cmb = com_lst[com]  
            await snd_kys(key_cmb,cmd)   # call the snd_kys function with the appropriate key combos
            system('cls')            # clear the screen [does not work as a subprocess]
        return                       # exit this function, return to main()
    if cmd in com_lst:
        key_cmb = com_lst[cmd]
        await snd_kys(key_cmb,cmd)       # call the snd_keys function with the appropriate key combo
        if cmd == 'com_ext':         # command to close the script, a key combo is sent to exit the ahk script, then this script will end.
            sys.exit()
            quit()
    return



# FUNCTION alias
# VARIABLE none
# return none
# INFO prints command aliases to screen
async def alias():
    await warning()
    print('*'*33)
    for o in com_als:
        s = com_als[o]
        st = '* '+o+' : '+(str(s).replace("'",'').replace('[','').replace(']','').replace(',',' |'))
        le = len(st)
        ct = 32-le
        st = st+' '*ct+'*'
        print(st)       # print alias in format of ['command' : ['alias0', 'alias1']
    print('*'*33)
    return


    
# FUNCTION unpack
# VARIABLE o as String 
# RETURN String
# INFO Unpacks command data into a readable format 64line len
async def unpack(o):
    s = com_gid[o]
    if not s.startswith('!'):
        st = '* '+o+' : Print '+s+' report'
        le = len(st)
        ct = 64-le
        st = st+' '*ct+'*'
        return(st)
    else:
        st = '* '+o+' : '+s.replace('!','')
        le = len(st)
        ct = 64-le
        st = st+' '*ct+'*'
        return(st)



# FUNCTION help
# VARIABLE none
# RETURN none
# INFO prints all available commands to screen
async def help():
    await warning()
    print('*'*65)
    for o in com_gid:
        s = await unpack(o)
        print(s)
    print('*'*65)
    return



# FUNCTION warning
# VARIABLE none
# RETURN none
# INFO prints a usage warning
async def warning():
    print('*'*wrn_len)
    print(str_wrn)
    print('*'*wrn_len)
    


# FUNCTION main
# VARIABLE none
# RETURN none
# INFO keep alive, gets input and relays to decoder
async def main():
    system('cls')
    await help()
    while True:
        await history(False, '')
        await set_ttl('waiting')
        cmd = input('>> ')
        await decode(cmd.lower())
##
## INIT ##
subprocess.Popen("%s %s" % (pth+'AutoHotkeyU64.exe', pth+'test.ahk')) # LOAD AHK script to run hotkeys, (for interacting with OPERA)
asyncio.run(main())                                                     # LOAD into main function, entering the keep alive loop
##
