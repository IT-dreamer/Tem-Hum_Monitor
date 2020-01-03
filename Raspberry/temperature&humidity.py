# coding:UTF-8
"""
author:AFei
data:2020.01.02
version:1.0
function:以arduino为下位机，对温湿度进行监控，并将相关数据上传到OneNet
         使用HTTP协议，HTTP协议是无法实现客户端和服务器双向通信的，因此它只能限制在客户端给服务器发送数据
improve:使用MQTT协议，服务器端也可以向客户端发送数据
attention:此代码是以树莓派为平台的
"""
# ====import====
import serial
import requests
import json
import time

APIKEY = '8=Bz1JrjznaKeK8EADOVqSvx0dk='  # API地址（私有）
apiheaders = {'api-key': APIKEY, 'Content-Length': '120'}   # HTTP的header部分
url = 'http://api.heclouds.com/devices/579381146/datapoints'    # 设备的url

port = "/dev/ttyACM0"   #树莓派上的arduino端口号
SerialFromArduino = serial.Serial(port, 9600, timeout=1)    # 连接arduino，波特率为9600，延时为1s，超过1s则断开
SerialFromArduino.flushInput()  # 清空flash

def data_post():
    response = str(SerialFromArduino.readline())    # 读取aruduino发送过来的数据
    humidity = response[9:11]   # 取湿度
    print(humidity)
    temperature = response[26:28]   #取温度
    print(temperature)

    # 将温湿度两个数据加入到json报文中，注意拼写，否则云平台上会出现乱码
    PayLoad = ({"datastreams":[{"id":"humidity", "datapoints":[{"value":humidity}]},
                               {"id":"temperature", "datapoints":[{"value":temperature}]}]})

    jdate = json.dumps(PayLoad)     # 使用dumps函数，不能使用dump函数，因为dump是将转换完的json数据放入到某一文件中
    r = requests.post(url, headers=apiheaders, data=json.dumps(PayLoad))    # 使用post命令，要严格遵守OneNet的开发文档要求
    return r


while True:
    time.sleep(2)
    resp = data_post()