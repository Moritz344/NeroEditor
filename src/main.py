import customtkinter as ctk
import CTkMessagebox
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
            msg = CTkMessagebox.CTkMessagebox(
            self,
            icon="warning",
            title="Exit",
            option_1="No",
            option_2="Yes",
            text_color="white",
            message="Are you sure you saved your file?",
            fade_in_duration=0.5,
            font=(font,20),
                    )
            response = msg.get()
            if response == "Yes":
                self.destroy()


        self.protocol("WM_DELETE_WINDOW",on_closing)

        Widgets(self)
        

        self.mainloop()


StartScreen()
App()


