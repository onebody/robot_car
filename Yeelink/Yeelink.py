#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json


class Yeelink_util():
    # 设备URI
    apiurl = 'http://api.yeelink.net/v1.0/device/{deviceID}/sensor/{sensorID}/datapoints'
    # 用户密码
    apiheaders = {'U-ApiKey': '913b9a04facaa48be5677b76cbbb2259'}

    # APP_Key
    APP_Key = '913b9a04facaa48be5677b76cbbb2259'

    # 设备ID
    deviceID = ''

    # 传感器ID
    sensorID = ''

    def setup(self, APP_Key, deviceID, sensorID):
        self.APP_Key = APP_Key
        self.deviceID = deviceID
        self.sensorID = sensorID

    def setAPP_Key(self, APP_Key):
        self.APP_Key = APP_Key

    def setDeviceID(self, deviceID):
        self.deviceID = deviceID

    def setSensorID(self, sensorID):
        self.sensorID = sensorID


    def getValue(self, key):
        #发送请求
        self.apiheaders['U-ApiKey'] = self.APP_Key
        self.apiurl = self.apiurl.replace('{deviceID}', self.deviceID).replace('{sensorID}', self.sensorID)
        r = requests.get(self.apiurl, headers=self.apiheaders)
        # 打印响应内容
        print("ResponseContent:  %s" % r.text)
        # 转换为字典类型 请注意 2.7.4版本使用r.json()
        json_r = json.loads(r.text)
        # {'value':x} x=1打开状态，x=0关闭状态
        if (r.status_code == requests.codes.ok):
            print("key name :%s " % key)
            return json_r.get(key)
        else:
            print("request error")