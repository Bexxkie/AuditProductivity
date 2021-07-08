from multiprocessing import Process as pr

import mptest2

if __name__ == '__main__':
    ls = [3,2]
    proc = pr(target = mptest2.start, args=[ls])
    proc.start()
    #proc.join()
