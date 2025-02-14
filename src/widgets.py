import customtkinter as ctk
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import sys
from CTkListbox import *

class Widgets(ctk.CTkFrame):
    def __init__(self,window,):
        super().__init__(master=window,)
        
        self.font = "Arial"
        self.font_size = 25
        self.create_textbox(window)
        self.menu_func(window)
        
        # gedrückte tasten
        self.pressed_keys = set()

        window.bind("<KeyPress>",self.key_press)
        window.bind("<KeyRelease>",self.key_release)
        
    def key_press(self,event):
       self.pressed_keys.add(event.keysym)
       self.check_combination()
    def key_release(self,event):
        # Es sollten nur tasten im set sein die gedrückt gehalten werden
       if event.keysym in self.pressed_keys:
           self.pressed_keys.remove(event.keysym)

    def check_combination(self):
       # Reinzoomen 
       if "Control_L" in self.pressed_keys and "plus" in self.pressed_keys:
           self.font_size += 1
           self.update_textbox_font()
       # Rauszoomen 
       elif "Control_L" in self.pressed_keys and "minus" in self.pressed_keys:
           self.font_size -= 1
           self.update_textbox_font()
    
            

    def create_textbox(self,window):
        self.textbox = ctk.CTkTextbox(window,width=1920,height=1080,font=(self.font,self.font_size))
        self.textbox.place(x=0,y=0)

    def update_textbox_font(self):
        self.textbox.configure(font=(self.font,self.font_size))


    def menu_func(self,master):
            def open_file():
                # file path
                path = filedialog.askopenfile(title="Open File",filetypes=[("Textdateien","*.txt")]).name
                
                if path:
                    with open(path,"r",encoding="utf-8") as file:
                        content = file.read()

                        self.textbox.delete(1.0,tk.END)
                        self.textbox.insert(tk.END,content)
    
                                
                
            def save_file():
                path = filedialog.asksaveasfile(title="Save File",filetypes=[("Textdateien","*.txt")]).name
                
                if path:
                    with open(path,"w",encoding="utf-8") as file:
                        content = self.textbox.get(1.0,tk.END) # holt den text aus dem editor
                        file.write(content) # speichert den text in die datei

            def close_file():
                sys.exit(0)
            
                

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


    
            menu = Menu(master)
            master.config(menu=menu)
    
            fileMenu = Menu(menu,tearoff=False)
            helpMenu = Menu(menu,tearoff=False)
            
            # adding the menus
            menu.add_cascade(label="File", menu=fileMenu)
            menu.add_cascade(label="Help",menu=helpMenu)

            helpMenu.add_command(label="help")
            
            
            fileMenu.add_command(label="Open",command=open_file )
            fileMenu.add_command(label="Save",command=save_file )
            fileMenu.add_command(label="Exit",command=close_file)
            fileMenu.add_separator()

            # sub menu
            subMenu = Menu(fileMenu,tearoff=0)
            fileMenu.add_cascade(label="Preferences",menu=subMenu)
            subMenu.add_command(label="Font",command=update_font)





