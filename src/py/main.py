import os
import sys
import pymorphy3 as pymorphy
import numpy as np
import ctypes as ct
from ctypes import POINTER, pointer, cast, c_char_p, c_void_p, c_int
from typing import Tuple
npct = np.ctypeslib


SHARED_LIBRARY_PATH = '/home/main/coding/Hackaton/src/cpp/'
SHARED_LIBRARY_NAME = 'libvector.so'
COMMAND_FLAGS = {"analyze-docs"    : 0b00000001,
                 "analyze-themes"  : 0b00000010,
                 "distribute-docs" : 0b00000100}
lib = npct.load_library(SHARED_LIBRARY_NAME, SHARED_LIBRARY_PATH)
libc = ct.CDLL("libc.so.6") # free(pointer)

def gen_c_array(l: list[str]):
    for i in l:
        yield i.encode('utf-8')
    yield None

# возвращает УКАЗАТЕЛЬ И ВНЕШНЮЮ ДЛИНУ
def arrays_to_c(arr: list[list[str]]) -> Tuple[c_void_p, c_int]:
    outer_len = len(arr)
    ret = (POINTER(c_char_p) * outer_len) ( )
    for i in range(outer_len):
        current_length = len(arr[i]) + 1 # для nulptr в конце
        ret[i] = (c_char_p * current_length) ( *gen_c_array(arr[i]) )
        # print(*(cast(i, POINTER(c_int)) for i in ret[i])) ## THIS LINE CRASHES MY LINUX
    return cast(ret, c_void_p), outer_len


def call_c(array_p:       c_void_p, # Укзатель на 1 элемент массива. Возвращается функцией arrays_to_c 
           array_s:       c_int,    # Длина массива. Возвращается array_to_c
           flags:         c_int,    # Флаги выполнения. Парсятся через аргументы командной строки. 
                                    # Oтвечают за то, какие задания выполняются
           path_to_docs:  str,      # Путь к документам. Необходим для 1 задания.
           analyze_out:   str,      # Путь к выводу документов. Необходим, если выполняется 1 задание отдельно от всех.
           analyze_in:    str,      # Путь в вводу анализированных документов. Нужен, если выполняется 2 задание отдельно от 1
           theme_div_out: str,      # Путь к выводу документов, рассортированных по близости темы. Нужен, если выполняется 2 задание
           theme_div_in:  str,      # Путь к вводу документов с близостью тем. Нужен, если выполняется 3 задание отдельно от 2.
           final_out:     str       # Путь к финальному выводу. Нужен, если выполняется 3 задание.
           ):
    test_f = lib.print_2d_array
    test_f.argtypes = [c_void_p,
                       c_int]
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
    return


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
            case "3": flags |= 0b00000100
            case "0": flags |= 0b00000111
            case _: exit()
        
    if sys.argv[1] in COMMAND_FLAGS.keys():
        flags |= COMMAND_FLAGS[sys.argv[1]]
    elif flags == 0:
        print(f"\x1b[91m INVALID COMMAND {sys.argv[1]}\x1b[0m")
        print_help()
        exit()

    print("flags:", flags)

    test = [["hello from python", "to C", "and back to python!"]]
    call_c(*arrays_to_c(test), flags, "", "", "", "", "", "")
            
if __name__ == "__main__":
    main()
