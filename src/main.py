import customtkinter as ctk
from widgets import *
from tkinter import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry("1000x600")
        self.title("Text Editor")
        
        menu_func(self)
        Widgets(self)

        self.mainloop()

App()
