import threading
import time

class myThread(threading.Thread):
    def __init__(self, t_name):
        threading.Thread.__init__(self, name=t_name)
        self.thread_name = t_name
        self.thread_stop = False
        self.index = 0

    def run(self): #Overwrite run() method, put what you want the thread do here
        while not self.thread_stop:
            self.index = self.index + 1
            print ('Thread %s, Time:%s  index: %d\n  ' % (self.thread_name, time.ctime(), self.index))
            time.sleep(1)


    def stop(self):
        self.thread_stop = True