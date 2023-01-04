
import sys
import numpy as np

R = 1000

def Pt(x, y=0, z=0): return np.array([x, y, z])

def augment_coordinates(xx):
  more = [x - 2*R for x in xx]
  rv = list(set(xx + more))
  rv.sort()
  return rv

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
  xs = augment_coordinates([p[0] for p in beacons])
  ys = augment_coordinates([p[1] for p in beacons])
  zs = augment_coordinates([p[2] for p in beacons])

  # setup slices
  z2pts = {}
  for z in zs:
    pts = []
    for p in beacons:
      if p[2] == z:
        pts.append(p)
    z2pts[z] = pts

  good_overlaps = set()

  for x in xs:
    for y in ys:
      for z in zs:
        boxmin = np.array([x, y, z])
        zmin = z
        zmax = z + 2*R
        overlap = []
        for z, pts in z2pts.items():
          if zmin <= z and z <= zmax:
            for p in pts:
              if in_box(boxmin, p):
                overlap.append(tuple(p))
        if len(overlap) >= at_least:
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

# main(sys.argv[1])
# main('2021/d19sample.txt')