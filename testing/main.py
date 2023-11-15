from ctypes import *
from random import randint

class uni(Union):
    _fields_ = [('p', c_char_p),
                ('a', c_longlong)]

l = CDLL("lib.so")
f = l.print2d
f.argtypes = [POINTER(POINTER(c_char_p)),
              c_int,
              c_int]
x = ((c_char_p * 3) * 10) ()
for i in range(10):
    for j in range(3):
        x[i][j] = str(randint(100, 999)).encode('utf-8')
print(x)
print(x[0][0])
print(hex(addressof(x[0])))
for i in range(10):
    for j in range(3):
        print(x[i][j], end = ' ')
    print()
print("addresses")
for i in range(10):
    for j in range(3):
        # addr = addressof(x[i])+sizeof(POINTER(c_char))*j
        # print(hex(addr), cast(addr, POINTER(c_char))[0], end = ' ')
        t = uni()
        t.p = x[i][j]
        ad = t.a
        print(string_at(ad), end = ' ')
        print(hex(ad), end=' ')

    print()

f(cast(x, POINTER(POINTER(c_char_p))), 10, 3)

