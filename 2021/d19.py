
import sys
import numpy as np

with open(sys.argv[1]) as f:
  text = f.read()

scanner2beacons = []

for grouptext in text.split('\n\n'):
  group = grouptext.split('\n')
  header = group[0]
  assert 'scanner' in header
  beacons = []
  for line in group[1:]:
    p = np.array([int(x) for x in line.split(',')])
    beacons.append(p)
  scanner2beacons.append(beacons)

for bs in scanner2beacons:
  print('---')
  print(bs)