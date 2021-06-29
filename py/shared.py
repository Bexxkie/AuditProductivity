import os
import sys
import datetime as dt

from PIL import Image



def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


idir = resource_path("image_refs\\")
#idir = os.getcwd()+'\\res\\image_refs\\'
args = \
{
    'autoLog':0,
    'threadStop':0,
    'delay':1,
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
reports_state_list = ['ico_root','misc','reports_window','reports','btn_search']
def get(argName):
    return args[argName]

def set(argName,value):
    args[argName] = value

def return_message(msg):
    sys.stdout.write(str(msg)+'\n')
    sys.stdout.flush()
    return 1


def build_message_info(msg,timestamp,send):
    message = ('@info%'+str(timestamp)+"%"+str(msg))
    if not send:
        return(message)
    return_message(message)
    return 1

# controlName 0=set, 1=sendCommand, value
def build_message_command(control,get_set,send,value=None):
    message = ('@uvar%'+str(get_set)+'%'+str(control))
    if value is not None:
        message = (message+'%'+str(value))
    if not send:
        return(message)
    return_message(message)
    return 1

def update_time():
    """Updates time"""
    hour = dt.datetime.now().hour
    if hour > 20:
        return dt.date.today() + dt.timedelta(days=1)
    return dt.date.today()
