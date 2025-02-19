import customtkinter as ctk
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import sys
from CTkListbox import *
from settings import *
from tkinter import messagebox



class StartScreen(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.geometry("400x300")
        self.title("NoteEditor")
        self.maxsize(400,300)
        self.minsize(400,300)
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")

        def start_app():
            self.destroy()
        def on_closing():
            if messagebox.askokcancel("Exit","Are you sure you want to close the window?"):
                sys.exit(0)

        start_btn = ctk.CTkButton(self,text="Start",command=start_app)
        start_btn.place(x=230,y=130)

        quit_btn = ctk.CTkButton(self,text="Quit",command=on_closing)
        quit_btn.place(x=230,y=180)

        
        image_ = tk.PhotoImage(file="image_2.png",)
        image_ = image_.subsample(3,3)
        photo = tk.Label(self,image=image_)

        photo.place(x=10,y=80)

        header = ctk.CTkLabel(self,text="NoteEditor",font=("opensans",40))
        header.place(x=10,y=15)
        
        self.protocol("WM_DELETE_WINDOW",on_closing)


        self.mainloop()

        

class Widgets(ctk.CTkFrame):
    def __init__(self,window,):
        super().__init__(master=window,)
        
        self.font = "Arial"
        self.font_size = standard_font_size
        self.max_font_size = max_font_size
        self.min_font_size = min_font_size
        self.text_color = "white"
        self.fg_color = background_color
        self.create_textbox(window)
        self.menu_func(window)

        self.path = path

        
        self.file_name(window,self.path)
        # self.rename_file(window)

        # gedrückte tasten
        self.pressed_keys = set()
        
        window.bind("<KeyPress>",self.key_press)
        window.bind("<KeyRelease>",self.key_release)

    def file_name(self,window,path):
        self.file_btn = ctk.CTkButton(window,text=path,corner_radius=0,fg_color="#007090",hover_color="#01a7c2")
        self.file_btn.place(x=0,y=0)

    def rename_file(self,window):
        # frägt beim starten der app nach einem namen für eine datei
        new_name = simpledialog.askstring("Rename","Enter a new file name: ")

        if new_name:
            self.update_file_name(new_name)


    def update_file_name(self,path):
        self.path = path
        # als ob das funktioniert hat
        path = self.path.split("/")
        self.file_btn.configure(text=path[-1])
        
        
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
    
            

    def create_textbox(self,window):
        self.textbox = ctk.CTkTextbox(window,width=1920,height=1080,corner_radius=0,text_color=self.text_color,fg_color=self.fg_color,font=(self.font,self.font_size))
        self.textbox.place(x=0,y=28)

    def update_textbox_font(self):
        self.textbox.configure(fg_color=self.fg_color,text_color=self.text_color,font=(self.font,self.font_size))
    


    def menu_func(self,master):
            def open_file():
                try:
                 # file path
                 self.path = filedialog.askopenfile(title="Open File",filetypes=[("Textdateien","*.txt",),("Python-Dateien","*.py")],).name
                
                 if self.path:
                     self.update_file_name(self.path)
                     with open(self.path,"r",encoding="utf-8") as file:
                         content = file.read()
                         self.textbox.delete(1.0,tk.END)
                         self.textbox.insert(tk.END,content)
                except Exception as e:
                    print("what did you do to get this bro lock in")
            def save():
                try:
                    with open(self.path,"w",encoding="utf-8") as file:
                        content = self.textbox.get(1.0,tk.END)
                        file.write(content)
                        
                except Exception :
                    print("use your brain ones pls")
                
            def save_file():
                try:
                    self.path = filedialog.asksaveasfile(title="Save File",filetypes=[("Textdateien","*.txt"),("Python-Dateien","*.py")]).name
                
                    if self.path:
                        self.update_file_name(self.path)
                        with open(self.path,"w",encoding="utf-8") as file:
                            content = self.textbox.get(1.0,tk.END) # holt den text aus dem editor
                            file.write(content) # speichert den text in die datei

                except Exception as e:
                    print("Bro opened the window to close it again ")


            def close_file():
                sys.exit(0)
            def change_colors():
                root = ctk.CTk()
                root.title("Colorschemes")
                root.minsize(200,200)

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
                    elif selected == "Standard":
                        self.fg_color = background_color
                        self.update_textbox_font()

                colorschemes = CTkListbox(root,width=170,height=180,command=change_selected)
                colorschemes.place(x=0,y=0)

                colorschemes.insert(3,"Dark Slate Grey")
                colorschemes.insert(1,"Pumpkin")
                colorschemes.insert(2,"Vermilton")
                colorschemes.insert(0,"Standard")

                root.mainloop()
            
                

            def update_font():
                root = ctk.CTk()
                root.title("Font")
                root.geometry("200x250")
                root.minsize(200,250)

                def change_font(selected):
                    self.font = selected
                    self.update_textbox_font()

                listbox = CTkListbox(root,height=200,command=change_font)
                listbox.place(x=10,y=10)
                listbox.insert(0,"opensans")
                listbox.insert(1,"Arial")
                listbox.insert(2,"Times New Roman")
                listbox.insert(3,"Bahnschrift")
                listbox.insert(4,"Calibri")
                listbox.insert("END","chiller")

                root.mainloop()

            def about_window():
                root = ctk.CTk()
                root.geometry("650x300")
                root.title("About")
                root.maxsize(650,300)
                
                
                text_list="""Thanks for using this app!

I'm Currently learning how to make guis with python(customtkinter).
If you have anything I can do better please make a pull request on my
github @Moritz344 or if you need any help."""




                normal_text = ctk.CTkTextbox(
                    master=root,
                    font=("opensans",20),
                    width=700,
                    height=500,
                    text_color="green",
                    fg_color="black",

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

            menu = Menu(master)
            master.configure(menu=menu)

    
            fileMenu = Menu(menu,tearoff=False)
            helpMenu = Menu(menu,tearoff=False)
            
            # adding the menus
            menu.add_cascade(label="File", menu=fileMenu)
            menu.add_cascade(label="Help",menu=helpMenu)
            

            helpMenu.add_command(label="About",command=about_window)
            
            
            fileMenu.add_command(label="Open",command=open_file )
            fileMenu.add_command(label="Save",command=save)
            fileMenu.add_command(label="Save New File",command=save_file )
            fileMenu.add_command(label="Exit",command=close_file)
            fileMenu.add_separator()

            # sub menu
            subMenu = Menu(fileMenu,tearoff=0)
            fileMenu.add_cascade(label="Preferences",menu=subMenu)
            subMenu.add_command(label="Font",command=update_font)
            subMenu.add_command(label="Colorscheme",command=change_colors)
            subMenu.add_command(label="Light mode",command=light_mode)
            subMenu.add_command(label="Dark mode",command=dark_mode)





