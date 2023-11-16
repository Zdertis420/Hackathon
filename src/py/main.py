import os
import sys
import pymorphy3 as pymorphy
import numpy as np
import ctypes as ct
from ctypes import POINTER, pointer, cast, c_char_p, c_void_p, c_int, c_uint
from typing import Tuple
from random import randint
npct = np.ctypeslib


SHARED_LIBRARY_PATH = '/home/main/coding/Hackaton/build'
SHARED_LIBRARY_NAME = 'libvector.so'
COMMAND_FLAGS = {"analyze-docs"    : 0b00000001,
                 "analyze-themes"  : 0b00000010,
                 "all"             : 0b00000011} 
lib = npct.load_library(SHARED_LIBRARY_NAME, SHARED_LIBRARY_PATH)
libc = ct.CDLL("libc.so.6") # free(pointer)


def perror(*args, **kwargs):
    print(*args, file = sys.stderr, **kwargs)


def gen_c_array(l: list[str]):
    for i in l:
        yield i.encode('utf-8')
    yield None


# возвращает УКАЗАТЕЛЬ И ВНЕШНЮЮ ДЛИНУ
def arrays_to_c(arr: list[list[str]]) -> Tuple[c_void_p, c_uint]:
    outer_len = len(arr)
    ret = (POINTER(c_char_p) * outer_len) ( )
    for i in range(outer_len):
        current_length = len(arr[i]) + 1 # для nulptr в конце
        ret[i] = (c_char_p * current_length) ( *gen_c_array(arr[i]) )
        # print(*(cast(i, POINTER(c_int)) for i in ret[i])) ## THIS LINE CRASHES MY LINUX
    return cast(ret, POINTER(POINTER(c_char_p))), outer_len


def strings_to_c(*args):
    for i in args:
        if not i:
            yield None
        else:
            yield i.encode('utf-8')
    pass


def test_c():
    test_f = lib.print_2d_array
    test_f.argtypes = [c_void_p, c_int]
    print(array_p, array_s, flags, path_to_docs, analyze_out, theme_div_out, final_out)
    test_arr =  \
    [
        ["hello", "i", "am", "gay"],
        [", ", " ,", " , "],
        ["123"],
        ["as", "a", "a", "a", "a", "b"],
        ["", "", ""],
        ["whatsup everynyan", "[]"]
    ]
    test_f(*arrays_to_c(test_arr))


def call_c(array_docs:    list[list[str]],  # Массив с документами 
           array_themes:  list[list[str]],  # Массив с темами
           flags:         int,              # Флаги выполнения. Парсятся через аргументы командной строки. 
                                            # Oтвечают за то, какие задания выполняются
           path_to_docs:  str,              # Путь к документам. Необходим для 1 задания.
           analyze_out:   str,              # Путь к выводу документов. Необходим, если выполняется 1 задание отдельно от всех.
           analyze_in:    str,              # Путь в вводу анализированных документов. Нужен, если выполняется 2 задание отдельно от 1
           themes_in:     str,              # Путь к темам. необходим для 2 задания.
           final_out:     str               # Путь к финальному выводу. Нужен, если выполняется 2 задание.
           ):
    driver_func = lib.driver
    driver_func.argtypes = [
        c_uint,
        POINTER(POINTER(c_char_p)), c_uint,
        POINTER(POINTER(c_char_p)), c_uint,
        c_char_p, c_char_p, c_char_p, 
        c_char_p, c_char_p
    ] 
    driver_func.restype = c_char_p
    
    ## Никита или андрей, проведите проверку на аргументы
    ## в сответствии с тем, что я выше описал
    args = [
        flags, *arrays_to_c(array_docs), *arrays_to_c(array_themes), 
        *strings_to_c(path_to_docs, analyze_out, analyze_in, themes_in, final_out)
    ]
    error = driver_func(*args)
    if not error:
        print("\x1b[91;1m", error, "\x1b[0m")
        exit()


def print_help():
    print("PROGRAM USAGE:\nnothing here yet...") # TODO: вывести помощь


def main():
    if "--help" in sys.argv or len(sys.argv) < 2:
        print_help()
        exit(0)

    flags = 0
    if "--task" in sys.argv:
        index = sys.argv.index("--task") + 1
        match sys.argv[index]:
            case "1": flags |= 0b00000001
            case "2": flags |= 0b00000010
            case "0": flags |= 0b00000011
            case _: exit()
    
    if sys.argv[1] in COMMAND_FLAGS.keys():
        flags |= COMMAND_FLAGS[sys.argv[1]]
    elif flags == 0:
        print(f"\x1b[91m INVALID COMMAND {sys.argv[1]}\x1b[0m")
        print_help()
        exit()
    
    instr, outstr = "", ""
    if "-o" in sys.argv:
        index = sys.argv.index("-o") + 1
        instr = sys.argv[idnex]
    if "-i" in sys.argv:
        index = sys.argv.index("-i") + 1
        outstr = sys.argv[index]

    if not instr or not outstr:
        print()

    print("flags:", bool(flags&1), bool(flags&2))
    # + ["THIS STRING IS EVERYWHERE"]
    docsv = [
        [str(i) for i in range(10)] + ["THIS STRING IS EVERYWHERE"],
        10*[str(randint(-10, 10)) for i in range(10)] + ["THIS STRING IS EVERYWHERE"],
        ["test", "lmao", "kill me"] + ["THIS STRING IS EVERYWHERE"],
        ["empty", "aaa"] + ["THIS STRING IS EVERYWHERE"],
        ["empty", "empty", "kill me"] + ["THIS STRING IS EVERYWHERE"],
        2*[str(i**2) for i in range(100)] + ["THIS STRING IS EVERYWHERE"]
    ];
    themesv = [["test1"], ["test2"]]
    print(*(i[-1] for i in docsv))
    call_c(docsv, themesv, 3, "", "", "", "", "")





if __name__ == "__main__":
    main()

