import os
import time
import shared
import pyautogui as pg
import pygetwindow as gw
from PIL import Image
#
import shared

def find_object(image_string):
    """RETRIEVE RECT, STRING"""
    # print(image_string)
    try:
        rect = pg.locateOnScreen(shared.image_list[image_string], grayscale=1)
        return rect
    except OSError as _err:
        shared.build_message_info(_err,1,1)

def click_object(rect, dbl=0):
    """SEND CLICK EVENT, RECT, BOOL"""
    if rect is None:
        return 0
    if dbl:
        pg.doubleClick(rect)
    else:
        pg.click(rect)
    time.sleep(shared.get("delay"))
    return 1

def type_object(string, press=0, count=1):
    """SEND TYPE EVENT, STRING, BOOL, INT"""
    if press:
        pg.press(string, presses=count)
    else:
        pg.typewrite(string)
    return 1

def close_window():
    """CLOSE WINDOW, RETURN TO ROOT HELPER"""
    if find_object("btn_close"):
        click_object(find_object("btn_close"))
        return 1
    if find_object("btn_exit"):
        click_object(find_object("btn_exit"))
        return 1
    return 0

def load_reports(report_name):
    if window_exists():
        # make sure we're at root
        while find_object("ico_root_t") is None:
            close_window()
        click_object(find_object('misc'))
        click_object(find_object('reports_window'))
        click_object(find_object("reports"))
        type_object(report_name)
        click_object(find_object("btn_search"))
        click_object(find_object(report_name), True)

def window_exists():
    """CHECKS FOR OPERA WINDOW, RETURNS WINDOW IF TRUE, ELSE RETURN NONE"""
    try:
        window = gw.getWindowsWithTitle('OPERA PMS')[0]
    except IndexError:
        return None
    #if !window.isActive:
    #    pg.application.Application().connect(handle=window._hWnd).top_window().set_focus()
    window.restore()
    return window
