import customtkinter as ctk
import subprocess
import CTkMessagebox
from CTkSpinbox import *
import os
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import sys
from CTkListbox import *
from settings import *
from tkinter import messagebox
import json
from PIL import Image,ImageTk
import re
from CTkToolTip import *
from CTkMenuBar import *
from CTkScrollableDropdown import *

# TODO: zip datei release


class StartScreen(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.geometry("800x600")
        self.title(project_name)
        self.maxsize(800,600)
        self.minsize(800,600)
        ctk.set_appearance_mode("system")


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
        
        def show_value():
            print(tooltip_1.get())
        self.github_icon = ctk.CTkImage(light_image=Image.open("assets/github_icon.png"),size=(50,50))
        self.github_btn = ctk.CTkButton(self,text="",image=self.github_icon,fg_color="#212121",
        width=50,height=20,
        hover_color="#212121")
        self.github_btn.place(x=0,y=540)
        tooltip_1 = CTkToolTip(self.github_btn,delay=0.3,message="github.com/Moritz344")


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



class SyntaxHighlighting:
    def __init__(self,textbox,filetype,fg_color,text_color,syntax):
       
        self.textbox = textbox
        self.current_filetype = filetype
        self.fg_color = fg_color
        self.text_color = text_color
        self.syntax_toggle = syntax
        
        if self.current_filetype == "Python " and self.syntax_toggle == "on":
            self.textbox.tag_config("keyword",foreground=keyword)
            self.textbox.tag_config("string",foreground=string)
            self.textbox.tag_config("comment",foreground=comment)

            self.textbox.tag_config("other1",foreground="#fb4934")
            self.textbox.tag_config("other2",foreground="#b16286")
       
            self.textbox.bind("<KeyRelease>",self.highlighting_syntax)
            self.textbox.bind("<Button-1>",self.highlighting_syntax)
        else:
            self.change_colors()
        
        self.textbox.bind("<KeyRelease>",self.autocompletion)
        self.textbox.bind("<KeyPress>",self.autocompletion)

    def change_colors(self):
        if self.fg_color == "#171614":
            self.text_color = "white"
            self.textbox.tag_config("keyword",foreground="white")
            self.textbox.tag_config("string",foreground="white")
            self.textbox.tag_config("comment",foreground="white")

            self.textbox.tag_config("other1",foreground="white")
            self.textbox.tag_config("other2",foreground="white")
       
            self.textbox.bind("<KeyRelease>",self.highlighting_syntax)
        elif self.fg_color == "white":
            self.text_color = "black"
            self.textbox.tag_config("keyword",foreground="black")
            self.textbox.tag_config("string",foreground="black")
            self.textbox.tag_config("comment",foreground="black")

            self.textbox.tag_config("other1",foreground="black")
            self.textbox.tag_config("other2",foreground="black")
       
            self.textbox.bind("<KeyRelease>",self.highlighting_syntax)

    def autocompletion(self,event=None):
            pos = self.textbox.index("insert")
            text = self.textbox.get("1.0",pos)
            prev_char = self.textbox.get(pos + "-1c",pos)
            blocked_chars = ("BackSpace","Delete","Caps_Lock","Right","Left","Down","Up","Shift_R","Control_L","Alt_R","Alt_L","Delete","ISO_Level3_Shift")
            print("Debug: ",event.keysym)
            if self.current_filetype == "Python ":
                if prev_char  == '(' and not event.keysym in blocked_chars:
                    print("DEBUG",prev_char)
                    self.textbox.insert(pos,')')
                    self.textbox.mark_set("insert", pos)
                    if event.keysym in ("BackSpace","Delete"):
                        self.textbox.delete(pos + "-1c" ,pos)
                elif prev_char == '{' :
                    if event.keysym not in blocked_chars:
                        if event.type != tk.EventType.KeyPress:
                            self.textbox.insert(pos,'}')
                            self.textbox.mark_set("insert", pos)
                    if event.keysym in ("BackSpace","Delete"):
                        self.textbox.delete(pos + "-1c" ,pos)
                elif prev_char == '[':
                    if event.keysym not in blocked_chars:
                        if event.type != tk.EventType.KeyPress:
                            self.textbox.insert(pos,']')
                            self.textbox.mark_set("insert", pos)
                    if event.keysym in ("BackSpace","Delete"):
                        self.textbox.delete(pos + "-1c" ,pos)
                    # deleted autocompletion for ""

    def highlighting_syntax(self,event=None):
            cursor_pos = self.textbox.index("insert")

            self.keywords = r"\b(import|from|if|else|elif|while|for|finally|with|as|pass|break|continue|lambda|yield|global|nonlocal|assert|raise)\b"
            strings = r"(['\"])(?:(?=(\\?))\2.)*?\1"  
            comments = r"#.*"  

            other_1 = r"\b(def|return|except|try|class)\b"
            other_2 = r"\b(print)\b"
            
            text = self.textbox.get("1.0","end-1c")
            
            for pattern, tag in [(self.keywords, "keyword"), (other_2,"other2"),(strings, "string"), (comments, "comment"), (other_1,"other1")]:
                for match in re.finditer(pattern, text):
                    start_idx = f"1.0 + {match.start()} chars"
                    end_idx = f"1.0 + {match.end()} chars"

                    self.textbox.tag_add(tag, start_idx, end_idx)

            self.textbox.mark_set("insert", cursor_pos)





class Widgets(ctk.CTkFrame):
    def __init__(self,window,):
        super().__init__(master=window,)

        
        self.font = font
        self.colorscheme = colorscheme

        self.files = files
        
        self.used_files = []
        
        self.textbox = None
        self.counter = None
        self.filetype_label = None
        self.info_window = None

        self.font_size = standard_font_size
        self.max_font_size = max_font_size
        self.min_font_size = min_font_size
        self.font_art = "normal"


        self.anzahl_tabs = tabs
        self.syntax = "on"
        self.border_spacing = border_spacing
        
        self.current_filetype = None
        self.current_lines = 0
        self.filesize = 0

        self.path = path
        self.text_color = "white"
        self.fg_color = background_color
        self.menu_func(window)
        self.create_textbox(window)
        
        


        # button + icons für dateien
        self.text_icon = ctk.CTkImage(light_image=Image.open("assets/note.png"),size=(20,20))
        self.final_icon = self.text_icon
        self.python_icon = ctk.CTkImage(light_image=Image.open("assets/python_icon.png"),size=(20,20))
        self.html_icon = ctk.CTkImage(light_image=Image.open("assets/html.png"),size=(20,20))
        self.json_icon = ctk.CTkImage(light_image=Image.open("assets/json.png"),size=(20,20))
        self.javascript_icon = ctk.CTkImage(light_image=Image.open("assets/js.png"),size=(20,20))
        self.css_icon = ctk.CTkImage(light_image=Image.open("assets/css.png"),size=(20,20))
        self.csv_icon = ctk.CTkImage(light_image=Image.open("assets/csv.png"),size=(20,20))
        self.file_name(window,self.path,self.final_icon)


        # gedrückte tasten
        self.pressed_keys = set()
        

        window.bind("<KeyPress>",self.key_press)
        window.bind("<KeyRelease>",self.key_release)
        
            

        

    def update_icon(self):
        self.path_end = self.path.split(".")
        if self.path_end[-1] == "py":
            self.file_btn.configure(image=self.python_icon)
            self.current_filetype = "Python "
        elif self.path_end[-1] == "html":
            self.file_btn.configure(image=self.html_icon)
            self.current_filetype = "HTML "
        elif self.path_end[-1] == "js":
            self.file_btn.configure(image=self.javascript_icon)
            self.current_filetype = "Javascript "
        elif self.path_end[-1] == "css":
            self.file_btn.configure(image=self.css_icon)
            self.current_filetype = "CSS "
        elif self.path_end[-1] == "json":
            self.file_btn.configure(image=self.json_icon)
            self.current_filetype = "JSON "
        elif self.path_end[-1] == "csv":
            self.current_filetype = "CSV "
            self.file_btn.configure(image=self.csv_icon)
        else:
            self.current_filetype = "Textfile"
            self.file_btn.configure(image=self.text_icon)


    def count_lines(self):
        content = self.textbox.get("1.0","end")
        lines = content.split("\n")

        for i,line in enumerate(lines):
            self.current_lines = i
        
    

    def current_window_size(self,window,) -> int:
        
        width,height =  window.winfo_width(),window.winfo_height()

        return width,height
                

    def file_name(self,window,path,final_icon):

        
        self.file_btn = ctk.CTkButton(window,text=path,corner_radius=0,fg_color="#32373b",
        font=("opensans",15),
        image=final_icon,
        hover_color="#32373b",
        )
        self.update_icon()
        self.file_btn.place(x=0,y=30)

            


    def update_file_name(self,path) -> str:
        self.path = path
        path = self.path.split("/")
        self.file_btn.configure(text=path[-1])
        self.path_len = len(path[-1])
        self.update_icon()
        SyntaxHighlighting(self.textbox,self.current_filetype,self.fg_color,self.text_color,self.syntax)
        
        
        
    def key_press(self,event):
       self.pressed_keys.add(event.keysym)
       self.check_combination()
    def key_release(self,event):
        # Es sollten nur tasten im set sein die gedrückt gehalten werden
       if event.keysym in self.pressed_keys:
           self.pressed_keys.remove(event.keysym)

    def check_combination(self):
       # Reinzoomen 
       if "Control_L" in self.pressed_keys and "plus" in self.pressed_keys and self.font_size < self.max_font_size:
           self.font_size += 1
           self.update_textbox_font()
       # Rauszoomen 
       elif "Control_L" in self.pressed_keys and "minus" in self.pressed_keys and self.font_size >= self.min_font_size:
           self.font_size -= 1
           self.update_textbox_font()

       elif  "Control_L" in self.pressed_keys and "z" in self.pressed_keys :
            self.undo()
       elif "Control_L" in self.pressed_keys and "y" in self.pressed_keys:
            self.redo()
    
    def undo(self):
        try:
            self.textbox.edit_undo()
        except Exception :
            print("nothing to undo.")
    def redo(self):
        try:
            self.textbox.edit_redo()
        except Exception:
            print("nothing to redo")



    def settings(self):
        window = ctk.CTkToplevel()
        window.geometry("300x350")
        window.title("Settings")
        window.minsize(300,350)
        window.maxsize(300,350)

        def change_tabs(value):
            self.anzahl_tabs = value
            self.write_preferences_to_json("settings","tabs",self.anzahl_tabs)
            self.update_textbox_font()

        def change_syntax():
            self.syntax = self.check_var.get()
            self.write_preferences_to_json("settings","syntax",self.syntax)
            SyntaxHighlighting(self.textbox,self.current_filetype,self.fg_color,self.text_color,self.syntax)

        def change_border_spacing(v):
            self.border_spacing = v
            self.write_preferences_to_json("settings","border_spacing",self.border_spacing)
            self.update_textbox_font()

        # sprache ändern

        
        tab_label = ctk.CTkLabel(window,text="Tabs",font=("opensans",25))
        tab_label.place(x=120,y=11)


        self.spinbox = CTkSpinbox(window,
            start_value=self.anzahl_tabs,
            max_value=50,
            min_value=5,
            step_value=5,
            scroll_value=5,
            command=change_tabs)
        self.spinbox.place(x=100,y=50)
        
        self.check_var = ctk.StringVar(value="on")

        syntax_label = ctk.CTkLabel(window,text="Syntax Highlighter",font=("opensans",25))
        syntax_label.place(x=60,y=111)

        CTkToolTip(syntax_label,delay=0.3,message="Only Python supported")

        self.checkbutton = ctk.CTkCheckBox(window,text=f"on/off",
        variable=self.check_var,onvalue="on",offvalue="off",command=change_syntax
                                           )
        self.checkbutton.place(x=100,y=150)
        CTkToolTip(self.checkbutton,delay=0.3,message="Only Python supported")

        border_spacing_label = ctk.CTkLabel(window,text="Border Spacing",font=("opensans",25))
        border_spacing_label.place(x=60,y=211)

        self.spinbox_2 = CTkSpinbox(window,
            start_value=self.border_spacing,
            max_value=50,
            min_value=0,
            step_value=2,
            scroll_value=5,
            command=change_border_spacing)
        self.spinbox_2.place(x=100,y=250)

    def file_info(self):


        self.info_window = ctk.CTkToplevel(self)
        self.info_window.geometry("500x300")
        self.info_window.title("File Info")


        self.info_window.minsize(500,300)
        self.info_window.maxsize(500,300)



        info_frame = ctk.CTkFrame(self.info_window,width=500,height=600,corner_radius=0)
        info_frame.place(x=0,y=0)

        icon = ctk.CTkLabel(info_frame,text="Icons by Flaticon",font=("opensans",15))
        icon.place(x=360,y=270)

        header = ctk.CTkLabel(info_frame,text="File Info",font=("opensans",40),)
        header.place(x=180,y=5)


        self.filetype_label = ctk.CTkLabel(info_frame,
        text=f"Filetype: \t\t{self.current_filetype}",
        width=0,
        height=0,
        font=("opensans",standard_font_size))
        
        self.filetype_label.place(x=10,y=110)

        
        self.path_name = self.path.split("/")
        self.path_label = ctk.CTkLabel(info_frame,
        text=f"Path: \t\t{self.path_name[-1]}",
        font=("opensans",standard_font_size))
        self.path_label.place(x=10,y=140)

        
        try:
            self.filesize = os.path.getsize(self.path)
        except Exception:
            pass


        self.filesize_label = ctk.CTkLabel(info_frame,
        text=f"Filesize: \t\t{self.filesize}B",
        font=("opensans",standard_font_size),
        )
        self.filesize_label.place(x=10,y=170)
        
        self.counter = ctk.CTkLabel(info_frame,text=f"Lines: \t\t{self.current_lines}",
        width=0,
        height=0,
        font=("opensans",standard_font_size))
        self.count_lines()
        self.counter.place(x=10,y=80)


        tooltip_1 = CTkToolTip(self.path_label,message=f"{self.path}")
        tooltip_2 = CTkToolTip(self.filetype_label,
        message=f"{self.current_filetype}")

        tooltip_3 = CTkToolTip(self.filesize_label,
        message=f"{self.filesize}B (that's massive)")
        tooltip_4 = CTkToolTip(self.counter,
        message=f"{self.current_lines}")


    def create_textbox(self,window):

        
        self.textbox = ctk.CTkTextbox(window,width=1920,height=1080,corner_radius=0,
        text_color=self.text_color,
        fg_color=self.fg_color,
        undo=True,
        wrap=None,
        tabs=self.anzahl_tabs,
        border_spacing=self.border_spacing,
        font=(self.font,self.font_size,self.font_art))
        self.textbox.place(x=0,y=60)
        

    def update_textbox_font(self):
        self.textbox.configure(fg_color=self.fg_color,text_color=self.text_color,font=(self.font,self.font_size)
        ,tabs=self.anzahl_tabs,border_spacing=self.border_spacing)


    def open_new_file(master) : 
            try:
                 new_window = ctk.CTkToplevel(master)
                 new_window.geometry("800x600")
                    
                 new_file = filedialog.askopenfile(title="Open File",
                 filetypes=datatypes).name

                 new_window.title(new_file)
                 with open(new_file,"r") as file:
                    content = file.read()
                    
                    text_widget = ctk.CTkTextbox(new_window,
                    wrap=tk.WORD,
                    width=1920,
                    height=1080,
                    font=(font,standard_font_size))
                    text_widget.insert(tk.END, content)
                    text_widget.place(x=0,y=0)



            except Exception as e:
                print(e)

    def write_preferences_to_json(self,main,key,new_value):
        try:
            # get the content of the file
            with open("data.json","r") as file:
                content = json.load(file)

            if main in content:
                # z.b: content["preferences"]["font"] = "Arial"
                content[main][key] = new_value



            with open("data.json","w") as file:
                # aktualisiere json file
                json.dump(content,file,indent=4)

        except Exception as e:
            print(e)

    def menu_func(self,master):
            def open_file():
                try:
                 # file path
                 self.path = filedialog.askopenfile(title="Open File",
                 filetypes=datatypes).name
                 if self.path:
                     #self.used_files.append(self.path)
                     self.write_preferences_to_json("other","files",self.path)
                     self.update_file_name(self.path)
                     with open(self.path,"r",encoding="utf-8") as file:
                         content = file.read()
                         self.textbox.delete(1.0,tk.END)
                         self.textbox.insert(tk.END,content)
                         self.count_lines()

                         CTkMessagebox.CTkMessagebox(title="Opened File",icon="check",
                         message=f"Opened File successfuly in {self.path}")
                except Exception as e:
                    print("please please please",e)
            def save():
                try:
                    if self.path != "<untitled>":
                        with open(self.path,"w",encoding="utf-8") as file:
                            content = self.textbox.get(1.0,tk.END)
                            file.write(content)
                            CTkMessagebox.CTkMessagebox(title="Saved File",icon="check",
                            message=f"Saved File successfuly in {self.path}")
                        
                except Exception as e:
                    print("oof",e)
                
            def save_file():
                try:
                    self.path = filedialog.asksaveasfile(title="Save File",
                    filetypes=datatypes).name

                    if self.path:
                        self.update_file_name(self.path)
                        with open(self.path,"w",encoding="utf-8") as file:
                            content = self.textbox.get(1.0,tk.END)
                            file.write(content) 

                except Exception as e:
                    print("AHHHHHHHHHHHHHHH",e)
            

            def close_file():
                sys.exit(0)

            def update_preferences():
                root = ctk.CTkToplevel(self)
                root.title("Preferences")
                root.geometry("300x200")

                root.minsize(300,200)
                root.maxsize(300,200)

                header = ctk.CTkLabel(root,text="Preferences",font=("opensans",30)).place(x=70,y=5)


                def change_font(selected):
                    self.font = selected
                    self.write_preferences_to_json("preferences","font",selected)
                    self.update_textbox_font()

                values = ["Comic Sans MS","Arial","opensans",]

                optionmenu_1= ctk.CTkOptionMenu(root,width=240)
                optionmenu_1.set("Font")
                optionmenu_1.place(x=25,y=70)


                def change_bg(selected):
                    if selected == "Dark Slate Grey":
                        self.fg_color = "#374b4a"
                        self.update_textbox_font()
                    elif selected == "Pumpkin":
                        self.fg_color = "#ff8c42"
                        self.update_textbox_font()
                    elif selected == "Vermilton":
                        self.fg_color = "#ff3c38"
                        self.update_textbox_font()
                    elif selected == "Last Used":
                        self.fg_color = self.colorscheme
                        self.update_textbox_font()
                    elif selected == "Standard":
                        self.fg_color = background_color
                        self.update_textbox_font()

                    self.write_preferences_to_json("preferences","colorscheme",self.fg_color)



                optionmenu_2 = ctk.CTkOptionMenu(root,width=240)
                optionmenu_2.place(x=25,y=120)
                optionmenu_2.set("BG color")
                
                bg_colors = ["Dark Slate Grey","Pumpkin","Vermilton","Last Used","Standard"]

                CTkScrollableDropdown(optionmenu_1,values=values,command=change_font)
                CTkScrollableDropdown(optionmenu_2,values=bg_colors,command=change_bg)



            def about_window():
                root = ctk.CTkToplevel(self)
                root.geometry("350x300")
                root.title("About")
                root.maxsize(650,300)
                root.minsize(650,300)
                try:
                    nero_image = ctk.CTkImage(Image.open("assets/nero.png"),size=(80,80))
                    nero_label = ctk.CTkLabel(root,text="",image=nero_image)
                    nero_label.place(x=279,y=60)
                except Exception as e:
                    print(e)
                expl = "NeroEditor is a minimalistic \neditor written in python"
                ctk.CTkLabel(master=root,
                text="NeroEditor",#
                font=("opensans",30)).place(x=250,y=10)
                ctk.CTkLabel(root,
                text=expl,
                font=("opensans",standard_font_size)).place(x=170,y=150)
                
                github_icon = ctk.CTkImage(Image.open("assets/github_icon.png"),size=(35,35))
                github_link = ctk.CTkLabel(root,text="",
                font=("opensans",10,),image=github_icon)
                github_link.place(x=600,y=250)
                
                tooltip_1 = CTkToolTip(github_link,message="https://github.com/Moritz344/NeroEditor")


            def light_mode():
                self.fg_color = "white"
                self.text_color = "black"
                self.update_textbox_font()
            def dark_mode():
                self.fg_color = "#171614"
                self.text_color = "white"
                self.update_textbox_font()
            
            def new_file():
                file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=datatypes)


                if file_path:
                    with open(file_path,"w+") as file:
                        file_content = file.read()
                        self.path = file_path
                        self.update_file_name(self.path)


                        self.textbox.delete("1.0",tk.END)
                        self.textbox.insert(tk.END,file_content)

                        msg =CTkMessagebox.CTkMessagebox(
                            self,
                            icon="check",
                            title="New File",
                            option_1="Ok",
                            text_color="white",
                            message=f"Your file got created sucessfuly in: {file_path}",
                            font=("opensans",20),)

                        msg.geometry("+500+300")

                        self.write_preferences_to_json("other","files",self.path)
                        self.update_file_name(self.path)
                        self.count_lines()







            def run_python_file() -> None:

                try:
                    with open(self.path,"r",encoding="utf-8") as file:
                        content = file.read()

                    try:
                        self.path_name = self.path.split(".")
                        if sys.platform == "win32" and self.path_name[-1] == "py":
                            subprocess.run(["python",self.path],
                            creationflags=subprocess.CREATE_NEW_CONSOLE)
                        else:
                            CTkMessagebox.CTkMessagebox(title="Warning",
                            message=f"{self.current_filetype} is not a Python file!",
                            icon="warning",
                            font=("opensans",20),
                            )

                    except Exception as e:
                        print("Fehler beim Öffnen des Terminals.",e)

                except Exception:
                    print("No Python file found")
                    CTkMessagebox.CTkMessagebox(title="Warning",
                    message="No Python file found",
                    icon="warning",
                    font=("opensans",20),
                    )

            def open_recent_file() -> None:

                with open(self.files,"r",encoding="utf-8") as file:
                    content = file.read()
                    
                    path_name = self.files.split("/")
                    path_recent = path_name[-1]

                    self.update_file_name(self.files)
                    
                    self.textbox.delete(1.0,tk.END)
                    self.textbox.insert(1.0,content)
                    
                
                    self.count_lines()



            menu = CTkMenuBar(master,bg_color="#171614")
            button_1 = menu.add_cascade("File")
            button_4 = menu.add_cascade("Settings")
            button_2 = menu.add_cascade("Help")
            button_3 = menu.add_cascade("Execute")
            
            dropdown_1 = CustomDropdownMenu(widget=button_1)
            dropdown_1.add_option(option="Open",command=open_file)
            dropdown_1.add_option(option="Create New",command=new_file)
            dropdown_1.add_option(option="Save ",command=save)
            dropdown_1.add_option(option="Open New File In Window",
            command=self.open_new_file)
            dropdown_1.add_option(option="Save File As",command=save_file)
            

            

            
            # Recent File submenu
            submenu_1 = dropdown_1.add_submenu("Recent File")
            submenu_1.add_option(option=f"{files}",command=open_recent_file)

            dropdown_2 = CustomDropdownMenu(widget=button_2)
            dropdown_2.add_option(option="About")


            # Preference submenu

            dropdown_2 = CustomDropdownMenu(widget=button_2)
            dropdown_2.add_option(option="About",command=about_window)

            dropdown_3 = CustomDropdownMenu(widget=button_3)
            dropdown_3.add_option(option="Run Python Script",
            command=run_python_file)

            dropdown_4 = CustomDropdownMenu(widget=button_4)

            dropdown_4.add_option(option="Settings",command=self.settings)
            dropdown_4.add_option(option="File Info",command=self.file_info)

            submenu_2 = dropdown_4.add_submenu("Preferences")
            submenu_2.add_option(option="Open Preferences Window",command=update_preferences)
            submenu_2.add_option(option="Light mode",command=light_mode)
            submenu_2.add_option(option="Dark mode",command=dark_mode)


            dropdown_1.add_option(option="Exit",command=close_file)

 



