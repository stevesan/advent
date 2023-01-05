
import sys
import numpy as np

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

  for beacons in scanner2beacons:
    good_overlaps = gen_overlaps(beacons)
    print(len(good_overlaps))

main(sys.argv[1])
# main('2021/d19sample.txt')