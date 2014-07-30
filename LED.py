#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from Yeelink import Yeelink_util

class LED():
    def checkLEDStatus(self):
        yeelink = Yeelink_util()
        yeelink.setup("913b9a04facaa48be5677b76cbbb2259", "12835", "20887")

        while True:
            ledValue = yeelink.getValue("value")
            #timestamp = yeelink.getValue("timestamp")

            if ledValue == 1:
                print("led on")
                # bus.write_byte( 0x20 , 1 )
            else:
                print("led off")
                # bus.write_byte( 0x20 , 0 )
                # 延时1S
            time.sleep(1)


led = LED()
led.checkLEDStatus()