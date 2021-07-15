import time

# debug
import sys
from icecream import ic

from led import LedThread
from tswitch import SwThread
from presenter import PreThread

def setupPresenter(th, que_out):
    th = PreThread(que_out)
    th.start()
    return th.rcv_que

def setupInputs(ths, que_pre):
    ths["sw"] = SwThread(que_pre)
    for in_th in ths.values():
        in_th.start()

def setupOutputs(ths):
    ths["led"] = LedThread()
    for out_th in ths.values():
        out_th.start()

    return {k:v.rcv_que for k, v in ths.items()}

def cleanUp(pre, in_ths, out_ths):
    for out_th in out_ths.values():
        out_th.stop()

    pre.stop()

    for in_th in in_ths.values():
        in_th.stop()

def main():
    # ic.enable()
    ic.disable()

    out_ths = {}
    que_out = setupOutputs(out_ths)

    pre = {}
    que_pre = setupPresenter(pre, que_out)

    in_ths = {}
    setupInputs(in_ths, que_pre)

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("stop")

    cleanUp(pre, in_ths, out_ths)
    return

if __name__ == "__main__":
    main()
