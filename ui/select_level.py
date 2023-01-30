#!/usr/bin/python3
import rclpy
from rclpy.node import Node
import tkinter as tk
from tkinter import *
import sys

NUM_TRAY = 3
NUM_TABLE = 8
TABLE_ID = [None]



for i in range(1,NUM_TABLE+1):
    TABLE_ID.append(str(i))
TRAY1,TRAY2,TRAY3 = TABLE_ID.copy(),TABLE_ID.copy(),TABLE_ID.copy()



class GUI(Node):
    def __init__(self):
        super().__init__('gui')
        screen_width = 500
        screen_height = 600
        self.w = screen_width
        self.h = screen_height
        self.root = Tk()
        self.root.title('Select your Table')
        self.TFont = ("Times New Roman", 15)
        self.root.geometry(str(screen_width)+'x'+str(screen_height))
        self.root.eval('tk::PlaceWindow . center')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing) # To Immediately close program
        self.info("Tray's floor",self.w /10,self.h/12)
        self.info("Table Id",self.w /1.6,self.h/12)

        self.variable1 = StringVar(self.root)
        self.variable1.set(TRAY1[0]) 
        self.variable2 = StringVar(self.root)
        self.variable2.set(TRAY2[0]) 
        self.variable3 = StringVar(self.root)
        self.variable3.set(TRAY3[0]) 

        self.data = [0,0,0]

        for i in range(1,NUM_TRAY+1):
            self.info(str(i),self.w /5,self.h/12 + i*60)

       
        self.timer_period = 300
        self.update()
        # self.root.mainloop()
    
    def on_closing(self):
        self.root.destroy()
        sys.exit()
    def info(self,text,posx,posy):
        Label(text =str(text)).place(x=posx,y=posy) 

    def update(self):

        OptionMenu(self.root, self.variable1, *TRAY1).place(x=self.w/1.6,y=self.h/12 + 1*60-10)
        OptionMenu(self.root, self.variable2, *TRAY2).place(x=self.w/1.6,y=self.h/12 + 2*60-10)
        OptionMenu(self.root, self.variable3, *TRAY3).place(x=self.w/1.6,y=self.h/12 + 3*60-10)
        self.root.after(self.timer_period,self.update)

        if self.variable1.get()!='None' :
            self.data[0] = int(self.variable1.get())
            try:
                TRAY2.remove(self.variable1.get())
            except:
                pass
            try:
                TRAY3.remove(self.variable1.get()) 
            except:
                pass
        if self.variable2.get()!='None' :
            self.data[1] = int(self.variable2.get())
            try:
                TRAY1.remove(self.variable2.get())
            except:
                pass
            try:
                TRAY3.remove(self.variable2.get()) 
            except:
                pass
        if self.variable3.get()!='None' :
            self.data[2] = int(self.variable3.get())
            try:
                TRAY1.remove(self.variable3.get())
            except:
                pass
            try:
                TRAY2.remove(self.variable3.get()) 
            except:
                pass

        if self.data[0]!=0 and self.data[1]!=0 and self.data[2]!=0:
            print(self.data)
        

def main(args=None):
    rclpy.init(args=args)
    gui = GUI()
    gui.root.mainloop()
    rclpy.spin(gui)


if __name__ == '__main__':

    main()