#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#  @author:  peng tao
# 
#    Mar 14, 2018 14:53:45 PM

from tkinter import*
from tkinter import filedialog as fdialog
from tkinter.dialog import*
from tkinter.messagebox import*
import tkinter.ttk as ttk
py3 = 1
import Image_support

import testImg

def save_file():
    pass
    '''
    file=fdialog.asksaveasfile(mode="wb", title="Save Figure", defaultextension=".png", filetypes = (("png files","*.png"),("all files","*.*")))
    if file is None:
        return None
    img_to_save=open(".temp/generated_plot.png","rb").read()
    file.write(img_to_save)
    file.close()
    '''
def showAbout():
        showinfo("face detect version 1.0","quit key: 'q','Esc'\n directiong key:'2''4''6''8'\n delete key :'d'\n save key:'s'\n data: 2018/3/20 \n, other maybe call me 110114112")


class Menubar:
    def __init__(self, master):       
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Save", command=save_file)
        filemenu.add_command(label="Quit", command=root.destroy)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About facedetect",command= showAbout)
        menubar.add_cascade(label="Help", menu=helpmenu)
        root.config(menu=menubar)

def destroy_app():
    global root
    root.destroy()
    exit(0)
# global colors variables for theme switch
_activebgcolordark = '#808080'
_bgcolorlight = '#ffffff'
_fgcolorlight = '#000000'
_lightwindowbackground = '#f2f2f2'

faceImagePath = 'V:\\pt_data\\test'#"C:/Users/Public/Pictures/Sample Pictures"  'V:\\NIR_ALL'# #"V:/NIR_7440/ALL2" #
outTxtPath = 'H:\\facedetection\\python\\faceImageManage\\pic'  #'V:/NIR_ALL_480x572labeltxt/sevenDot'
selectMethod = 4
nwidth = 480
nheight = 572

class New_Toplevel_1:
    def __init__(self, top=None):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""
        top.geometry("640x660+408+185")#("555x398+408+185")  x  y 
        top.title("FaceImageManage 572x480")
        self.showImagef= None
        self.file_path = faceImagePath
        root.configure(background=_lightwindowbackground)
        self.flagfix = 0
        self.Label1 = Label(top)
        self.Label1.place(x=4, y=580, height=18, width=60)
        self.Label1.configure(text='facePath:')
        self.Label1.configure(fg=_fgcolorlight)
        self.Label1.configure(background=_lightwindowbackground)
        self.methodNum = 1
        self.getpath = Entry(top)
        self.getpath.place(x=70, y=580, height=20, width=400)
        self.getpath.configure(background=_bgcolorlight)
        self.getpath.configure(font="TkFixedFont")
        #self.getpath.configure(width=100)
        self.getpath.insert(0, self.file_path)
        self.getpath.configure(fg=_fgcolorlight)
        
        self.file_outpath = outTxtPath
        self.Label2 = Label(top)
        self.Label2.place(x=4, y=618, height=18, width=60)
        self.Label2.configure(text='outPath:')
        self.Label2.configure(fg=_fgcolorlight)
        self.Label2.configure(background=_lightwindowbackground)

        self.getoutpath = Entry(top)
        self.getoutpath.place(x=70, y=618, height=20, width=400)
        self.getoutpath.configure(background=_bgcolorlight)
        self.getoutpath.configure(font="TkFixedFont")
        #self.getoutpath.configure(width=100)
        self.getoutpath.insert(0, self.file_outpath)
        self.getoutpath.configure(fg=_fgcolorlight)

        self.selectMethod = selectMethod
        self.Label3 = Label(top)
        self.Label3.place(x=490, y=20, height=20, width=130)
        self.Label3.configure(text='method:(m:1,d:2,all:3,t:4)')
        self.Label3.configure(fg=_fgcolorlight)
        self.Label3.configure(background=_lightwindowbackground)

        self.getmethod = Entry(top)
        self.getmethod.place(x=490, y=40, height=20, width=130)
        self.getmethod.configure(background=_bgcolorlight)
        self.getmethod.configure(font="TkFixedFont")
       # self.getmethod.configure(width=100)
        self.getmethod.insert(0, self.selectMethod)
        self.getmethod.configure(fg=_fgcolorlight)

        self.stepnumf = 1
        self.Label4 = Label(top)
        self.Label4.place(relx=0.76, rely=0.35, height=20, width=60)
        self.Label4.configure(text='stepnum:')
        self.Label4.configure(fg=_fgcolorlight)
        self.Label4.configure(background=_lightwindowbackground)      
        
        self.stepnum = Entry(top)
        self.stepnum.place(relx=0.86, rely=0.35, height=30, width=50)
        self.stepnum.configure(background=_bgcolorlight)
        self.stepnum.configure(font="TkFixedFont")
       # self.stepnum.configure(width=100)
        self.stepnum.insert(0, self.stepnumf)
        self.stepnum.configure(fg=_fgcolorlight)
        
        self.threadlight = 20
        self.Label5 = Label(top)
        self.Label5.place(relx=0.76, rely=0.40, height=20, width=60)
        self.Label5.configure(text='threadlight:')
        self.Label5.configure(fg=_fgcolorlight)
        self.Label5.configure(background=_lightwindowbackground)

        self.exlight = Entry(top)
        self.exlight.place(relx=0.86, rely=0.40, height=30, width=50)
        self.exlight.configure(background=_bgcolorlight)
        self.exlight.configure(font="TkFixedFont")
       # self.exlight.configure(width=100)
        self.exlight.insert(0, self.threadlight)
        self.exlight.configure(fg=_fgcolorlight)

        self.Canvas1 = Canvas(top)
        #self.Canvas1.place(relx=0.005, rely=0, relheight=1, relwidth=0.75)
        self.Canvas1.place(x=2, y=1, height=nheight, width=nwidth)   #
        self.Canvas1.configure(background=_bgcolorlight)
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(relief=RIDGE)
        self.Canvas1.configure(selectbackground="#c4c4c4")
        #self.Canvas1.configure(width=480)      
        #self.showImagef = Image_support.PictureWindow(self.Canvas1, self.getpath.get(),self.getoutpath.get(),int(self.getmethod.get()),nwidth,nheight)
        
        self.Canvas1.bind('<Configure>',lambda x: Image_support.Plot(1,self.Canvas1, self.file_path,3) )

        self.next = Button(top)
        self.next.place(relx=0.76, rely=0.8, height=50, width=70)
        self.next.configure(activebackground=_activebgcolordark)
        self.next.configure(command=lambda: self.detectDot(1))
        self.next.configure(cursor="left_ptr")
        self.next.configure(text='next')
        #self.next.configure(width=47)
        self.next.configure(background=_bgcolorlight)
        self.next.configure(fg=_fgcolorlight)
        
        self.bt_fix = Button(top)
        self.bt_fix.place(relx=0.76, rely=0.65, height=40, width=60)
        self.bt_fix.configure(activebackground=_activebgcolordark)
        self.bt_fix.configure(command=lambda: self.detectDot(2))
        #self.bt_fix.configure(background=_bgcolorlight)
        self.bt_fix.configure(cursor="left_ptr")
        self.bt_fix.configure(text='fix')
        self.bt_fix.configure(background=_bgcolorlight)
        self.bt_fix.configure(fg=_fgcolorlight)

        self.bt_test = Button(top)
        self.bt_test.place(relx=0.88, rely=0.14, height=30, width=50)
        self.bt_test.configure(activebackground=_activebgcolordark)
        self.bt_test.configure(command=lambda: self.testshowpic())
        #self.bt_fix.configure(background=_bgcolorlight)
        self.bt_test.configure(cursor="left_ptr")
        self.bt_test.configure(text='test')
        self.bt_test.configure(background=_bgcolorlight)
        self.bt_test.configure(fg=_fgcolorlight)

        self.bt_skip = Button(top)
        self.bt_skip.place(relx=0.76, rely=0.55, height=40, width=60)
        self.bt_skip.configure(activebackground=_activebgcolordark)
        self.bt_skip.configure(command=lambda: self.skipPic())
        #self.bt_skip.configure(background=_bgcolorlight)
        self.bt_skip.configure(cursor="left_ptr")
        self.bt_skip.configure(text='skip')
        self.bt_skip.configure(background=_bgcolorlight)
        self.bt_skip.configure(fg=_fgcolorlight)

        self.bt_start = Button(top)
        self.bt_start.place(relx=0.76, rely=0.14, height=30, width=50)
        self.bt_start.configure(activebackground=_activebgcolordark)
        self.bt_start.configure(command=lambda: self.startDetection())
        #self.bt_fix.configure(background=_bgcolorlight)
        self.bt_start.configure(cursor="left_ptr")
        self.bt_start.configure(text='start')
        self.bt_start.configure(background=_bgcolorlight)
        self.bt_start.configure(fg=_fgcolorlight)

        self.bt_close = Button(top)
        self.bt_close.place(relx=0.76, rely=0.24, height=30, width=50)
        self.bt_close.configure(activebackground=_activebgcolordark)
        self.bt_close.configure(command=lambda: self.closetxt())
        #self.bt_fix.configure(background=_bgcolorlight)
        self.bt_close.configure(cursor="left_ptr")
        self.bt_close.configure(text='save')
        self.bt_close.configure(background=_bgcolorlight)
        self.bt_close.configure(fg=_fgcolorlight)
    
    def closetxt(self):
        if(self.showImagef==None):
            return
        self.showImagef.closeOpentxt()

    def startDetection(self):
        if(self.showImagef==None):
            self.flagfix = 0
            self.methodNum = int(self.getmethod.get())
            Image_support.Plot(1,self.Canvas1, self.file_path,1)
            self.showImagef = Image_support.PictureWindow(self.Canvas1, self.getpath.get(),self.getoutpath.get(),int(self.getmethod.get()),nwidth,nheight)
        else:
            if  self.methodNum !=  int(self.getmethod.get()):
                self.methodNum =  int(self.getmethod.get())
                self.showImagef.setdmethod(int(self.getmethod.get()))
                Image_support.Plot(1,self.Canvas1, self.file_path,5)
            else:
                Image_support.Plot(1,self.Canvas1, self.file_path,1)
            
            #del self.showImagef
            #self.showImagef= None
    def detectDot(self,method):
        if self.showImagef ==None:
            return
        if method == 1 :
            self.flagfix = 1
            self.methodNum = int(self.getmethod.get())
            num = int(self.stepnum.get())
            if num<1:
                num = 1
            if self.methodNum ==4:
                numlight = int(self.exlight.get())
                self.flagfix = 1
                self.showImagef.next_image(num,numlight)
            else:
                self.showImagef.next_image(num,255)
        elif method == 2 and self.flagfix ==1:
            num = int(self.stepnum.get())
            if self.methodNum != 4:
                self.showImagef.fix_image()
            
    def skipPic(self):
        if self.showImagef ==None:
            return
        num = int(self.stepnum.get())
        if num<1:
            num = 1
        self.showImagef.skip_pic(num)

    def testshowpic(self):
        testShow = testImg.testShowImg(self.getoutpath.get(),nwidth,nheight) 
        testShow.searchFile()
        testShow.whileFile()
        del testShow

    @staticmethod
    def popup1(event):
        Popupmenu1 = Menu(root, tearoff=0)
        Popupmenu1.configure(activebackground="#f9f9f9")
        Popupmenu1.post(event.x_root, event.y_root)

def Manage_main():
    """ inter the main routine"""
    global  root
    root=Tk()
    #root.state("zoomed")
    root.resizable(width=False, height=False)
    top = New_Toplevel_1(root)
    m = Menubar(root)
    root.protocol('WM_DELETE_WINDOW', destroy_app)
    root.mainloop()


if __name__ == "__main__":
    Manage_main()
