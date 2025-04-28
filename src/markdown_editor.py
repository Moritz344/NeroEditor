import markdown
import webview
import customtkinter as ctk
import tkinter as tk
from settings import *
import threading
from tkinterweb import HtmlFrame

class MarkdownViewerApp(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        root.geometry("800x600")
        root.title("Markdown Editor")
        
        # Markdown file
        self.textbox_1 = ctk.CTkTextbox(root,width=1000,height=900,border_width=1,
        border_color="white",corner_radius=0,wrap="word",font=("opensans",standard_font_size))
        self.textbox_1.pack(side="left",anchor="sw",)
        # --


        convert = ctk.CTkButton(root,text="preview",command=lambda: self.preview(root))
        convert.place(x=0,y=0)
        html = "<br>"
        
        # converted box
        self.textbox_2 = ctk.CTkTextbox(root,width=1000,height=900,border_width=1,
        border_color="white",wrap="char",corner_radius=0,font=("opensans",standard_font_size))
        
        self.html_frame = None

    
    def preview(self,window):
        text_input = self.textbox_1.get("0.0","end-1c")
        
        full_text = text_input.replace("\n\n", "\n<br>\n")
        
        html = markdown.markdown(full_text)
        
        if not self.html_frame:
            self.html_frame = HtmlFrame(window,width=800,height=1000,messages_enabled=True)
            self.html_frame.pack(side="top",fill="both",padx=10,pady=0,expand=True)
        else:
            self.html_frame.load_html(html)



