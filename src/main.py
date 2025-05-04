import customtkinter as ctk
import CTkMessagebox
from widgets import *
from tkinter import *
from settings import *
from start_screen import StartScreen 
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry("1000x600")
        self.minsize(1000,600)
        self.configure(fg_color=colorscheme)
        w = Widgets(self)
        self.title(project_name)

        def on_closing():
            print("main:",w.saving)
            if not w.saving:
                msg = CTkMessagebox.CTkMessagebox(
                self,
                icon="warning",
                title="Exit",
                option_1="No",
                option_2="Yes",
                text_color="white",
                message="You did not save your file. Do you still want to quit?",
                font=("opensans",20),
                        )
                response = msg.get()
                if response == "Yes":
                    self.destroy()
            else:
                self.destroy()



        self.protocol("WM_DELETE_WINDOW",on_closing)

        self.mainloop()

#StartScreen() # wird auskommentiert für debug zwecken
App()


