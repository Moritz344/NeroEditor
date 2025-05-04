import markdown
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog,simpledialog
from settings import *
from tkinterweb import HtmlFrame
from CTkMenuBar import *
from PIL import Image
import os

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

        self.pressed_keys = set()
        self.font_size = 20
        self.max_font_size = max_font_size
        self.min_font_size = min_font_size
        self.zoom_size = 1
        self.max_zoom = 3
        self.min_zoom = 1
        

        self.topbar = ctk.CTkFrame(root,width=1910,height=50,fg_color="white",corner_radius=0,)
        self.topbar.pack(side="top",anchor="w")


        bold_img = ctk.CTkImage(Image.open("assets/bold.png"),size=(30,30))
        italic_img = ctk.CTkImage(Image.open("assets/italic.png"),size=(30,30))
        headline_img = ctk.CTkImage(Image.open("assets/heading.png"),size=(30,30))
        list_img = ctk.CTkImage(Image.open("assets/list.png"),size=(30,30))


        bold_btn = ctk.CTkButton(self.topbar,width=10,image=bold_img,hover_color="#DEDEDE",text="",fg_color="transparent",command=self.bold_btn)
        bold_btn.place(x=10,y=10)

        kursiv_btn = ctk.CTkButton(self.topbar,width=10,image=italic_img, hover_color="#DEDEDE",text="", fg_color="transparent",command=self.kursiv_btn)
        kursiv_btn.place(x=60,y=10)

        list_btn = ctk.CTkButton(self.topbar,width=10,image=list_img,text="",  hover_color="#DEDEDE",fg_color="transparent",command=self.list_item)
        list_btn.place(x=110,y=10)

        header_btn = ctk.CTkButton(self.topbar,width=10,image=headline_img,text="",  hover_color="#DEDEDE",fg_color="transparent",command=self.header_btn)
        header_btn.place(x=160,y=10)


        # Markdown file
        self.textbox_1 = ctk.CTkTextbox(root,width=1000,height=900,border_width=0,
        border_color="white",undo=True,corner_radius=0,wrap="word",tabs=3,font=("opensans",self.font_size))
        self.textbox_1.pack(side="left",anchor="sw",fill="both",pady=10)
        # --



        self.path = ""
        
        self.html_frame = HtmlFrame(root,width=800,zoom=self.zoom_size,shrink=False)
        self.html_frame.pack(side="top",fill="both",padx=10,pady=10,expand=True)
            
        self.textbox_1.bind("<KeyPress>",lambda event: self.preview(root,event))
        self.textbox_1.bind("<KeyRelease>",lambda event: self.preview(root,event))


        self.textbox_1.bind("<KeyPress>",self.key_press)
        self.textbox_1.bind("<KeyRelease>",self.key_release)

    def update_textbox_font(self):
        self.textbox_1.configure(font=("opensans",self.font_size))
        self.html_frame.configure(zoom = self.zoom_size)


    def key_press(self,event):
       self.pressed_keys.add(event.keysym)
       self.check_combination()
    def key_release(self,event):
       if event.keysym in self.pressed_keys:
           self.pressed_keys.remove(event.keysym)

    def check_combination(self):
       # Reinzoomen 
       if "Control_L" in self.pressed_keys and "plus" in self.pressed_keys and self.font_size < self.max_font_size:
           self.font_size += 5
           if self.zoom_size < self.max_zoom:
            self.zoom_size += 1
           self.update_textbox_font()
       # Rauszoomen 
       elif "Control_L" in self.pressed_keys and "minus" in self.pressed_keys and self.font_size >= self.min_font_size:
           self.font_size -= 5
           if self.zoom_size > self.min_zoom:
            self.zoom_size -= 1
           self.update_textbox_font()

       elif  "Control_L" in self.pressed_keys and "z" in self.pressed_keys :
            self.undo()
       elif "Control_L" in self.pressed_keys and "y" in self.pressed_keys:
            self.redo()

    def list_item(self):
        pos = self.textbox_1.index("insert")
        self.textbox_1.insert(pos,"- List item")

    def header_btn(self):
        pos = self.textbox_1.index("insert")
        self.textbox_1.insert(pos,"# Headline")

    def undo(self):
        try:
            self.textbox_1.edit_undo()
        except Exception :
            print("nothing to undo.")
    def redo(self):
        try:
            self.textbox_1.edit_redo()
        except Exception:
            print("nothing to redo")

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
        filetypes=[("Markdown","*.md"),("Text","*.txt")])
        
        if file_path:
          try:
              content = self.textbox_1.get(1.0,tk.END)
              with open(file_path,"w",encoding="utf-8") as file:
                  file.write(content)
          except Exception as e:
              print(e)

    def open_file(self,):
        file_path = filedialog.askopenfilename(title="Open Markdown File",
        filetypes=[("Markdown ","*.md",),("Show all ","*.*")]
        )

        print(type(file_path))

  
        
        if file_path:
          self.path = file_path
          try:
              with open(self.path,"r",encoding="utf-8") as file:
                  content = file.read()
                  print(type(self.path))

                  self.textbox_1.delete(1.0,tk.END)
                  self.textbox_1.insert(tk.END,content)
                  
          except Exception as e:
              print(e)


    def save_file(self,):
      if self.path:  # Überprüfe, ob ein Pfad gesetzt ist
        try:
            content = self.textbox_1.get(1.0, tk.END)
            with open(self.path, "w", encoding="utf-8") as file:
                file.write(content)
        except OSError as e:
            print("This error could appear if windows blocks this directory.")
            print("Windows Security -> Virus and Threat Protection -> Manage Ransomware Protection -> Allow an app through controlled folder access. Then add Python[version].exe by clicking Add an allowed app.")
            print(e)
      else:
        self.new_file()  # Wenn kein Pfad gesetzt ist, erstelle eine neue Datei



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
