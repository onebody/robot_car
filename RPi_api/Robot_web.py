#!/usr/bin/env python
# # coding=gbk
#
# Imports
import web

from Robot_auto import *


urls = (
    '/robot_api', 'index'
)

robot_car = Robot_Car()

class index:
    def GET(self):
        i = web.input()
        action = i.action
        robot_car.manual(action)
        return "Hello, world!>>>" + action


if __name__ == "__main__":
    print("Robot HTTP server is running....")
    app = web.application(urls, globals())
    app.run()