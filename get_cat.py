import cat
import os
from random import random

HERE = os.getcwd()

catfilename = str(int(100 + (random() * 899)))
c = cat.getCat(directory=HERE, filename=catfilename, format='png')
print(c)
