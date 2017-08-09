# -*- coding: utf-8 -*-
'''
@author: xinghuazhang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: xing_hua_zhang@126.com
@software: PyCharm 2017.1.4
@file: TCPClient.py
@time: 2017/8/8 13:37
@desc:
'''
from socket import *
from Tkinter import*
from PIL import ImageTk,Image
from ScrolledText import ScrolledText
import struct
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
#####################################################################
class TcpClient:
    # HOST = 'localhost'
    PORT = 8000
    HOST = '127.0.0.1'
    BUFFSIZE = 1024
    ADDR = (HOST, PORT)

    # define the function to close GUI
    def close(self):
        self.root.destroy()

    # define the function to welcome
    def do(self):
        filewin = Toplevel(self.root)
        label = Label(filewin, text="\n \n欢迎使用聪明的一休机器人\n\n相信他能为您带来便利，期待您的反馈！\n\n", font=('隶书', 20, 'bold'), fg='red')
        label.pack()

    # define the function to describe the using methods
    def use(self):
        filewin = Toplevel(self.root)
        label = Label(filewin, text="聪明的一休机器人十分可爱，快来聊一聊吧~", font=('隶书', 15))
        label.pack()
        label = Label(filewin, text="**************************************", font=('隶书', 15), fg='red')
        label.pack()
        label = Label(filewin, text="注：聪明的一休机器人持续升级中...敬请期待", font=('宋体', 13), fg='red')
        label.pack(side=BOTTOM)

    # define the function to describe about author
    def about(self):
        filewin = Toplevel(self.root)
        label = Label(filewin, text="\n \n聪明的一休机器人\n\n作者：***\n\nQQ:6666666666\n\n", font=('隶书', 20, 'bold'))
        label.pack()

    #Demo tk root
    def GUI_Demo(self):
        self.root = Tk()
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="欢迎使用", command=self.do, font=('隶书', 10, 'bold'))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="退出", command=self.close, font=('隶书', 10, 'bold'))
        self.menubar.add_cascade(label="开始", menu=self.filemenu)
        self.filemenu1 = Menu(self.menubar, tearoff=0)
        self.filemenu1.add_command(label="使用说明", command=self.use, font=('隶书', 10, 'bold'))
        self.filemenu1.add_separator()
        self.filemenu1.add_command(label="关于作者", command=self.about, font=('隶书', 10, 'bold'))
        self.menubar.add_cascade(label="帮助", menu=self.filemenu1)
        self.root.config(menu=self.menubar)
        self.root.geometry()
        self.root.maxsize(500, 400)
        self.root.minsize(500, 400)
        self.root.title("聪明的一休哥")
        self.frame = Frame(self.root)
        self.frame.pack(side=BOTTOM)
        self.image2 = Image.open('D:\Python2.7\Lib\site-packages\PIL\picture.jpg')
        self.background_image = ImageTk.PhotoImage(self.image2)
        self.textlabel = Label(self.root, image=self.background_image)
        self.textlabel.pack(side=LEFT)
        self.scrolledtext = ScrolledText(self.root, width=35, height=20, font=('隶书', 12, 'bold'), fg='blue')
        self.scrolledtext.insert(END, "Hello，我是一休哥，能为您做点什么呢？" + "\n")
        self.E = Entry(self.frame, bd=5, font='隶书', fg='blue', width=15)
        self.E.grid(row=3, column=10)
        self.button = Button(self.frame, text="发送", activebackground='yellow', width=10, height=1, fg='blue', command=self.sentmessage)
        self.button.grid(row=3, column=11)
        self.E.bind("<KeyPress-Return>", self.sendMsgEvent)  # 事件绑定，定义快捷键
        self.scrolledtext.pack()
        self.root.mainloop()

    def sentfile(self):
        filename = self.E.get()  # 输入文件名
        self.E.delete(0, END)
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
        self.scrolledtext.insert(END, "聪明的一休说：" + recvdata + "\n")
        fp.close()

    def sentmessage(self):
        if(self.E.get().split('.')[-1]=='aiml'):
            self.scrolledtext.insert(END, "你说：我发送了文件" + self.E.get() + "\n")  # create listbox to insert new element
            self.sentfile()
        else:
            self.scrolledtext.insert(END, "你说：" + self.E.get() + "\n")  # create listbox to insert new element
            print self.E.get()
            str = self.E.get()
            self.E.delete(0, END)
            self.Alice_RESPOND(str)

    def Alice_RESPOND(self,str):
        self.client.send(str)
        recvdata = self.client.recv(self.BUFFSIZE)
        self.scrolledtext.insert(END, "聪明的一休说：" + recvdata + "\n")

    def sendMsgEvent(self,event):  # 发送消息事件
        if event.keysym == "Return":  # 按回车键可发送
            self.sentmessage()

    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))
        self.GUI_Demo()
#####################################################################
if __name__ == "__main__":
    client = TcpClient()