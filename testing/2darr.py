import numpy as np
import numpy.ctypeslib as npct
import ctypes as ct
from typing import Tuple

def arr_arr_to_c(arr2d: np.array[list[str]]) -> Tuple[ct.POINTER(ct.POINTER(ct.c_char_p)), ct.c_int, ct.c_int]:
    transformed_array = (ct.POINTER(ct.c_char)p) * len(arr2d))()
    for inner_array, inner_orig in zip(transformed_array, arr2d):
        inner_array = (ct.c_char_p * (len(inner_orig) + 1)) (i.encode('utf-8') for i in (*inner_orig))

    

def array_to_c_2d(arr_2d: np.ndarray[np.ndarray[str]]) -> Tuple[ct.POINTER(ct.POINTER(ct.c_char)), ct.c_int, ct.c_int]:
    flat_arr = np.concatenate([np.char.encode(row, 'utf-8') for row in arr_2d])
    c_arr = (ct.c_char_p * len(flat_arr))(*flat_arr)
    c_arr_ptrs = (ct.POINTER(ct.c_char) * len(arr_2d))()
    for i in range(len(arr_2d)):
        c_arr_ptrs[i] = ct.cast(ct.pointer(c_arr[i * len(arr_2d[0])]), ct.POINTER(ct.c_char))

    return c_arr_ptrs, len(arr_2d), len(arr_2d[0])




data = np.array([["apple", "orange", ""],
                 ["banana", "grape", "kiwi"],
                 ["cherry", "", ""]], dtype='U')

c_arr_ptrs, rows, max_length = array_to_c_2d(data)

print(c_arr_ptrs, rows, max_length)
