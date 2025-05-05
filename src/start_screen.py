from settings import project_name
import customtkinter as ctk
from CTkToolTip import *
import sys
from PIL import Image

class StartScreen(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.geometry("800x600")
        self.title(project_name)
        self.maxsize(800,600)
        self.minsize(800,600)
        ctk.set_appearance_mode("dark")
        
        self.configure(cursor="@Normal.cur")

        def start_app():
            self.destroy()



        button_frame = ctk.CTkFrame(self,width=800,height=420,fg_color="#222222",)
        button_frame.place(x=0,y=180)

        header_frame = ctk.CTkFrame(self,width=800,height=200,corner_radius=0,fg_color="#222222")

        start_btn = ctk.CTkButton(
        master=button_frame,
        text="Start",
        width=200,
        height=50,
        font=("opensans",50),
        command=start_app,

        )


        start_btn.place(x=280,y=130)

        quit_btn = ctk.CTkButton(
        button_frame,
        width=200,
        text="Quit",
        font=("opensans",50),
        command=lambda: sys.exit() 
        )

        quit_btn.place(x=280,y=210)
        try:
            self.github_icon = ctk.CTkImage(light_image=Image.open("assets/github_icon.png"),size=(50,50))
            self.github_btn = ctk.CTkButton(self,text="",image=self.github_icon,fg_color="#212121",
            width=50,height=20,
            hover_color="#212121")
            self.github_btn.place(x=0,y=540)
            CTkToolTip(self.github_btn,delay=0.3,message="github.com/Moritz344")
        except Exception as e:
            print("I was not able to load this image",e)


        header_frame.place(x=0,y=0)
        header = ctk.CTkLabel(
        header_frame,
        text="Welcome",
        width=300,
        height=100,
        font=("Segoe UI Light",100),
        corner_radius=10
        )
        header.place(x=180,y=50)

        self.protocol("WM_DELETE_WINDOW",lambda: sys.exit())


        self.mainloop()
