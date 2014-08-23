#!/usr/bin/env python
# # coding=gbk
#
# Imports
import web

from Robot_auto import *


urls = (
    '/robot_api', 'index'
)

print("Robot HTTP server is running....")
robot_car = Robot_Car()


class index:
    distanceType_Before = 'Before'
    distanceType_After = 'After'

    isAuto = True

    delays = 0.5  #
    steps = 100  #

    def GET(self):
        i = web.input()
        action = i.action
        robot_car.manual(action)
        return "Hello, world!>>>" + action


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()