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

  def abs(self):
    return Int2(abs(self.x), abs(self.y))

  def sum(self):
    return self.x + self.y
  
  def mandist(self, other):
    return (self - other).abs().sum()

  def rot90ccw(self, N):
    """ rotate by 90 degrees, counter-clockwise, N-times """
    sine = [0, 1, 0, -1][N % 4]
    cosine = [1, 0, -1, 0][N % 4]
    x = cosine * self.x - sine * self.y
    y = sine * self.x + cosine * self.y
    return Int2(x, y)

  def rot90cw(self, N):
    """ rotate by 90 degrees, clockwise, N-times """
    return self.rot90ccw(-N)

  def __add__(u,v):
    if type(v) == int:
      return Int2(u.x + v, u.y + v)
    elif type(v) == tuple:
      assert type(v[0]) == int
      assert type(v[1]) == int
      return Int2(u.x + v[0], u.y + v[1])
    else:
      assert type(v) == Int2
      return Int2(u.x+v.x, u.y+v.y)

  def __sub__(u,v):
    if type(v) == int:
      return Int2(u.x-v, u.y-v)
    else:
      return Int2(u.x-v.x, u.y-v.y)

  def __mul__(u, v):
    assert type(v) == int
    return Int2(u.x * v, u.y * v)

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
    return '%d,%d' % (self.x, self.y)

  def __str__(self):
    return self.__repr__()

  def mod(self, n):
    return Int2(self.x % n, self.y % n)

  @staticmethod
  def min(a, b):
    """ Component-wise min """
    return Int2( min(a.x, b.x), min(a.y, b.y) )

  @staticmethod
  def max(a, b):
    """ Component-wise max """
    return Int2( max(a.x, b.x), max(a.y, b.y) )

  def astuple(self):
    return (self.x, self.y)


assert Int2(1, 0).rot90cw(2) == Int2(-1, 0)
assert Int2(1, 0).rot90cw(6) == Int2(-1, 0)
assert Int2(1, 0).rot90ccw(1) == Int2(0, 1)
assert Int2(1, 0).rot90ccw(2) == Int2(-1, 0)
assert Int2(1, 0).rot90ccw(10) == Int2(-1, 0)
assert Int2(5, 4).mod(3) == Int2(2, 1)