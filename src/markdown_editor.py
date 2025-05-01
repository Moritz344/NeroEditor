import markdown
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog,simpledialog
from settings import *
import threading
from tkinterweb import HtmlFrame
from CTkMenuBar import *
import CTkMessagebox

ctk.set_appearance_mode("dark")

class MarkdownViewerApp(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        root.geometry("800x600")
        root.title("Markdown Editor")
        

        self.menu = CTkMenuBar(root,)
        file_btn = self.menu.add_cascade("File")

        dropdown = CustomDropdownMenu(widget=file_btn)
        dropdown.add_option("Open",command=self.open_file)
        dropdown.add_option("Save",command=self.save_file)
        dropdown.add_option("New File",command=self.new_file)
        dropdown.add_option("Exit",command=root.destroy)

        self.topbar = ctk.CTkFrame(root,width=1920,height=50,fg_color="black",corner_radius=0)
        self.topbar.pack()

        bold_btn = ctk.CTkButton(self.topbar,width=10,text="Bold",command=self.bold_btn)
        bold_btn.place(x=10,y=10)

        kursiv_btn = ctk.CTkButton(self.topbar,width=10,text="Kursiv",command=self.kursiv_btn)
        kursiv_btn.place(x=60,y=10)

        list_btn = ctk.CTkButton(self.topbar,width=10,text="List",command=self.list_item)
        list_btn.place(x=120,y=10)

        header_btn = ctk.CTkButton(self.topbar,width=10,text="T",command=self.header_btn)
        header_btn.place(x=170,y=10)

        # Markdown file
        self.textbox_1 = ctk.CTkTextbox(root,width=1000,height=900,border_width=1,
        border_color="white",corner_radius=0,wrap="word",tabs=3,font=("opensans",standard_font_size))
        self.textbox_1.pack(side="left",anchor="sw",fill="both")
        # --




        self.path = ""
        
        self.html_frame = HtmlFrame(root,width=800,zoom=1)
        self.html_frame.pack(side="top",fill="both",padx=10,pady=00,expand=True)
            
        self.textbox_1.bind("<KeyPress>",lambda event: self.preview(root,event))
        self.textbox_1.bind("<KeyRelease>",lambda event: self.preview(root,event))

    def list_item(self):
        pos = self.textbox_1.index("insert")
        self.textbox_1.insert(pos,"- List item")

    def header_btn(self):
        pos = self.textbox_1.index("insert")
        self.textbox_1.insert(pos,"# Headline")


    def kursiv_btn(self):
        pos = self.textbox_1.index("insert")
        self.textbox_1.insert(pos,"**")

        self.textbox_1.mark_set("insert",f"{pos} +1c ")
    def bold_btn(self):
        pos = self.textbox_1.index("insert")
        self.textbox_1.insert(pos,"****")

        # 3 stellen nach vorne bewegen
        self.textbox_1.mark_set("insert",f"{pos} +2c ")

    def new_file(self,):
        file_path = filedialog.asksaveasfilename(title="Create File",
        filetypes=[("Markdown","*.md")])
        
        if file_path:
          try:
              with open(file_path,"w",encoding="utf-8") as file:
                  content = self.textbox_1.get("0.0","end")
                  file.write(content)
          except Exception as e:
              print(e)

    def open_file(self,):
        file_path = filedialog.askopenfile(title="Open Markdown File",
        filetypes=[("Show Markdown files","*.md",),("Show all files","*.*")]
        ).name

        self.path = file_path
        
        if file_path:
          try:
              with open(file_path,"r",encoding="utf-8") as file:
                  content = file.read()

                  self.textbox_1.delete("0.0","end")
                  self.textbox_1.insert("end",content)
          except Exception as e:
              print(e)


    def save_file(self,):
        if self.path != "":
            with open(self.path,"w+") as file:
                content = self.textbox_1.get("0.0","end")
                file.write(content)
        else:
            self.new_file()

    def wrap_html_with_style(self,html_content: str) -> str:
        return f"""
        <html>
          <head>
            <style>
              body {{
                font-family: 'Arial', sans-serif;
                font-size: 16px;
                padding: 20px;
                background-color: #f0f0f0;
              }}
              h1 {{
                color: dark blue;
              }}
              h2 {{
                color: #274c77;
              }}
              h3{{
                color: #274c77;
              }}
              h4 {{
                color: #274c77;
              }}
              code {{
                color: #f9e2af;
              }}
            </style>
          </head>
          <body>
            {html_content}
          </body>
        </html>
        """

    
    def preview(self,window,event=None):
        text_input = self.textbox_1.get("0.0","end")
        full_input = text_input.replace("\n","<br>")
        
        html_1 = markdown.markdown(text_input, extensions=["nl2br"]) # extension ding rendert zeilenumbrüche in <br> um danke!!!
        html_output = self.wrap_html_with_style(html_1)
        self.html_frame.load_html(html_output)


root = ctk.CTk()
MarkdownViewerApp(root)
root.mainloop()
