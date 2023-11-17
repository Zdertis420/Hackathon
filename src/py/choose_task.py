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

    out_path_docs = path_docs
    docs = god_func(in_path=path_docs, out_path=out_path_docs, flag=2)
    out_path_themes = path_themes
    themes = god_func(in_path=path_themes, out_path=out_path_themes, flag=2)

    print(docs, themes, sep = "\n")

if flag == 0:
    path_docs = filedialog.askdirectory()
    in_path = path_docs
    docs = god_func(in_path=path_docs, out_path=in_path, flag=2)

    print(docs)
