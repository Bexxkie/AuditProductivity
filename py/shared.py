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
    'alog_thread': None,
    'departures_thread': None,
    'eRate_thread':None,
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
    "btn_ok": idir + "common\\ok.png",
    "file": idir + "common\\file.png",
    "save": idir + "common\\save.png",
    ## folio
    "a_bill": idir + "folio\\advance_bill.png",
    "a_guest": idir + "folio\\all_guest.png",
    "a_windows": idir + "folio\\all_windows.png",
    "c_cards": idir + "folio\\credit_card.png",
    "depart": idir + "folio\\depart_tomorrow.png",
    "r_order": idir + "folio\\room_order.png",
    "sim": idir + "folio\\simulate.png",
    ## exclusion rates
    "block": idir+"res_forecast\\block.png",
    "block_def": idir+"res_forecast\\block_def.png",
    "deliminated_data": idir+"res_forecast\\deliminated_data.png",
    "dropdown": idir+"res_forecast\\dropdown.png",
    "print_to_file": idir+"res_forecast\\print_to_file.png",
    "rate_code": idir+"res_forecast\\rate_code.png",
    "res_forecast1": idir+"res_forecast\\res_forecast1.png",

}
reports_state_list = ['ico_root','misc','reports_window','reports','btn_search']
def get(argName):
    return args[argName]

def set(argName,value):
    args[argName] = value

def get_alog_ass():
    return [
        image_list['btn_login'],
        image_list['login'],
        image_list['login_a'],
        args['pass']
    ]

def get_dep_ass():
    return [
        image_list['ico_root_t'],
        image_list['misc'],
        image_list['reports_window'],
        image_list['reports'],
        image_list['btn_search'],
        image_list['btn_close'],
        image_list['btn_exit'],
        image_list['btn_print'],
        image_list['departures'],
        str(update_time().strftime('%m-%d-%y'))
    ]

def get_er_ass():
    return [
        image_list['misc'],
        image_list['reports_window'],
        image_list['reports'],
        image_list['res_forecast1'],
        image_list['btn_search'],
        image_list['print_to_file'],
        image_list['dropdown'],
        image_list['deliminated_data'],
        image_list['btn_ok'],
        image_list['rate_code'],
        image_list['block'],
        image_list['block_def'],
        image_list['file'],
        image_list['save'],
        image_list['ico_root_t'],
        image_list['btn_close'],
        image_list['btn_exit'],
    ]



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
