
import math

letter2scale = {
  '2':2, '1':1, '0': 0, '-':-1, '=': -2
}
scale2letter = {scale:letter for letter, scale in letter2scale.items()}

def encode(value, place=None):
  if place is None:
    place = int(math.log(value) / math.log(5))
  if place == 0:
    return scale2letter.get(value, None)
  for letter, q in letter2scale.items():
    remain = value - (5**place) * q
    rest = encode(remain, place-1)
    if rest is not None:
      return letter + rest

  return None
assert encode(4890) == '2=-1=0'

def solve(inputf):
  sum = 0
  with open(inputf, 'r') as f:
    for line in f:
      line = line.strip()
      w = len(line)
      num = 0
      for i in range(w):
        power = w-i-1
        p = 5 ** power
        q = letter2scale[line[i]]
        num += p * q
      print(num)
      sum += num
  return encode(sum)

assert solve('d25s.txt') == '2=-1=0'