import sys
#
import shared
import handler
def main():
    shared.build_message_info('Listener active..',1,1)
    for msg in sys.stdin:
        if shared.get('debug'):
            con = msg.split('*')
            con[1] = '*'*len(con[1])
            shared.build_message_info(str(con[0]+con[1]),1,1)
        handler.interpret(msg) # send to handler
        #time.sleep(1)
    sys.exit()
