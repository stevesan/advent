from util import Int2

DIR2OFS = {
  'N':Int2(0, 1),
  'NE':Int2(1, 1),
  'E':Int2(1, 0),
  'SE':Int2(1,-1),
  'S':Int2(0,-1),
  'SW':Int2(-1,-1),
  'W':Int2(-1,0),
  'NW':Int2(-1,1)
}
_8NBORS = list(DIR2OFS.values())

def print_elves(elves:set[Int2]):
  xx = [p.x for p in elves]
  yy = [p.y for p in elves]
  empties = 0
  for y in range(max(yy), min(yy)-1, -1):
    rowstr = ''
    for x in range(min(xx), max(xx)+1):
      p = Int2(x,y)
      if p in elves:
        rowstr += '#'
      else:
        rowstr += '.'
        empties += 1
    print(rowstr)
  return empties

def solve(inputf, num_rounds):
  dirchecks = [
    ['N', 'NE', 'NW'],
    ['S', 'SE', 'SW'],
    ['W', 'NW', 'SW'],
    ['E', 'NE', 'SE'],
  ]

  with open(inputf, 'r') as f:
    lines = [l.strip() for l in f.readlines()]
  lines.reverse()

  elves:set[Int2] = set()
  for y in range(len(lines)):
    for x in range(len(lines[y])):
      c = lines[y][x]
      if c == '#':
        p = Int2(x, y)
        elves.add(p)

  num_elves = len(elves)

  for round in range(num_rounds):
    elf2proposed = {}
    for elf in elves:
      if not any(elf + nbor in elves for nbor in _8NBORS):
        continue
    
      for dirs in dirchecks:
        ofs = [DIR2OFS[d] for d in dirs]
        if not any(elf + o in elves for o in ofs):
          elf2proposed[elf] = elf + ofs[0]
          break

    # print(f'elf2proposed:')
    # print(elf2proposed)

    # second round
    prop2count = {}
    for prop in elf2proposed.values():
      if prop not in prop2count:
        prop2count[prop] = 0
      prop2count[prop] += 1

    # print('prop2count:')
    # print(prop2count)

    for elf, prop in elf2proposed.items():
      if prop2count[prop] == 1:
        assert prop not in elves
        elves.remove(elf)
        elves.add(prop)
    assert len(elves) == num_elves

    # cycle direction consideration order..
    first = dirchecks.pop(0)
    dirchecks.append(first)

    print(f'after {round+1} rounds:')
    print_elves(elves)


  print(f'after {num_rounds} rounds:')
  return print_elves(elves)

solve('d23small.txt', 3)
assert solve('d23sample.txt', 10) == 110
print(solve('d23real.txt', 10))