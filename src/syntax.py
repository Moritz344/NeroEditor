from settings import *
import re

class SyntaxHighlighting:
    def __init__(self,textbox,filetype,fg_color,text_color,syntax,scrollbar):
        self.textbox = textbox
        self.scrollbar = scrollbar
        self.current_filetype = filetype
        self.fg_color = fg_color
        self.text_color = text_color
        self.syntax_toggle = syntax
        self.autocompletion_toggle = False
        try:
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
        except Exception as e:
            print(e)


        if self.autocompletion_toggle:
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
            # pyright: ignore
            self.textbox.bind("<KeyRelease>",self.highlighting_syntax)

    def autocompletion(self,event=None):
            pos = self.textbox.index("insert")
            text = self.textbox.get("1.0",pos)
            prev_char = self.textbox.get(pos + "-1c",pos)
            blocked_chars = ("BackSpace","Delete","Caps_Lock","Right","Left","Down","Up","Shift_R","Control_L","Alt_R","Alt_L","Delete","ISO_Level3_Shift","Shift_L")
            print("Debug: ",event.keysym)
            print("DEBUG",prev_char)
            if self.current_filetype == "Python ":
                if prev_char  == '(' and not event.keysym in blocked_chars:
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
