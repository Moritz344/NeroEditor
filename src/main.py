import customtkinter as ctk
from widgets import *
from tkinter import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("system")
        self.geometry("1000x600")
        self.minsize(1000,600)
        self.title("NoteEditor")


        def on_closing():
            if messagebox.askyesno("Exit","WAIT!!! ARE YOU SURE YOU SAVED YOUR FILE??? (calmly)"):
                self.destroy()

        self.protocol("WM_DELETE_WINDOW",on_closing)
        
        Widgets(self)

        self.mainloop()


StartScreen()
App()

