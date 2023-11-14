import os
import sys
import pymorphy3 as pymorphy
import numpy as np
import ctypes as ct
from typing import Tuple
npct = np.ctypeslib


SHARED_LIBRARY_PATH = '/home/main/coding/mixed'
SHARED_LIBRARY_NAME = 'main.so'
COMMAND_FLAGS = {"analyze-docs"    : 0b00000001,
                 "analyze-themes"  : 0b00000010,
                 "distribute-docs" : 0b00000100}
lib = npct.load_library(SHARED_LIBRARY_NAME, SHARED_LIBRARY_PATH)
libc = ct.CDLL("libc.so.6") # free(pointer)


def array_to_c(arr: np.ndarray[str]) -> Tuple[ct.POINTER(ct.c_char_p), ct.c_int]:
    c_arr = (ct.c_char_p * len(arr))(*np.char.encode(arr, 'utf-8'))
    return ct.cast(c_arr, ct.POINTER(ct.c_char_p)), len(arr)
    # как вызывать эту функцию, если Си принимает массив:
    # lib.some_function(*array_to_c(твой_массив), остальные_аргументы)
    # можно распаковать возвращаемый тип звёздочкой прям сходу


def call_c(array_p:       ct.POINTER(ct.c_char_p),
           array_s:       ct.c_int,
           flags:         int, 
           path_to_docs:  str,
           analyze_out:   str,
           theme_div_out: str,
           final_out:     str):
    test_f = lib.print_a
    test_f.argtypes = [ct.POINTER(ct.c_char_p),
                       ct.c_int,
                       ct.c_int]
    print(array_p, array_s, flags, path_to_docs, analyze_out, theme_div_out, final_out)
    test_f(array_p, array_s, flags)
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
            case "0": flags |= 0b00001111
        
    if sys.argv[1] in COMMAND_FLAGS.keys():
        flags |= COMMAND_FLAGS[sys.argv[1]]
    elif index == 0:
        print(f"\x1b[91m INVALID COMMAND {sys.argv[1]}\x1b[0m")
        print_help()
        exit()

    print("flags:", flags)

    test = np.array(["hello from python", "to C", "and back to python!"])
    call_c(*array_to_c(test), flags, "", "", "", "")
            
if __name__ == "__main__":
    main()
