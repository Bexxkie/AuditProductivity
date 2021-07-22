import ctypes

import npyscreen
import sys
import subprocess
import curses
from pynput.keyboard import Key, Controller
import datetime
import os
import asyncio
import random
import time
import winsound
import configparser
#from cryptography.fernet import Fernet


CONFIG = configparser.ConfigParser()
CONFIG.read('CONFIG.ini')
#KEY         = CONFIG['GLOB']['key']
#CYPHER      = CONFIG['GLOB']['pss']
__NAME__    = CONFIG['GLOB']['nme'] # AuditExpress3
__AUTHOR__  = CONFIG['GLOB']['ath'] # BrianG
__VERSION__ = CONFIG['PYTH']['ver'] # version
__CHLOG__   = CONFIG['GLOB']['log'] # Last changes
_T_ = False
#cipher_suite = Fernet(KEY.encode())
#decryptedPass = cipher_suite.decrypt(CYPHER.encode())

#pth = os.getcwd().replace('Python', 'AHK\\')
pth = os.getcwd()
KBD = Controller()
COMMAND_LIST = {
    'REPORTS_SHORT': ['csh_adt', 'rat_chk', 'cdt_lmt', 'cdt_rcn', 'dwn_r04'],
    'REPORTS_LONG': ['csh_adt', 'rat_chk', 'cdt_lmt', 'cdt_rcn', 'dwn_r13'],
    'csh_adt': [Key.f20, '1'],
    'rat_chk': [Key.f20, '2'],
    'cdt_lmt': [Key.f20, '3'],
    'cdt_rcn': [Key.f20, '4'],
    'dwn_r04': [Key.f20, '5'],
    'dwn_r13': [Key.f20, '6'],
    'LOGIN': [Key.f20, '0'],
    'QUIT': [Key.f20, 'x'],
    'PRINT_DEPARTURES_LIST': [Key.f20, '7'],
    'LOAD_BATCH_FOLIOS_MENU': [Key.f20, '8'],
    'ihg_rep': [Key.f20, '9'],
    'PRINT_OCCUPANCY_ GRAPH': [Key.f20, Key.f19],
    'LOAD_QUICK_CHECKOUT': [Key.f19, '1'],
    'PRINT_REG_CARDS': [Key.f19, '3'],
    'PETERS_REPORTS' :[Key.f19, '4']
  
}


COMMAND_INTERFACE_SINGLE = [
    'HELP',
    "CHANGELOG",
    'REPORTS_SHORT',
    'REPORTS_LONG',
    'PRINT_DEPARTURES_LIST',
    'LOAD_BATCH_FOLIOS_MENU',
    'LOGIN',
    'LOAD_QUICK_CHECKOUT',
    'QUIT',
    'PRINT_OCCUPANCY_GRAPH',
    'csh_adt',
    'rat_chk',
    'cdt_lmt',
    'cdt_rcn',
    'dwn_r04',
    'dwn_r13',
    'PRINT_REG_CARDS',
    'PETERS_REPORTS'
]


_p = " > " # Info pane prefix
_info = [
    'Click, or use the arrow keys and SPACE/ENTER to select an option.',
    "VERSION: "+__VERSION__+" | "+__CHLOG__,
    'Standard Reports - Run every successive shift',
    'Full Reports - Run first shift',
    'Print Next-Day Departures',
    'Load Batch Folios Menu For Next-Day Departures',
    'Enter OPERA Password - Required for cashier functions',
    'Load Quick Checkout Screen',
    'Close AuditExpress And Related Services',
    'Print The Occupancy Graph - Unreliable',
    'Print Cahier Audit',
    'Print Guests in-house rate check',
    'Print Credit Limit All Payment Types',
    'Print Credit Card Reconcilliation',
    'Print Downtime Report(04)',
    'Print Downtime Report(13)',
    'Print Registration cards',
    'Print morning reports for peter'
]


PREPAID_RTC =[
    "IDAWV",
    "IDUWV",
    "IDHWV",
    "IDHNP",
    "IDHVC",
    "IDH25",
    "IDIN2",
    "IDU00",
    "IDUVC",
    "IWU25",
    "IWH25",
    "IDU25",
    "IDU14",
    "IDAX4"
]


def draw(dir):
    if dir == 0:
        top = "(\_(\ "
        eyeIndex = random.choice(["'",">","-"])
        mouth = random.choice(["x","*",".","_","=","ω"])
        bot = "|"+eyeIndex+mouth+eyeIndex+")"
        
        return top+'\n'+" "+bot
    
    if dir == 1:
        top = "/)_/)"
        eyeIndex = random.choice(["'","<","-"])
        mouth = random.choice(["x","*",".","_","=","ω"])
        bot = "("+eyeIndex+mouth+eyeIndex+"|"
        
        return " "+top+'\n'+bot
        
    if dir == 2:
        top = "(\_/)"
        eyeIndex = random.choice(["'","<", ">","-"])
        mouth = random.choice(["x","*",".","_","=","ω"])
        bot = "("+eyeIndex+mouth+eyeIndex+")"
        
        return top+'\n'+bot

#def draw(er,fc):
#    l = "("
#    r = ")"
#    e = ears.get(er)
#    if er == '1':
#        l = " |"
#    elif er == '2':
#        r = "|"
#        e = " "+ears.get(er)
#    f = face.get(fc).replace('l',l).replace('r',r)
#    return e+'\n'+f

class AuditExpress(npyscreen.NPSAppManaged):
    ##
    def onStart(self):
        curses.resize_term(30,100)
        # use this to init the form, add screens and whatnot
        self.addForm("MAIN", FormMain, name="AuditExpress3", columns=100, lines=30, color="STANDOUT")


class FormMain(npyscreen.FormBaseNew):
    def create(self):
        ctypes.windll.kernel32.SetConsoleTitleW(__NAME__)
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        # id =0, info box
        _widget_box_info = self.add(
            BoxInfo,
            name="INFO",
            color="IMPORTANT",
            value=_p+_info[0],
            editable=False,
            rel_x=2,
            rel_y=0,
            max_width=68,

        )
        #id = 1, command box
        _widget_box_commands = self.add(
            Box,
            name="COMMANDS",
            contained_widget_arguments={
                'values': COMMAND_INTERFACE_SINGLE,
                'color': 'STANDOUT'
            },
           # value=True,
            relx=2,
            rely=5,
            max_width=34,
            max_height=18,
            color="STANDOUT",
            labelColor="STANDOUT",
            widget_inherit_color=True
        )
        #id =2, history box
        _widget_box_history = self.add(
            npyscreen.BoxTitle,
            name="HISTORY",
            value=[],
            color="STANDOUT",
            labelColor="STANDOUT",
            relx=36,
            rely=5,
            max_width=34,
            max_height=15,
            editable=True
        )
        #id=3, bun
        _widget_box_bun = self.add(
            npyscreen.BoxTitle,
            name = "",
            values = draw(0).split('\n'),
            relx=70,
            rely=1,
            max_width=11,
            max_height=4,
            lavelColor="VERYGOOD",
            editable=False
            )
        #id =4, submit button
        _widget_button_submit = self.add(
            ButtonSubmit,
            name="SUBMIT",
            color="VERYGOOD",
            values="SUBMIT",
            relx=36,
            rely=20,
            max_width=10,
            max_height=4,
        )
        #id =5, quit button
        _widget_button_exit = self.add(
            ButtonExit,
            name="EXIT",
            color="CRITICAL",
            values="EXIT",
            relx=45,
            rely=20,
            max_width=10,
            max_height=4,
        )
        #id =6, prepaid ratescreen
        _widget_rtc = self.add(
            RTC_box,
            color="STANDOUT",
            name = "PPD RTC",
            contained_widget_arguments={
                'values': PREPAID_RTC,
                'color': 'STANDOUT'
            },
            relx=70,
            rely=5,
            max_height=15,
        )
        #id =7, RTC button
        _widget_rtc_button = self.add(
            RTC_button,
            name="SEARCH",
            color="VERYGOOD",
            values="SEARCH",
            relx = 70,
            rely=20,
            )
        

#
# DEFINE CUSTOM WIDGETS
#
class BoxInfo(npyscreen.Textfield):
    pass

#
# COMMAND SELECTOR CHILDS 'BOX'
# this is for the list of options
#
class NewSelectOne(npyscreen.SelectOne):
    def when_cursor_moved(self):
        _line = self.cursor_line
        print(_line)
        a = self.parent.get_widget(0)
        b = self.parent.get_widget(3)
        c = self.parent.get_widget(2)
        x = random.randint(0,2)
        b.values = draw(x).split('\n')
        b.update(b)
        c.update(c)
        if _T_: 
            winsound.Beep(random.randrange(200,2000),50)
        a.value = _p+_info[_line]
        a.update(a)

    def handle_mouse_event(self, mouse_event):
        mouse_id, rel_x, rel_y, z, bstate = self.interpret_mouse_event(mouse_event)
        if rel_y < 0:
            _line = 0
        elif rel_y > len(_info)-1:
            _line = len(_info)-1
        else:
            _line = rel_y
        self.cursor_line = _line
        self.h_select(self)
#
# RTC menu
#
class RTC_select(npyscreen.SelectOne):

    def when_cursor_moved(self):
       _line = self.cursor_line
       b = self.parent.get_widget(3)
       x = random.randint(0,2)
       b.values = draw(x).split('\n')
       b.update(b)
       
    def handle_mouse_event(self,mouse_event):
        mouse_id, rel_x, rel_y, z, bstate = self.interpret_mouse_event(mouse_event)
        if rel_y < 0:
            _line = 0
        elif rel_y > len(PREPAID_RTC)-1:
            _line = len(PREPAID_RTC)-1
        else:
            _line = rel_y
        self.cursor_line = _line
        self.h_select(self)
        
#
# RTC boundingbox
#      
class RTC_box(npyscreen.BoxTitle):
    _contained_widget = RTC_select
    
#
# RTC_BUTTON
#
class RTC_button(npyscreen.ButtonPress):
    def handle_mouse_event(self, mouse_event):
        mouse_id, rel_x, rel_y, z, bstate = self.interpret_mouse_event(mouse_event)
        # send commands
        t = datetime.datetime.now().strftime("%T")
        try:
            try:
                a = self.parent.get_widget(6)._contained_widget.get_selected_objects(self.parent.get_widget(6))[0]
            except:
                a = "IDAWV"
            b = self.parent.get_widget(2)
            history = b.get_values()
            history.append("<" + t + "> " + "RTC CHECK: "+a)
            w = self.parent
            #h = asyncio.run(decode_commands(a, w, history))
            index = PREPAID_RTC.index(a)
            asyncio.run(RTC_check(index))
            b.update(clear=True)
        except (IndexError,ValueError) as error:
            b = self.parent.get_widget(2)
            #history = b.get_values().append("<"+t+"> NO SELECTION")
            #b.value = history
            index = PREPAID_RTC.index(a)
            asyncio.run(RTC_check(index))
            b.update(clear = True)
    
    def whenPressed(self):
        t = datetime.datetime.now().strftime("%T")
        try:
            try:
                a = self.parent.get_widget(6)._contained_widget.get_selected_objects(self.parent.get_widget(6))[0]
            except:
                a = "IDAWV"
            b = self.parent.get_widget(2)
            history = b.get_values()
            history.append("<" + t + "> " + "RTC CHECK: "+a)
            w = self.parent
            #h = asyncio.run(decode_commands(a, w, history))
            index = PREPAID_RTC.index(a)
            asyncio.run(RTC_check(index))
            b.update(clear=True)
        except (IndexError,ValueError) as error:
            b = self.parent.get_widget(2)
            #history = b.get_values().append("<"+t+"> NO SELECTION")
            #b.value = history
            index = PREPAID_RTC.index(a)
            asyncio.run(RTC_check(index))
            b.update(clear = True)
#
# VISUAL ONLY, PARENTS 'NEWSELECTONE'
# this is the box drawn around options menu
#
class Box(npyscreen.BoxTitle):
    _contained_widget = NewSelectOne
#
# QUIT SHORTCUT
#
class ButtonExit(npyscreen.ButtonPress):
    def handle_mouse_event(self, mouse_event):
        mouse_id, rel_x, rel_y, z, bstate = self.interpret_mouse_event(mouse_event)
        w = self.parent
        if _T_: 
            winsound.Beep(3000,1500)
        asyncio.run(decode_commands("QUIT",w))
        self.parent.parentApp.switchForm(None)
        sys.exit(0)

    def whenPressed(self):
        w = self.parent
        if _T_:
            winsound.Beep(3000,1500)
        asyncio.run(decode_commands("QUIT",w))
        self.parent.parentApp.switchForm(None)

#
# RUN CURRENT COMMAND
#
class ButtonSubmit(npyscreen.ButtonPress):
    def handle_mouse_event(self, mouse_event):
        mouse_id, rel_x, rel_y, z, bstate = self.interpret_mouse_event(mouse_event)
        # send commands
        t = datetime.datetime.now().strftime("%T")
        try:
            a = self.parent.get_widget(1)._contained_widget.get_selected_objects(self.parent.get_widget(1))[0]
            b = self.parent.get_widget(2)
            history = b.get_values()
            history.append("<" + t + "> " + a)
            w = self.parent
            h = asyncio.run(decode_commands(a, w, history))
            b.value = h
            b.update(clear=True)
            if a == "QUIT":
                self.parent.parentApp.switchForm(None)
        except IndexError as error:
            b = self.parent.get_widget(2)
            history = b.get_values().append("<"+t+"> NO SELECTION")
            b.value = history
            b.update(b)

    def whenPressed(self):
        t = datetime.datetime.now().strftime("%T")
        try:
            a = self.parent.get_widget(1)._contained_widget.get_selected_objects(self.parent.get_widget(1))[0]
            b = self.parent.get_widget(2)
            history = b.get_values()
            history.append("<" + t + "> "+a)
            w = self.parent
            h = asyncio.run(decode_commands(a, w, history))
            b.value = h
            b.update(clear=True)
            if a == "QUIT":
                self.parent.parentApp.switchForm(None)
        except IndexError as error:
            b = self.parent.get_widget(2)
            history = b.get_values().append("<"+t+"> NO SELECTION")
            b.value = history
            b.update(clear=True)

#
# 
#
def terminal_dimensions():
    return curses.initscr().getmaxyx()

#
# check RTC
#
async def RTC_check(rtcIndex):
    await reset()
    rtcIndex+=1
    key = Key.f18
    if rtcIndex >=10:
        key = Key.f17
        rtcIndex -=9
    KBD.press(key)
    KBD.press(str(rtcIndex))
    
    KBD.release(key)
    KBD.release(str(rtcIndex))
    await asyncio.sleep(2)
    return
    

#
# RESET CODE
#
async def reset():
    KBD.press(Key.f19)
    KBD.press('0')
    KBD.release(Key.f19)
    KBD.release('0')
    await asyncio.sleep(2)
    return

#
# ENTER HERE, STEP ONE OF KEY_RELAY
#
async def decode_commands(command, widget, history = []):
    #startScripts()
    #await asyncio.sleep(1)
    b = widget.get_widget(3)
    c = widget.get_widget(2)
    x = random.randint(0,2)
    b.values = draw(x).split('\n')
    b.update(b)
    c.update(c)
    #ctypes.windll.kernel32.SetConsoleTitleW("AuditExpress - PARSING COMMANDS...")
    # if NOT login, send reset code
    if command != "LOGIN" and command != "QUIT" and command != "HELP" and command != "CHANGELOG":
        await reset()
    if command == "HELP" or command == "CHANGELOG":
        #ctypes.windll.kernel32.SetConsoleTitleW("AuditExpress - WAITING INPUT...")
        return
    if command == "PETERS_REPORTS":
        key_cmb = COMMAND_LIST[command]
        await run_command("PETERS_REPORTS", key_cmb)
        key_cmb = [key_cmb[0], str(int(key_cmb[1])+1)]
        await run_command("PETERS_REPORTS", key_cmb)
        return history
#   # batch reports
    if command.startswith("REPORTS"):
        for com in COMMAND_LIST[command]:
            history.append("<--{"+com+"}-->")
            key_cmb = COMMAND_LIST[com]
            await run_command(com, key_cmb)
    # any other command
    else:
        key_cmb = COMMAND_LIST[command]
        await run_command(command, key_cmb)
    #ctypes.windll.kernel32.SetConsoleTitleW("AuditExpress - WAITING INPUT...")
    return history

#
# SEND KEYS 
#
async def run_command(command, key_cmb):
    KBD.press(key_cmb[0])
    KBD.press(key_cmb[1])
    KBD.release(key_cmb[0])
    KBD.release(key_cmb[1])
    if command != "QUIT" and command != "LOGIN" and command != "HELP":
        await reset()
    if command == "QUIT":
        return
    await asyncio.sleep(5)
    return
    
    
def startScripts():
    subprocess.Popen('AuditExpress++Helper.exe')#+decryptedPass.decode())


def tune():
    if _T_:
        a = 0
        while a <6:
            winsound.Beep(random.randrange(300,1500),100)
            a+=1
    startScripts()
    app = AuditExpress()
    app.run()   

tune()