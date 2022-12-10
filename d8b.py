
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

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
rows = len(grid)
cols = len(grid[0])
W = cols - 1
H = rows - 1

visible_cells = set()

scores = []

for i in range(rows):
  for j in range(cols):
    score = 1
    for dir in dirs:
      dist = 0
      p, q = i, j
      maxht = grid[p][q]
      p += dir[0]
      q += dir[1]
      while p < rows and q < cols and p >= 0 and q >= 0:
        ht = grid[p][q]
        dist += 1
        if ht >= maxht:
          break
        p += dir[0]
        q += dir[1]
      score *= dist
    scores.append(score)

print(max(scores))
