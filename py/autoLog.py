import ctypes
import time
from PIL import Image
#
import shared
import interactor
user32 = ctypes.windll.user32

def alog():
    shared.build_message_info('alog ready..',1,1)
    while 1:
        while shared.get("autoLog"):
            if user32.GetForegroundWindow() != 0:
                if bool(find_login()):
                    interactor.type_object(shared.get("pass"))
                    interactor.click_object(interactor.find_object("btn_login"))
            else:
                time.sleep(shared.get('delay'))
        else:
            #shared.return_message('@info%1%tic off')
            time.sleep(shared.get('delay'))



def find_login():
    if interactor.find_object("login"):
        interactor.click_object(interactor.find_object("login"))
        return 1
    if interactor.find_object("login_a"):
        interactor.click_object(interactor.find_object("login_a"))
        return 1
    return 0
