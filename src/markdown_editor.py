import markdown
import webview
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog,simpledialog
from settings import *
import threading
from tkinterweb import HtmlFrame
from CTkMenuBar import *

class MarkdownViewerApp(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        root.geometry("800x600")
        root.title("Markdown Editor")

        # -- 

        self.menu = CTkMenuBar(root,)
        file_btn = self.menu.add_cascade("File")

        dropdown = CustomDropdownMenu(widget=file_btn)
        dropdown.add_option("Open",command=self.open_file)
        dropdown.add_option("Save",command=self.save_file)
        dropdown.add_option("New File",command=self.new_file)
        dropdown.add_option("Exit",command=root.destroy)

        # Markdown file
        self.textbox_1 = ctk.CTkTextbox(root,width=1000,height=900,border_width=1,
        border_color="white",corner_radius=0,wrap="word",font=("opensans",standard_font_size))
        self.textbox_1.pack(side="left",anchor="sw",fill="both")
        # --



        #convert = ctk.CTkButton(root,text="preview",command=lambda: self.preview(root))
        #convert.place(x=0,y=0)
        html = "<br>"

        self.path = ""
        
        # converted box
        
        self.html_frame = HtmlFrame(root,width=800,messages_enabled=True)
        self.html_frame.pack(side="top",fill="both",padx=10,pady=0,expand=True)

        self.textbox_1.bind("<KeyPress>",lambda event: self.preview(root,event))
        self.textbox_1.bind("<KeyRelease>",lambda event: self.preview(root,event))

    def new_file(self,window):
        file_path = filedialog.askcreatefile()
    def open_file(self,):
        file_path = filedialog.askopenfile(title="Open Markdown File",
        filetypes=[("Markdown","*.md")]
        ).name

        self.path = file_path

        with open(file_path,"r",encoding="utf-8") as file:
            content = file.read()

            self.textbox_1.delete("0.0","end")
            self.textbox_1.insert("end",content)


    def save_file(self,):
        with open(self.path,"w+") as file:
            content = self.textbox_1.get("0.0","end")
            file.write(content)


        
    
    def preview(self,window,event=None):
        text_input = self.textbox_1.get("0.0","end-1c")
        full_text = text_input.replace("\n\n", "\n<br>\n")
        
        html = markdown.markdown(full_text)
        
        self.html_frame.load_html(html)


root = ctk.CTk()
MarkdownViewerApp(root)
root.mainloop()
