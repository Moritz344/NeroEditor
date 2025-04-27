import markdown
import webview
import customtkinter as ctk

class MarkdownViewerApp(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(master=root)
        self.root = root
        self.geometry("800x600")
        self.title("Markdown Editor")

        textbox_1 = ctk.CTkTextbox(self,width=1000,height=1080,border_width=1,
        border_color="white",corner_radius=0)
        textbox_1.pack(side="left",anchor="nw",expand=True)
        textbox_2 = ctk.CTkTextbox(self,width=1000,height=1080,border_width=1,
        border_color="white",corner_radius=0)
        textbox_2.pack(side="right",anchor="ne",expand=True)
