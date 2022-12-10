import sys

def bet(x, a, b):
  return x >= a and x <= b

def fully_contains(a, b):
  a1, a2 = [int(x) for x in a.split('-')]
  b1, b2 = [int(x) for x in b.split('-')]
  return bet(b1, a1, a2) and bet(b2, a1, a2)

count = 0
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    a, b = line.split(',')
    if fully_contains(a, b) or fully_contains(b, a):
      count += 1

print(count)