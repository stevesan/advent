
class Int2:
  x = 0
  y = 0

  def __init__(self, x, y=None):
    assert type(x) == int
    if y is None:
      y = x
    assert type(y) == int
    self.x = x
    self.y = y

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __ne__(self, other):
    return not self == other

  def __add__(u,v):
    if type(v) == int:
      return Int2(u.x + v, u.y + v)
    else:
      return Int2(u.x+v.x, u.y+v.y)

  def __sub__(u,v):
    if type(v) == int:
      return Int2(u.x-v, u.y-v)
    else:
      return Int2(u.x-v.x, u.y-v.y)

  def all_lte(self, other):
    return self.x <= other.x and self.y <= other.y

  def all_gte(self, other):
    return self.x >= other.x and self.y >= other.y

  def __lt__(self, other):
    """ Lexographic compare """
    return (self.x, self.y) < (other.x, other.y)

  def __gt__(self, other):
    """ Lexographic compare """
    return (self.x, self.y) > (other.x, other.y)

  def __hash__(self):
    return hash((self.x, self.y))

  def __repr__(self):
    return '(%d,%d)' % (self.x, self.y)

  def __str__(self):
    return self.__repr__()

  @staticmethod
  def min(a, b):
    """ Component-wise min """
    return Int2( min(a.x, b.x), min(a.y, b.y) )

  @staticmethod
  def max(a, b):
    """ Component-wise max """
    return Int2( max(a.x, b.x), max(a.y, b.y) )

class Grid2:
  def __init__(self,_W, _H, default):
    self.W = _W
    self.H = _H
    self.grid = list(range(self.W*self.H))
    for i in range(self.W*self.H):
      self.grid[i] = default

  def __getitem__(G, u):
    return G.pget(u)

  def __setitem__(G, u, val):
    G.pset(u, val)

  def check(self,p):
    return p.x >= 0 and p.x < self.W and p.y >= 0 and p.y < self.H

  def get(self,x,y):
    assert self.check(Int2(x, y))
    return self.grid[self.W*y + x]

  def pget(self,p):
    assert self.check(p)
    return self.grid[self.W*p.y + p.x]

  def set(self,x,y,value):
    assert self.check(Int2(x, y))
    self.grid[self.W*y+x] = value

  def pset(self,p,value):
    assert self.check(p)
    self.grid[self.W*p.y+p.x] = value


paths = []
with open('d14a-input.txt') as f:
  for line in f:
    line = line.strip()
    pt_strs = line.split(' -> ')
    path = []
    for s in pt_strs:
      xs, ys = s.split(',')
      pt = Int2(int(xs), int(ys))
      path.append(pt)
    paths.append(path)

# print(paths)

allpts = []
for path in paths:
  for p in path: allpts.append(p)

# figure out bounds and recenter
width = max([p.x for p in allpts] + [500]) + 1
height = max([p.y for p in allpts]) + 1

print('size is ', width, height)

G = Grid2(width, height, '.')

def print_grid():
  for i in range(height):
    line = ''
    for j in range(490, width):
      val = G.get(j, i)
      line += val
    print(line)

for path in paths:
  for i in range(len(path) - 1):
    start = path[i]
    end = path[i+1]
    dir = Int2.max(Int2(-1), Int2.min(Int2(1), (end - start)))
    while start != end:
      G[start] = '#'
      start += dir
    G[start] = '#'

print_grid()
print('dropping sand..')

# drop sand..
def drop_sand():
  """ Return False if sand fell into abyss"""
  p = Int2(500, 0)
  assert G[p] in ['o', '.']

  # Totally full?
  if G[p] == 'o': return False

  while True:
    # Case where we fall out of bounds - sand can do this, we just need to check
    if not G.check(p): return False
    q = p + Int2(0, 1)
    # IMPORTANT: Note how we allow sand to fall out of bounds - thus the "not G.check" clauses
    if not G.check(q) or G[q] == '.':
      p = q
    elif G[q] == '#' or G[q] == 'o':
      # Try left..
      q.x -= 1
      if not G.check(q) or G[q] == '.':
        p = q
      else:
        # Try right..
        q.x += 2
        if not G.check(q) or G[q] == '.':
          p = q
        else:
          # Can't move anymore - mark rest and done
          G[p] = 'o'
          return True

grains = 0
while drop_sand():
  grains += 1
# print_grid()
print('final grain count: ', grains)
