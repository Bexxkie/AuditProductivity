import ctypes

import npyscreen
import sys
import subprocess
import curses
from pynput.keyboard import Key, Controller
import datetime
import os
import asyncio

__NAME__    = "AuditExpress3"
__AUTHOR__  = "BrianG"
__VERSION__ = "1.2"


pth = os.getcwd().replace('Python', 'AHK\\')
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
    'LOAD_QUICK_CHECKOUT': [Key.f19, '1']
}

COMMAND_INTERFACE_SINGLE = [
    'HELP',
    'REPORTS_SHORT',
    'REPORTS_LONG',
    'PRINT_DEPARTURES_LIST',
    'LOAD_BATCH_FOLIOS_MENU',
    'LOGIN',
    'LOAD_QUICK_CHECKOUT',
    'QUIT',
    'PRINT_OCCUPANCY_GRAPH',
    'csh_adt',
    'cdt_lmt',
    'cdt_rcn',
    'dwn_r04',
    'dwn_r13'
]
_p = " > " # Info pane prefix
_info = [
    'Click, or use the arrow keys and SPACE/ENTER to select an option.',
    'Standard Reports - Run every successive shift',
    'Full Reports - Run first shift',
    'Print Next-Day Departures',
    'Load Batch Folios Menu For Next-Day Departures',
    'Enter OPERA Password - Required for cashier functions',
    'Load Quick Checkout Screen',
    'Close AuditExpress And Related Services',
    'Print The Occupancy Graph - Unreliable',
    'Print Cahier Audit',
    'Print Credit Limit All Payment Types',
    'Print Credit Card Reconcilliation',
    'Print Downtime Report(04)',
    'Print Downtime Report(13)'
]


class AuditExpress(npyscreen.NPSAppManaged):

    ##
    def onStart(self):
        curses.resize_term(30,75)
        # use this to init the form, add screens and whatnot
        self.addForm("MAIN", FormMain, name="AuditExpress2", columns=75, lines=30, color="STANDOUT")


class FormMain(npyscreen.FormBaseNew):
    def create(self):
        ctypes.windll.kernel32.SetConsoleTitleW("WAITING INPUT...")
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
            editable=False
        )
        #id =3, submit button
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
        #id =4, quit button
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

#
# DEFINE CUSTOM WIDGETS
#
class BoxInfo(npyscreen.Textfield):
    pass

#
# COMMAND SELECTOR CHILDS 'BOX'
#
class NewSelectOne(npyscreen.SelectOne):
    def when_cursor_moved(self):
        _line = self.cursor_line
        print(_line)
        a = self.parent.get_widget(0)
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
# VISUAL ONLY, PARENTS 'NEWSELECTONE'
#
class Box(npyscreen.BoxTitle):
    _contained_widget = NewSelectOne

#
# QUIT SHORTCUT
#
class ButtonExit(npyscreen.ButtonPress):
    def handle_mouse_event(self, mouse_event):
        mouse_id, rel_x, rel_y, z, bstate = self.interpret_mouse_event(mouse_event)
        asyncio.run(decode_commands("QUIT"))
        self.parent.parentApp.switchForm(None)
        sys.exit(0)

    def whenPressed(self):
        asyncio.run(decode_commands("QUIT"))
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
            h = asyncio.run(decode_commands(a, history))
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
            h = asyncio.run(decode_commands(a, history))
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
async def decode_commands(command, history = []):
    ctypes.windll.kernel32.SetConsoleTitleW("PARSING COMMANDS...")
    # if NOT login, send reset code
    if command != "LOGIN" and command != "QUIT" and command != "HELP":
        await reset()
    if command == "HELP":
        ctypes.windll.kernel32.SetConsoleTitleW("WAITING INPUT...")
        return
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
    ctypes.windll.kernel32.SetConsoleTitleW("WAITING INPUT...")
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
        await asyncio.sleep(3)
    return
    
    
subprocess.Popen("%s %s" % (pth+'AutoHotkeyU64.exe', pth+'test.ahk'))
app = AuditExpress()
app.run()   