import ctypes
import time
import pyautogui as pg
import asyncio
#
# We need to listen and wait for the loginbox to show
# The only objects i need here are, login, login_a, pass, btn_login
#

# think i need to pass this in from the start
args = {}
user32 = ctypes.windll.user32

def start(arg):
    args['btn_login'] = arg[0]
    args['login'] = arg[1]
    args['login_a'] = arg[2]
    args['password'] = arg[3]
    asyncio.run(alog())

async def alog():
    while 1:
        if user32.GetForegroundWindow()==0: # is the screen locked?
            await asyncio.sleep(2)
        else:
            rect = await find_login()
            if rect is not None:
                await click_object(rect)
                pg.typewrite(args['password'])
                #await click_object(find_login(1))
            await asyncio.sleep(1)
                #await click_object(await find_login(1))
        await asyncio.sleep(1)
# return object
async def find_login(object=0):
    try:
        if bool(object):
            rect = pg.locateOnScreen(args['btn_login'], grayscale=1)
        for img in [args['login'], args['login_a']]:
            rect = pg.locateOnScreen(img, grayscale=1)
            if rect is not None:
                break
        return rect
    except OSError as _err:
        print(_err)
        return None

async def click_object(rect):
    pg.click(rect,interval=1)
    await asyncio.sleep(1)

async def type_object(string):
    pg.typewrite(string)
