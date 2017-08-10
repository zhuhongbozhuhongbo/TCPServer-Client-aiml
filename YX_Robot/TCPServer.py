# -*- coding: utf-8 -*-
'''
@author: xinghuazhang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: xing_hua_zhang@126.com
@software: PyCharm 2017.1.4
@file: TCPServer.py
@time: 2017/8/8 13:35
@desc:
'''
from socket import *
from time import ctime
import sys
import aiml
import struct
import os
import threading
reload(sys)
sys.setdefaultencoding('utf-8')
#####################################################################
os.chdir("D:\Robot") #打开aiml库
kernel = aiml.Kernel()
# if os.path.isfile("bot_brain.brn"):
#     kernel.bootstrap(brainFile = "bot_brain.brn")
# else:
#     kernel.bootstrap(learnFiles = "std-startup.xml", commands = "HELLO AIML")
#     kernel.saveBrain("bot_brain.brn")
kernel.learn("StartUp.xml")
kernel.respond("LOAD AIML B")
#####################################################################
def function(tcpclient, addr):
    FILEINFO_SIZE = struct.calcsize('128sI')
    #定义文件信息（包含文件名和文件大小）大小。128s代表128个char[]（文件名），I代表一个integer or long（文件大小）
    while True:
        try:
            fhead = tcpclient.recv(FILEINFO_SIZE)
            if not fhead:
                print "the socket partner maybe closed"
                tcpclient.close()
                break
            if "aiml" not in fhead.split('.')[-1]:
                tcpclient.send(kernel.respond(fhead).encode('utf-8'))
            else:
                filename, filesize = struct.unpack('128sI', fhead)
                #把接收到的数据库进行解包，按照打包规则128sI
                print "address is: ",addr
                print filename,len(filename),type(filename)
                print filesize
                filename = 'New_'+filename.strip('\00')   #命名新文件new_传送的文件
                fp = open(filename,'wb')     #新建文件，并且准备写入
                restsize = filesize
                print "recving..."
                while True:
                    if restsize > 1024:      #如果剩余数据包大于1024，就去1024的数据包
                        filedata = tcpclient.recv(1024)
                    else:
                        filedata = tcpclient.recv(restsize)
                        fp.write(filedata)
                        break
                    if not filedata:
                        break
                    fp.write(filedata)
                    filesize -= len(filedata)
                    restsize = filesize      #计算剩余数据包大小
                    if restsize <= 0:
                        break
                fp.close()
                print "recv succeeded !!File named:",filename
                kernel.learn(filename) #学习新aiml文件
                tcpclient.send("文件上传成功！".encode('utf-8'))
        except:
            print "the socket partner maybe closed"
            tcpclient.close()
            break
#####################################################################
HOST = '127.0.0.1'
PORT = 8000
BUFFERSIZE = 1024
ADDRESS = (HOST, PORT)
localIP = gethostbyname(gethostname()) #得到本地ip
print "local ip:%s "%localIP
s = socket(AF_INET, SOCK_STREAM)
s.bind(ADDRESS)
s.listen(10) #监听10个客户端client
#####################################################################
while True:
    print 'Waiting for clients cennect......'
    tcpclient, addr = s.accept()
    print 'Connected By ', addr
    tmpThread = threading.Thread(target=function, args=(tcpclient, addr))  # 如果接收到文件，创建线程
    tmpThread.start()     #执行线程
print 'TCPServer end'
