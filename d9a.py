
import numpy as np

input = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2'''

with open('9a.txt', 'r') as f: input = f.read()

tail_positions = set()

tail = np.array([0, 0])
head = np.array([0, 0])

def arr2tup(arr):
  assert len(arr) == 2
  return (arr[0], arr[1])
tail_positions.add(arr2tup(tail))

dir2delta = {
  'R': (1, 0),
  'U': (0, 1),
  'L': (-1, 0),
  'D': (0, -1)
}

for move in input.split('\n'):
  parts = move.split(' ')
  delta = dir2delta[parts[0]]
  delta = np.array(delta)
  count = int(parts[1])
  for _ in range(count):
    head = head + delta
    to_head = head - tail
    if max(abs(to_head)) == 1:
      # touching - no move
      pass
    else:
      # move towards, but only a maximum of 1 square per direction
      tail_move = np.clip(to_head, -1, 1)
      tail = tail + tail_move
      tail_positions.add(arr2tup(tail))

print(len(tail_positions))