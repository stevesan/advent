
from util import Int2
import time
from dataclasses import dataclass


@dataclass
class Sensor:
  pos:Int2
  closest_beacon_pos:Int2
  radius:int

  def get_intxs(self, y):
    dy = abs(self.pos.y - y)
    if dy > self.radius: return None
    dx = self.radius - dy
    return (self.pos.x - dx, self.pos.x + dx)

def main(inputf, maxcoord):
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


  for query_y in range(maxcoord):
    if query_y % 10000 == 0:print(f'trying {query_y}')
    pairs = []
    for sen in sensors:
      intxs = sen.get_intxs(query_y)
      if intxs:
        pairs.append([sen, intxs[0]])
        pairs.append([sen, intxs[1]])

    pairs.sort(key=lambda p: p[1])
    # print(pairs)

    prev_x = pairs[0][1]
    overlaps = [pairs[0][0]]
    for pair in pairs[1:]:
      sen = pair[0]
      x = pair[1]
      if len(overlaps) == 0 and x >= prev_x + 2:
        # found one!
        print(f'found free spot at {prev_x+1}, {query_y}')
        return (prev_x+1) * 4000000 + query_y

      if sen in overlaps:
        overlaps.remove(sen)
      else:
        overlaps.append(sen)
        assert Int2(x, query_y).mandist(sen.pos) == sen.radius

      prev_x = x

assert main('d15sample.txt', 20) == 56000011
# assert main('d15test1.txt', 10) == 1
# assert main('d15test2.txt', 10) == 0
# assert main('d15test3.txt', 10) == 0
import sys
main(sys.argv[1], int(sys.argv[2]))