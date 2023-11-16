from task1 import god_func
from tkinter import filedialog

def god_func2():
    path_docs = filedialog.askdirectory()
    path_themes = filedialog.askdirectory()

    god_func(path_docs, flag=2)
    god_func(path_themes, flag=2)
