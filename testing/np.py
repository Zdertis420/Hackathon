import numpy
from time import time
from random import randint

## ИСПОЛЬЗУЯ NUMPY 
start = time()

arr = numpy.array(("string" + str(randint(-2**31, 2*31-1)) for _ in range(10000)), dtype='<U64')
stop = time()

print("через np.array:", (stop-start) * 1000000, "миллисекунд")

## ИСПОЛЬЗУЯ MAP:
start = time()

arr = [0]*10000
arr = map(lambda _: randint(-2**31, 2**31-1), arr)
stop = time()

print("через map:", (stop-start) * 1000000, "миллисекунд")

## ИСПОЛЬЗУЯ ГЕНЕРАТОРЫ ПИТОНА
start = time()

arr = ["string" + str(randint(-2**31, 2*31-1)) for _ in range(10000)]
stop = time()

print("через генератор:", (stop-start) * 1000000, "миллисекунд")


