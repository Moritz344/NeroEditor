import customtkinter as ctk
import subprocess
import CTkMessagebox
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

# Toplevel window speichern nach schließen

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
        width=100,height=20,
        hover_color="#212121")
        self.github_btn.place(x=10,y=540)
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
    def __init__(self,textbox,filetype,fg_color,text_color):
        
        self.textbox = textbox
        self.current_filetype = filetype
        self.fg_color = fg_color
        self.text_color = text_color
        
        if self.current_filetype == "Python File":
            self.textbox.tag_config("keyword",foreground=keyword)
            self.textbox.tag_config("string",foreground=string)
            self.textbox.tag_config("comment",foreground=comment)

            self.textbox.tag_config("other1",foreground="#fb4934")
            self.textbox.tag_config("other2",foreground="#b16286")
       
            self.textbox.bind("<KeyRelease>",self.highlighting_syntax)
        else:
            self.change_colors()

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

    def highlighting_syntax(self,event=None):
            cursor_pos = self.textbox.index("insert")

            keywords = r"\b(import|from|if|else|elif|while|for|finally|with|as|pass|break|continue|lambda|yield|global|nonlocal|assert|raise)\b"
            strings = r"(['\"])(?:(?=(\\?))\2.)*?\1"  
            comments = r"#.*"  

            other_1 = r"\b(def|return|except|try|class)\b"
            other_2 = r"\b(print)\b"
            
            text = self.textbox.get("1.0","end-1c")
            
            for pattern, tag in [(keywords, "keyword"), (other_2,"other2"),(strings, "string"), (comments, "comment"), (other_1,"other1")]:
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

        self.font_size = standard_font_size
        self.max_font_size = max_font_size
        self.min_font_size = min_font_size
        self.font_art = "normal"
        
        
        
        self.current_filetype = None

        self.path = path
        self.text_color = "white"
        self.fg_color = background_color
        self.menu_func(window)
        self.create_textbox(window)
        self.create_counter(window)
        
        
        
        


        # button + icons für dateien
        self.text_icon = ctk.CTkImage(light_image=Image.open("assets/note.png"),size=(20,20))
        self.final_icon = self.text_icon
        self.python_icon = ctk.CTkImage(light_image=Image.open("assets/python_icon.png"),size=(20,20))
        self.file_name(window,self.path,self.final_icon)


        # gedrückte tasten
        self.pressed_keys = set()


        window.bind("<KeyPress>",self.key_press)
        window.bind("<KeyRelease>",self.key_release)

    
            

        
    def check_filetype(self):
        if ".py" in self.path:
            self.current_filetype = "Python File"
        elif ".txt" in self.path:
            self.current_filetype = "Textfile"

        SyntaxHighlighting(self.textbox,self.current_filetype,self.fg_color,self.text_color)
        self.filetype_label.configure(text=f"| {self.current_filetype}")

    def update_icon(self):
        if ".py" in self.path:
            self.file_btn.configure(image=self.python_icon)
        else:
            self.file_btn.configure(image=self.text_icon)

    def count_lines(self):
        content = self.textbox.get("1.0","end")
        lines = content.split("\n")

        for i,line in enumerate(lines):
            count = self.counter.cget("text")
            

            self.counter.configure(text=f"Lines: {i}")



    def current_window_size(self,window,) -> int:
        
        width,height =  window.winfo_width(),window.winfo_height()

        return width,height
                

    def file_name(self,window,path,final_icon):

        
        self.file_btn = ctk.CTkButton(window,text=path,corner_radius=0,fg_color="#32373b",
        font=("opensans",15),
        image=final_icon,
        )



        
        self.update_icon()
        

        self.file_btn.place(x=0,y=0)

            


    def update_file_name(self,path) -> str:
        self.path = path
        path = self.path.split("/")
        self.file_btn.configure(text=path[-1])
        self.path_len = len(path[-1])
        self.update_icon()
        
        
        
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

    def create_counter(self,window):

        line_frame = ctk.CTkFrame(window,height=600,width=20,corner_radius=0)
        
        info_frame = ctk.CTkFrame(window,width=1920,height=20,corner_radius=0)
        info_frame.place(x=0,y=28)


        self.filetype_label = ctk.CTkLabel(info_frame,
        text=self.current_filetype,
        width=0,
        height=0,
        font=(font,15))

        self.filetype_label.place(x=100,y=3)
        
        self.counter = ctk.CTkLabel(info_frame,text="Lines: 0",
        width=0,
        height=0,
        font=(font,15)

                                    )
        self.counter.place(x=2,y=3)

    def create_textbox(self,window):

        
        self.textbox = ctk.CTkTextbox(window,width=1920,height=1080,corner_radius=0,
        text_color=self.text_color,
        fg_color=self.fg_color,
        undo=True,
        font=(self.font,self.font_size,self.font_art))
        self.textbox.place(x=0,y=49)


    def update_textbox_font(self):
        self.textbox.configure(fg_color=self.fg_color,text_color=self.text_color,font=(self.font,self.font_size))


    def open_new_file(master) -> None: 
        try:
                 new_window = ctk.CTkToplevel(master)
                 new_window.geometry("800x600")
                 new_file = filedialog.askopenfile(title="Open File",
                 filetypes=[("Textdateien","*.txt",),
                ("Python-Dateien","*.py"),
                ("Markdown","*.md")]).name

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
        except Exception :
            print("Closed new file window.")

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
                 filetypes=[("Textdateien","*.txt",),
                ("Python-Dateien","*.py"),
                ("Markdown","*.md")]).name
                 if self.path:
                     self.used_files.append(self.path)
                     self.write_preferences_to_json("other","files",self.path)
                     self.update_file_name(self.path)
                     with open(self.path,"r",encoding="utf-8") as file:
                         content = file.read()
                         self.textbox.delete(1.0,tk.END)
                         self.textbox.insert(tk.END,content)
                         self.count_lines()
                         self.check_filetype()
                except Exception as e:
                    print("please please please",e)
            def save():
                try:
                    with open(self.path,"w",encoding="utf-8") as file:
                        content = self.textbox.get(1.0,tk.END)
                        file.write(content)
                        
                except Exception :
                    print("oof")
                
            def save_file():
                try:
                    self.path = filedialog.asksaveasfile(title="Save File",filetypes=
                    [("Textdateien","*.txt"),
                    ("Python-Dateien","*.py"),
                    ("Markdown-Dateien","*.md")]).name

                
                    if self.path:
                        self.update_file_name(self.path)
                        with open(self.path,"w",encoding="utf-8") as file:
                            content = self.textbox.get(1.0,tk.END)
                            file.write(content) 

                except Exception as e:
                    print("AHHHHHHHHHHHHHHH",e)
            

            def close_file():
                sys.exit(0)
            def change_colors():
                root = ctk.CTk()
                root.title("Colorschemes")
                root.minsize(200,200)
                root.maxsize(200,200)

                def change_selected(selected):
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






                colorschemes = CTkListbox(
                master=root,
                width=170,
                height=183,
                command=change_selected,
                border_width=0,
                fg_color=background_color,
                scrollbar_button_color=background_color,
                scrollbar_button_hover_color=background_color

                )
                colorschemes.place(x=5,y=0)

                colorschemes.insert(4,"Dark Slate Grey")
                colorschemes.insert(3,"Pumpkin")
                colorschemes.insert(2,"Vermilton")
                colorschemes.insert(0,"Last Used")
                colorschemes.insert(1,"Standard")

                root.mainloop()
            
                

            def update_font():
                root = ctk.CTk()
                root.title("Font")
                root.geometry("190x230")
                root.maxsize(190,230)
                root.minsize(190,230)

                def change_font(selected):
                    self.font = selected
                    self.write_preferences_to_json("preferences","font",selected)
                    self.update_textbox_font()

                listbox = CTkListbox(root,
                height=200,
                command=change_font,
                border_width=0,
                fg_color=background_color,
                scrollbar_button_color=background_color,
                scrollbar_button_hover_color=background_color

                )
                listbox.place(x=10,y=10)
                listbox.insert(0,"opensans")
                listbox.insert(1,"Arial")
                listbox.insert(2,"Times New Roman")
                listbox.insert(3,"Bahnschrift")
                listbox.insert(4,"Calibri")
                listbox.insert(5,"Cambria")
                listbox.insert(6,"Comic Sans MS")
                listbox.insert("END","chiller")


                root.mainloop()

            def about_window():
                root = ctk.CTk()
                root.geometry("650x300")
                root.title("About")
                root.maxsize(650,300)
                root.minsize(650,300)
                
                
                text_list="""Thanks for using this app!

I'm Currently learning how to make guis with python(customtkinter).
If you have anything I can do better please make a pull request on my
github @Moritz344 or if you need any help."""




                normal_text = ctk.CTkTextbox(
                    master=root,
                    font=("opensans",20),
                    width=700,
                    height=500,
                    text_color="white",
                    fg_color=background_color,

                )


                normal_text.insert("10.0",text_list)
                normal_text.configure(state="disabled")
                normal_text.place(x=0,y=0)

                root.mainloop()
            def light_mode():
                self.fg_color = "white"
                self.text_color = "black"
                self.update_textbox_font()
            def dark_mode():
                self.fg_color = "#171614"
                self.text_color = "white"
                self.update_textbox_font()

            def run_python_file() -> None:

                try:
                    with open(self.path,"r",encoding="utf-8") as file:
                        content = file.read()

                    

                    try:
                        if sys.platform == "win32":
                            subprocess.run(["python",self.path],
                            creationflags=subprocess.CREATE_NEW_CONSOLE)
                        else:
                            subprocess.Popen(["x-terminal-emulator","-e","python3",self.path]) 

                    except Exception as e:
                        print("Fehler beim Öffnen des Terminals.",e)

                except Exception:
                    print("No Python file found")
                    CTkMessagebox.CTkMessagebox(title="Warning",
                    message="No Python file found",
                    icon="warning",
                    fade_in_duration=1,
                    font=(font,20),
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
                    self.check_filetype()



            menu = Menu(master)
            master.configure(menu=menu)

    
            fileMenu = Menu(menu,tearoff=False)
            helpMenu = Menu(menu,tearoff=False)
            ausführenMenu = Menu(menu,tearoff=False)

            
            # adding the menus
            menu.add_cascade(label="File", menu=fileMenu)
            menu.add_cascade(label="Execute",menu=ausführenMenu)
            menu.add_cascade(label="Help",menu=helpMenu)
            

            helpMenu.add_command(label="About",command=about_window)

            ausführenMenu.add_command(label="Run Python Script",command=run_python_file)
            
            
            fileMenu.add_command(label="Open",command=open_file )
            fileMenu.add_command(label="Save",command=save)
            fileMenu.add_command(label="Open New File In Window",command=self.open_new_file)
            fileMenu.add_command(label="Save File As",command=save_file )
            fileMenu.add_command(label="Exit",command=close_file)
            fileMenu.add_separator()

            # sub menu
            subMenu = Menu(fileMenu,tearoff=0)
            fileMenu.add_cascade(label="Preferences",menu=subMenu)
            subMenu.add_command(label="Font",command=update_font)
            subMenu.add_command(label="Colorscheme",command=change_colors)
            subMenu.add_command(label="Light mode",command=light_mode)
            subMenu.add_command(label="Dark mode",command=dark_mode)
            
            RecentMenu = Menu(fileMenu,tearoff=0)
            fileMenu.add_cascade(label="Recent File",menu=RecentMenu)
            RecentMenu.add_command(label=f"{files}",command=open_recent_file)
 



