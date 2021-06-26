import os
import time
import shared
import pyautogui as pg
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
