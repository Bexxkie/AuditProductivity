#
# btn-autolog
# btn-departures
# btn-folios
# btn-audit
import threading
import os
import ctypes
import asyncio
import sys
import time
import keyboard
import pyautogui as pg
from PIL import Image


user32 = ctypes.windll.user32
idir = os.getcwd()+'\\res\\image_refs\\'

args = \
{
    'autoLog':0,
    'threadStop':0,
    "loginThread": threading.Thread(name="autologin_thread"),
    'keyThread': threading.Thread(name="keyListener_thread"),
    'delay':2,
    'debug':0,
    'pass':'',
}
image_list = \
{
    ## root
    "reports_window": idir + "reports_window.png",
    "ico_root": idir + "root_test.png",
    "ico_root_t": idir + "root.png",
    "departures": idir + "departure_all.png",
    "cashier_login_window": idir + "cashier_login_window.png",
    "field_reports": idir + "report_bar.png",
    "finpayments": idir + "finpayments.png",
    "finjrnlbytrans": idir + "finjrnlbytrans.png",
    "first_open": idir + "first_open.png",
    ## banner
    "misc": idir + "banner\\misc_banner.png",
    "reports": idir + "banner\\reports_banner.png",
    "menu_misc": idir + "banner\\misc_menu.png",
    "cashier": idir + "banner\\cashiering_banner.png",
    "func": idir + "banner\\shift_functions.png",
    "batch": idir + "banner\\batch_folios_banner.png",
    ## common
    "btn_search": idir + "common\\search.png",
    "btn_yes": idir + "common\\yes.png",
    "btn_print": idir + "common\\print.png",
    "btn_close": idir + "common\\close.png",
    "btn_exit": idir + "common\\exit.png",
    "btn_login": idir + "common\\login.png",
    "btn_next": idir + "common\\next.png",
    "login": idir + "common\\password_box.png",
    "login_a": idir + "common\\password_box_a.png",
    ## folio
    "a_bill": idir + "folio\\advance_bill.png",
    "a_guest": idir + "folio\\all_guest.png",
    "a_windows": idir + "folio\\all_windows.png",
    "c_cards": idir + "folio\\credit_card.png",
    "depart": idir + "folio\\depart_tomorrow.png",
    "r_order": idir + "folio\\room_order.png",
    "sim": idir + "folio\\simulate.png",
}

# seperates communication type, command name, and password
# @'comtype'>'comname'*'password'
def interpret(message):
    messge = message.split('*')     #[@comtype>>comname, password]
    contrl = messge[0].split('>>')   #[@comtype, comname]
    comtpe = contrl[0]              # @comtype
    contrl = contrl[1]              # comname(?%value)
    passwd = messge[1]              # password
    if(passwd != args['pass']):
        args['pass'] = passwd
    # get commandType
    if comtpe == '@com':
        # command, button click to do something
        return execute(contrl)
    if comtpe == '@set':
        # set variable
        args[contrl.split('%')[0]] = int(contrl.split('%')[1])
        if args['debug']:
            return '   @inf<<'+contrl+' : '+str(args[contrl.split('%')[0]])
        return '@inf<<'
    return '@inf<<no command'


# get new value from JS
def request_var(argname):
    print('@req<<'+argname+'\n')

# execute commands linked to a control
def execute(control):
    if control == 'btn-autolog':
        # since autolog is a toggle, i need to ensure the togglestate is accurate.
        # so on the return it should be like 'yo this is off, or this is on'
        if args['autoLog']:
            args["loginThread"] = threading.Thread(target=auto_log, daemon=1)
            args["loginThread"].start()
            args['keyListener'] = threading.Thread(target=keyListener,daemon=1)
            args['keyListener'].start()


    return '@tim<<'+control

#KeyboardInterrupt
def keyListener():
    while args['keyListener'].is_alive() and args['loginThread'].is_alive():
        if keyboard.is_pressed("escape"):
            args["threadStop"] = 1
    print('@psh<<btn-autolog%'+str(args['autoLog']))
    print('closing thread')
    sys.stdout.flush()
    sys.exit("stopping thread")

# setup loading stuff
def initialize():
    ind = 0
    maxSize = len(image_list)
    for image in image_list.keys():
        image_list[image] = Image.open(image_list[image])
        ind+=1

def auto_log():
    """DISPATCH LOGIN THREAD"""
    asyncio.run(alog_helper())
    sys.exit()
#
# Login functions
#
#
async def alog_helper():
    """LOGIN THREAD"""
    while args["autoLog"]:
        if user32.GetForegroundWindow() != 0:
            sys.stdout.flush()
            if await find_login():
                await type_object(args["pass"])
                await click_object(await find_object("btn_login"))
        else:
            time.sleep(args['delay'])
    return


async def find_login():
    """FIND LOGIN_BOX, CLICKS AND RETURNS BOOL"""
    if await find_object("login"):
        await click_object(await find_object("login"))
        return 1
    if await find_object("login_a"):
        await click_object(await find_object("login_a"))
        return 1
    return 0


#
# Thread helpers
#
#
async def heartbeat(force_stop=0):
    """ENSURE THREAD SHOULD BE RUNNING,
    PRESSING ESCAPE SIGNALS A SHUTDOWN
    force_stop TRUE forcibly kills thread
    """
    if args["threadStop"] or force_stop:
        if args["autoLog"]==1:
            args["autoLog"] = 0
        args["threadStop"] = 0
        sys.exit('closing thread')

#
# General functions
#
#
async def find_object(image_string):
    """RETRIEVE RECT, STRING"""
    # print(image_string)
    if not await(heartbeat()):
        try:
            rect = pg.locateOnScreen(image_list[image_string], grayscale=1)
            # print(rect)
            return rect
        except OSError as _err:
            print('   @inf<<'+_err)
            await heartbeat(1)

async def click_object(rect, dbl=0):
    """SEND CLICK EVENT, RECT, BOOL"""
    if rect is None:
        return 0
    if dbl:
        pg.doubleClick(rect)
    else:
        pg.click(rect)
    await asyncio.sleep(args["delay"])
    return 1

async def type_object(string, press=0, count=1):
    """SEND TYPE EVENT, STRING, BOOL, INT"""
    if press:
        pg.press(string, presses=count)
    else:
        pg.typewrite(string)
    return 1
