import customtkinter as ctk
import CTkMessagebox
from widgets import *
from tkinter import *
from settings import project_name
from start_screen import StartScreen 
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry("1000x600")
        self.minsize(1000,600)
        self.title(project_name)
        arrow = "@Normal.cur"
        self.configure(cursor=arrow,)

        w = Widgets(self)

        def on_closing():
            if not w.saving:
                msg = CTkMessagebox.CTkMessagebox(
                self,
                icon="warning",
                title="Exit",
                option_1="No",
                option_2="Yes",
                text_color="white",
                message="Are you sure you saved your file?",
                font=("opensans",20),
                        )
                response = msg.get()
                if response == "Yes":
                    self.destroy()
            else:
                self.destroy()



        self.protocol("WM_DELETE_WINDOW",on_closing)

        self.mainloop()


StartScreen() # wird auskommentiert für debug zwecken
App()


