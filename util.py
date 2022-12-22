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
    return '%d,%d' % (self.x, self.y)

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

  def astuple(self):
    return (self.x, self.y)