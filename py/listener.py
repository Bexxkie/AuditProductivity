import time
import sys
import asyncio
import os
from PIL import Image


def return_message(msg,timestamp='tstamp'):
    print(timestamp+msg)
    sys.stdout.flush()

def listener():
    while 1:
        for msg in sys.stdin:
            return_message('return: '+msg.strip())
        time.sleep(1)

idir = ('C:\\Users\\admin\\AuditProductivity\\AuditExpress\\image_refs\\')
imagelist = \
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

# return Image object
def request(filename):
    return imagelist[filename]

def initialize():
    ind = 0
    maxSize = len(imagelist)
    for image in imagelist.keys():
        imagelist[image] = Image.open(imagelist[image])
        ind+=1
        return_message(str(ind)+'/'+str(maxSize)+' files','')
    return_message("loading complete",'')
initialize()
listener()
