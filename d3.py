import sys

def score(L):
  L = ord(L)
  if L >= ord('a') and L <= ord('z'):
    return L - ord('a') + 1
  else:
    return L - ord('A') + 27

total = 0
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    N = len(line)
    assert N % 2 == 0
    left = line[0:(N//2)]
    right = line[(N//2):]
    print('---------')
    print(left)
    print(right)
    assert len(left) == len(right)
    lset = set([a for a in left])
    rset = set([a for a in right])
    common = lset.intersection(rset)
    print(common)
    assert len(common) == 1
    c = next(iter(common))
    print(score(c))
    total += score(c)

print(total)