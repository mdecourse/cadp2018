from tkinter import *
import serial
import sys
import numpy as np
from matplotlib import pyplot, rcParams
import vrep
import math



class printer(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        


        Label(pri, text="Axis").grid(column=0, row=0)
        Label(pri, text="").grid(column=0, row=1)
        Label(pri, text="X").grid(column=0, row=2)
        Label(pri, text="").grid(column=0, row=3)
        Label(pri, text="Y").grid(column=0, row=4)
        Label(pri, text="").grid(column=0, row=5)
        Label(pri, text="Z").grid(column=0, row=6)

        Label(pri, text="Position").grid(column=1, row=0)
        Label(pri, text="-125<=X<=125").grid(column=1, row=1)
        Label(pri, text="-125<=Y<=125").grid(column=1, row=3)
        Label(pri, text="0<=Z<=400").grid(column=1, row=5)

        a = Entry(pri, width=12, justify=RIGHT)
        b = Entry(pri, width=12, justify=RIGHT)
        c = Entry(pri, width=12, justify=RIGHT)
                #x.delete(0,END)
                #y.delete(0,END)
        a.grid(row=2, column=1)
        b.grid(row=4, column=1)
        c.grid(row=6, column=1)


        def show_entry_fields():

            deg = math.pi/180

            x = a.get()
            y = b.get()
            z = c.get()

            if x =='' or y==''or z =='':
                x = 0
                y = 0
                z = 0
                print("Error")
            
            else:
                x = float(a.get())
                y = float(b.get())
                z = float(c.get())


                if float(x) >= 125:
                    x = 125
                    print("X_axis is out of range")
                if float(y) >= 125:
                    y = 125
                    print("Y_axis is out of range")
                if float(z) >= 400:
                    z = 400     
                    print("Z_axis is out of range")
                if float(x) <= -125:
                    x = -125
                    print("X_axis is out of range")
                if float(y) <= -125:
                    y = -125
                    print("Y_axis is out of range")
                if float(z) < 0:
                    z = 0
                    print("Z_axis is out of range")

                if (float(x) <= -125*math.sin(30*deg)) & (float(y) >= 125*math.cos(30*deg)):
                    x = -125*math.sin(30*deg)
                    y = 125*math.cos(30*deg)

                if (float(x) <= -125*math.sin(30*deg)) & (float(y) <= -125*math.cos(30*deg)):
                    x = -125*math.sin(30*deg)
                    y = -125*math.cos(30*deg)

                if (float(x) >= 125*math.sin(30*deg)) & (float(y) >= 125*math.cos(30*deg)):
                    x = 125*math.sin(30*deg)
                    y = 125*math.cos(30*deg)

                if (float(x) >= -125*math.sin(30*deg)) & (float(y) <= -125*math.cos(30*deg)):
                    x = 125*math.sin(30*deg)
                    y = -125*math.cos(30*deg)


                e=x/1000
                r=y/1000
                t=z/889
                if t <= 0.11656:
                    t = t+0.11656


                vrep.simxFinish(-1)
                clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
                if clientID!= -1:
                    print("Connected to remote server")
                else:
                    print('Connection not successful')
                    sys.exit('Could not connect')
                errorCode,plate=vrep.simxGetObjectHandle(clientID,'plate',vrep.simx_opmode_oneshot_wait)
                if errorCode == -1:
                    print('Can not find left or right motor')
                    sys.exit()                
                errorCode=vrep.simxSetObjectPosition(clientID,plate,-1,[e,r,t], vrep.simx_opmode_oneshot)
                print(x,y,z)


                #print("%s,%s,%s" % (x, y, z))


        Button(pri, text='Quit', width=5, command=pri.quit).grid(row=8, column=2, sticky=W, pady=4)
        Button(pri, text='Go', width=5, command=show_entry_fields).grid(row=8, column=0, sticky=W, pady=4)



if __name__ == '__main__':
    pri = Tk()
    pri.title("Printer")
    pri.geometry('180x220');  #設定視窗大小
    pri.resizable(0, 0) #鎖定視窗大小
    app = printer(master=pri)

    app.mainloop()


