

import os, sys
from dataclasses import dataclass
import numpy as np

input = '''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5'''

with open('d18real.txt', 'r') as f: input = f.read()

# input = '1,1,1\n2,1,1'

lavacubes = {}
cubeslist = []
for line in input.split('\n'):
  cor = np.array([int(c) for c in line.split(',')])
  lavacubes[tuple(cor)] = True
  cubeslist.append(cor)

minx = min(c[0] for c in cubeslist)
miny = min(c[1] for c in cubeslist)
minz = min(c[2] for c in cubeslist)
maxx = max(c[0] for c in cubeslist)
maxy = max(c[1] for c in cubeslist)
maxz = max(c[2] for c in cubeslist)

mins = (minx-1, miny-1, minz-1)
maxs = (maxx+1, maxy+1, maxz+1)

print(mins, maxs)
print(f'read {len(lavacubes)} cubes..')
faces = [np.array(d) for d in [
  (1, 0, 0),
  (-1, 0, 0),
  (0, 1, 0),
  (0, -1, 0),
  (0, 0, 1),
  (0, 0, -1),
]]

touched_lava_faces = set()
num_touches = 0
visited_positions = set()
Q = [mins]
while Q:
  p = Q.pop(0)

  print(tuple(p))
  
  for face in faces:
    q = np.array(p) + face
    if all(q >= mins) and all(q <= maxs):
      if tuple(q) in lavacubes:
        num_touches += 1
      else:
        if tuple(q) not in visited_positions:
          visited_positions.add(tuple(q))
          Q.append(q)

print(f'lava cubes = {lavacubes}')
print(num_touches)