
from math import *

def main():
  x = 10 ** 2818201
  print(log10(x))
  # x = 1
  x += 1
  sum = 0
  for _ in range(1000):
    x *= 1234
    sum += x % 19
    sum += 1

  print(sum)

import cProfile
cProfile.run('main()')