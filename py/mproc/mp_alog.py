import ctypes
import time
import tkinter as tk
import pyautogui as pg

#
# We need to listen and wait for the loginbox to show
# The only objects i need here are, login, login_a, pass, btn_login
#

# think i need to pass this in from the start
btn_login = None
login = None
login_a = None
password = None

user32 = ctypes.windll.user32

def start(args):
    tk.messagebox.showinfo("info",str(args))
    btn_login = args[0]
    login = args[1]
    login_a = args[2]
    password = args[3]
    alog()

def alog():
    while 1:
        if user32.GetForegroundWindow()!=0: # is the screen locked?
            click_object(find_login())
            type_object(password)
            click_object(btn_login)
        else:
            time.sleep(1)


# return object
def find_login():
    try:
        for img in [login, login_a]:
            rect = pg.locateOnScreen(img, grayscale=1)
            if rect is not None:
                return rect
    except OSError as _err:
        print(_err)
        return None

def click_object(rect):
    if rect is None:
        return 0
    if dbl:
        pg.doubleClick(rect)
    else:
        pg.click(rect)
    time.sleep(1)
    return 1
