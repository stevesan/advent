

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

cubes = {}
cubeslist = []
for line in input.split('\n'):
  cor = np.array([int(c) for c in line.split(',')])
  cubes[tuple(cor)] = True
  cubeslist 

print(f'read {len(cubes)} cubes..')
faces = [np.array(d) for d in [
  (1, 0, 0),
  (-1, 0, 0),
  (0, 1, 0),
  (0, -1, 0),
  (0, 0, 1),
  (0, 0, -1),
]]

exposed = 0
for cube in cubes.keys():
  for face in faces:
    nbor = np.array(cube) + face
    if tuple(nbor) not in cubes:
      exposed += 1

print(exposed)