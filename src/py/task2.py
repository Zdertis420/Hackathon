from task1 import god_func
from tkinter import filedialog

def god_func2():
    path_docs = filedialog.askdirectory()
    path_themes = filedialog.askdirectory()

    ## пусть возвращает 2 списка в таком формате:
    ## [
    ##    [""], ""] ## документ 1
    ##    [""]     ## документ 2
    ## ]

    return god_func(in_path=path_docs, out_path = in_path + "/output", flag=2), \
           god_func(in_path=path_themes, out_path = in_path + "/output_themes", flag=2)


if __name__ == "__main__":
    god_func2()
