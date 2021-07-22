


#
# Audit Express
#

__AUTHOR__ =  'BrianG'
__VERSION__ = '0.0a -dev'

import npyscreen
import os
import sys
import ctypes
import datetime
import subprocess
import curses
from pynput.keyboard import Key, Controller
import tempfile

pth = os.getcwd().replace('Python', 'AHK\\')


COMMAND_LIST = {
'REPORTS_SHORT':['csh_adt','rat_chk','cdt_lmt','cdt_rcn','dwn_r04'],
'REPORTS_LONG':['csh_adt','rat_chk','cdt_lmt','cdt_rcn','dwn_r13'],
'csh_adt':[Key.f20, '1'],
'rat_chk':[Key.f20, '2'],
'cdt_lmt':[Key.f20, '3'],
'cdt_rcn':[Key.f20, '4'],
'dwn_r04':[Key.f20, '5'],
'dwn_r13':[Key.f20, '6'],
'LOGIN':[Key.f20, '0'],
'QUIT':[Key.f20, 'x'],
'PRINT_DEPARTURES_LIST':[Key.f20, '7'],
'LOAD_BATCH_FOLIOS_MENU':[Key.f20, '8'],
'ihg_rep':[Key.f20, '9'],
'PRINT_OCCUPANCY_ GRAPH':[Key.f20, Key.f19],
'LOAD_QUICK_CHECKOUT':[Key.f19, '1']
}


COMMAND_INTERFACE_SINGLE = [
'0.REPORTS_SHORT', 
'1.REPORTS_LONG',
'2.PRINT_DEPARTURES_LIST',
'3.LOAD_BATCH_FOLIOS_MENU',
'4.LOGIN',
'5.LOAD_QUICK_CHECKOUT',
'6.QUIT',
'7.PRINT_OCCUPANCY_GRAPH'
]
_TEMP = tempfile.NamedTemporaryFile(delete=False, mode="w+t")
_TEMPNAME = _TEMP.name
__CTIME__ = 0
class AuditExpressAPP(npyscreen.NPSApp):
    def handle_mouse_event(self, mouse_event):
        mouse_id, rel_x, rel_y, z, bstate = self.interpret_mouse_event(mouse_event)
        KBD.press(Key.ENTER)
        KBD.release(Key.ENTER)
    def main(self):
        HISTORY = []
        __CTIME__=0
        while True:
            #self. = self.add(name = "Audit Express "+__VERSION__,)
            form = npyscreen.ActionFormMinimal(name="Audit express Version: "+__VERSION__+"  Command count: "+str(__CTIME__))
            column_height = terminal_dimensions()[0] - 9
            widget_commands = form.add(
                npyscreen.SelectOne,
                name = "COMMANDS",
                relx = 2,
                rely = 2,
                max_width = 30,
                max_height = column_height,
                values = COMMAND_INTERFACE_SINGLE,
                scroll_exit=True
            )
            widget_history = form.add(
                Column,
                name = "HISTORY",
                relx = 33,
                rely = 2,
                editable = False,
                values = HISTORY,
                max_height = column_height
            )
            #B = F.add(npyscreen.BoxTitle,name="b1",max_width=30,relx=2,max_height=2)
            #h = F.add(npyscreen.TitleFixedText, name = "History", value = str(__HISTORY__).replace(",","").replace("'",""))
            #ms = Widget_Commands.add(npyscreen.SelectOne, max_height=8, value = [0], name="Command", values = COMMAND_INTERFACE_SINGLE, scroll_exit=True)
            
            #selection = self.add(npyscreen.TitleSelectOne, max_height=8, value = [1,], name="Command", values = COMMAND_INTERFACE_SINGLE, scroll_exit=True)
            #_FRM.edit()
            #screen2()
            #DECODE_COMMANDS(selection.get_selected_objects())
            form.edit()   
            try:
                command = widget_commands.get_selected_objects()[0].split(".")
                t = datetime.datetime.now().strftime("%T")
                HISTORY = widget_history.get_values()
                HISTORY.append("("+t+") "+command[1])
                widget_history.update(clear = True)
                os.system("keyRelay.py " + command[1])
                if command[1]=="QUIT":
                    break
            except:
                t = datetime.datetime.now().strftime("%T")
                HISTORY = widget_history.get_values()
                HISTORY.append("("+t+") no selection")
                widget_history.update(clear = True)
            #if command[1] == "QUIT":
        
class Column(npyscreen.BoxTitle):
    def resize(self):
        self.max_height = int(0.73 * terminal_dimensions()[0])

def terminal_dimensions():
    return curses.initscr().getmaxyx()                
#subprocess.Popen("%s %s" % (pth+'AutoHotkeyU64.exe', pth+'test.ahk'))
App = AuditExpressAPP()
App.run()