import asyncio
import ctypes
import sys
from pynput.keyboard import Key, Controller

KBD = Controller()

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

async def DECODE_COMMANDS(command):
    #for command in commands:
    if command.startswith("REPORTS"):
        for com in COMMAND_LIST[command]:
            key_cmb = COMMAND_LIST[com]
            await RUN_COMMAND(com,key_cmb)
    else:
        key_cmb = COMMAND_LIST[command]
        await RUN_COMMAND(command,key_cmb)
        
            
            
async def RUN_COMMAND(command,key_cmb):
    KBD.press(key_cmb[0])
    KBD.press(key_cmb[1])
    KBD.release(key_cmb[0])
    KBD.release(key_cmb[1])
    #ctypes.windll.user32.MessageBoxW(0, command, str(key_cmb), 1)
    #print(command)

async def main(a=None):
    if a is None:
        ctypes.windll.user32.MessageBoxW(0, "awaiting commands","notice", 1)
    else:
        #ctypes.windll.user32.MessageBoxW(0, a,"notice", 1)
        await DECODE_COMMANDS(a)
    
asyncio.run(main(sys.argv[1]))