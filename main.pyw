#!/usr/bin/python
# -*- coding:utf-8 -*-
# from cgitb import text
from email.mime import image
import os
import configparser
import sys
import tkinter as tk
from PIL import Image, ImageTk
import math
import win32api
cofing = configparser.ConfigParser()
currentPath = os.path.split(os.path.realpath(sys.argv[0].encode('utf-8')))[0]
cofingPath = os.path.join(currentPath,b'config.ini')
cofing.read(cofingPath,'utf-8')
appList = eval(cofing.get('setting','app_list'))
colNum = int(cofing.get('setting','col_num'))
root = tk.Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
rootWidth = colNum*100+100
rootHeight = math.ceil(len(appList)/colNum)*100+200
posX = round((screenWidth-rootWidth)/2)
posY =  round((screenHeight-rootHeight)/2)
root.title('打开app')
root.geometry(str(rootWidth)+"x"+str(rootHeight)+"+"+str(posX)+"+"+str(posY))
# root.geometry("800x400+880+400")
appFrm = tk.Frame(root)
appFrm.pack()
imageList = []
checkboxFlagList = []
def openApp():
    for i in range(len(appList)):
        appPath = appList[i]['path'].replace('\\','/')
        if checkboxFlagList[i].get()>0:
            # os.startfile('"'+appPath+'"')
            win32api.ShellExecute(0, 'open',appPath, '','',0)
    sys.exit()
def changeCheckboxFlag(index):
    checkboxFlagList[index].set(not checkboxFlagList[index].get())

def printKey(event):
    if event.char == '\r':
        openApp()
    if event.char == '\x1b':
        root.destroy()
def main():
    curRow = 0
    curCol = 0
    for i in range(len(appList)):
        appDesc = appList[i]['desc']
        appImage = appList[i]['image']
        appItemFrm = tk.Frame(appFrm)
        appItemFrm.grid(row=curRow,column=curCol)
        if curCol == colNum-1 :
            curRow = curRow + 1
            curCol = 0
        else:
            curCol = curCol + 1
        if appImage.find('openAppLogo')>=0:
            appImage = os.path.join(currentPath,appImage.encode('utf-8'))
        imageList.append(ImageTk.PhotoImage(Image.open(appImage)))
        tk.Button(appItemFrm,width=100,height=100, image=imageList[i],command=lambda i=i:changeCheckboxFlag(i)).pack()
        tk.Label(appItemFrm, text=appDesc).pack()
        checkboxFlagList.append(tk.BooleanVar())
        checkboxFlagList[i].set(appList[i]['default'])
        tk.Checkbutton(appItemFrm, variable=checkboxFlagList[i]).pack()
    confirmFrm = tk.Frame(root)
    confirmFrm.pack()
    tk.Button(confirmFrm, text="确定",command=openApp).pack(side='left')
    tk.Button(confirmFrm, text="取消",command=root.destroy).pack(side='left')
    keypress = tk.Frame(root)
    keypress.focus_set()
    keypress.bind('<Key>',printKey)
    keypress.pack()
    root.mainloop()

main()