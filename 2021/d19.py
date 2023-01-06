
import sys
import numpy as np
from collections import defaultdict
from dataclasses import dataclass
import math

R = 1000

def Pt(x, y=0, z=0): return np.array([[x], [y], [z]], ndmin=2)
def p2t(p): return (p[0][0], p[1][0], p[2][0])
def t2p(t): return Pt(t[0], t[1], t[2])

POS_X = np.array([1, 0, 0])
POS_Y = np.array([0, 1, 0])
POS_Z = np.array([0, 0, 1])

# matrices that rotate +X into all 6 faces of a cube
CUBE_FACE_ROTS = [np.transpose(np.array(axes, ndmin=2)) for axes in [
  [POS_X, POS_Y, POS_Z],
  [POS_Z, POS_Y, -POS_X],
  [-POS_X, POS_Y, -POS_Z],
  [-POS_Z, POS_Y, POS_X],
  [POS_Y, -POS_X, POS_Z],
  [-POS_Y, POS_X, POS_Z],
]]

def get_rotation_matrix(axis, theta):
    """
    Find the rotation matrix associated with counterclockwise rotation
    about the given axis by theta radians.
    Credit: http://stackoverflow.com/users/190597/unutbu

    Args:
        axis (list): rotation axis of the form [x, y, z]
        theta (float): rotational angle in radians

    Returns:
        array. Rotation matrix.
    """

    axis = np.asarray(axis)
    theta = np.asarray(theta)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]], ndmin=2) 

def enum_24_rots():
  for A in CUBE_FACE_ROTS:
    for i in range(4):
      theta = math.pi * i * 0.5
      axis = A[:, 0]
      B = get_rotation_matrix(axis, theta)
      yield np.round(B @ A)

# for R in enum_24_rots():
#   print('-----')
#   print(np.round(R @ Pt(1, 0, 0)))
#   print(np.round(R @ Pt(0, 1, 0)))

def bb_min(vecs:list[np.ndarray]):
  minx = min(v[0][0] for v in vecs)
  miny = min(v[1][0] for v in vecs)
  minz = min(v[2][0] for v in vecs)
  mins = Pt(minx, miny, minz)
  return mins

def rotate_and_realign(R:np.ndarray, vecs:list[np.ndarray]):
  rotated = [np.round(R@v) for v in vecs]
  mins = bb_min(rotated)
  return mins, [v-mins for v in rotated]

def pointsets_equal(A, B):
  if len(A) != len(B): return False
  A = [p2t(p) for p in A]
  B = [p2t(p) for p in B]
  for a in A:
    if a not in B: return False
  return True

assert pointsets_equal(
  rotate_and_realign(CUBE_FACE_ROTS[0], [
    Pt(1, 1, 1),
    Pt(1, 2, 1)
  ])[1],
  [Pt(0, 0, 0), Pt(0, 1, 0)])

assert pointsets_equal(
  [Pt(1, 2, 3), Pt(4, 5, 6)],
  [Pt(4, 5, 6), Pt(1, 2, 3)],
)

assert not pointsets_equal(
  [Pt(1, 2, 3), Pt(4, 5, 6)],
  [Pt(4, 2, 6), Pt(1, 2, 3)],
)

def augment_coordinates(xx, at_least):
  more = [x - 2*R for x in xx]
  rv = xx + more
  rv.sort()
  N = at_least
  return rv[N-1:-N+1]
  # return rv

def get_box_min(boxcenter):
  return boxcenter - Pt(R, R, R)

def in_box(boxmin, p):
  center = boxmin + Pt(R, R, R)
  delta = p - center
  return all(abs(delta) <= R)

assert in_box(get_box_min(Pt(500, 0, -500)), Pt(-500, 1000, -1500))
assert in_box(get_box_min(Pt(500, 0, -500)), Pt(1500, -1000, 500))
assert in_box(get_box_min(Pt(500, 0, -500)), Pt(1500, -1001, 500)) == False
assert in_box(get_box_min(Pt(500, 0, -500)), Pt(1501, 0, -500)) == False

def gen_overlaps(beacons:list[np.array], at_least=12):
  xs = augment_coordinates([p[0] for p in beacons], at_least)
  ys = augment_coordinates([p[1] for p in beacons], at_least)
  zs = augment_coordinates([p[2] for p in beacons], at_least)

  xx = np.array([p[0] for p in beacons])
  yy = np.array([p[1] for p in beacons])
  zz = np.array([p[2] for p in beacons])

  good_overlaps = set()

  print(f'n = {len(xs)*len(ys)*len(zs)}, {len(xs)} {len(ys)} {len(zs)}')

  for x in xs:
    for y in ys:
      for z in zs:
        dx = np.abs(xx - x - R)
        dy = np.abs(yy - y - R)
        dz = np.abs(zz - z - R)
        pt_ids = np.nonzero(np.logical_and(
          dx <= R,
          np.logical_and(
            dy <= R,
            dz <= R
        )))[0]

        if len(pt_ids) >= at_least:
          overlap = [p2t(beacons[i]) for i in pt_ids]
          overlap.sort()
          good_overlaps.add(tuple(overlap))

  return good_overlaps

assert len(gen_overlaps([Pt(0), Pt(1), Pt(2)], 2)) == 3

def compute_moments(pts:list[np.ndarray]):
  rv = []
  sum = Pt(0)
  for p in pts:
    sum += p
  mean = sum / len(pts)
  for pow in [0, 1, 2, 3]:
    mom = 0
    for p in pts:
      d = np.linalg.norm(p - mean)
      mom += d ** pow
    rv.append(int(mom))

  return tuple(rv)

assert compute_moments([Pt(-1), Pt(1)]) == (2, 2, 2, 2)

@dataclass
class ScannerGroup:
  id: int
  beacons: list[np.array]

@dataclass
class Xform:
  id: object
  translation: np.ndarray
  rotation: np.ndarray
  inverted: bool = False

  def inverse(self):
    assert not self.inverted
    id = (self.id[1], self.id[0])
    return Xform(id, -self.translation, np.linalg.inv(self.rotation), inverted=True)

  def apply(self, v):
    if self.inverted:
      return self.rotation @ (v + self.translation)
    else:
      return (self.rotation @ v) + self.translation

def find_xform_chain(edge2xform, start:int, end:int, visited=set()):
  if (start, end) in edge2xform:
    return [edge2xform[(start, end)]]

  for (p, q), xform in edge2xform.items():
    if p != start: continue
    if q in visited: continue
    chain_from_q = find_xform_chain(edge2xform, q, end, visited.union([q]))
    if chain_from_q:
      return [xform] + chain_from_q
  
  return None

test_xforms = {
  (0, 1): 'a',
  (1, 2): 'b',
  (2, 3): 'c',
}
assert find_xform_chain(test_xforms, 0, 3) == ['a', 'b', 'c']

def main(inputf):
  with open(inputf) as f:
    text = f.read()

  scanner2beacons = []

  for grouptext in text.split('\n\n'):
    group = grouptext.split('\n')
    header = group[0]
    assert 'scanner' in header
    beacons = []
    for line in group[1:]:
      x, y, z = [int(x) for x in line.split(',')]
      beacons.append(Pt(x, y, z))
    scanner2beacons.append(beacons)

  num_readings = sum([len(bs) for bs in scanner2beacons])
  print(f'total readings = {num_readings}')

  moments2groups = defaultdict(lambda: [])
  for scanner_id, beacons in enumerate(scanner2beacons):
    good_overlaps = gen_overlaps(beacons)
    for group in good_overlaps:
      vecs = [t2p(t) for t in group]
      moments = compute_moments(vecs)
      entry = ScannerGroup(scanner_id, group)
      moments2groups[moments].append(entry)

  edge2xform = {}

  for moments, groups in moments2groups.items():
    if len(groups) > 1:
      assert len(groups) == 2
      print(f'----- matching group for moments = {moments}. scanners {groups[0].id} and {groups[1].id}')
      Aid = groups[0].id
      Bid = groups[1].id
      A = [t2p(t) for t in groups[0].beacons]
      B = [t2p(t) for t in groups[1].beacons]
      # Still need to re-align, but rotate with identity
      Amins = bb_min(A)
      for R in enum_24_rots():
        Bmins, rotated = rotate_and_realign(R, B)
        Bxformed = [Amins + v for v in rotated]
        translation = Amins - Bmins
        if pointsets_equal(A, Bxformed):
          print(f'found matching trans={np.transpose(translation)}, Rot:\n{R}, ')
          
          edge = (Bid, Aid)
          xform = Xform(
            id=edge,
            translation=translation,
            rotation=R)
          edge2xform[edge] = xform

          # invx = xform.inverse()
          # for p in A:
          #   p = invx.apply(p)
          #   assert p2t(p) in [p2t(q) for q in B]

          break

  # add inverses
  inverses = {}
  for (a, b), xform in edge2xform.items():
    inverses[(b,a)] = xform.inverse()
  edge2xform.update(inverses)

  # find all unique points
  uniques = set()

  def apply_chain(chain, p):
    for T in chain:
      p = T.apply(p)
    return p

  for scanner_id, beacons in enumerate(scanner2beacons):
    if scanner_id == 0:
      chain = []
    else:
      chain = find_xform_chain(edge2xform, scanner_id, 0)
      print(f'found chain: {chain}')
      assert chain

    print(f'scanner {scanner_id} rel to 0 pos: {np.transpose(apply_chain(chain, Pt(0)))}')
    for p in beacons:
      p = np.round(apply_chain(chain, p))
      uniques.add(p2t(p))
    
  print(f'found {len(uniques)} unique pts')
  
main(sys.argv[1])
# main('2021/d19sample.txt')