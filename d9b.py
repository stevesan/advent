
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

node_positions = [np.array([0, 0]) for _ in range(10)]

def arr2tup(arr):
  assert len(arr) == 2
  return (arr[0], arr[1])
tail_positions.add(arr2tup(node_positions[-1]))

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
    # move the head
    node_positions[0] += delta
    # now move other nodes if needed
    for i in range(1, 10):
      p = i-1
      q = i
      to_leader = node_positions[p] - node_positions[q]
      if max(abs(to_leader)) == 1:
        # touching - no move
        pass
      else:
        # move towards, but only a maximum of 1 square per direction
        tail_move = np.clip(to_leader, -1, 1)
        node_positions[q] = node_positions[q] + tail_move
    # all nodes have moved - mark tail position
    tail_positions.add(arr2tup(node_positions[-1]))

print(len(tail_positions))