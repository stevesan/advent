from collections import defaultdict
from util import Int2
import heapq

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

def shortest_path(frames, width, height, time0, startpt, endpt):
  p0 = Int2(0, height-1)
  assert len(frames[0][p0]) == 0

  endpt = Int2(width-1, 0)
  front = set([p0])
  time = 0
  while True:
    next_frame = frames[(time+1) % len(frames)]
    next_front = set()
    for p in front:
      # Add (0, 0) for the wait option
      for dir in list(DIR2DELTA.values()) + [Int2(0, 0)]:
        q = p + dir
        if q.x < 0 or q.y < 0 or q.x >= width or q.y >= height:
          continue
        if len(next_frame[q]) > 0:
          continue
        if q == endpt:
          return time + 1
        next_front.add(q)
    front = next_front
    time += 1
    # print(f'next exploring: {next_front}, minute {time+1}')
    # print_frame(next_frame, width, height)
    if len(next_front) == 0: return None


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

def solve(inputf, period):
  with open(inputf, 'r') as f:
    lines = f.readlines()
  lines.reverse()
  height = len(lines) - 2
  width = len(lines[0]) - 2

  assert period % width == 0
  assert period % height == 0

  f0 = make_frame()
  for x in range(width):
    for y in range(height):
      p = Int2(x, y)
      c = lines[y+1][x+1]
      if c == '.':
        continue
      else:
        f0[p].append(c)

  f = f0
  frames = []
  for i in range(period):
    # print(f'---- after minute {i}')
    f = step_blizzards(f, width, height)
    frames.append(f)

  bestt = shortest_path(frames, width, height, 0,
  Int2(0, height-1), Int2(width-1, 0))
  return bestt + 2

# solve('d24sample.txt', 5)
solve('d24s2.txt', 12) == 18
# print(solve('d24real.txt', 700))