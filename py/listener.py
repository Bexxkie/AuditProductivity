import sys
#
import shared
import handler
def main():
    shared.return_message('@info%1%Listner active..')
    for msg in sys.stdin:
        if shared.get('debug'):
            con = msg.split('*')
            con[1] = '*'*len(con[1])
            shared.return_message("@info%1%"+str(con[0]+con[1]))
        handler.interpret(msg) # send to handler
        #time.sleep(1)
    sys.exit()
