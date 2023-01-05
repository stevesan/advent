
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
      yield B @ A

# for R in enum_24_rots():
#   print('-----')
#   print(np.round(R @ Pt(1, 0, 0)))
#   print(np.round(R @ Pt(0, 1, 0)))

def rotate_and_realign(R:np.ndarray, vecs:list[np.ndarray]):
  rotated = [np.round(R@v) for v in vecs]
  minx = min(v[0][0] for v in rotated)
  miny = min(v[1][0] for v in rotated)
  minz = min(v[2][0] for v in rotated)
  mins = Pt(minx, miny, minz)
  return [v-mins for v in rotated]

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
  ]),
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

  double_counts = 0
  for moments, groups in moments2groups.items():
    if len(groups) > 1:
      assert len(groups) == 2
      double_counts += len(groups[0].beacons)
      print(f'----- matching groups, moments = {moments}:')
      for group in groups:
        vecs = [t2p(t) for t in group]

        print(f'  scanner {group.id}, {len(group.beacons)} pts')

  print(f'total readings = {num_readings}')
  print(f'actual num beacons = {num_readings - double_counts}')
  
main(sys.argv[1])
# main('2021/d19sample.txt')