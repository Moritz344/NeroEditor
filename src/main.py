import customtkinter as ctk
from widgets import *
from tkinter import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("system")
        self.geometry("1000x600")
        self.minsize(1000,600)
        self.title("Text Editor")
        
        Widgets(self)

        self.mainloop()


StartScreen()
App()

