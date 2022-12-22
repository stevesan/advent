import os, sys, time
from dataclasses import dataclass
from util import Int2

# right is first
cw_dirs = [Int2(1, 0), Int2(0, -1), Int2(-1, 0), Int2(0, 1)]
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

def opposite(dir): return (dir+2) % 4

def get_pass(x, y, dir, height):
  col = x + 1
  row = height - y
  return 1000 * row + 4 * col + dir

assert get_pass(7, 6, 0, 12) == 6032

def solve(inputf):
  width = 0
  num_lines = 0
  last_line = None
  with open(inputf, 'r') as f:
    for line in f:
      if line[-1] == '\n':
        line = line[:-1]
      width = max(width, len(line))
      num_lines += 1
      last_line = line

  movesline = last_line

  height = num_lines - 2
  print('w/h', width, height)
  # True means open, False means wall
  grid:dict[Int2, bool] = {}
  y = height - 1
  with open(inputf, 'r') as f:
    for line in f:
      if line[-1] == '\n':
        line = line[:-1]
      for x in range(len(line)):
        p = Int2(x, y)
        letter = line[x]
        if letter == '.':
          grid[p] = True
        elif letter == '#':
          grid[p] = False
      y -= 1

  # find starting pt
  starty = height - 1
  startx = None
  for x in range(width):
    p = Int2(x, starty)
    if grid.get(p, None) == True:
      startx = x
      break
  assert startx is not None

  # analyze move str..
  moves = []
  for letter in movesline:
    if letter == 'R': moves.append('R')
    elif letter == 'L': moves.append('L')
    else:
      if len(moves) == 0:
        moves.append(letter)
      else:
        if moves[-1] in ['R', 'L']:
          moves.append(letter)
        else:
          moves[-1] = moves[-1] + letter

  def find_next_valid(p, dir):
    delta = cw_dirs[dir]
    while True:
      p += delta
      p.x = p.x % width
      p.y = p.y % height
      if p in grid:
        return p

  dir = 0
  p = Int2(startx, starty)
  print('start at', p)
  i = 0
  print(moves)
  for move in moves:
    i += 1
    if move == 'R':
      dir = (dir + 1) % 4
    elif move == 'L':
      dir = (dir - 1) % 4
    else:
      for i in range(int(move)):
        q = find_next_valid(p, dir)
        if grid[q] == False:
          break
        else:
          p = q
  print('final pos', p, dir)
  print('pass', get_pass(p.x, p.y, dir, height))
  return p, dir

X = None
real_faces = [
  [X, 0, 1],
  [X, 2, X],
  [3, 4, X],
  [5, X, X],
]

@dataclass
class Crossing:
  start:int
  end:int
  dir:int
  turns:int

crossings = [
Crossing(3, 5, DOWN, 0),
Crossing(0, 5, UP, -1),
Crossing(1, 5, UP, 0),
Crossing(4, 5, DOWN, -1),
Crossing(4, 2, UP, 0),
Crossing(1, 2, DOWN, -1),
Crossing(0, 2, DOWN, 0),
Crossing(3, 2, UP, -1),
Crossing(3, 4, RIGHT, 0),
Crossing(1, 4, RIGHT, 2),
Crossing(0, 1, RIGHT, 0),
Crossing(3, 0, LEFT, 2),
]

assert solve('d22t1.txt') == (Int2(8, 5), 3)
solve('d22sample.txt') == (Int2(7, 6), 0)
solve('d22real.txt')