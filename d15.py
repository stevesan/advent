
from util import Int2
import time
from dataclasses import dataclass


@dataclass
class Sensor:
  pos:Int2
  closest_beacon_pos:Int2
  radius:int

  def get_intxs(self, y):
    dy = self.pos.y - y
    dx = self.radius - abs(dy)
    return (self.pos.x - dx, self.pos.x + dx)

def main(inputf, query_y):
  beacons = set()
  sensor_poss = set()
  sensors:list[Sensor] = []
  with open(inputf, 'r') as f:
    for line in f:
      line = line.strip()
      parts = line.split(' ')
      sx = int(parts[2].split('=')[1][:-1])
      sy = int(parts[3].split('=')[1][:-1])
      bx = int(parts[8].split('=')[1][:-1])
      by = int(parts[9].split('=')[1])
      pos = Int2(sx, sy)
      bpos = Int2(bx, by)
      r = pos.mandist(bpos)
      sensor = Sensor(pos, closest_beacon_pos=bpos, radius=r)
      beacons.add(bpos)
      sensor_poss.add(pos)
      sensors.append(sensor)

  all_xs = [s.pos.x for s in sensors] + [s.closest_beacon_pos.x for s in sensors]
  all_ys = [s.pos.y for s in sensors] + [s.closest_beacon_pos.y for s in sensors]

  all_rads = [s.radius for s in sensors]
  maxrad = max(all_rads)

  mins = Int2(min(all_xs), min(all_ys))
  maxs = Int2(max(all_xs), max(all_ys))

  print(mins, maxs)

  excluded_spots = 0

  t0 = time.time()
  # TODO actually we need to account for the largest radii as well..subtract that off
  x0 = mins.x-maxrad
  x1 = maxs.x + maxrad + 1
  print('xrange', x0, x1)
  for x in range(x0, x1):
    t1 = time.time()
    if t1 - t0 > 1:
      t0 = t1
      print(f'{x-mins.x+maxrad} of {maxs.x+maxrad+1-mins.x+maxrad}')
    q = Int2(x, query_y)
    if q in beacons or q in sensor_poss: continue
    excluded = False
    for sen in sensors:
      qdist = q.mandist(sen.pos)
      if qdist <= sen.radius:
        excluded = True
        break
    if excluded:
      excluded_spots += 1
  print(excluded_spots)
import sys

main(sys.argv[1], int(sys.argv[2]))