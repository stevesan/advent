import numpy as np
import time
tu = tuple
ar = np.array

input = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
with open('d17real.txt', 'r') as f: input = f.read()
# input = '>'

print(f'jet pattern len: {len(input)}')

WIDTH = 7
shapestext = '''####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##'''

shapes_lines = shapestext.split('\n\n')
print(shapes_lines)
assert len(shapes_lines) == 5
shapes = []
for shape_lines in shapes_lines:
  lines = shape_lines.split('\n')
  lines.reverse()
  height = len(lines)
  width = len(lines[0])
  shape = {}
  for x in range(width):
    for y in range(height):
      val = lines[y][x]
      if val == '#':
        shape[(x,y)] = True
      else:
        assert val == '.'
  shapes.append(shape)

for shape in shapes:
  print(shape)

grid = set()
def gget(p): return tuple(p) in grid
def gset(p): grid.add(tuple(p))

def get_height():
  if len(grid) == 0: return 0
  return max(p[1] for p in grid) + 1

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, 1)
DOWN = (0, -1)

JET2DIR = {'<':LEFT, '>':RIGHT}

t0 = time.time()
t00 = t0
pushindex = 0
max_y_set = -1
statestr = ''
milestones = []
BIGN = 1000000000000
for rocknum in range(2022):
  prev_max_y = max_y_set
  t1 = time.time()
  if t1 - t0 > 1:
    t0 = t1
    rate = (t1 - t00) / (rocknum/1000)
    print(f'iter {rocknum:,}, t={t1-t00:.2f}, {rate} s/krock')

  if rocknum % len(shapes) == 0 and pushindex % len(input) == 0:
    milestones.append(get_height())
    print(f'milestones: {milestones}')

  shape = shapes[rocknum % len(shapes)]
  height = max_y_set + 1
  pos = (2, height + 3)

  jetindex = 0
  for falliter in range(height + 10):
    pushdir = JET2DIR[input[pushindex % len(input)]]
    pushindex += 1

    # push
    any_blocked = False
    for bpos in shape:
      bpos = ar(bpos) + ar(pos)
      bpos = bpos + ar(pushdir)
      x = bpos[0]
      if x < 0 or x >= WIDTH or gget(bpos):
        any_blocked = True
        break
    if not any_blocked:
      # print(f'pushed {pushdir[0]}')
      pos = tu(ar(pos) + ar(pushdir))

    # fall
    any_blocked = False
    for bpos in shape:
      bpos = ar(bpos) + ar(pos)
      bpos = bpos + ar(DOWN)
      y = bpos[1]
      if y < 0 or gget(bpos):
        any_blocked = True
        break
    if not any_blocked:
      # print(f'fell one')
      pos = tu(ar(pos) + ar(DOWN))
    else:
      # done - rasterize this shape into the grid
      for bpos in shape:
        bpos = ar(bpos) + ar(pos)
        # print(f'setting {bpos}')
        gset(bpos)
        max_y_set = max(max_y_set, bpos[1])
      break

  if False:
    if max_y_set > prev_max_y:
      # add to our string..
      for y in range(prev_max_y+1, max_y_set+1):
        for x in range(WIDTH):
          p = (x, y)
          statestr += '#' if gget(p) else '.'
        statestr += '\n'

      # check for symmetry..
      S = len(statestr)
      if S % 2 == 0:
        A = statestr[0:S//2]
        B = statestr[S//2:]
        # print(max_y_set, A, B)
        if A == B:
          print('detected symmetry!')
          print(A)
          print(B)
          break

print(get_height())

print(np.diff(milestones))