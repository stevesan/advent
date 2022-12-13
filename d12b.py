import numpy as np

def arr2tup(arr):
  assert len(arr) == 2
  return (arr[0], arr[1])

def vnew(row, col): return tuple([row, col])
def vadd(a, b): return vnew(a[0] + b[0], a[1] + b[1])
def v2np(v): return np.array(v)

grid = []
start_pos = None
end_pos = None
with open('d12a-input.txt') as f:
  row = 0
  for line in f:
    line = line.strip()
    col = 0
    rowvals = []
    for x in line:
      gridval = 0
      if x == 'S':
        pass
      elif x == 'E':
        start_pos = vnew(row, col)
        gridval = ord('z') - ord('a')
      else:
        gridval = ord(x) - ord('a')
      rowvals.append(gridval)
      col += 1
    grid.append(rowvals)
    row += 1

print(grid)
print(start_pos)
print(end_pos)

DIRS = [
  (1, 0),
  (0, 1),
  (-1, 0),
  (0, -1)
]

DIR2CHAR = ['V', '>', '^', '<']

pos2len = {start_pos: 0}
pos2prev = {}
pos2prevmove = {}
visited = set([start_pos])
def visit(node):
  queue = [node]
  while queue:
    node = queue.pop()
    assert node in visited
    len_to_nbor = pos2len[node] + 1
    nodeval = grid[node[0]][node[1]]
    for dir in DIRS:
      nbor = vadd(node, dir)

      if nbor[0] < 0 or nbor[0] >= len(grid): continue
      if nbor[1] < 0 or nbor[1] >= len(grid[0]): continue

      nborval = grid[nbor[0]][nbor[1]]
      if nodeval > nborval + 1: continue

      if nbor not in visited or len_to_nbor < pos2len[nbor]:
        visited.add(nbor)
        pos2len[nbor] = len_to_nbor
        pos2prev[nbor] = node
        pos2prevmove[nbor] = dir
        queue.append(nbor)

visit(start_pos)

lens = []
for row in range(len(grid)):
  line = ''
  for col in range(len(grid[row])):
    pos = vnew(row, col)
    val = grid[row][col]
    if val == 0 and pos in pos2len:
      print(row, col, pos2len[pos])
      lens.append(pos2len[pos])

print(min(lens))

# for row in len(grid):
#   line = ''
#   for col in len(grid[row]):
#     pos = vnew(row, col)
#     for i in range(4):
#       if 