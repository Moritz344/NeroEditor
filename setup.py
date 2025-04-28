from setuptools import setup, find_packages
from datetime import *

today = datetime.date.today()
version = f"1.0.0.dev{today.strftime('%Y%m%d')}"



setup(
    name='Neroeditor',  
    version=version,    
    packages=find_packages(where='src'),  
    package_dir={'': 'src'},               
    include_package_data=True,            
    install_requires=[
    "assets/", "data.json", "settings.py", "syntax.py", "widgets.py", "start_screen.py",
    "hand.cur", "Normal.cur","CTkListbox/", "CTkMenuBar/", "CTkMessagebox/", "CTkScrollableDropdown", "CTkToolTip/",
    "write_to_json.py", "markdown_editor.py"
    ],
    python_requires='>=3.9',                # Mindest-Python-Version
    entry_points={
        'console_scripts': [
            'Neroeditor=main:main', 
        ],
    },
)
