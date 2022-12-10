
from dataclasses import dataclass

input = '''\
30373
25512
65332
33549
35390'''

with open('8a.txt', 'r') as f: input = f.read()

lines = input.split('\n')
grid = [[int(x) for x in l] for l in lines]
print(grid)

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
rows = len(grid)
cols = len(grid[0])
W = cols - 1
H = rows - 1

visible_cells = set()

for dirnum, lookdir in enumerate(dirs):
  movedir = dirs[(dirnum+1) % 4]
  i = int(H/2 - lookdir[0]*H/2 - movedir[0]*H/2)
  j = int(W/2 - lookdir[1]*W/2 - movedir[1]*W/2)

  print(f'starting from {i} {j}, lookdir = {lookdir}, movedir={movedir}')

  while i < rows and j < cols and i >= 0 and j >= 0:
    p = i
    q = j
    maxht = None
    while p < rows and q < cols and p >= 0 and q >= 0:
      ht = grid[p][q]
      if maxht is None or ht > maxht:
        maxht = ht
        visible_cells.add((p, q))
        # print(f'{p} {q} = {ht} is visible')
      p += lookdir[0]
      q += lookdir[1]

    i += movedir[0]
    j += movedir[1]

print(len(visible_cells))