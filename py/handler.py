#
# btn-autolog
# btn-departures
# btn-folios
# btn-audit
import os
import ctypes
import asyncio
import pyautogui as pg
from PIL import Image
user32 = ctypes.windll.user32
args = \
{
    'autolog':False,
    'threadStop':False,
}
idir = ('C:\\Users\\admin\\AuditProductivity\\AuditExpress\\image_refs\\')
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
# seperates password and control data
def interpret(message):
    message = message.split('*')
    control = message[0]
    password = message[1]
    msg = execute(control)
    return(msg)

# execute commands linked to a control
def execute(control):
    if control == 'btn-autolog':
        # since autolog is a toggle, i need to ensure the togglestate is accurate.
        # so on the return it should be like 'yo this is off, or this is on'
        if(asyncio.run(find_login())):
            return('found_login')
        return('no_login')
    return(control)



def initialize():
    ind = 0
    maxSize = len(image_list)
    for image in image_list.keys():
        image_list[image] = Image.open(image_list[image])
        ind+=1
        #return_message(str(ind)+'/'+str(maxSize)+' files','')
    #return_message("loading complete",'')
async def find_login():
    """FIND LOGIN_BOX, CLICKS AND RETURNS BOOL"""
    if await find_object("login"):
        await click_object(await find_object("login"))
        return True
    if await find_object("login_a"):
        await click_object(await find_object("login_a"))
        return True
    return False

async def find_object(image_string):
    """RETRIEVE RECT, STRING"""
    # print(image_string)
    if not await(heartbeat()):
        try:
            rect = pg.locateOnScreen(image_list[image_string], grayscale=True)
            # print(rect)
            return rect
        except OSError as _err:
            print(_err)
            await heartbeat(True)

async def heartbeat(force_stop=False):
    """ENSURE THREAD SHOULD BE RUNNING,
    PRESSING ESCAPE SIGNALS A SHUTDOWN
    force_stop TRUE forcibly kills thread
    """
    if args["threadStop"] or force_stop:
        if args["autoLog"]:
            args["autoLog"] = False
            #print_history("-cancelled_command")
        args["threadStop"] = False
        sys.exit("Cancelling_thread")

async def click_object(rect, dbl=False):
    """SEND CLICK EVENT, RECT, BOOL"""
    if rect is None:
        return False
    if dbl:
        pg.doubleClick(rect)
    else:
        pg.click(rect)
    await asyncio.sleep(args["delay"])
    return True
