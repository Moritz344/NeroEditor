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
from PIL import Image
from CTkToolTip import *
from CTkMenuBar import *
from CTkScrollableDropdown import *
from syntax import SyntaxHighlighting
from write_to_json import *
from ctkcomponents import *
from markdown_editor import MarkdownViewerApp


class Widgets(ctk.CTkFrame):
    def __init__(self,window,):
        super().__init__(master=window,)

        self.font = font
        self.colorscheme = colorscheme

        self.files = files
        self.used_files = []
        self.max_recent_files = 5
        self.saving = None
        self.version = "v1.5.0"
        
        self.textbox = None
        self.scrollbar = None
        self.counter = None
        self.filetype_label = None
        self.info_window = None

        self.font_size = standard_font_size
        self.max_font_size = max_font_size
        self.min_font_size = min_font_size
        self.font_art = "normal"

        self.nerdfont_1 = "0xProto Nerd Font Propo"
        self.nerdfont_2 = "FiraMono NerdFont"
        self.nerdfont_3 = "Hack Nerd Font"
        self.nerdfont_4 = "BigBlueTerm437 Nerd Font Mono"

        self.anzahl_tabs = tabs
        self.syntax = "on"
        self.border_spacing = border_spacing
        
        self.current_filetype = None
        self.current_lines = 0
        self.filesize = 0

        self.path = path
        self.text_color = "white"
        self.fg_color = background_color
        
        


        # button + icons für dateien
        self.text_icon = ctk.CTkImage(light_image=Image.open("assets/note.png"),size=(20,20))
        self.final_icon = self.text_icon
        self.python_icon = ctk.CTkImage(light_image=Image.open("assets/python_icon.png"),size=(20,20))
        self.html_icon = ctk.CTkImage(light_image=Image.open("assets/html.png"),size=(20,20))
        self.json_icon = ctk.CTkImage(light_image=Image.open("assets/json.png"),size=(20,20))
        self.javascript_icon = ctk.CTkImage(light_image=Image.open("assets/js.png"),size=(20,20))
        self.css_icon = ctk.CTkImage(light_image=Image.open("assets/css.png"),size=(20,20))
        self.csv_icon = ctk.CTkImage(light_image=Image.open("assets/csv.png"),size=(20,20))
        self.file_name(window,self.path,self.final_icon,)

        self.menu_func(window)
        self.create_textbox(window)

        # gedrückte tasten
        self.pressed_keys = set()

        

        window.bind("<KeyPress>",self.key_press)
        window.bind("<KeyRelease>",self.key_release)



    def save_file_only(self,window):
                try:
                    if self.path != "<untitled>":
                        with open(self.path,"w",encoding="utf-8") as file:
                            content = self.textbox.get(1.0,tk.END)
                            file.write(content)
                            self.saving = True
                            path_name = self.path.split("/")
                            CTkNotification(master=window,state="info",message=f"Saved file: {path_name[-1]}")

                except TypeError:
                    print("cringe")

    def run_python_file(self,window) :
                try:
                    with open(self.path,"r",encoding="utf-8") as file:
                        content = file.read()
                        
                        full_path = self.path
                        path_name = full_path.split(".")
                        if sys.platform == "win32" and path_name[-1] == "py":
                                subprocess.run(["python3",self.path],
                                creationflags=subprocess.CREATE_NEW_CONSOLE)

                        else:
                            CTkMessagebox.CTkMessagebox(title="Warning",
                            message=f"{self.current_filetype} is not a Python file! Or you are running on Linux.",
                            icon="warning",
                            font=("opensans",20),
                            )

                except Exception as e:
                    print("No Python file found",e)
                    CTkMessagebox.CTkMessagebox(title="Warning",
                    message="No Python file found",
                    icon="warning",
                    font=("opensans",20),
                    )
    def open_file(self,window):
        try:
            # file path
            self.path = filedialog.askopenfile(title="Open File",
            filetypes=datatypes).name
            print(len(files))
            print(len(self.used_files))
            if self.path:
                if self.max_recent_files > len(files) and self.max_recent_files > len(self.used_files):
                   self.used_files.append(self.path)
                   write_preferences_to_json("other","files",self.used_files)
                else:
                    print("DEBUG: There are more recent files than allowed.")
                print(self.used_files)
                self.update_file_name(self.path)
                with open(self.path,"r",encoding="utf-8") as file:
                    self.saving = False
                    content = file.read()
                    self.textbox.delete(1.0,tk.END)
                    self.textbox.insert(tk.END,content)
                    self.count_lines()
                    file_path = self.path  
                    file = file_path.split("/")
                    CTkNotification(window,state="info",message=f"...{file[-3]}/{file[-2]}/{file[-1]}",)

        except Exception as e:
                    print(e)
    def ask_save_file(self):
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
    def markdown_file(self,):
            root = ctk.CTk()
            MarkdownViewerApp(root)
            root.mainloop()
    def new_file(self,window):
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
                    file_path = self.path
                    file = file_path.split("/")
                    CTkNotification(master=window,state="info",message=f"Created new file {file[-1]}")
                    self.update_file_name(self.path)
                    self.count_lines()


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
        elif self.path_end[-1] == "md":
            self.current_filetype = "Markdown"
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
        self.file_btn = ctk.CTkButton(window,text=f"{path}",fg_color="transparent",
        font=("opensans",15),
        image=final_icon,
        hover_color="#32373b",
        )


        trennstrich = ctk.CTkFrame(window,width=1920,height=2,fg_color="#59626C")
        trennstrich_2 = ctk.CTkLabel(window,text="|",font=("opensans",20),text_color="grey")
        trennstrich_3 = ctk.CTkLabel(window,text="|",font=("opensans",20),text_color="grey")
        trennstrich_4 = ctk.CTkLabel(window,text="|",font=("opensans",20),text_color="grey")

        # -- icons for buttons
        save_img = ctk.CTkImage(Image.open("assets/save.png"),size=(20,20))
        new_file_img = ctk.CTkImage(Image.open("assets/new_file.png"),size=(20,20))
        open_img = ctk.CTkImage(Image.open("assets/open_file.png"),size=(20,20))
        undo_img = ctk.CTkImage(Image.open("assets/undo.png"),size=(20,20))
        redo_img = ctk.CTkImage(Image.open("assets/redo.png"),size=(20,20))
        build_img = ctk.CTkImage(Image.open("assets/build.png"))
        # --

        # - buttons
        save_btn = ctk.CTkButton(window,text="",image=save_img,width=20,height=20,fg_color="transparent",
        command=lambda: self.save_file_only(window), 
        hover_color="#32373b",)

        undo_btn = ctk.CTkButton(window,text="",image=undo_img,width=10,height=10,fg_color="transparent",command=self.undo,
        font=("opensans",15))

        redo_btn = ctk.CTkButton(window,text="",image=redo_img,width=10,height=10,fg_color="transparent",command=self.redo,
        font=("opensans",15),)

        build_btn = ctk.CTkButton(window,text="",image=build_img,width=10,height=10,fg_color="transparent",
                                  command=lambda: self.run_python_file(window),hover_color="#32373b",
        font=("opensans",15),)

        open_btn = ctk.CTkButton(window,text="",image=open_img,width=20,height=20,fg_color="transparent",
        command=lambda: self.open_file(window), hover_color="#32373b")

        
        new_file_btn = ctk.CTkButton(window,text="",image=new_file_img,width=20,height=20,fg_color="transparent",
        command=lambda: self.new_file(window),hover_color="#32373b")

        # - tooltips
        CTkToolTip(save_btn,message="Save file",delay=0.2)
        CTkToolTip(new_file_btn,message="Make New File",delay=0.2)
        CTkToolTip(open_btn,message="Open File",delay=0.3)
        CTkToolTip(build_btn,message="Run Python File",delay=0.2)
        CTkToolTip(undo_btn,message="Undo",delay=0.2)
        CTkToolTip(redo_btn,message="Redo",delay=0.2)

        # -

        save_btn.place(x=5,y=30)
        new_file_btn.place(x=50,y=30)
        open_btn.place(x=95,y=30)
        undo_btn.place(x=150,y=30)
        redo_btn.place(x=190,y=30)
        build_btn.place(x=235,y=30)
        self.update_icon()
        self.file_btn.place(x=275,y=30)
        trennstrich.place(x=0,y=58)
        trennstrich_2.place(x=140,y=30)
        trennstrich_3.place(x=225,y=30)
        trennstrich_4.place(x=270,y=30)


    def update_file_name(self,path) :

        self.path = path
        path = self.path.split("/")
        #print("Debug:",path)
        self.file_btn.configure(text=path[-1])
        self.path_len = len(path[-1])
        self.update_icon()
        SyntaxHighlighting(self.textbox,self.current_filetype,self.fg_color,self.text_color,self.syntax,self.scrollbar)
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

        # header
        settings_img = ctk.CTkImage(Image.open("assets/adjustment.png"),size=(50,50))
        ctk.CTkLabel(window,text=" Settings",compound="left",image=settings_img,font=("Arial",50)).place(x=30,y=5)

        def change_tabs(value):
            self.anzahl_tabs = value
            write_preferences_to_json("settings","tabs",self.anzahl_tabs)
            self.update_textbox_font()

        def change_syntax():
            self.syntax = self.check_var.get()
            write_preferences_to_json("settings","syntax",self.syntax)
            SyntaxHighlighting(self.textbox,self.current_filetype,self.fg_color,self.text_color,self.syntax,self.scrollbar)

        def change_border_spacing(v):
            self.border_spacing = v
            write_preferences_to_json("settings","border_spacing",self.border_spacing)
            self.update_textbox_font()

        tab_label = ctk.CTkLabel(window,text="Tabs",font=("opensans",25))
        tab_label.place(x=30,y=95)


        self.spinbox = CTkSpinbox(window,
            start_value=self.anzahl_tabs,
            max_value=50,
            min_value=5,
            step_value=5,
            scroll_value=5,
            command=change_tabs)
        self.spinbox.place(x=170,y=90)
        self.check_var = ctk.StringVar(value="on")

        syntax_label = ctk.CTkLabel(window,text="Syntax",font=("opensans",25))
        syntax_label.place(x=30,y=150)

        CTkToolTip(syntax_label,delay=0.3,message="Only Python supported")

        self.checkbutton = ctk.CTkCheckBox(window,text=f"on/off",
        variable=self.check_var,onvalue="on",offvalue="off",command=change_syntax)
        self.checkbutton.place(x=170,y=153)
        CTkToolTip(self.checkbutton,delay=0.3,message="Only Python supported")

        border_spacing_label = ctk.CTkLabel(window,text="Spacing",font=("opensans",25))
        border_spacing_label.place(x=30,y=205)

        self.spinbox_2 = CTkSpinbox(window,
            start_value=self.border_spacing,
            max_value=50,
            min_value=0,
            step_value=2,
            scroll_value=5,
            command=change_border_spacing)
        self.spinbox_2.place(x=170,y=198)


    def file_info(self):
        self.info_window = ctk.CTkToplevel(self)
        self.info_window.geometry("850x600")
        self.info_window.minsize(850,600)
        self.info_window.maxsize(850,600)
        self.info_window.title("File Info")
        font_size = 50
        font_family= ctk.CTkFont(family="opensans",size=font_size)


        

        try:
            if self.path == "<untitled>":
                raise Exception
            info_frame = ctk.CTkFrame(self.info_window,width=1500,height=600,corner_radius=0,)
            info_frame.place(x=0,y=0)

            file_daten_frame = ctk.CTkFrame(self.info_window,width=1500,height=400,corner_radius=0,fg_color="transparent")
            file_daten_frame.place(x=0,y=200)
            
            file_img = ctk.CTkImage(Image.open("assets/folder.png"),size=(100,100))
            file_label = ctk.CTkLabel(info_frame,image=file_img,text="",)
            file_label.place(x=180,y=50)
            header = ctk.CTkLabel(info_frame,text="File Info",font=("opensans",100),)
            header.pack(side=TOP,padx=300,pady=50,anchor="n")

            trennlinie = ctk.CTkFrame(self.info_window,width=1500,height=5,fg_color='#59626C')

            try:
                self.filesize = os.path.getsize(self.path)
            except Exception:
                pass
            self.path_name = self.path.split("/")

            trennlinie.place(x=0,y=200)

            self.daten = ctk.CTkTextbox(file_daten_frame,
            font=font_family,width=850,height=600)
            
            self.daten.tag_config("filetype",foreground="#95b8d1")
            self.daten.tag_config("path_tag",foreground="pink")

            self.daten.place(x=0,y=0)
            self.daten.insert("0.0",f" \t{self.current_filetype}\n","filetype")
            self.daten.insert("0.0","Filetype ")
            self.daten.insert("0.0",f"Filesize \t{self.filesize}B\n")

            self.daten.insert("0.0",f" \t{self.path_name[-1]}\n","path_tag")
            self.daten.insert("0.0","Path")

            self.daten.insert("0.0",f"Lines      \t{self.current_lines}\n")
            self.daten.configure(state="disabled")
            self.count_lines()


        except Exception as e:
            print("DEBUG:",e)
            self.info_window.destroy()
            CTkMessagebox.CTkMessagebox(icon="warning",title="Error",
            message="Please create or open a file before you want to view this option.")


    def create_textbox(self,window):
        self.textbox = ctk.CTkTextbox(window,width=1920,height=1080,corner_radius=0,
        text_color=self.text_color,
        fg_color=self.fg_color,
        undo=True,
        wrap="word",
        tabs=self.anzahl_tabs,
        border_spacing=self.border_spacing,
        font=(self.font,self.font_size,self.font_art),
        activate_scrollbars=False,
        )
        self.textbox.place(x=0,y=60)
        # scrollbars
        self.scrollbar = ctk.CTkScrollbar(master=window,orientation="vertical",command=self.textbox.yview
        ,height=1080,minimum_pixel_length=20,hover=True,fg_color=colorscheme)
        self.scrollbar.pack(side=RIGHT,padx=0,pady=32,)


        self.textbox.configure(yscrollcommand=self.scrollbar.set,)

        

    def update_textbox_font(self):
        self.textbox.configure(fg_color=self.fg_color,text_color=self.text_color,font=(self.font,self.font_size)
        ,tabs=self.anzahl_tabs,border_spacing=self.border_spacing)


    def open_new_file(master):
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

    def menu_func(self,master):
            

            def close_file():
                sys.exit(0)

            def update_preferences():
                root = ctk.CTkToplevel(self)
                root.title("Preferences")
                root.geometry("400x300")

                root.minsize(400,300)
                root.maxsize(400,300)
                
                pref_img = ctk.CTkImage(Image.open("assets/colour.png"),size=(50,50))

                ctk.CTkLabel(root,text=" Preferences",compound="left",image=pref_img,font=("Arial",50)).place(x=30,y=5)

                # trennlinie
                ctk.CTkFrame(root,width=400,height=5,fg_color="#59626C").place(x=0,y=65)


                def change_font(selected):
                    try:
                        self.font = selected
                        optionmenu_1.set(self.font)
                        write_preferences_to_json("preferences","font",selected)
                        self.update_textbox_font()
                    except Exception as e:
                        CTkMessagebox.CTkMessagebox(message="This shouldnt happen.Please report this",icon="warning")
                        print("DEBUG:",e)

                values = ["Comic Sans MS",
                          "Arial","opensans",self.nerdfont_1,self.nerdfont_2,self.nerdfont_3,
                          "minecraft",self.nerdfont_4,
                ]

                optionmenu_1= ctk.CTkOptionMenu(root,width=240)
                optionmenu_1.set(self.font)
                optionmenu_1.place(x=80,y=130)


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

                    write_preferences_to_json("preferences","colorscheme",self.fg_color)



                optionmenu_2 = ctk.CTkOptionMenu(root,width=240)
                optionmenu_2.place(x=80,y=170)
                optionmenu_2.set("BG color")
                bg_colors = ["Dark Slate Grey","Pumpkin","Vermilton","Last Used","Standard"]

                CTkScrollableDropdown(optionmenu_1,values=values,command=change_font)
                CTkScrollableDropdown(optionmenu_2,values=bg_colors,command=change_bg)



            def about_window():
                root = ctk.CTkToplevel(self)
                root.geometry("300x200")
                root.title("About")

                root.minsize(300,200)
                root.maxsize(300,200)

                frame_1 = ctk.CTkFrame(root,width=300,height=200)
                frame_1.place(x=0,y=0)

                try:
                    nero_image = ctk.CTkImage(Image.open("assets/nero.png"),size=(100,100))
                    nero_label = ctk.CTkLabel(frame_1,text="",image=nero_image)
                    nero_label.place(x=10,y=10)
                except Exception as e:
                    print(e)

                ctk.CTkLabel(master=frame_1,
                    text="NeroEditor",#
                    font=("opensans",30)).place(x=120,y=20)

                ctk.CTkLabel(frame_1,
                    text=self.version,
                    font=("opensans",standard_font_size)).place(x=120,y=55)
                
                github_icon = ctk.CTkImage(Image.open("assets/github_icon.png"),size=(50,50))
                github_link = ctk.CTkLabel(frame_1,text="",
                font=("opensans",10,),image=github_icon)
                github_link.place(x=10,y=140)

                kofi_img = ctk.CTkImage(Image.open("assets/mug.png"),size=(50,50))
                kofi_label = ctk.CTkLabel(frame_1,text="",image=kofi_img,)
                kofi_label.place(x=80,y=140)
                
                CTkToolTip(github_link,message="https://github.com/Moritz344/NeroEditor")
                CTkToolTip(kofi_label,message="https://ko-fi.com/moritz344")

                icon = ctk.CTkLabel(frame_1,text="Icons by Flaticon",font=("opensans",15))
                icon.place(x=120,y=80)
                


            def light_mode():
                self.fg_color = "white"
                self.scrollbar.configure(fg_color=self.fg_color)
                self.text_color = "black"
                self.update_textbox_font()
            def dark_mode():
                self.fg_color = "#171614"
                self.scrollbar.configure(fg_color=self.fg_color)
                self.text_color = "white"
                self.update_textbox_font()

            def open_recent_file(file_path,window):
                try:
                    path = file_path
                    with open(path,"r",encoding="utf-8") as file:
                        content = file.read()
                        path_name = path.split("/")
                        CTkNotification(master=window,state="info",message=f"Opened Recent File: {path_name[-1]}")

                        self.update_file_name(path)
                        self.textbox.delete(1.0,tk.END)
                        self.textbox.insert(1.0,content)
                        self.count_lines()
                except Exception as e:
                    CTkMessagebox.CTkMessagebox(title="Error",icon="warning",message="That path does not exist.",
                    font=("opensans",20))
                    print(e)


            self.menu = CTkMenuBar(master,bg_color=colorscheme,)
            button_1 = self.menu.add_cascade("File",hover_color="#32373b")
            button_4 = self.menu.add_cascade("Settings", hover_color="#32373b")
            button_2 = self.menu.add_cascade("Help", hover_color="#32373b")
            button_3 = self.menu.add_cascade("Execute", hover_color="#32373b")
            
            dropdown_1 = CustomDropdownMenu(widget=button_1,hover_color="#32373b")
            dropdown_1.add_option(option="Open",command=lambda: self.open_file(master))
            dropdown_1.add_option(option="Save ",command=lambda: self.save_file_only(master))
            dropdown_1.add_option(option="New File",command=lambda: self.new_file(master))
            dropdown_1.add_option(option="Save File As",command=self.ask_save_file)
            dropdown_1.add_option(option="Open New File In Window",command=self.open_new_file)
            dropdown_1.add_option(option="Open Markdown Editor",command=lambda: self.markdown_file())

            # Recent File submenu
            self.submenu_1 = dropdown_1.add_submenu("Recent Files")

            for file in files:
                self.submenu_1.add_option(f"{file}",command = lambda f=file: open_recent_file(f,master))

            dropdown_2 = CustomDropdownMenu(widget=button_2)
            dropdown_2.add_option(option="About")


            # Preference submenu

            dropdown_2 = CustomDropdownMenu(widget=button_2)
            dropdown_2.add_option(option="About",command=about_window)

            dropdown_3 = CustomDropdownMenu(widget=button_3)
            dropdown_3.add_option(option="Run Python Script",
            command=lambda: self.run_python_file(master))

            dropdown_4 = CustomDropdownMenu(widget=button_4)

            dropdown_4.add_option(option="Settings",command=self.settings)
            dropdown_4.add_option(option="File Info",command=self.file_info)

            submenu_2 = dropdown_4.add_submenu("Preferences")
            submenu_2.add_option(option="Open Preferences Window",command=update_preferences)
            submenu_2.add_option(option="Light mode",command=light_mode)
            submenu_2.add_option(option="Dark mode",command=dark_mode)


            dropdown_1.add_option(option="Exit",command=close_file)

 



