import numpy as np
tu = tuple
ar = np.array

input = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
# with open('d17real.txt', 'r') as f: input = f.read()

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


grid = {}
def gget(p): return grid[tuple(p)]
def gset(p, val): grid[tuple(p)] = val

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, 1)
DOWN = (0, -1)

JET2DIR = {'<':LEFT, '>':RIGHT}

dirs = [ar(d) for d in [
  (1, 0, 0),
  (-1, 0, 0),
  (0, 1, 0),
  (0, -1, 0),
  (0, 0, 1),
  (0, 0, -1),
]]
