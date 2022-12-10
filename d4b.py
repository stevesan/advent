import sys

def overlaps(a, b):
  a1, a2 = [int(x) for x in a.split('-')]
  b1, b2 = [int(x) for x in b.split('-')]
  disjoint = b2 < a1 or b1 > a2
  return not disjoint

count = 0
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    a, b = line.split(',')
    if overlaps(a, b):
      count += 1

print(count)