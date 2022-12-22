import os, sys, time
from dataclasses import dataclass
from util import Int2

# right is first
cw_dirs = [Int2(1, 0), Int2(0, -1), Int2(-1, 0), Int2(0, 1)]

def get_pass(x, y, dir, height):
  col = x + 1
  row = height - y
  print(row, col)
  return 1000 * row + 4 * col + dir

assert get_pass(7, 6, 0, 12) == 6032

def solve(inputf):
  width = 0
  num_lines = 0
  last_line = None
  with open(inputf, 'r') as f:
    for line in f:
      line = line[:-1]
      width = max(width, len(line))
      num_lines += 1
      last_line = line

  moves = last_line

  height = num_lines - 2
  print(width, height)
  # True means can move, False means wall
  grid:dict[Int2, bool] = {}
  y = height - 1
  with open(inputf, 'r') as f:
    for line in f:
      line = line.strip()
      for x in range(len(line)):
        p = Int2(x, y)
        letter = line[x]
        if letter == '.':
          grid[p] = True
        elif letter == '#':
          grid[p] = False
      y -= 1


solve('d22sample.txt')