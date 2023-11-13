import os
import sys
import pymorphy3

def print_help():
    print("PROGRAM USAGE:\nnothing here yet...") # TODO: вывести помощь


if "--help" in sys.argv or len(sys.argv) < 2:
    print_help()
    exit(0)

match argv[1]:
    case "all":
        print("doing all work")
    case "analyze-docs":
        print("doing task 1")
    case "vectorize"

    case _:
        print_help()
        exit()
