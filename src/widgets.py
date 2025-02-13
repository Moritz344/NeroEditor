import customtkinter as ctk
from tkinter import *
import tkinter as tk
from tkinter import filedialog

class Widgets(ctk.CTkFrame):
    def __init__(self,window,):
        super().__init__(master=window,)


        self.create_textbox(window)

    def update_size(self):
        self.font_size += 1

            

    def create_textbox(self,window):
        self.font_size = 30
        self.textbox = ctk.CTkTextbox(window,width=1000,height=600,font=("opensans",self.font_size))
        self.textbox.place(x=0,y=0)


def menu_func(master):
        def open_file():
            path = filedialog.askopenfile().name
            print(path)
            print("Open File!")
        def save_file():
            print("Saved File!")


        menu = Menu(master)
        master.config(menu=menu)

        fileMenu = Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)

        fileMenu.add_command(label="Open",command=open_file )
        fileMenu.add_command(label="Save",command=save_file )


