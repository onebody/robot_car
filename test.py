#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

def checkLEDStatus():
    while True:
        print("led on")
        time.sleep(10)

checkLEDStatus()