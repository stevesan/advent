from collections import defaultdict
from util import Int2

DIR2DELTA = {
  '>':Int2(1, 0),
  '<':Int2(-1, 0),
  '^':Int2(0, 1),
  'v':Int2(0, -1),
}

def print_frame(f, width, height):

  for y in range(height-1, -1, -1):
    rowstr = ''
    for x in range(width):
      items = f[Int2(x, y)]
      if len(items) == 0:
        rowstr += '.'
      elif len(items) == 1:
        rowstr += items[0]
      else:
        rowstr += str(len(items))
    print(rowstr)

def make_frame():
  return defaultdict(lambda:[])

def step_blizzards(f, width, height):
  rv = make_frame()
  for x in range(width):
    for y in range(height):
      p = Int2(x, y)
      items = f[p]
      for item in items:
        dt = DIR2DELTA[item]
        q = p + dt
        q = q.mod2(width, height)
        rv[q].append(item)
  return rv

def solve(inputf):
  with open(inputf, 'r') as f:
    lines = f.readlines()
  lines.reverse()
  height = len(lines) - 2
  width = len(lines[0]) - 2

  f0 = make_frame()

  p0 = Int2(0, height-1)

  for x in range(width):
    for y in range(height):
      p = Int2(x, y)
      c = lines[y+1][x+1]
      if c == '.':
        continue
      else:
        f0[p].append(c)

  f = f0
  for i in range(6):
    print(f'---- after minute {i}')
    print_frame(f, width, height)
    f = step_blizzards(f, width, height)
solve('d24sample.txt')