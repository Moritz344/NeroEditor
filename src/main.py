import customtkinter as ctk
from widgets import *
from tkinter import *
from settings import project_name

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("system")
        self.geometry("1000x600")
        self.minsize(1000,600)
        self.title(project_name)



        def on_closing():
            if messagebox.askyesno("Exit","Are you sure you saved your file?"):
                self.destroy()

        self.protocol("WM_DELETE_WINDOW",on_closing)

        
        Widgets(self)

        self.mainloop()


StartScreen()
App()

