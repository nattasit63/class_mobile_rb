#!/usr/bin/python3
import rclpy
from rclpy.node import Node
import tkinter as tk
from tkinter import *
import sys
from std_msgs.msg import Int8MultiArray

NUM_TRAY = 3 *2
NUM_TABLE = 8
TABLE_ID = [None]



for i in range(1,NUM_TABLE+1):
    TABLE_ID.append(str(i))
TRAY1,TRAY2,TRAY3,TRAY4,TRAY5,TRAY6 = TABLE_ID.copy(),TABLE_ID.copy(),TABLE_ID.copy(),TABLE_ID.copy(),TABLE_ID.copy(),TABLE_ID.copy()



class GUI(Node):
    def __init__(self):
        super().__init__('gui')
        self.gui_plublisher = self.create_publisher(Int8MultiArray,'gui/table_list',10)
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
        self.info("Robot ID : 1",self.w /10-30,self.h/12-30)
        self.info("Tray's floor",self.w /10,self.h/12)
        self.info("Table Id",self.w /1.6,self.h/12)

        self.variable1 = StringVar(self.root)
        self.variable1.set(TRAY1[0]) 
        self.variable2 = StringVar(self.root)
        self.variable2.set(TRAY2[0]) 
        self.variable3 = StringVar(self.root)
        self.variable3.set(TRAY3[0]) 

        self.info("Robot ID : 2",self.w /10-30,self.h/12+250)
        self.info("Tray's floor",self.w /10,self.h/12+250+30)
        self.info("Table Id",self.w /1.6,self.h/12+250+30)

        self.variable4 = StringVar(self.root)
        self.variable4.set(TRAY4[0]) 
        self.variable5 = StringVar(self.root)
        self.variable5.set(TRAY5[0]) 
        self.variable6 = StringVar(self.root)
        self.variable6.set(TRAY6[0]) 

        self.data = [0,0,0,0,0,0]

        for i in range(1,NUM_TRAY-2):
            self.info(str(i),self.w /5,self.h/12 + i*60)
        for i in range(4,NUM_TRAY+1):
            self.info(str(i),self.w /5,self.h/12 + i*60+100)

        self.enter_button=tk.Button(self.root, text="Enter", command=self.handle_enter).place(x=200,y=550)
    
        self.timer_period = 300
        self.update()
        # self.root.mainloop()
    def handle_enter(self):
        # print('Enter : OK')
        self.gui_plublisher.publish(self.msg)
        return True
    
    def on_closing(self):
        self.root.destroy()
        sys.exit()
    def info(self,text,posx,posy):
        Label(text =str(text)).place(x=posx,y=posy) 
    def tray_list(self,tray_id,value):
        list_tray = [TRAY1,TRAY2,TRAY3,TRAY4,TRAY5,TRAY6]
        del list_tray[tray_id-1]
        for tray in list_tray:
            tray.remove(value)
    def update(self):

        OptionMenu(self.root, self.variable1, *TRAY1).place(x=self.w/1.6,y=self.h/12 + 1*60-10)
        OptionMenu(self.root, self.variable2, *TRAY2).place(x=self.w/1.6,y=self.h/12 + 2*60-10)
        OptionMenu(self.root, self.variable3, *TRAY3).place(x=self.w/1.6,y=self.h/12 + 3*60-10)
        OptionMenu(self.root, self.variable4, *TRAY4).place(x=self.w/1.6,y=self.h/12 + 4*60-10+100)
        OptionMenu(self.root, self.variable5, *TRAY5).place(x=self.w/1.6,y=self.h/12 + 5*60-10+100)
        OptionMenu(self.root, self.variable6, *TRAY6).place(x=self.w/1.6,y=self.h/12 + 6*60-10+100)
        self.root.after(self.timer_period,self.update)


        if self.variable1.get()!='None' :
            self.data[0] = int(self.variable1.get())
            try:
                self.tray_list(1,self.variable1.get())
            except:
                pass
        if self.variable2.get()!='None' :
            self.data[1] = int(self.variable2.get())
            try:
                self.tray_list(2,self.variable2.get())
            except:
                pass
        if self.variable3.get()!='None' :
            self.data[2] = int(self.variable3.get())
            try:
                self.tray_list(3,self.variable3.get())
            except:
                pass
        if self.variable4.get()!='None' :
            self.data[3] = int(self.variable4.get())
            try:
                self.tray_list(4,self.variable4.get())
            except:
                pass
        if self.variable5.get()!='None' :
            self.data[4] = int(self.variable5.get())
            try:
                self.tray_list(5,self.variable5.get())
            except:
                pass
        if self.variable6.get()!='None' :
            self.data[5] = int(self.variable6.get())
            try:
                self.tray_list(6,self.variable6.get())
            except:
                pass


        if self.data[0]!=0 and self.data[1]!=0 and self.data[2]!=0 and self.data[3]!=0 and self.data[4]!=0 and self.data[5]!=0 and self.handle_enter:
            print('Table List : ',self.data)
            self.msg = Int8MultiArray()
            self.msg.data = self.data
            
    

def main(args=None):
    rclpy.init(args=args)
    gui = GUI()
    gui.root.mainloop()
    rclpy.spin(gui)


if __name__ == '__main__':

    main()