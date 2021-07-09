import ctypes
import pyautogui as pg
import pygetwindow as gw
import asyncio

args = {}
user32 = ctypes.windll.user32

def start(arg):
    # for departures we need a lot of images
    args['ico_root_t'] = arg[0]
    args['misc'] = arg[1]
    args['reports_window'] = arg[2]
    args['reports'] = arg[3]
    args['btn_search'] = arg[4]
    args['btn_close'] = arg[5]
    args['btn_exit'] = arg[6]
    args['btn_print'] = arg[7]
    args['departures'] = arg[8]
    args['date'] = arg[9]
    asyncio.run(departure())

async def departure():
    if await window_exists():
        await ensure_root()
        pg.click(await find_object('misc'))
        pg.click(await find_object('reports_window'))
        pg.click(await find_object('reports'))
        await type_object('departures')
        pg.click(await find_object('btn_search'))
        pg.doubleClick(await find_object('departures'))
        await type_object(args['date'])
        pg.press('tab',presses=2)
        pg.click(await find_object('btn_print'))



async def ensure_root():
    while await find_object('ico_root_t') is None:
        for obj in ['btn_close', 'btn_exit']:
            rect = await find_object(obj)
            if rect is not None:
                await click_object(rect)


async def click_object(rect):
    pg.click(rect,interval=1)
    await asyncio.sleep(1)


async def find_object(object):
    try:
        return pg.locateOnScreen(args[object], grayscale=1)
    except OSError as _err:
        print(_err)
        return None

async def type_object(string):
    pg.typewrite(string)

async def window_exists():
    """CHECKS FOR OPERA WINDOW, RETURNS WINDOW IF TRUE, ELSE RETURN NONE"""
    try:
        window = gw.getWindowsWithTitle('OPERA PMS')[0]
    except IndexError:
        return None
    #if !window.isActive:
    #    pg.application.Application().connect(handle=window._hWnd).top_window().set_focus()
    window.activate()
    #window.restore()
    return window
