from cx_Freeze import setup, Executable
import sys
import os

today = datetime.date.today()
version = f"1.0.0.dev{today.strftime('%Y%m%d')}"

include_files = ["assets/","data.json","settings.py","syntax.py","widgets.py","start_screen.py","hand.cur","Normal.cur",     
"CTkListbox/","CTkMenuBar/","CTkMessagebox/","CTkScrollableDropdown","CTkToolTip/","write_to_json.py","markdown_editor.py"]

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # damit kein Terminal erscheint bei GUI-Apps

setup(
    name="NeroEditor",
    version="1.5",
    description="NeroEditor is a simple and flexible text editor with basic features for editing text.",
    options={"build_exe": {
        "packages": ["customtkinter", "tkinter","PIL","sys","json","CTkSpinbox","ctkcomponents"],
        "include_files": include_files,
        "include_msvcr": True
    }},
    executables=[Executable("main.py", base=base)]
)
