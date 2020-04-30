# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 10:31:25 2020

@author: georg
"""


from tkinter import *
import Assignment_1 as my_script
#import Assignment1_reduced_file.py as red

def funcion_prueba(f1, f2):
    #my_script.execute_my_script('MicroGridTestConfiguration_T1_BE_EQ_V2.xml', 'MicroGridTestConfiguration_T1_BE_SSH_V2.xml')                 
    my_script.execute_my_script(f1, f2)       

'''
window=Tk()
btn=Button(window, text="This is Button widget", fg='blue', command=funcion_prueba)
btn.place(x=80, y=100)
#btn.bind(window, text='Prueba', )
window.title('Hello Python')
window.geometry("300x200+10+10")
window.mainloop()
'''

class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='First file')
        self.lbl2=Label(win, text='Second file')
        #self.lbl3=Label(win, text='Result')
        self.t1=Entry(bd=3)
        self.t2=Entry()
        #self.t3=Entry()
        self.btn1 = Button(win, text='Execute_')
        #self.btn2=Button(win, text='Subtract')
        self.lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        self.lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=100)
        self.b1=Button(win, text='Execute', command=self.add)
        #self.b2=Button(win, text='Subtract')
        #self.b2.bind('<Button-1>', self.sub)
        self.b1.place(x=100, y=150)
        #self.b2.place(x=200, y=150)
        #self.lbl3.place(x=100, y=200)
        #self.t3.place(x=200, y=200)
    def add(self):
        #self.t3.delete(0, 'end')
        num1=str(self.t1.get())
        num2=str(self.t2.get())
        funcion_prueba(num1, num2)
        #self.t3.insert(END, str(result))


window=Tk()
mywin=MyWindow(window)
window.title('Hello Python')
window.geometry("400x300+10+10")
window.mainloop()