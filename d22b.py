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

S = 50

X = None
real_faces = [
  [X, 0, 1],
  [X, 2, X],
  [3, 4, X],
  [5, X, X],
]
real_faces.reverse()

@dataclass
class Edge:
  start:int
  end:int
  dir:int
  turns:int

edges = [
  Edge(3, 5, DOWN, 0),
  Edge(0, 5, UP, -1),
  Edge(1, 5, UP, 0),
  Edge(4, 5, DOWN, -1),
  Edge(4, 2, UP, 0),
  Edge(1, 2, DOWN, -1),
  Edge(0, 2, DOWN, 0),
  Edge(3, 2, UP, -1),
  Edge(3, 4, RIGHT, 0),
  Edge(1, 4, RIGHT, 2),
  Edge(0, 1, RIGHT, 0),
  Edge(3, 0, LEFT, 2),
]

width = 150
height = 200

def get_cube_face(p:Int2):
  cx = p.x // S
  cy = p.y // S
  if cx < 0 or cy < 0 or cx >= 3 or cy >= 4:
    return None
  return real_faces[cy][cx]

def get_face_botleft(face):
  for cy in range(4):
    for cx in range(3):
      if real_faces[cy][cx] == face:
        return Int2(cx, cy) * S

assert get_face_botleft(0) == Int2(50, 150)
assert get_face_botleft(3) == Int2(0, 50)
assert get_face_botleft(1) == Int2(100, 150)
assert get_face_botleft(5) == Int2(0, 0)
assert get_face_botleft(4) == Int2(50, 50)

def get_face_nbor(face, dir):
  for edge in edges:
    if edge.start == face and edge.dir == dir:
      return edge.end, edge.turns % 4
    # going over the other way?
    if edge.end == face and edge.dir == opposite(dir + edge.turns):
      return edge.start, (-edge.turns) % 4

assert get_face_nbor(1, RIGHT) == (4, 2)
assert get_face_nbor(4, UP) == (2, 0)
assert get_face_nbor(4, LEFT) == (3, 0)
assert get_face_nbor(4, DOWN) == (5, 3)
assert get_face_nbor(4, RIGHT) == (1, 2)
assert get_face_nbor(1, DOWN) == (2, 3)
assert get_face_nbor(2, RIGHT) == (1, 1)
assert get_face_nbor(2, DOWN) == (4, 0)
assert get_face_nbor(2, UP) == (0, 0)
assert get_face_nbor(2, LEFT) == (3, 1)

assert get_cube_face(Int2(50,199)) == 0
assert get_cube_face(Int2(51,199)) == 0

def do_move(p, dir):
  start_face = get_cube_face(p)
  assert start_face is not None
  q = p + cw_dirs[dir]
  if get_cube_face(q) is not None:
    # same face - normal
    return q, dir
  
  # need to find the actual new face we're on..
  new_face, turns = get_face_nbor(start_face, dir)
  assert new_face is not None

  # print('q', q.mod(S).rot90cw(turns))
  xformed_ofs = ((q.mod(S)*2+1).rot90cw(-turns)-1)//2
  # print('debug', (q.mod(S)))
  new_face_ofs = xformed_ofs.mod(S)
  new_bot_left = get_face_botleft(new_face)
  # print('new ofs', new_face_ofs, 'botleft', new_bot_left)
  # print('new face', new_face)
  # print('turns', turns)
  newpos = new_bot_left + new_face_ofs
  assert get_cube_face(newpos) == new_face
  newdir = (dir - turns) % 4
  # print('new pos', newpos)
  # print('new dir', newdir)
  return (newpos, newdir)

assert do_move(Int2(50,199), RIGHT) == (Int2(51, 199), RIGHT)
assert do_move(get_face_botleft(4)+(S-1, 2), RIGHT) == (get_face_botleft(1) + (S-1, S-3), LEFT)
assert do_move(get_face_botleft(3)+(S-1, 2), RIGHT) == (get_face_botleft(4) + (0, 2), RIGHT)
assert do_move(get_face_botleft(4)+(0, 2), LEFT) == (get_face_botleft(3) + (S-1, 2), LEFT)

print('---- expected pos for this one:', get_face_botleft(5) + (S-1, S-11))
assert do_move(get_face_botleft(4)+(10, 0), DOWN) == (get_face_botleft(5) + (S-1, S-11), LEFT)
assert do_move(get_face_botleft(4)+(10, S-1), UP) == (get_face_botleft(2) + (10, 0), UP)

assert do_move(get_face_botleft(2)+(10, 0), DOWN) == (get_face_botleft(4) + (10, S-1), DOWN)
assert do_move(get_face_botleft(2)+(S-1, 10), RIGHT) == (get_face_botleft(1) + (S-11, 0), UP)

def solve():
  inputf = 'd22real.txt'
  last_line = None
  with open(inputf, 'r') as f:
    for line in f:
      last_line = line
  movesline = last_line

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

  dir = 0
  p = Int2(startx, starty)
  print('*** start at', p)
  i = 0
  for move in moves:
    print('-------')
    i += 1
    if move == 'R':
      dir = (dir + 1) % 4
    elif move == 'L':
      dir = (dir - 1) % 4
    else:
      print(f'from {p}, moving {dir} x {move}')
      for i in range(int(move)):
        q, new_dir = do_move(p, dir)
        if grid[q] == False:
          break
        else:
          assert get_cube_face(q) is not None
          p = q
          dir = new_dir
      print(f'  end at {p}, {dir}')
  print('final pos', p, dir)
  print('pass', get_pass(p.x, p.y, dir, height))
  return p, dir

solve()