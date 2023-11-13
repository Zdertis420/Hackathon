import os
import sys
import pymorphy3 as pymorphy
import numpy as np
import ctypes as ct
npct = np.ctypeslib


SHARED_LIBRARY_PATH = '/home/main/coding/mixed'
SHARED_LIBRARY_NAME = 'main.so'
COMMAND_FLAGS = {"analyze-docs"    : 0b00000001,
                 "analyze-themes"  : 0b00000010,
                 "distribute_docs" : 0b00000100}
lib = npct.load_library(SHARED_LIBRARY_NAME, SHARED_LIBRARY_PATH)


def call_c(flags:         int, 
           path_to_docs:  str,
           analyze_out:   str,
           theme_div_out: str,
           final_out:     str):

    lib.test()
    print(lib.test())
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
    call_c(flags, "", "", "", "");
            
if __name__ == "__main__":
    main()
