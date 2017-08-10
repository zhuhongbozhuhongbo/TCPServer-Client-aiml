# -*- coding: utf-8 -*-
'''
@author: xinghuazhang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: xing_hua_zhang@126.com
@software: PyCharm 2017.1.4
@file: TCPClient_NonGraphical.py
@time: 2017/8/9 18:03
@desc:
'''
from socket import *
import struct
import sys
import os
import time
reload(sys)
sys.setdefaultencoding('utf-8')
#####################################################################
class TcpClient:
    # HOST = 'localhost'
    PORT = 8000
    HOST = '127.0.0.1'
    BUFFSIZE = 1024
    ADDR = (HOST, PORT)

    def sentfile(self):
        filename = self.message  # 输入文件名
        FILEINFO_SIZE = struct.calcsize('128sI')  # 编码格式大小
        fhead = struct.pack('128sI', filename.split('\\')[-1], os.stat(filename).st_size)  # 按照规则进行打包
        self.client.send(fhead)  # 发送文件基本信息数据
        fp = open(filename, 'rb')
        while True:  # 发送文件
            filedata = fp.read(1024)
            if not filedata:
                break
            self.client.send(filedata)
        print "sending over..."
        recvdata = self.client.recv(self.BUFFSIZE)
        print "[%s]" % time.ctime()
        print "聪明的一休说：" + recvdata
        fp.close()

    def sentmessage(self):
        print "[%s]"%time.ctime()
        self.message=raw_input('你说：')
        if(self.message.split('.')[-1]=='aiml'):
            self.sentfile()
        else:
            self.Alice_RESPOND()

    def Alice_RESPOND(self):
        self.client.send(self.message)
        recvdata = self.client.recv(self.BUFFSIZE)
        print "[%s]" % time.ctime()
        print "聪明的一休说：" + recvdata

    def sendMsgEvent(self,event):  # 发送消息事件
        if event.keysym == "Return":  # 按回车键可发送
            self.sentmessage()

    def __init__(self):
        #self.client = socket(AF_INET, SOCK_STREAM)
        #self.client.connect((self.HOST, self.PORT))
        while True:
            self.client = socket(AF_INET, SOCK_STREAM)
            try:
                self.client.connect((self.HOST, self.PORT))
                self.sentmessage()
                time.sleep(1) #sleep 1s
            except error,e:
                print "Get connect error as",e
                continue
            self.client = socket(AF_INET, SOCK_STREAM)
#####################################################################
if __name__ == "__main__":
    client = TcpClient()