from task1 import god_func
from tkinter import filedialog

flag = 2

if flag == 1:
    path_docs = filedialog.askdirectory()
    in_path = path_docs
    god_func(in_path=path_docs, out_path=in_path, flag=1)

if flag == 2:
    path_docs = filedialog.askdirectory()
    path_themes = filedialog.askdirectory()

    in_path = path_docs
    docs = god_func(in_path=path_docs, out_path=in_path, flag=2)
    in_path = path_themes
    themes = god_func(in_path=path_themes, out_path=in_path, flag=2)

    print(docs, themes)

if flag == 0:
    path_docs = filedialog.askdirectory()
    in_path = path_docs
    docs = god_func(in_path=path_docs, out_path=in_path, flag=2)

    print(docs)
