from ctypes import *
from random import randint

lib = CDLL('lib.so')
func = lib.print2d
func.argtypes = [POINTER(POINTER(c_char_p)),
                 c_int,
                 c_int]
#initializing the array of strings
x = (POINTER(c_char_p) * 10) ()
for i in range(10):
    x[i] = (c_char_p * 10) ()
    for j in range(10):
        x[i][j] = str(randint(100, 999)).encode('utf-8')

#it prints what i expect it to print
for i in range(10):
    for j in range(10):
        if (randint(1, 3) == 2 and j > 5):
            x[i][j] = None
        print(x[i][j], end = ' ')
    print()


    
func(cast(x, POINTER(POINTER(c_char_p))), 10, 10)
