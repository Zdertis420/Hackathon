import numpy as np

f = open("bigfile1")
array = np.array(i for i in f.read().split())
