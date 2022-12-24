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


def shortest_path(frames, width, height):
  nframes = len(frames)
  visited:set[(int, Int2)] = set()
  p0 = Int2(0, height-1)
  assert len(frames[0][p0]) == 0

  endpt = Int2(width-1, 0)
  Q:list[(int, Int2)] = []
  pair2dist = {}
  first_pair = (0, p0)
  pair2dist[first_pair] = 0
  heapq.heappush(Q, first_pair)

  while Q:
    time, p = heapq.heappop(Q)
    if p == endpt:
      print(f'reached end pt. time = {time}')
      return time
    if (p, time) in visited: continue
    visited.add((p, time))
    next_frame = frames[(time + 1) % nframes]
    qdist = pair2dist[(p, time)] + 1
    for dir in DIR2DELTA.values():
      q = p + dir
      nbor_pair = (q, time + 1)
      if len(next_frame[q]) > 0:
        # blocked
        continue
      if nbor_pair in visited: continue
      if nbor_pair not in pair2dist or pair2dist[nbor_pair] > qdist:
        pair2dist[nbor_pair] = qdist
        # not updating - just pushing the new entry. we always check if
        # the top item is already visited, so we won't have duplicates
        heapq.heappush(Q, (qdist, nbor_pair))

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

  return shortest_path(frames, width, height)

solve('d24sample.txt', 5)
solve('d24s2.txt', 12)
# solve('d24real.txt', 700)