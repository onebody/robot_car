#!/usr/bin/env python
## coding=gbk
#
# Imports
import web
import threading
from thread_test import myThread

urls = (
    '/robot_api', 'index'
)

#myTh = threading.currentThread()
#if (myTh == None or isinstance(myTh, myThread)):


#print isinstance(myTh, myThread)
#print("thread is : %s , %s" % (str(myTh == None), myTh))


class index:
    myTh = myThread("robot")

    def GET(self):
        i = web.input()
        action = i.action
        msg = ""
        if (self.myTh == None ):
            self.myTh = myThread("robot")

        threadflag = self.myTh.isAlive()

        if (action == 'go'):
            if (threadflag == 1):
                self.myTh.thread_stop = False
            else:
                self.myTh.start()
            msg = "go"
        elif (action == "back"):
            self.myTh.stop()
            self.myTh = None
            msg = "stop"

        return "Hello, world!>>>" + action + "---" + unicode(msg, "gbk")


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()