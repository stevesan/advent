
import sys
import numpy as np
from dataclasses import dataclass

R = 1000

def Pt(x, y=0, z=0): return np.array([x, y, z])

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

  good_overlaps = set()

  print(f'n = {len(xs)*len(ys)*len(zs)}, {len(xs)} {len(ys)} {len(zs)}')

  for x in xs:
    for y in ys:
      for z in zs:
        boxmin = np.array([x, y, z])
        overlap = []
        for p in beacons:
          if in_box(boxmin, p):
            overlap.append(tuple(p))
        if len(overlap) >= at_least:
          overlap.sort()
          good_overlaps.add(tuple(overlap))

  return good_overlaps

assert len(gen_overlaps([Pt(0), Pt(1), Pt(2)], 2)) == 3

def compute_moments(pts):
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
      p = np.array([int(x) for x in line.split(',')])
      beacons.append(p)
    scanner2beacons.append(beacons)

  num_readings = sum([len(bs) for bs in scanner2beacons])
  print(f'total readings = {num_readings}')

  moments2groups = {}
  for scanner_id, beacons in enumerate(scanner2beacons):
    good_overlaps = gen_overlaps(beacons)
    print(len(good_overlaps))

    for group in good_overlaps:
      moments = compute_moments(group)

      if moments not in moments2groups:
        moments2groups[moments] = []
      entry = ScannerGroup(scanner_id, group)
      moments2groups[moments].append(entry)

  double_counts = 0
  for moments, groups in moments2groups.items():
    if len(groups) > 1:
      assert len(groups) == 2
      double_counts += len(groups[0].beacons)
      print(f'----- matching groups, moments = {moments}:')
      for group in groups:
        print(f'  scanner {group.id}, {len(group.beacons)} pts')

  print(f'total readings = {num_readings}')
  print(f'actual num beacons = {num_readings - double_counts}')
  
main(sys.argv[1])
# main('2021/d19sample.txt')