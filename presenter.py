from queue import Queue
import threading
import ast

class PreThread(threading.Thread):
    def __init__(self, snd_ques={}):
        ic()
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.setDaemon(True)

        self._rcv_que = Queue()
        self._snd_ques = snd_ques
        return

    def stop(self):
        ic()
        self.stop_event.set()
        return


    def run(self):
        ic()
        while True:
            item = self.rcv_que.get()
            print("[pre_th]", "run : get : ", item)
            if "sw" in item["type"]:
                self._recvice_sw(item)
            else:
                print("[pre_th]", "Error : ", item)

        return
    
    def _recvice_sw(self, item):
        ic()

        def send_que_sw_no1():
            
            self._snd_ques["oled"].put({"type": "oled", "time": val_time, "disp": val_disp})
            return

        def send_que_sw_no2():
            if "oled" not in self._snd_ques:
                ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "que not found!")
                return
            val_time = "3000"
            val_disp = self._sysdat.get_next_display()
            self._snd_ques["oled"].put({"type": "oled", "time": val_time, "disp": val_disp})
            return

        name = item["name"]
        action = item["action"]
        if "no1" in name:
            send_que_sw_no1(action)
        elif "no2" in name:
            send_que_sw_no2(action)
        else:
            ic(sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, "command not found!", name)
        return
        
    @property
    def rcv_que(self):
        return self._rcv_que


def main():
    import time

    pre_th = PreThread()
    pre_th.start()
    q = pre_th.rcv_que
    q.put("123")
    time.sleep(1)

    for i in range(5):
        q.put(i)
        time.sleep(1)
    pre_th.stop()
   
    return

if __name__ == "__main__":
    main()