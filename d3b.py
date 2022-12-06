
import sys

def score(L):
  L = ord(L)
  if L >= ord('a') and L <= ord('z'):
    return L - ord('a') + 1
  else:
    return L - ord('A') + 27

total = 0
with open(sys.argv[1]) as f:
  while True:
    try:
      lines = [next(f), next(f), next(f)]
      lines = [l.strip() for l in lines]
      sets = [set(iter(l)) for l in lines]
      common = sets[0].intersection(sets[1]).intersection(sets[2])
      print(common)
      total += score(next(iter(common)))
    except StopIteration:
      break

  print(total)